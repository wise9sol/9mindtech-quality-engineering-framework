import time

import pytest
import requests


@pytest.mark.api
@pytest.mark.smoke
def test_get_returns_200_for_health_endpoint(api_base_url: str) -> None:
    """Verify the posts endpoint responds with 200 within acceptable time."""
    start = time.time()
    response = requests.get(f"{api_base_url}/posts/1")
    elapsed_ms = (time.time() - start) * 1000
    assert response.status_code == 200
    assert elapsed_ms < 2000


@pytest.mark.api
@pytest.mark.regression
def test_get_returns_correct_content_type(api_base_url: str) -> None:
    """Verify GET responses include an application/json content-type header."""
    response = requests.get(f"{api_base_url}/posts/1")
    assert "application/json" in response.headers.get("Content-Type", "")