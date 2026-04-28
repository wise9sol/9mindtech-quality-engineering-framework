import time

import pytest
import requests


@pytest.mark.api
@pytest.mark.regression
def test_post_returns_201_on_valid_payload(api_base_url: str) -> None:
    """Verify POST with a valid payload returns 201 within acceptable time."""
    payload = {"title": "test", "body": "test body", "userId": 1}

    start = time.time()
    response = requests.post(f"{api_base_url}/posts", json=payload)
    elapsed_ms = (time.time() - start) * 1000

    assert response.status_code == 201
    assert elapsed_ms < 2000


@pytest.mark.api
@pytest.mark.regression
def test_post_returns_201_on_second_valid_payload(api_base_url: str) -> None:
    """Verify POST with another valid payload also returns 201."""
    payload = {"title": "second post", "body": "more content", "userId": 2}

    response = requests.post(f"{api_base_url}/posts", json=payload)

    assert response.status_code == 201
    assert "id" in response.json()