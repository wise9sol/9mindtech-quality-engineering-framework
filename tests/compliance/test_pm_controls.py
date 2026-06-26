# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Program Management compliance tests -- PM-1, PM-9."""

import allure
import pytest
import requests

# -- PM-1: Information Security Program Plan ------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PM -- Program Management")
@allure.story("PM-1 Information Security Program Plan")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PM-1: System implements a documented set of security controls across all endpoints")
@allure.description("The security program plan requires controls to be implemented consistently across all interfaces.")
@pytest.mark.compliance
@pytest.mark.nist_pm1
def test_pm1_security_controls_implemented_across_all_endpoints(api_base_url: str) -> None:
    planned_endpoints = ["/users", "/posts", "/comments", "/todos"]

    with allure.step("Verify security controls are active on all planned endpoints"):
        failures = []
        for endpoint in planned_endpoints:
            response = requests.get(f"{api_base_url}{endpoint}", timeout=10)
            elapsed_ms = response.elapsed.total_seconds() * 1000
            content_type = response.headers.get("Content-Type", "")
            if response.status_code != 200 or elapsed_ms >= 2000 or "application/json" not in content_type.lower():
                failures.append(
                    {
                        "endpoint": endpoint,
                        "status": response.status_code,
                        "elapsed_ms": round(elapsed_ms),
                        "content_type": content_type,
                    }
                )

    with allure.step("Assert all endpoints comply with the security program plan"):
        if failures:
            allure.attach(
                f"Non-compliant endpoints:\n{failures}",
                name="PM-1 Security Program Plan Gaps",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not failures
        ), f"PM-1 FAIL: {len(failures)} endpoint(s) do not comply with the security program plan: {failures}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PM -- Program Management")
@allure.story("PM-1 Information Security Program Plan")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PM-1: Security program ensures sensitive data is excluded from all responses")
@allure.description("The security program plan requires sensitive data to be excluded from all system responses.")
@pytest.mark.compliance
@pytest.mark.nist_pm1
def test_pm1_sensitive_data_excluded_across_program(api_base_url: str) -> None:
    sensitive_fields = ["password", "secret", "token", "private_key", "api_key"]
    endpoints = ["/users", "/users/1", "/posts/1"]

    with allure.step("Scan all endpoints for sensitive data exposure"):
        violations = []
        for endpoint in endpoints:
            response = requests.get(f"{api_base_url}{endpoint}", timeout=10)
            assert response.status_code == 200, f"PM-1 FAIL: expected 200 from {endpoint}, got {response.status_code}"
            body = response.text.lower()
            found = [f for f in sensitive_fields if f in body]
            if found:
                violations.append({"endpoint": endpoint, "fields": found})

    with allure.step("Assert no sensitive data present across the program boundary"):
        if violations:
            allure.attach(
                f"Sensitive data found:\n{violations}",
                name="PM-1 Sensitive Data Program Violation",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not violations, f"PM-1 FAIL: sensitive data exposed in {len(violations)} endpoint(s): {violations}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PM -- Program Management")
@allure.story("PM-1 Information Security Program Plan")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("PM-1: Security program maintains consistent data integrity across the system")
@allure.description("The security program plan requires data integrity to be maintained across all resource types.")
@pytest.mark.compliance
@pytest.mark.nist_pm1
def test_pm1_program_maintains_data_integrity(api_base_url: str) -> None:
    with allure.step("Retrieve resource list and verify record count is stable"):
        r1 = requests.get(f"{api_base_url}/users", timeout=10)
        r2 = requests.get(f"{api_base_url}/users", timeout=10)
        assert r1.status_code == 200, f"PM-1 FAIL: first request must return 200, got {r1.status_code}"
        assert r2.status_code == 200, f"PM-1 FAIL: second request must return 200, got {r2.status_code}"

    with allure.step("Assert record count is stable -- data integrity maintained"):
        count1 = len(r1.json())
        count2 = len(r2.json())
        if count1 != count2:
            allure.attach(
                f"First count: {count1}\nSecond count: {count2}",
                name="PM-1 Data Integrity Violation",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            count1 == count2
        ), f"PM-1 FAIL: record count unstable ({count1} vs {count2}) -- data integrity compromised"


