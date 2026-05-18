"""jsonschema definitions for the JSONPlaceholder /posts resource."""

POST: dict[str, object] = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "additionalProperties": False,
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "userId": {"type": "integer"},
    },
}

POST_LIST: dict[str, object] = {
    "type": "array",
    "items": POST,
}

POST_CREATED: dict[str, object] = {
    "type": "object",
    "required": ["id"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "userId": {"type": "integer"},
    },
}
