# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Configuration Management compliance tests -- CM-2, CM-6, CM-7, CM-8."""

import os

import allure
import pytest
import requests


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CM -- Configuration Management")
@allure.story("CM-2 Baseline Configuration")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CM-2: API response headers declare a content-type baseline")
@allure.description("Every API response must include a Content-Type header as part of the baseline configuration.")
@pytest.mark.compliance
@pytest.mark.nist_cm2
def test_cm2_response_declares_content_type(api_base_url: str) -> None:
    with allure.step("Request a known resource"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
    with allure.step("Assert Content-Type header is present"):
        content_type = response.headers.get("Content-Type", "")
        assert content_type, "CM-2 FAIL: response must declare a Content-Type header"
    with allure.step("Assert Content-Type specifies JSON"):
        assert (
            "application/json" in content_type.lower()
        ), f"CM-2 FAIL: API baseline requires application/json, got '{content_type}'"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CM -- Configuration Management")
@allure.story("CM-2 Baseline Configuration")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CM-2: API_BASE_URL environment variable is set and non-empty")
@allure.description("A missing or empty API_BASE_URL indicates a misconfigured baseline environment.")
@pytest.mark.compliance
@pytest.mark.nist_cm2
def test_cm2_api_base_url_is_configured() -> None:
    with allure.step("Read API_BASE_URL from environment"):
        url = os.getenv("API_BASE_URL", "")
    with allure.step("Assert variable is non-empty"):
        assert url, "CM-2 FAIL: API_BASE_URL must be set -- missing baseline configuration"
    with allure.step("Assert URL is reachable"):
        try:
            response = requests.get(url, timeout=10)
            assert (
                response.status_code < 500
            ), f"CM-2 FAIL: baseline API_BASE_URL returned server error {response.status_code}"
        except requests.exceptions.ConnectionError as exc:
            pytest.fail(f"CM-2 FAIL: baseline API_BASE_URL is unreachable -- {exc}")


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CM -- Configuration Management")
@allure.story("CM-2 Baseline Configuration")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("CM-2: API response schema matches baseline structure")
@allure.description("The user resource schema must remain stable.")
@pytest.mark.compliance
@pytest.mark.nist_cm2
def test_cm2_user_schema_matches_baseline(api_base_url: str) -> None:
    baseline_fields = {"id", "name", "username", "email", "address", "phone", "website", "company"}
    with allure.step("Fetch a single user record"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
        assert response.status_code == 200, f"CM-2 FAIL: expected 200, got {response.status_code}"
    with allure.step("Assert response schema matches baseline"):
        actual = set(response.json().keys())
        missing = baseline_fields - actual
        assert not missing, f"CM-2 FAIL: user schema missing baseline fields: {missing}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CM -- Configuration Management")
@allure.story("CM-6 Configuration Settings")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("CM-6: API enforces HTTPS-only configuration")
@allure.description("The system configuration must enforce HTTPS.")
@pytest.mark.compliance
@pytest.mark.nist_cm6
def test_cm6_api_enforces_https_only(api_base_url: str) -> None:
    with allure.step("Assert configuration uses HTTPS scheme"):
        assert api_base_url.startswith(
            "https://"
        ), f"CM-6 FAIL: system configuration must enforce HTTPS, got '{api_base_url}'"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CM -- Configuration Management")
@allure.story("CM-7 Least Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CM-7: Unsupported HTTP methods return 405")
@allure.description("The API must disable unnecessary HTTP methods.")
@pytest.mark.compliance
@pytest.mark.nist_cm7
def test_cm7_unsupported_methods_return_405(api_base_url: str) -> None:
    with allure.step("Send PATCH request to read-only endpoint"):
        response = requests.patch(f"{api_base_url}/users", timeout=10)
    with allure.step("Assert 405 or 404"):
        assert response.status_code in (
            404,
            405,
        ), f"CM-7 FAIL: unsupported method must return 404/405, got {response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CM -- Configuration Management")
