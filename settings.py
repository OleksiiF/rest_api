from run import AuthForNewItem

MONGO_HOST = 'localhost'
MONGO_PORT = 27017

RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET']
API_VERSION = 'v1'

DOMAIN = {
    'users': {
    'resource_methods': ['POST'],
        'schema': {
            'username': {
                'type': 'string',
                'minlength': 5,
                'maxlength': 32,
                'required': True,
                'unique': True,
            },
            'password': {
                'type': 'string',
                'minlength': 8,
                'maxlength': 32,
                'required': True,
            }
        }
    },

    'categories': {
        'schema': {
            'title': {
                'type': 'string',
                'minlength': 5,
                'maxlength': 32,
                'required': True,
                'unique': True
            },
            'description': {
                'type': 'string',
                'minlength': 10,
                'maxlength': 300,
            },
            'parent_category': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'categories',
                    'field': '_id',
                    'embeddable': True
                }
            }
        },
        # comment it if you want add item through API
        'resource_methods': ['GET']
    },

    'items': {
        'authentication': AuthForNewItem,
        'public_methods': ['GET'],
        'public_item_methods': ['GET'],
        'schema': {
            'name': {
                'type': 'string',
                'minlength': 5,
                'maxlength': 32,
                'required': True,
            },
            'price': {
                'type': 'float'
            },
            'views': {
                'type': 'integer',
                'default': 0
            },
            'photo': {
                'type': 'media',
            },
            'parent_category': {
                'required': True,
                'type': 'objectid',
                'data_relation': {
                    'resource': 'categories',
                    'field': '_id',
                    'embeddable': True
                }
            },
            'owner': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'users',
                    'field': '_id',
                    'embeddable': True
                }
            }
        }
    }
}
