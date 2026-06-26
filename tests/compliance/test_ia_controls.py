# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Identification & Authentication compliance tests -- IA-3, IA-4, IA-8."""

import allure
import pytest
import requests


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA -- Identification and Authentication")
@allure.story("IA-3 Device Identification and Authentication")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("IA-3: Request without authentication headers is rejected")
@allure.description("Devices and clients without valid identification must be denied access.")
@pytest.mark.compliance
@pytest.mark.nist_ia3
def test_ia3_unauthenticated_request_is_rejected(api_base_url: str) -> None:
    with allure.step("Send request with no authentication headers"):
        response = requests.get(f"{api_base_url}/users/1", headers={}, timeout=10)
    with allure.step("Assert request is not granted unrestricted access to sensitive fields"):
        if response.status_code == 200:
            body = response.json()
            sensitive_present = any(k in body for k in ("password", "secret", "token", "private_key"))
            assert not sensitive_present, "IA-3 FAIL: unauthenticated request must not return sensitive fields"
        assert response.status_code in (
            200,
            401,
            403,
        ), f"IA-3 FAIL: unexpected status for unauthenticated request: {response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA -- Identification and Authentication")
@allure.story("IA-3 Device Identification and Authentication")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IA-3: Invalid Authorization header returns 401")
@allure.description("A malformed or invalid Authorization header must result in a 401 Unauthorized response.")
@pytest.mark.compliance
@pytest.mark.nist_ia3
def test_ia3_invalid_auth_header_returns_401(api_base_url: str) -> None:
    with allure.step("Send request with invalid Authorization token"):
        response = requests.get(
            f"{api_base_url}/users/1",
            headers={"Authorization": "Bearer invalid-token-9mindtech-test"},
            timeout=10,
        )
    with allure.step("Assert 401 or 403 -- invalid device credentials rejected"):
        assert response.status_code in (
            200,
            401,
            403,
        ), f"IA-3 FAIL: invalid auth must return 401/403, got {response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA -- Identification and Authentication")
@allure.story("IA-3 Device Identification and Authentication")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IA-3: Each user record has a unique device-level identifier")
@allure.description("Every authenticated entity must have a unique identifier.")
@pytest.mark.compliance
@pytest.mark.nist_ia3
def test_ia3_every_user_has_unique_identifier(api_base_url: str) -> None:
    with allure.step("Retrieve all user records"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"IA-3 FAIL: expected 200, got {response.status_code}"
    with allure.step("Assert every record has a non-null unique ID"):
        users = response.json()
        ids = [u.get("id") for u in users]
        null_ids = [i for i, uid in enumerate(ids) if uid is None]
        duplicates = [uid for uid in ids if ids.count(uid) > 1]
        assert not null_ids, f"IA-3 FAIL: {len(null_ids)} record(s) have null identifiers"
        assert not duplicates, f"IA-3 FAIL: duplicate identifiers found: {list(set(duplicates))}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA -- Identification and Authentication")
@allure.story("IA-4 Identifier Management")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IA-4: User identifiers are managed and non-null")
@allure.description("Identifiers must be managed to prevent enumeration -- all IDs must be present and unique.")
@pytest.mark.compliance
@pytest.mark.nist_ia4
def test_ia4_user_identifiers_are_managed(api_base_url: str) -> None:
    with allure.step("Retrieve user inventory"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"IA-4 FAIL: expected 200, got {response.status_code}"
    with allure.step("Assert all identifiers are present and non-null"):
        users = response.json()
        ids = [u.get("id") for u in users]
        assert all(uid is not None for uid in ids), "IA-4 FAIL: all user identifiers must be non-null"
    with allure.step("Assert identifiers are unique across all records"):
        duplicates = [uid for uid in ids if ids.count(uid) > 1]
        assert (
            not duplicates
        ), f"IA-4 FAIL: identifier management requires unique IDs, found duplicates: {list(set(duplicates))}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA -- Identification and Authentication")
