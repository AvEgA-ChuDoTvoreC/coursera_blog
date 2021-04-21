

GOODS_ADD_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 64
        },
        'description': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024
        },
        'price': {
            'anyOf': [
                {
                    'type': 'integer',
                    'minimum': 1,
                    'maximum': 1000000,
                },
                {
                    'type': 'string',
                    'minLength': 1,
                    'pattern': '^\d+$'
                }
            ]
        },
    },
    'required': ['title', 'description', 'price']
}

GOODS_REVIEW_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'text': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1024
        },
        'grade': {
            'anyOf': [
                {
                    'type': 'integer',
                    'minimum': 1,
                    'maximum': 10,
                },
                {
                    'type': 'string',
                    'minLength': 1,
                    'pattern': '^\d+$'
                }
            ]
        },
    },
    'required': ['text', 'grade']
}