@allure.story("CM-7 Least Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CM-7: Non-existent endpoints return 404, not server internals")
@allure.description("Disabled endpoints must return 404, not 500.")
@pytest.mark.compliance
@pytest.mark.nist_cm7
def test_cm7_nonexistent_endpoint_returns_404_not_server_error(api_base_url: str) -> None:
    with allure.step("Request a non-existent endpoint"):
        response = requests.get(f"{api_base_url}/admin/config/internal", timeout=10)
    with allure.step("Assert 404"):
        assert response.status_code == 404, f"CM-7 FAIL: disabled endpoint must return 404, got {response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CM -- Configuration Management")
@allure.story("CM-7 Least Functionality")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("CM-7: Response body does not expose server version or platform")
@allure.description("Server headers must not advertise platform details.")
@pytest.mark.compliance
@pytest.mark.nist_cm7
def test_cm7_response_does_not_expose_server_version(api_base_url: str) -> None:
    with allure.step("Send request and inspect response headers"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
    with allure.step("Assert Server header does not expose version details"):
        server_header = response.headers.get("Server", "")
        version_patterns = ["apache/", "nginx/", "iis/", "express/", "php/", "tomcat/"]
        exposed = [p for p in version_patterns if p in server_header.lower()]
        assert not exposed, f"CM-7 FAIL: server header must not expose version details, found: {exposed}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CM -- Configuration Management")
@allure.story("CM-8 System Component Inventory")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CM-8: All user accounts are inventoried and retrievable")
@allure.description("The system must maintain a complete retrievable inventory of all user account components.")
@pytest.mark.compliance
@pytest.mark.nist_cm8
def test_cm8_user_account_inventory_is_complete(api_base_url: str) -> None:
    with allure.step("Retrieve full user account inventory"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"CM-8 FAIL: inventory endpoint must return 200, got {response.status_code}"
    with allure.step("Assert inventory is non-empty"):
        users = response.json()
        assert users, "CM-8 FAIL: system component inventory must not be empty"
    with allure.step("Assert every inventory record has a unique identifier"):
        ids = [u.get("id") for u in users]
        assert all(ids), "CM-8 FAIL: every inventory record must have an id field"
        assert len(ids) == len(set(ids)), "CM-8 FAIL: inventory IDs must be unique"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CM -- Configuration Management")
@allure.story("CM-8 System Component Inventory")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CM-8: Individual component lookup matches inventory record")
@allure.description("A single component retrieved by ID must match the corresponding inventory record.")
@pytest.mark.compliance
@pytest.mark.nist_cm8
def test_cm8_individual_component_matches_inventory(api_base_url: str) -> None:
    with allure.step("Retrieve full inventory"):
        all_response = requests.get(f"{api_base_url}/users", timeout=10)
        assert all_response.status_code == 200
        inventory = {u["id"]: u for u in all_response.json()}
    with allure.step("Retrieve individual component by ID"):
        target_id = 1
        single_response = requests.get(f"{api_base_url}/users/{target_id}", timeout=10)
        assert (
            single_response.status_code == 200
        ), f"CM-8 FAIL: component {target_id} must be retrievable from inventory"
    with allure.step("Assert individual record matches inventory"):
        single = single_response.json()
        inventory_record = inventory.get(target_id)
        assert single == inventory_record, f"CM-8 FAIL: component {target_id} does not match its inventory record"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CM -- Configuration Management")
@allure.story("CM-8 System Component Inventory")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("CM-8: Post components are attributed to known users")
@allure.description("All post components must be attributed to an inventoried user account.")
@pytest.mark.compliance
@pytest.mark.nist_cm8
def test_cm8_post_components_attributed_to_known_users(api_base_url: str) -> None:
    with allure.step("Retrieve user inventory"):
        users_response = requests.get(f"{api_base_url}/users", timeout=10)
        assert users_response.status_code == 200
        known_user_ids = {u["id"] for u in users_response.json()}
    with allure.step("Retrieve post component inventory"):
        posts_response = requests.get(f"{api_base_url}/posts", timeout=10)
        assert posts_response.status_code == 200
    with allure.step("Assert every post is attributed to a known user"):
        orphaned = [p for p in posts_response.json() if p.get("userId") not in known_user_ids]
        assert not orphaned, f"CM-8 FAIL: {len(orphaned)} post(s) are not attributed to any inventoried user"