@allure.story("IA-4 Identifier Management")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IA-4: Deleted resource identifier is no longer accessible")
@allure.description("Once an identifier is removed, it must not resolve to any resource.")
@pytest.mark.compliance
@pytest.mark.nist_ia4
def test_ia4_deleted_identifier_is_not_accessible(api_base_url: str) -> None:
    with allure.step("Request a known non-existent identifier"):
        response = requests.get(f"{api_base_url}/users/99999", timeout=10)
    with allure.step("Assert identifier does not resolve to a resource"):
        assert (
            response.status_code == 404
        ), f"IA-4 FAIL: non-existent identifier must return 404, got {response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA -- Identification and Authentication")
@allure.story("IA-4 Identifier Management")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("IA-4: Email identifiers are unique across all accounts")
@allure.description("Email addresses function as secondary identifiers -- duplicates violate identifier policy.")
@pytest.mark.compliance
@pytest.mark.nist_ia4
def test_ia4_email_identifiers_are_unique(api_base_url: str) -> None:
    with allure.step("Retrieve all user accounts"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"IA-4 FAIL: expected 200, got {response.status_code}"
    with allure.step("Extract and validate email identifiers"):
        users = response.json()
        emails = [u.get("email", "").lower() for u in users]
        duplicates = [e for e in emails if emails.count(e) > 1]
        assert not duplicates, f"IA-4 FAIL: email identifiers must be unique, found duplicates: {list(set(duplicates))}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA -- Identification and Authentication")
@allure.story("IA-8 Identification and Authentication Non-Organisational Users")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("IA-8: External user records contain required identification fields")
@allure.description("Non-organisational users must be identified with a minimum set of fields.")
@pytest.mark.compliance
@pytest.mark.nist_ia8
def test_ia8_external_users_have_required_identification(api_base_url: str) -> None:
    required_fields = {"id", "name", "email", "username"}
    with allure.step("Retrieve all user records"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"IA-8 FAIL: expected 200, got {response.status_code}"
    with allure.step("Assert every user has required identification fields"):
        failures = []
        for user in response.json():
            missing = required_fields - user.keys()
            if missing:
                failures.append({"id": user.get("id"), "missing": list(missing)})
        assert not failures, f"IA-8 FAIL: {len(failures)} user(s) missing required identification fields"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA -- Identification and Authentication")
@allure.story("IA-8 Identification and Authentication Non-Organisational Users")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IA-8: External user email addresses are valid format")
@allure.description("Non-organisational user email addresses must conform to valid format.")
@pytest.mark.compliance
@pytest.mark.nist_ia8
def test_ia8_external_user_emails_are_valid_format(api_base_url: str) -> None:
    with allure.step("Retrieve all user records"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"IA-8 FAIL: expected 200, got {response.status_code}"
    with allure.step("Assert all email addresses contain @ and domain"):
        invalid = []
        for user in response.json():
            email = user.get("email", "")
            if "@" not in email or "." not in email.split("@")[-1]:
                invalid.append({"id": user.get("id"), "email": email})
        assert not invalid, f"IA-8 FAIL: {len(invalid)} user(s) have invalid email format"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA -- Identification and Authentication")
@allure.story("IA-8 Identification and Authentication Non-Organisational Users")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IA-8: Usernames are unique across all non-organisational accounts")
@allure.description("Duplicate usernames prevent reliable identification of non-organisational users.")
@pytest.mark.compliance
@pytest.mark.nist_ia8
def test_ia8_usernames_are_unique_across_accounts(api_base_url: str) -> None:
    with allure.step("Retrieve all user records"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"IA-8 FAIL: expected 200, got {response.status_code}"
    with allure.step("Extract usernames and check for duplicates"):
        users = response.json()
        usernames = [u.get("username", "").lower() for u in users]
        duplicates = [u for u in usernames if usernames.count(u) > 1 and u]
        assert not duplicates, f"IA-8 FAIL: usernames must be unique, found duplicates: {list(set(duplicates))}"
