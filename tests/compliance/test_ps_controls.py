# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Personnel Security compliance tests -- PS-3, PS-6."""

import re

import allure
import pytest
import requests

# -- PS-3: Personnel Screening --------------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PS -- Personnel Security")
@allure.story("PS-3 Personnel Screening")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PS-3: API enforces identity verification -- all user records contain required identity fields")
@allure.description("Personnel screening requires verified identities -- all records must contain identity fields.")
@pytest.mark.compliance
@pytest.mark.nist_ps3
def test_ps3_user_records_contain_required_identity_fields(api_base_url: str) -> None:
    identity_fields = {"id", "name", "username", "email"}

    with allure.step("Retrieve all user records"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert response.status_code == 200, f"PS-3 FAIL: expected 200, got {response.status_code}"
        assert elapsed_ms < 2000, f"PS-3 FAIL: response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert every user record contains required identity fields"):
        failures = []
        for user in response.json():
            missing = identity_fields - user.keys()
            if missing:
                failures.append({"id": user.get("id"), "missing": list(missing)})

    with allure.step("Assert no identity field gaps exist"):
        if failures:
            allure.attach(
                f"Records with missing identity fields:\n{failures}",
                name="PS-3 Identity Field Gaps",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not failures
        ), f"PS-3 FAIL: {len(failures)} record(s) missing identity fields required for screening: {failures}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PS -- Personnel Security")
@allure.story("PS-3 Personnel Screening")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PS-3: All user identities are unique -- no duplicate personnel records")
@allure.description("Personnel screening requires unique identities -- duplicate records indicate a screening gap.")
@pytest.mark.compliance
@pytest.mark.nist_ps3
def test_ps3_all_user_identities_are_unique(api_base_url: str) -> None:
    with allure.step("Retrieve all user records"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"PS-3 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert all user IDs are unique"):
        users = response.json()
        ids = [u.get("id") for u in users]
        duplicate_ids = [uid for uid in ids if ids.count(uid) > 1]
        if duplicate_ids:
            allure.attach(
                f"Duplicate IDs: {list(set(duplicate_ids))}",
                name="PS-3 Duplicate Personnel IDs",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not duplicate_ids
        ), f"PS-3 FAIL: duplicate personnel IDs found -- screening gap: {list(set(duplicate_ids))}"

    with allure.step("Assert all email addresses are unique"):
        emails = [u.get("email", "").lower() for u in users]
        duplicate_emails = [e for e in emails if emails.count(e) > 1 and e]
        if duplicate_emails:
            allure.attach(
                f"Duplicate emails: {list(set(duplicate_emails))}",
                name="PS-3 Duplicate Personnel Emails",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not duplicate_emails
        ), f"PS-3 FAIL: duplicate personnel emails found -- screening gap: {list(set(duplicate_emails))}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PS -- Personnel Security")
@allure.story("PS-3 Personnel Screening")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("PS-3: Personnel records do not expose sensitive screening data")
@allure.description("Screening data must not be exposed in API responses -- only identity fields are permitted.")
@pytest.mark.compliance
@pytest.mark.nist_ps3
def test_ps3_personnel_records_do_not_expose_screening_data(api_base_url: str) -> None:
    screening_keywords = ["ssn", "clearance", "background", "criminal", "fingerprint", "password", "secret"]

    with allure.step("Retrieve personnel records and scan for screening data exposure"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"PS-3 FAIL: expected 200, got {response.status_code}"
        body = response.text.lower()
        exposed = [kw for kw in screening_keywords if re.search(rf"\b{re.escape(kw)}\b", body)]

    with allure.step("Assert no sensitive screening data is exposed"):
        if exposed:
            allure.attach(
                f"Screening keywords found: {exposed}",
                name="PS-3 Screening Data Exposure",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not exposed, f"PS-3 FAIL: sensitive screening data exposed in personnel records: {exposed}"


# -- PS-6: Access Agreements ---------------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PS -- Personnel Security")
@allure.story("PS-6 Access Agreements")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PS-6: API enforces access agreements -- only agreed resource types are accessible")
@allure.description("Access agreements define permitted resources -- endpoints outside them must be inaccessible.")
@pytest.mark.compliance
@pytest.mark.nist_ps6
def test_ps6_only_agreed_resource_types_are_accessible(api_base_url: str) -> None:
    agreed_endpoints = ["/users", "/posts", "/comments", "/todos"]
    unagreed_endpoints = ["/admin", "/personnel", "/contracts", "/agreements"]

    with allure.step("Assert agreed endpoints are accessible"):
        for endpoint in agreed_endpoints:
            response = requests.get(f"{api_base_url}{endpoint}", timeout=10)
            assert (
                response.status_code == 200
            ), f"PS-6 FAIL: agreed endpoint {endpoint} must return 200, got {response.status_code}"

    with allure.step("Assert unagreed endpoints are inaccessible"):
        exposed = []
        for endpoint in unagreed_endpoints:
            response = requests.get(f"{api_base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                exposed.append({"endpoint": endpoint, "status": response.status_code})

    with allure.step("Assert no unagreed endpoints are accessible"):
        if exposed:
            allure.attach(
                f"Unagreed endpoints accessible:\n{exposed}",
                name="PS-6 Access Agreement Violation",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not exposed
        ), f"PS-6 FAIL: {len(exposed)} unagreed endpoint(s) accessible outside access agreement: {exposed}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PS -- Personnel Security")
@allure.story("PS-6 Access Agreements")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PS-6: Access agreement terms are reflected in consistent API response structure")
@allure.description("Access agreements define the structure -- all agreed resources must return consistent schemas.")
@pytest.mark.compliance
@pytest.mark.nist_ps6
def test_ps6_access_agreement_reflected_in_response_structure(api_base_url: str) -> None:
    with allure.step("Retrieve user resource and validate agreed schema"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert response.status_code == 200, f"PS-6 FAIL: expected 200, got {response.status_code}"
        assert elapsed_ms < 2000, f"PS-6 FAIL: response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert response conforms to the agreed data structure"):
        agreed_fields = {"id", "name", "username", "email"}
        actual = set(response.json().keys())
        missing = agreed_fields - actual
        if missing:
            allure.attach(
                f"Agreed fields: {agreed_fields}\nActual: {actual}\nMissing: {missing}",
                name="PS-6 Access Agreement Schema Gap",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not missing, f"PS-6 FAIL: response missing fields defined in access agreement: {missing}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PS -- Personnel Security")
@allure.story("PS-6 Access Agreements")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("PS-6: Access agreement prohibits exposure of other users data")
@allure.description("Access agreements restrict data scope -- a user-scoped request must not return other users data.")
@pytest.mark.compliance
@pytest.mark.nist_ps6
def test_ps6_access_agreement_prohibits_cross_user_data_exposure(api_base_url: str) -> None:
    target_user_id = 1

    with allure.step("Request posts scoped to a single user"):
        response = requests.get(
            f"{api_base_url}/posts",
            params={"userId": target_user_id},
            timeout=10,
        )
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert response.status_code == 200, f"PS-6 FAIL: scoped request must return 200, got {response.status_code}"
        assert elapsed_ms < 2000, f"PS-6 FAIL: scoped response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert response contains only the agreed user scope"):
        records = response.json()
        violations = [r for r in records if r.get("userId") != target_user_id]
        if violations:
            allure.attach(
                f"Out-of-scope records:\n{violations[:3]}",
                name="PS-6 Cross-User Data Exposure",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not violations, f"PS-6 FAIL: {len(violations)} record(s) returned outside the agreed user scope"
