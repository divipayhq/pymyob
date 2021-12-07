import re
from datetime import date
from typing import Optional, List, Dict

import requests

from .constants import DEFAULT_PAGE_SIZE
from .credentials import PartnerCredentials
from .endpoints import CRUD, METHOD_MAPPING, METHOD_ORDER
from .exceptions import (
    MyobBadRequest,
    MyobExceptionUnknown,
    MyobForbidden,
    MyobGatewayTimeout,
    MyobNotFound,
    MyobRateLimitExceeded,
    MyobUnauthorized,
)


class Manager:
    def __init__(
        self,
        company_id: Optional[str],
        credentials: PartnerCredentials,
        parent_url: str,
        path_name: Optional[str],
        resource: Optional[Dict] = None,
        raw_endpoints: Optional[List] = None,
        is_tle: Optional[bool] = False,
    ):
        """
        :param company_id   The ID of the company to fetch credentials from.
        :param credentials  The PartnerCredentials instance required to connect to Myob
        :param parent_url   The fully qualified path up to the parent resource.
                            A trailing slash is expected
        :param path_name    The unique part of the URL to which this resource applies.
                            A trailing slash is expected
        :param resource     {
                                methods: The methods available for this resource
                                hint: the name applied to the help documentation
                                resources: (Optional) nested child resources
                            }
        :param raw_endpoints Any endpoints that should be applied at the top level
        """

        self.company_id = company_id
        self.credentials = credentials
        self.path_name = path_name
        self.name = (resource or dict()).get("name")
        self.is_tle = is_tle
        self.base_url = f'{parent_url}{path_name or ""}'
        self.method_details = {}

        # Build ORM methods from given url endpoints.
        for method in (resource or dict()).get('methods', []):

            if method == CRUD:
                for m in METHOD_ORDER:
                    self.build_method(
                        m,
                        METHOD_MAPPING[m]['endpoint'](),
                        METHOD_MAPPING[m]['hint'](resource.get("hint")),
                    )
            else:
                self.build_method(
                    method,
                    METHOD_MAPPING[method]['endpoint'](),
                    METHOD_MAPPING[method]['hint'](resource.get("hint")),
                )
        # Build raw methods (ones where we don't want to tinker with the endpoint or hint)
        for method, endpoint, hint in (raw_endpoints or []):
            self.build_method(method, endpoint, hint)

        # Build out nested child resources
        for path_name, resource in (resource or dict()).get("resources", dict()).items():
            setattr(
                self,
                resource.get("name").lower(),
                Manager(
                    company_id=self.company_id,
                    credentials=self.credentials,
                    parent_url=self.nested_url(),
                    path_name=path_name,
                    resource=resource
                )
            )

    def nested_url(self) -> str:
        """
        Given the resource held by this Manager, determine provide
        the url which will act as the parent to them (when nested).
        """
        if self.is_tle:
            return self.base_url

        return f'{self.base_url}[{self.name.lower()}_uid]/'

    def build_method(self, method: str, endpoint: Optional[str], hint: str):
        full_endpoint = f'{self.base_url}{endpoint or ""}'
        url_keys = re.findall(r'\[([^\]]*)\]', full_endpoint)
        template = full_endpoint.replace('[', '{').replace(']', '}')

        required_kwargs = url_keys.copy()
        if method in ('PUT', 'POST'):
            required_kwargs.append('data')

        def inner(*args, timeout=None, **kwargs):
            if args:
                raise AttributeError("Unnamed args provided. Only keyword args accepted.")

            # Ensure all required url kwargs have been provided.
            missing_kwargs = set(required_kwargs) - set(kwargs.keys())
            if missing_kwargs:
                raise KeyError("Missing kwargs %s. Endpoint requires %s." % (
                    list(missing_kwargs), required_kwargs
                ))

            # Parse kwargs.
            url_kwargs = {}
            request_kwargs_raw = {}
            for k, v in kwargs.items():
                if k in url_keys:
                    url_kwargs[k] = v
                elif k != 'data':
                    request_kwargs_raw[k] = v

            # Determine request method.
            request_method = 'GET' if method == 'ALL' else method

            # Build url.
            url = template.format(**url_kwargs)

            # Build request kwargs (header/query/body)
            request_kwargs = self.build_request_kwargs(request_method, data=kwargs.get('data'), **request_kwargs_raw)
            response = requests.request(request_method, url, timeout=timeout, **request_kwargs)

            if response.status_code == 200:
                # We don't want to be deserialising binary responses..
                if not response.headers.get('content-type', '').startswith('application/json'):
                    return response.content

                try:
                    return response.json()
                except ValueError:
                    # Handle possible empty string response to DELETE request
                    if method == 'DELETE' and response.content == b'':
                        return {}
                    raise
            elif response.status_code == 201:
                return response.json()
            elif response.status_code == 400:
                raise MyobBadRequest(response)
            elif response.status_code == 401:
                raise MyobUnauthorized(response)
            elif response.status_code == 403:
                if response.json()['Errors'][0]['Name'] == 'RateLimitError':
                    raise MyobRateLimitExceeded(response)
                raise MyobForbidden(response)
            elif response.status_code == 404:
                raise MyobNotFound(response)
            elif response.status_code == 504:
                raise MyobGatewayTimeout(response)
            else:
                raise MyobExceptionUnknown(response)

        # Build method name
        method_name = '_'.join(p for p in endpoint.rstrip('/').split('/') if '[' not in p).lower()
        # If it has no name, use method.
        if not method_name:
            method_name = method.lower()
        # If it already exists, prepend with method to disambiguate.
        elif hasattr(self, method_name):
            method_name = '%s_%s' % (method.lower(), method_name)
        self.method_details[method_name] = {
            'kwargs': required_kwargs,
            'hint': hint,
        }
        setattr(self, method_name, inner)

    def build_request_kwargs(self, method, data=None, **kwargs):
        request_kwargs = {}

        # Build headers.
        if self.company_id:
            try:
                companyfile_credentials = self.credentials.companyfile_credentials[self.company_id]
            except KeyError:
                raise KeyError('There are no stored username-password credentials for this company id.')
        else:
            companyfile_credentials = ''

        request_kwargs['headers'] = {
            'Authorization': 'Bearer %s' % self.credentials.oauth_token,
            'x-myobapi-cftoken': companyfile_credentials,
            'x-myobapi-key': self.credentials.consumer_key,
            'x-myobapi-version': 'v2',
        }
        if 'headers' in kwargs:
            request_kwargs['headers'].update(kwargs['headers'])

        # Build query.
        request_kwargs['params'] = {}
        filters = []

        def build_value(value):
            if issubclass(type(value), date):
                return "datetime'%s'" % value
            if isinstance(value, bool):
                return str(value).lower()
            return "'%s'" % value

        if 'raw_filter' in kwargs:
            filters.append(kwargs['raw_filter'])

        for k, v in kwargs.items():
            if k not in ['orderby', 'format', 'headers', 'page', 'limit', 'templatename', 'timeout', 'raw_filter']:
                operator = 'eq'
                for op in ['lt', 'gt']:
                    if k.endswith('__%s' % op):
                        k = k[:-4]
                        operator = op
                if not isinstance(v, (list, tuple)):
                    v = [v]
                filters.append(' or '.join("%s %s %s" % (k, operator, build_value(v_)) for v_ in v))

        if filters:
            request_kwargs['params']['$filter'] = ' and '.join('(%s)' % f for f in filters)

        if 'orderby' in kwargs:
            request_kwargs['params']['$orderby'] = kwargs['orderby']

        page_size = DEFAULT_PAGE_SIZE
        if 'limit' in kwargs:
            page_size = int(kwargs['limit'])
            request_kwargs['params']['$top'] = page_size

        if 'page' in kwargs:
            request_kwargs['params']['$skip'] = (int(kwargs['page']) - 1) * page_size

        if 'format' in kwargs:
            request_kwargs['params']['format'] = kwargs['format']

        if 'templatename' in kwargs:
            request_kwargs['params']['templatename'] = kwargs['templatename']

        if method in ('PUT', 'POST'):
            request_kwargs['params']['returnBody'] = 'true'

        # Build body.
        if data is not None:
            request_kwargs['json'] = data

        return request_kwargs

    def __repr__(self):
        def print_method(name, args):
            return '%s(%s)' % (name, ', '.join(args))

        formatstr = '%%%is - %%s' % max(
            len(print_method(k, v['kwargs']))
            for k, v in self.method_details.items()
        )
        return '%s%s:\n    %s' % (self.name, self.__class__.__name__, '\n    '.join(
            formatstr % (
                print_method(k, v['kwargs']),
                v['hint'],
            ) for k, v in sorted(self.method_details.items())
        ))
