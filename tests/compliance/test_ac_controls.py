# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Access Control compliance tests — AC-2, AC-3, AC-17."""

import os

import allure
import pytest
import requests

API_BASE = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
BASE_URL = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")


# ── AC-2: Account Management ───────────────────────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AC — Access Control")
@allure.story("AC-2 Account Management")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("AC-2: Account list exposes only expected schema fields")
@allure.description("Every account record must contain id, name, email, and username.")
@pytest.mark.compliance
@pytest.mark.nist_ac2
def test_ac2_account_list_exposes_expected_fields() -> None:
    with allure.step("Request the user account list"):
        response = requests.get(f"{API_BASE}/users", timeout=10)

    with allure.step("Assert 200 status and response time"):
        assert response.status_code == 200, (
            f"AC-2 FAIL: account list endpoint must return 200, got {response.status_code}"
        )
        assert response.elapsed.total_seconds() * 1000 < 2000, (
            "AC-2 FAIL: account list must respond within 2000ms"
        )

    with allure.step("Assert required fields are present on every record"):
        users = response.json()
        required = {"id", "name", "email", "username"}
        for user in users:
            missing = required - user.keys()
            if missing:
                allure.attach(
                    f"User {user.get('id')} missing fields: {missing}\n{user}",
                    name="AC-2 Missing Fields",
                    attachment_type=allure.attachment_type.TEXT,
                )
            assert not missing, (
                f"AC-2 FAIL: account record must contain {required}, missing {missing}"
            )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AC — Access Control")
