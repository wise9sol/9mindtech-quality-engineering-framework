import pytest
import requests


@pytest.mark.api
@pytest.mark.regression
def test_api_status():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    assert len(response.json()) > 0