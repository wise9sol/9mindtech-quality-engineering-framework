import pytest
import requests
from jsonschema import validate

from utils.schemas.post import POST


@pytest.mark.api
@pytest.mark.regression
def test_put_updates_post_and_returns_200(api_base_url: str) -> None:
    """Verify PUT with a full payload returns 200 and the updated resource."""
    payload = {"id": 1, "title": "updated title", "body": "updated body", "userId": 1}
    response = requests.put(f"{api_base_url}/posts/1", json=payload)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() * 1000 < 2000
    validate(instance=response.json(), schema=POST)
    assert response.json()["title"] == "updated title"


@pytest.mark.api
@pytest.mark.regression
def test_patch_updates_post_field_and_returns_200(api_base_url: str) -> None:
    """Verify PATCH with a partial payload returns 200 and reflects the change."""
    payload = {"title": "patched title"}
    response = requests.patch(f"{api_base_url}/posts/1", json=payload)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() * 1000 < 2000
    assert response.json()["title"] == "patched title"


@pytest.mark.api
@pytest.mark.regression
def test_delete_post_returns_200(api_base_url: str) -> None:
    """Verify DELETE on an existing resource returns 200 and an empty body."""
    response = requests.delete(f"{api_base_url}/posts/1")

    assert response.status_code == 200
    assert response.elapsed.total_seconds() * 1000 < 2000
    assert response.json() == {}
