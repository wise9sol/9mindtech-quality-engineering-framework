import pytest
import requests


@pytest.mark.api
@pytest.mark.regression
def test_response_body_contains_required_fields(api_base_url: str) -> None:
    """Verify the API response body contains all required top-level fields."""
    response = requests.get(f"{api_base_url}/posts/1")

    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "title" in body
    assert "body" in body
    assert "userId" in body


@pytest.mark.api
@pytest.mark.regression
def test_response_values_have_expected_types(api_base_url: str) -> None:
    """Verify returned field types match the schema contract."""
    response = requests.get(f"{api_base_url}/posts/1")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body.get("id"), int)
    assert isinstance(body.get("title"), str)
    assert isinstance(body.get("body"), str)
    assert isinstance(body.get("userId"), int)