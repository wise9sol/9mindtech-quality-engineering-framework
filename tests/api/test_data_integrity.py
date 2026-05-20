# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
import pytest
import requests
from jsonschema import validate

from utils.schemas.post import POST, POST_LIST


@pytest.mark.api
@pytest.mark.regression
def test_response_body_contains_required_fields(api_base_url: str) -> None:
    """Verify the API response body conforms to the POST schema."""
    response = requests.get(f"{api_base_url}/posts/1")

    assert response.status_code == 200
    assert response.elapsed.total_seconds() * 1000 < 2000
    validate(instance=response.json(), schema=POST)


@pytest.mark.api
@pytest.mark.regression
def test_posts_list_matches_schema(api_base_url: str) -> None:
    """Verify the posts list endpoint returns a valid array of post objects."""
    response = requests.get(f"{api_base_url}/posts")

    assert response.status_code == 200
    assert response.elapsed.total_seconds() * 1000 < 2000
    validate(instance=response.json(), schema=POST_LIST)