@allure.story("AC-2 Account Management")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("AC-2: All account IDs are unique")
@allure.description("Duplicate account IDs indicate a broken account management control.")
@pytest.mark.compliance
@pytest.mark.nist_ac2
def test_ac2_account_ids_are_unique() -> None:
    with allure.step("Fetch all user accounts"):
        response = requests.get(f"{API_BASE}/users", timeout=10)
        assert response.status_code == 200, (
            f"AC-2 FAIL: expected 200, got {response.status_code}"
        )

    with allure.step("Extract and deduplicate account IDs"):
        users = response.json()
        ids = [u["id"] for u in users]
        duplicates = [i for i in ids if ids.count(i) > 1]

    with allure.step("Assert no duplicate IDs exist"):
        if duplicates:
            allure.attach(
                f"Duplicate IDs: {duplicates}",
                name="AC-2 Duplicate Account IDs",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not duplicates, (
            f"AC-2 FAIL: account IDs must be unique, found duplicates: {duplicates}"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AC — Access Control")
@allure.story("AC-2 Account Management")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("AC-2: Every account is linked to an organisation")
@allure.description("Account records without an organisation cannot be audited for access scope.")
@pytest.mark.compliance
@pytest.mark.nist_ac2
def test_ac2_accounts_linked_to_organisation() -> None:
    with allure.step("Fetch all user accounts"):
        response = requests.get(f"{API_BASE}/users", timeout=10)
        assert response.status_code == 200, (
            f"AC-2 FAIL: expected 200, got {response.status_code}"
        )

    with allure.step("Assert every account contains a company field"):
        for user in response.json():
            if "company" not in user:
                allure.attach(
                    f"User id={user.get('id')} missing company field",
                    name="AC-2 Missing Organisation",
                    attachment_type=allure.attachment_type.TEXT,
                )
            assert "company" in user, (
                f"AC-2 FAIL: account must be linked to an organisation, user id={user.get('id')}"
            )


# ── AC-3: Access Enforcement ───────────────────────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AC — Access Control")
@allure.story("AC-3 Access Enforcement")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("AC-3: Response body does not expose sensitive keywords")
@allure.description("API responses must not leak passwords, secrets, or private keys.")
@pytest.mark.compliance
@pytest.mark.nist_ac3
def test_ac3_response_does_not_expose_sensitive_keywords() -> None:
    with allure.step("Send request to user resource"):
        response = requests.get(f"{API_BASE}/users/1", timeout=10)
        assert response.status_code == 200, (
            f"AC-3 FAIL: expected 200, got {response.status_code}"
        )

    with allure.step("Scan response body for sensitive keywords"):
        body = response.text.lower()
        for keyword in ("password", "secret", "private_key", "access_token"):
            if keyword in body:
                allure.attach(
                    f"Keyword '{keyword}' found in:\n{response.text[:500]}",
                    name="AC-3 Sensitive Data Exposure",
                    attachment_type=allure.attachment_type.TEXT,
                )
            assert keyword not in body, (
                f"AC-3 FAIL: response must not expose '{keyword}'"
            )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AC — Access Control")
@allure.story("AC-3 Access Enforcement")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("AC-3: Non-existent resource returns 404, not data")
@allure.description("Out-of-range resource IDs must return 404, not internal data.")
@pytest.mark.compliance
@pytest.mark.nist_ac3
def test_ac3_nonexistent_resource_returns_404() -> None:
    with allure.step("Request a resource with an out-of-range ID"):
        response = requests.get(f"{API_BASE}/users/99999", timeout=10)

    with allure.step("Assert 404 status"):
        if response.status_code != 404:
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:500]}",
                name="AC-3 Unexpected Response",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert response.status_code == 404, (
            f"AC-3 FAIL: non-existent resource must return 404, got {response.status_code}"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AC — Access Control")
@allure.story("AC-3 Access Enforcement")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("AC-3: Query filter restricts results to authorised records only")
@allure.description("A userId filter must return only posts belonging to that user.")
@pytest.mark.compliance
@pytest.mark.nist_ac3
def test_ac3_query_filter_restricts_results_to_authorised_records() -> None:
    target_user_id = 1

    with allure.step(f"Fetch posts filtered to userId={target_user_id}"):
        response = requests.get(
            f"{API_BASE}/posts", params={"userId": target_user_id}, timeout=10
        )
        assert response.status_code == 200, (
            f"AC-3 FAIL: expected 200, got {response.status_code}"
        )

    with allure.step("Assert all returned records belong to the requested user"):
        wrong = [p for p in response.json() if p.get("userId") != target_user_id]
        if wrong:
            allure.attach(
                f"Records with wrong userId:\n{wrong}",
                name="AC-3 Access Leak",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not wrong, (
            f"AC-3 FAIL: filter must restrict results to userId={target_user_id}, "
            f"found {len(wrong)} non-matching record(s)"
        )


# ── AC-17: Remote Access ───────────────────────────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AC — Access Control")
@allure.story("AC-17 Remote Access")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("AC-17: API_BASE_URL uses HTTPS")
@allure.description("All remote API access must use HTTPS to protect data in transit.")
@pytest.mark.compliance
@pytest.mark.nist_ac17
def test_ac17_api_base_url_uses_https() -> None:
    with allure.step("Read API_BASE_URL from environment"):
        url = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

    with allure.step("Assert scheme is https"):
        if not url.startswith("https://"):
            allure.attach(
                f"API_BASE_URL={url}",
                name="AC-17 Insecure URL",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert url.startswith("https://"), (
            f"AC-17 FAIL: API_BASE_URL must use HTTPS, got '{url}'"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AC — Access Control")
@allure.story("AC-17 Remote Access")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("AC-17: BASE_URL uses HTTPS")
@allure.description("The application BASE_URL must use HTTPS to secure all remote sessions.")
@pytest.mark.compliance
@pytest.mark.nist_ac17
def test_ac17_base_url_uses_https() -> None:
    with allure.step("Read BASE_URL from environment"):
        url = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")

    with allure.step("Assert scheme is https"):
        if not url.startswith("https://"):
            allure.attach(
                f"BASE_URL={url}",
                name="AC-17 Insecure Base URL",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert url.startswith("https://"), (
            f"AC-17 FAIL: BASE_URL must use HTTPS, got '{url}'"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AC — Access Control")
@allure.story("AC-17 Remote Access")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("AC-17: Remote API responds within 2000ms latency threshold")
@allure.description("Remote connections must respond within 2000ms to ensure availability.")
@pytest.mark.compliance
@pytest.mark.nist_ac17
def test_ac17_remote_api_responds_within_latency_threshold() -> None:
    threshold_ms = 2000

    with allure.step("Send remote request and capture elapsed time"):
        response = requests.get(f"{API_BASE}/users/1", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000

    with allure.step(f"Assert response time < {threshold_ms}ms"):
        if elapsed_ms >= threshold_ms:
            allure.attach(
                f"Elapsed: {elapsed_ms:.0f}ms  Threshold: {threshold_ms}ms",
                name="AC-17 Latency Breach",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert elapsed_ms < threshold_ms, (
            f"AC-17 FAIL: remote API must respond within {threshold_ms}ms, took {elapsed_ms:.0f}ms"
        )