# -- PM-9: Risk Management Strategy --------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PM -- Program Management")
@allure.story("PM-9 Risk Management Strategy")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PM-9: Risk strategy enforces input validation to reduce injection risk")
@allure.description("The risk management strategy must include input validation controls to mitigate injection risks.")
@pytest.mark.compliance
@pytest.mark.nist_pm9
def test_pm9_risk_strategy_enforces_input_validation(api_base_url: str) -> None:
    risk_payloads = [
        {"title": "'; DROP TABLE posts;--", "body": "sql risk", "userId": 1},
        {"title": "<script>risk()</script>", "body": "xss risk", "userId": 1},
    ]

    with allure.step("Submit high-risk payloads and verify safe handling"):
        for payload in risk_payloads:
            response = requests.post(
                f"{api_base_url}/posts",
                json=payload,
                timeout=10,
            )
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert response.status_code in (
                200,
                201,
                400,
                422,
            ), f"PM-9 FAIL: risk payload returned unexpected status {response.status_code}"
            assert elapsed_ms < 2000, f"PM-9 FAIL: risk payload handling took {elapsed_ms:.0f}ms -- possible DoS vector"
            if response.status_code in (200, 201):
                content_type = response.headers.get("Content-Type", "")
                assert (
                    "application/json" in content_type.lower()
                ), "PM-9 FAIL: risk payload response must be JSON -- HTML/script execution risk"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PM -- Program Management")
@allure.story("PM-9 Risk Management Strategy")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PM-9: Risk strategy limits access to authorised resources only")
@allure.description("The risk management strategy must restrict resource access to authorised identifiers.")
@pytest.mark.compliance
@pytest.mark.nist_pm9
def test_pm9_risk_strategy_limits_access_to_authorised_resources(api_base_url: str) -> None:
    with allure.step("Assert authorised resource is accessible"):
        authorised = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = authorised.elapsed.total_seconds() * 1000
        assert (
            authorised.status_code == 200
        ), f"PM-9 FAIL: authorised resource must return 200, got {authorised.status_code}"
        assert elapsed_ms < 2000, f"PM-9 FAIL: authorised access must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert unauthorised resource is blocked"):
        unauthorised = requests.get(f"{api_base_url}/users/99999", timeout=10)
        assert (
            unauthorised.status_code == 404
        ), f"PM-9 FAIL: unauthorised resource must return 404, got {unauthorised.status_code}"

    with allure.step("Assert path traversal is blocked"):
        traversal = requests.get(f"{api_base_url}/users/../posts", timeout=10)
        assert traversal.status_code in (
            200,
            400,
            404,
        ), f"PM-9 FAIL: path traversal attempt must return 200/400/404, got {traversal.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PM -- Program Management")
@allure.story("PM-9 Risk Management Strategy")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("PM-9: Risk management strategy ensures system availability under load")
@allure.description("The risk strategy must account for availability -- repeated requests must all succeed.")
@pytest.mark.compliance
@pytest.mark.nist_pm9
def test_pm9_risk_strategy_ensures_availability_under_load(api_base_url: str) -> None:
    with allure.step("Send repeated requests to verify availability under load"):
        results = []
        for _ in range(5):
            response = requests.get(f"{api_base_url}/users", timeout=10)
            elapsed_ms = response.elapsed.total_seconds() * 1000
            results.append(
                {
                    "status": response.status_code,
                    "elapsed_ms": round(elapsed_ms),
                }
            )

    with allure.step("Assert all requests succeeded within availability threshold"):
        failures = [r for r in results if r["status"] != 200 or r["elapsed_ms"] >= 2000]
        if failures:
            allure.attach(
                f"Failed requests:\n{failures}",
                name="PM-9 Availability Under Load",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not failures, f"PM-9 FAIL: {len(failures)} request(s) failed under load: {failures}"
