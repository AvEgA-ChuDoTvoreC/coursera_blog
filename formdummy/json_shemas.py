REVIEW_SCHEMA = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "feedback": {
            "type": "string",
            "minLength": 3,
            "maxLength": 20
            },
        "grade": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
        },
    },
    "required":  ["feedback", "grade"]
}
