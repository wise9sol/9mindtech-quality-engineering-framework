import pytest
import requests
from jsonschema import validate

from utils.schemas.post import POST


@pytest.mark.api
@pytest.mark.smoke
def test_get_returns_200_for_health_endpoint(api_base_url: str) -> None:
    """Verify the posts endpoint responds with 200 within acceptable time."""
    response = requests.get(f"{api_base_url}/posts/1")

    assert response.status_code == 200
    assert response.elapsed.total_seconds() * 1000 < 2000
    validate(instance=response.json(), schema=POST)


@pytest.mark.api
@pytest.mark.regression
def test_get_returns_correct_content_type(api_base_url: str) -> None:
    """Verify GET responses include an application/json content-type header within acceptable time."""
    response = requests.get(f"{api_base_url}/posts/1")

    assert "application/json" in response.headers.get("Content-Type", "")
    assert response.elapsed.total_seconds() * 1000 < 2000
    validate(instance=response.json(), schema=POST)
