# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
import pytest
import requests
from jsonschema import validate

from utils.schemas.post import POST_CREATED


@pytest.mark.api
@pytest.mark.regression
def test_post_returns_201_on_valid_payload(api_base_url: str) -> None:
    """Verify POST with a valid payload returns 201 within acceptable time."""
    payload = {"title": "test", "body": "test body", "userId": 1}
    response = requests.post(f"{api_base_url}/posts", json=payload)

    assert response.status_code == 201
    assert response.elapsed.total_seconds() * 1000 < 2000
    validate(instance=response.json(), schema=POST_CREATED)


@pytest.mark.api
@pytest.mark.regression
def test_post_response_mirrors_submitted_data(api_base_url: str) -> None:
    """Verify POST response body echoes back the submitted fields."""
    payload = {"title": "mirror test", "body": "echo this", "userId": 42}
    response = requests.post(f"{api_base_url}/posts", json=payload)

    assert response.status_code == 201
    assert response.elapsed.total_seconds() * 1000 < 2000
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
