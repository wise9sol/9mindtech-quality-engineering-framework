POST = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "additionalProperties": False,
    "properties": {
        "id":     {"type": "integer"},
        "title":  {"type": "string"},
        "body":   {"type": "string"},
        "userId": {"type": "integer"},
    },
}

POST_LIST = {
    "type": "array",
    "items": POST,
}

POST_CREATED = {
    "type": "object",
    "required": ["id"],
    "properties": {
        "id":     {"type": "integer"},
        "title":  {"type": "string"},
        "body":   {"type": "string"},
        "userId": {"type": "integer"},
    },
}
