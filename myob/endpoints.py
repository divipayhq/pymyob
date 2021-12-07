from .utils import pluralise

ALL = 'ALL'
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'
CRUD = 'CRUD'  # shorthand for creating the ALL|GET|POST|PUT|DELETE endpoints in one swoop

METHOD_ORDER = [ALL, GET, POST, PUT, DELETE]

ENDPOINTS = {
    'Banking/': {
        'name': 'Banking',
        'hint': 'banking type',
        'methods': [ALL],
        'resources': {
            'SpendMoneyTxn/': {
                'name': 'SpendMoneyTxn',
                'hint': 'spend money transaction',
                'methods': [CRUD],
                'resources': {
                    'Attachment/': {
                        'name': 'Attachment',
                        'hint': 'spend money transaction attachment',
                        'methods': [ALL, DELETE, GET, POST]
                    }
                }
            },
            'ReceiveMoneyTxn/': {
                'name': 'ReceiveMoneyTxn',
                'hint': 'receive money transaction',
                'methods': [CRUD]
            },
            'TransferMoneyTxn/': {
                'name': 'TransferMoneyTxn',
                'hint': 'transfer money transaction',
                'methods': [CRUD]
            }
        }
    },
    'Contact/': {
        'name': 'Contacts',
        'hint': 'contact type',
        'methods': [ALL],
        'resources': {
            'Customer/': {
                'name': 'Customer',
                'hint': 'customer contact',
                'methods': [CRUD]
            },
            'Employee/': {
                'name': 'Employee',
                'hint': 'employee card',
                'methods': [CRUD]
            },
            'Supplier/': {
                'name': 'Supplier',
                'hint': 'supplier contact',
                'methods': [CRUD]
            }
        }
    },
    'Sale/CustomerPayment/': {
        'name': 'Customer_Payments',
        'hint': 'sale customer payment',
        'methods': [ALL, GET, POST, DELETE]
    },
    'Sale/Invoice/': {
        'hint': 'invoices',
        'name': 'invoice',
        'methods': [ALL],
        'resources': {
            'Item/': {
                'name': 'item',
                'hint': 'item type sale invoice',
                'methods': [CRUD]
            },
            'Service/': {
                'name': 'service',
                'hint': 'service type sale invoice',
                'methods': [CRUD]
            }
        }
    },
    # 'Sale/Order/': {
    #     'name': 'orders',
    #     'methods': [
    #         (ALL, '', 'sale order type'),
    #         (CRUD, 'Item/', 'item type sale order'),
    #         (CRUD, 'Service/', 'service type sale order'),
    #     ]
    # },
    # 'Sale/Quote/': {
    #     'name': 'quotes',
    #     'methods': [
    #         (ALL, '', 'sale quote type'),
    #         (CRUD, 'Item/', 'item type sale quote'),
    #         (CRUD, 'Service/', 'service type sale quote'),
    #     ]
    # },
    # 'GeneralLedger/': {
    #     'name': 'general_ledger',
    #     'methods': [
    #         (CRUD, 'TaxCode/', 'tax code'),
    #         (CRUD, 'Account/', 'account'),
    #         (CRUD, 'Category/', 'cost center tracking category'),
    #         (CRUD, 'Job/', 'job'),
    #         (ALL, 'JournalTransaction/', 'transaction journal'),
    #         (GET, 'JournalTransaction/', 'transaction journal'),
    #     ]
    # },
    # 'Inventory/': {
    #     'name': 'inventory',
    #     'methods': [
    #         (CRUD, 'Item/', 'inventory item'),
    #         (ALL, 'ItemPriceMatrix/', 'inventory item price matrix'),
    #         (GET, 'ItemPriceMatrix/', 'inventory item price matrix'),
    #         (PUT, 'ItemPriceMatrix/', 'inventory item price matrix'),
    #         (CRUD, 'Location/', 'inventory location'),
    #         (CRUD, 'Adjustment/', 'inventory adjustment')
    #     ]
    # },
    # 'Purchase/Order/': {
    #     'name': 'purchase_orders',
    #     'methods': [
    #         (ALL, '', 'purchase order type'),
    #         (CRUD, 'Item/', 'item type purchase order'),
    #     ]
    # },
    # 'Purchase/Bill/': {
    #     'name': 'purchase_bills',
    #     'methods': [
    #         (ALL, '', 'purchase bill type'),
    #         (CRUD, 'Item/', 'item type purchase bill'),
    #         (CRUD, 'Service/', 'service type purchase bill'),
    #         (CRUD, 'Miscellaneous/', 'miscellaneous type purchase bill'),
    #     ]
    # },
    # 'Company/': {
    #     'name': 'company',
    #     'methods': [
    #         (ALL, 'Preferences/', 'company data file preference')
    #     ]
    # },
}

METHOD_MAPPING = {
    ALL: {
        'endpoint': lambda: '',
        'hint': lambda name: 'Return all %s for an AccountRight company file.' % pluralise(name)
    },
    GET: {
        'endpoint': lambda: '[uid]/',
        'hint': lambda name: 'Return selected %s.' % name
    },
    PUT: {
        'endpoint': lambda: '[uid]/',
        'hint': lambda name: 'Update selected %s.' % name
    },
    POST: {
        'endpoint': lambda: '',
        'hint': lambda name: 'Create new %s.' % name
    },
    DELETE: {
        'endpoint': lambda: '[uid]/',
        'hint': lambda name: 'Delete selected %s.' % name
    },
}
