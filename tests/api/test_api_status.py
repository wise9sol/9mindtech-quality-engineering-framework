import pytest
import requests


@pytest.mark.api
@pytest.mark.smoke
def test_api_returns_exactly_100_posts(api_base_url: str) -> None:
    """Verify the posts endpoint returns the full set of 100 resources."""
    response = requests.get(f"{api_base_url}/posts")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    assert response.elapsed.total_seconds() * 1000 < 2000
    assert len(response.json()) == 100
