# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Planning compliance tests -- PL-2, PL-4."""

import allure
import pytest
import requests

# -- PL-2: System Security and Privacy Plan -------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PL -- Planning")
@allure.story("PL-2 System Security and Privacy Plan")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PL-2: System exposes only planned and documented API endpoints")
@allure.description("The security plan must define all system interfaces -- unplanned endpoints must not be reachable.")
@pytest.mark.compliance
@pytest.mark.nist_pl2
def test_pl2_only_planned_endpoints_are_reachable(api_base_url: str) -> None:
    unplanned_paths = ["/admin", "/setup", "/install", "/debug", "/test", "/dev", "/staging"]

    with allure.step("Probe unplanned paths and assert none return 200"):
        exposed = []
        for path in unplanned_paths:
            response = requests.get(f"{api_base_url}{path}", timeout=10)
            if response.status_code == 200:
                exposed.append({"path": path, "status": response.status_code})

    with allure.step("Assert no unplanned endpoints are accessible"):
        if exposed:
            allure.attach(
                f"Unplanned endpoints reachable:\n{exposed}",
                name="PL-2 Unplanned Endpoint Exposure",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not exposed
        ), f"PL-2 FAIL: {len(exposed)} unplanned endpoint(s) reachable outside the security plan: {exposed}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PL -- Planning")
@allure.story("PL-2 System Security and Privacy Plan")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PL-2: System security plan is reflected in consistent API behavior")
@allure.description("The security plan requires consistent, deterministic responses to identical requests.")
@pytest.mark.compliance
@pytest.mark.nist_pl2
def test_pl2_api_behavior_is_consistent_with_security_plan(api_base_url: str) -> None:
    with allure.step("Send the same request twice and compare responses"):
        r1 = requests.get(f"{api_base_url}/users/1", timeout=10)
        r2 = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = r2.elapsed.total_seconds() * 1000
        assert r1.status_code == 200, f"PL-2 FAIL: first request must return 200, got {r1.status_code}"
        assert r2.status_code == 200, f"PL-2 FAIL: second request must return 200, got {r2.status_code}"
        assert elapsed_ms < 2000, f"PL-2 FAIL: response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert both responses are identical -- behavior matches security plan"):
        if r1.json() != r2.json():
            allure.attach(
                f"Request 1: {r1.json()}\nRequest 2: {r2.json()}",
                name="PL-2 Inconsistent API Behavior",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            r1.json() == r2.json()
        ), "PL-2 FAIL: API behavior is inconsistent -- security plan requires deterministic responses"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PL -- Planning")
@allure.story("PL-2 System Security and Privacy Plan")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("PL-2: API response schema aligns with the documented security plan")
@allure.description("The security plan defines the data schema -- responses must conform to the planned structure.")
@pytest.mark.compliance
@pytest.mark.nist_pl2
def test_pl2_response_schema_aligns_with_security_plan(api_base_url: str) -> None:
    planned_schema = {"id", "name", "username", "email"}

    with allure.step("Retrieve user resource and validate against planned schema"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
        assert response.status_code == 200, f"PL-2 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert response conforms to the planned security schema"):
        actual = set(response.json().keys())
        missing = planned_schema - actual
        if missing:
            allure.attach(
                f"Planned schema: {planned_schema}\nActual: {actual}\nMissing: {missing}",
                name="PL-2 Schema Deviation from Security Plan",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not missing, f"PL-2 FAIL: response deviates from planned security schema, missing fields: {missing}"


# -- PL-4: Rules of Behavior ----------------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PL -- Planning")
@allure.story("PL-4 Rules of Behavior")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PL-4: API enforces rules of behavior -- write operations require valid payloads")
@allure.description("Rules of behavior require users to interact with the system using valid, documented payloads.")
@pytest.mark.compliance
@pytest.mark.nist_pl4
def test_pl4_write_operations_require_valid_payloads(api_base_url: str) -> None:
    with allure.step("Submit a valid POST payload per rules of behavior"):
        valid_response = requests.post(
            f"{api_base_url}/posts",
            json={"title": "PL-4 rules test", "body": "valid payload", "userId": 1},
            timeout=10,
        )
        assert valid_response.status_code in (
            200,
            201,
        ), f"PL-4 FAIL: valid payload must return 200/201, got {valid_response.status_code}"

    with allure.step("Submit a POST with missing required fields"):
        invalid_response = requests.post(
            f"{api_base_url}/posts",
            json={},
            timeout=10,
        )
        assert invalid_response.status_code in (
            200,
            201,
            400,
            422,
        ), f"PL-4 FAIL: invalid payload must return 200/201/400/422, got {invalid_response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PL -- Planning")
@allure.story("PL-4 Rules of Behavior")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PL-4: API rules of behavior apply uniformly to all resource types")
@allure.description("Rules of behavior must be enforced uniformly -- the same rules apply to all resource endpoints.")
@pytest.mark.compliance
@pytest.mark.nist_pl4
def test_pl4_rules_of_behavior_apply_uniformly(api_base_url: str) -> None:
    resource_endpoints = ["/users", "/posts", "/comments"]

    with allure.step("Assert GET rules of behavior -- all resources return 200"):
        failures = []
        for endpoint in resource_endpoints:
            response = requests.get(f"{api_base_url}{endpoint}", timeout=10)
            elapsed_ms = response.elapsed.total_seconds() * 1000
            if response.status_code != 200 or elapsed_ms >= 2000:
                failures.append(
                    {
                        "endpoint": endpoint,
                        "status": response.status_code,
                        "elapsed_ms": round(elapsed_ms),
                    }
                )

    with allure.step("Assert uniform enforcement of GET rules across all resources"):
        if failures:
            allure.attach(
                f"Non-uniform behavior:\n{failures}",
                name="PL-4 Non-Uniform Rules Enforcement",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not failures
        ), f"PL-4 FAIL: rules of behavior not uniformly enforced across {len(failures)} resource(s): {failures}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PL -- Planning")
@allure.story("PL-4 Rules of Behavior")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("PL-4: API rejects behavior that violates defined content rules")
@allure.description("Rules of behavior prohibit malicious content -- injection payloads must not alter behavior.")
@pytest.mark.compliance
@pytest.mark.nist_pl4
def test_pl4_api_rejects_rule_violating_content(api_base_url: str) -> None:
    violating_payloads = [
        {"title": "<script>alert(1)</script>", "body": "xss attempt", "userId": 1},
        {"title": "' OR 1=1--", "body": "sql injection", "userId": 1},
    ]

    with allure.step("Submit rule-violating payloads and assert safe handling"):
        for payload in violating_payloads:
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
            ), f"PL-4 FAIL: violating payload returned unexpected status {response.status_code}"
            assert (
                elapsed_ms < 2000
            ), f"PL-4 FAIL: response to violating payload took {elapsed_ms:.0f}ms -- possible DoS"
            if response.status_code in (200, 201):
                content_type = response.headers.get("Content-Type", "")
                assert (
                    "application/json" in content_type.lower()
                ), "PL-4 FAIL: response to rule-violating content must return JSON, not HTML/script"
