import time

import pytest
import requests


@pytest.mark.api
@pytest.mark.regression
def test_api_status(api_base_url: str) -> None:
    """Verify the posts endpoint is healthy and responds within acceptable time."""
    start = time.time()
    response = requests.get(f"{api_base_url}/posts")
    elapsed_ms = (time.time() - start) * 1000

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    assert len(response.json()) > 0
    assert elapsed_ms < 2000