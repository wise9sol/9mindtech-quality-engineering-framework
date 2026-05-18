import time

import pytest
import requests
from jsonschema import validate

from utils.schemas.post import POST, POST_LIST


@pytest.mark.api
@pytest.mark.regression
def test_response_body_contains_required_fields(api_base_url: str) -> None:
    """Verify the API response body contains all required top-level fields."""
    start = time.time()
    response = requests.get(f"{api_base_url}/posts/1")
    elapsed_ms = (time.time() - start) * 1000

    assert response.status_code == 200
    assert elapsed_ms < 2000
    validate(instance=response.json(), schema=POST)


@pytest.mark.api
@pytest.mark.regression
def test_response_values_have_expected_types(api_base_url: str) -> None:
    """Verify returned field types match the schema contract."""
    start = time.time()
    response = requests.get(f"{api_base_url}/posts/1")
    elapsed_ms = (time.time() - start) * 1000

    assert response.status_code == 200
    assert elapsed_ms < 2000
    validate(instance=response.json(), schema=POST)


@pytest.mark.api
@pytest.mark.regression
def test_posts_list_matches_schema(api_base_url: str) -> None:
    """Verify the posts list endpoint returns a valid array of post objects."""
    start = time.time()
    response = requests.get(f"{api_base_url}/posts")
    elapsed_ms = (time.time() - start) * 1000

    assert response.status_code == 200
    assert elapsed_ms < 2000
    validate(instance=response.json(), schema=POST_LIST)