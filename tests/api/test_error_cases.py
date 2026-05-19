import pytest
import requests


@pytest.mark.api
@pytest.mark.regression
def test_get_returns_404_for_nonexistent_post(api_base_url: str) -> None:
    """Verify GET on a non-existent resource ID returns 404."""
    response = requests.get(f"{api_base_url}/posts/99999")

    assert response.status_code == 404
    assert response.elapsed.total_seconds() * 1000 < 2000


@pytest.mark.api
@pytest.mark.regression
def test_get_returns_404_for_undefined_endpoint(api_base_url: str) -> None:
    """Verify GET on an undefined endpoint returns 404."""
    response = requests.get(f"{api_base_url}/nonexistent")

    assert response.status_code == 404
    assert response.elapsed.total_seconds() * 1000 < 2000
