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
        'hint': 'sale invoice type',
        'name': 'Invoices',
        'methods': [ALL],
        'resources': {
            'Item/': {
                'name': 'Item',
                'hint': 'item type sale invoice',
                'methods': [CRUD]
            },
            'Service/': {
                'name': 'Service',
                'hint': 'service type sale invoice',
                'methods': [CRUD]
            }
        }
    },
    'Sale/Order/': {
        'name': 'Orders',
        'hint': 'sale order type',
        'methods': [ALL],
        'resources': {
            'Item/': {
                'name': 'Item',
                'hint': 'item type sale order',
                'methods': [CRUD]
            },
            'Service/': {
                'name': 'Service',
                'hint': 'service type sale order',
                'methods': [CRUD]
            }
        }
    },
    'Sale/Quote/': {
        'name': 'Quotes',
        'hint': 'sale quote type',
        'methods': [ALL],
        'resources': {
            'Item/': {
                'name': 'Item',
                'hint': 'item type sale quote',
                'methods': [CRUD]
            },
            'Service/': {
                'name': 'Service',
                'hint': 'service type sale quote',
                'methods': [CRUD]
            }
        }
    },
    'GeneralLedger/': {
        'name': 'general_ledger',
        'hint': 'general ledger',
        'resources': {
            'TaxCode/': {
                'name': 'TaxCode',
                'hint': 'tax code',
                'methods': [CRUD]
            },
            'Account/': {
                'name': 'Account',
                'hint': 'account',
                'methods': [CRUD]
            },
            'Category/': {
                'name': 'Category',
                'hint': 'cost center tracking category',
                'methods': [CRUD]
            },
            'Job/': {
                'name': 'Job',
                'hint': 'job',
                'methods': [CRUD]
            },
            'JournalTransaction/': {
                'name': 'JournalTransaction',
                'hint': 'transaction journal',
                'methods': [ALL, GET]
            }
        },
    },
    'Inventory/': {
        'name': 'Inventory',
        'hint': 'inventory',
        'resources': {
            'Item/': {
                'name': 'Item',
                'hint': 'inventory item',
                'methods': [CRUD]
            },
            'ItemPriceMatrix/': {
                'hint': 'inventory item price matrix',
                'name': 'ItemPriceMatrix',
                'methods': [ALL, GET, PUT]
            },
            'Location/': {
                'name': 'Location',
                'hint': 'inventory location',
                'methods': [CRUD]
            },
            'Adjustment/': {
                'name': 'Adjustment',
                'hint': 'inventory adjustment',
                'methods': [CRUD]
            }
        }
    },
    'Purchase/Order/': {
        'name': 'Purchase_Orders',
        'hint': 'purchase order type',
        'methods': [ALL],
        'resources': {
            'Item/': {
                'name': 'Item',
                'hint': 'item type purchase order',
                'methods': [CRUD]
            }
        }
    },
    'Purchase/Bill/': {
        'name': 'Purchase_Bills',
        'hint': 'purchase bill type',
        'methods': [ALL],
        'resources': {
            'Item/': {
                'name': 'Item',
                'hint': 'item type purchase bill',
                'methods': [CRUD]
            },
            'Service/': {
                'name': 'Service',
                'hint': 'service type purchase bill',
                'methods': [CRUD]
            },
            'Miscellaneous/': {
                'name': 'Miscellaneous',
                'hint': 'miscellaneous type purchase bill',
                'methods': [CRUD]
            }
        }
    },
    'Company/': {
        'name': 'Company',
        'hint': 'company',
        'resources': {
            'Preferences/': {
                'name': 'Preferences',
                'hint': 'company data file preference',
                'methods': [ALL]
            }
        }
    },
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
