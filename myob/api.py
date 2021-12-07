from .constants import MYOB_BASE_URL
from .credentials import PartnerCredentials
from .endpoints import ALL, ENDPOINTS, GET
from .managers import Manager


class Myob:
    """ An ORM-like interface to the MYOB API. """
    def __init__(self, credentials):
        if not isinstance(credentials, PartnerCredentials):
            raise TypeError(
                'Expected a Credentials instance, got %s.' % (
                    type(credentials).__name__,
                )
            )
        self.credentials = credentials
        self.companyfiles = CompanyFiles(credentials)
        self._manager = Manager(
            company_id=None,
            parent_url=MYOB_BASE_URL,
            path_name=None,
            credentials=credentials,
            raw_endpoints=[
                (GET, 'Info/', 'Return API build information for each individual endpoint.'),
            ]
        )

    def info(self):
        return self._manager.info()

    def __repr__(self):
        return 'Myob:\n    %s' % '\n    '.join(['companyfiles', 'info'])


class CompanyFiles:
    def __init__(self, credentials):
        self.credentials = credentials
        self._manager = Manager(
            company_id=None,
            credentials=self.credentials,
            parent_url=MYOB_BASE_URL,
            path_name=None,
            raw_endpoints=[
                (ALL, '', 'Return a list of company files.'),
                (GET, '[id]/', 'List endpoints available for a company file.'),
            ]
        )
        self._manager.name = 'CompanyFile'

    def all(self):
        raw_companyfiles = self._manager.all()
        return [CompanyFile(raw_companyfile, self.credentials) for raw_companyfile in raw_companyfiles]

    def get(self, id, call=True):
        if call:
            # raw_companyfile = self._manager.get(id=id)['CompanyFile']
            # NOTE: Annoyingly, we need to pass company_id to the manager, else we won't have permission
            # on the GET endpoint. The only way we currently allow passing company_id is by setting it on the manager,
            # and we can't do that on init, as this is a manager for company files plural..
            # Reluctant to change manager code, as it would add confusion if the inner method let you override the company_id.
            manager = Manager(
                company_id=id,
                parent_url=MYOB_BASE_URL,
                credentials=self.credentials,
                path_name=None,
                raw_endpoints=[
                    (GET, '', '')
                ]
            )
            raw_companyfile = manager.get()['CompanyFile']
        else:
            raw_companyfile = {'Id': id}
        return CompanyFile(raw_companyfile, self.credentials)

    def __repr__(self):
        return self._manager.__repr__()


class CompanyFile:
    def __init__(self, raw, credentials):
        self.id = raw['Id']
        self.name = raw.get('Name')
        self.data = raw  # Dump remaining raw data here.
        self.credentials = credentials
        for path_name, resource in ENDPOINTS.items():
            setattr(
                self,
                Manager.plain_name(path_name).lower(),
                Manager(
                    company_id=self.id,
                    credentials=self.credentials,
                    parent_url=f'{MYOB_BASE_URL}{self.id}/',
                    path_name=path_name, resource=resource,
                    is_tle=True
                )
            )

    def __repr__(self):
        return 'CompanyFile:\n    %s' % '\n    '.join(sorted(v['name'] for v in ENDPOINTS.values()))
