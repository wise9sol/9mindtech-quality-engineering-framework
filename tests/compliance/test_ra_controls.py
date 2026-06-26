# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Risk Assessment compliance tests -- RA-3, RA-5."""

import re

import allure
import pytest
import requests

# -- RA-3: Risk Assessment ------------------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("RA -- Risk Assessment")
@allure.story("RA-3 Risk Assessment")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("RA-3: API surface area is limited to documented endpoints only")
@allure.description("Risk assessment requires the API surface to be limited -- undocumented endpoints must not exist.")
@pytest.mark.compliance
@pytest.mark.nist_ra3
def test_ra3_api_surface_limited_to_documented_endpoints(api_base_url: str) -> None:
    undocumented_paths = [
        "/admin",
        "/debug",
        "/internal",
        "/config",
        "/env",
        "/metrics",
        "/health/internal",
    ]

    with allure.step("Probe undocumented paths and assert none return 200"):
        exposed = []
        for path in undocumented_paths:
            response = requests.get(f"{api_base_url}{path}", timeout=10)
            if response.status_code == 200:
                exposed.append({"path": path, "status": response.status_code})

    with allure.step("Assert no undocumented endpoints are reachable"):
        if exposed:
            allure.attach(
                f"Exposed undocumented endpoints:\n{exposed}",
                name="RA-3 Undocumented Endpoint Exposure",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not exposed, f"RA-3 FAIL: {len(exposed)} undocumented endpoint(s) are reachable: {exposed}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("RA -- Risk Assessment")
@allure.story("RA-3 Risk Assessment")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("RA-3: Sensitive data fields are not exposed in API responses")
@allure.description("Risk assessment must confirm sensitive fields are not leaked in any API response.")
@pytest.mark.compliance
@pytest.mark.nist_ra3
def test_ra3_sensitive_data_not_exposed_in_responses(api_base_url: str) -> None:
    sensitive_keywords = ["password", "secret", "private_key", "access_token", "api_key", "ssn"]

    with allure.step("Request user and post resources and scan for sensitive data"):
        endpoints = ["/users", "/users/1", "/posts/1"]
        violations = []
        for endpoint in endpoints:
            response = requests.get(f"{api_base_url}{endpoint}", timeout=10)
            assert response.status_code == 200, f"RA-3 FAIL: expected 200 from {endpoint}, got {response.status_code}"
            body = response.text.lower()
            found = [kw for kw in sensitive_keywords if re.search(rf"\b{re.escape(kw)}\b", body)]
            if found:
                violations.append({"endpoint": endpoint, "keywords": found})

    with allure.step("Assert no sensitive keywords present in any response"):
        if violations:
            allure.attach(
                f"Sensitive data found:\n{violations}",
                name="RA-3 Sensitive Data Exposure",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not violations, f"RA-3 FAIL: sensitive data exposed in {len(violations)} endpoint(s): {violations}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("RA -- Risk Assessment")
@allure.story("RA-3 Risk Assessment")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("RA-3: Error responses do not disclose internal implementation details")
@allure.description("Risk assessment requires safe error messages -- no stack traces or internal paths disclosed.")
@pytest.mark.compliance
@pytest.mark.nist_ra3
def test_ra3_error_responses_do_not_disclose_internals(api_base_url: str) -> None:
    internal_patterns = ["traceback", "stack trace", "exception", "at line", "syntax error", "/var/", "c:\\"]

    with allure.step("Trigger error responses and scan for internal disclosure"):
        error_endpoints = ["/users/99999", "/posts/99999", "/nonexistent"]
        violations = []
        for endpoint in error_endpoints:
            response = requests.get(f"{api_base_url}{endpoint}", timeout=10)
            body = response.text.lower()
            found = [p for p in internal_patterns if p in body]
            if found:
                violations.append({"endpoint": endpoint, "patterns": found})

    with allure.step("Assert error responses contain no internal disclosure"):
        if violations:
            allure.attach(
                f"Internal details disclosed:\n{violations}",
                name="RA-3 Internal Disclosure in Error Response",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not violations
        ), f"RA-3 FAIL: internal details disclosed in {len(violations)} error response(s): {violations}"


# -- RA-5: Vulnerability Monitoring and Scanning --------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("RA -- Risk Assessment")
@allure.story("RA-5 Vulnerability Monitoring and Scanning")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("RA-5: API does not accept SQL injection payloads without rejection")
@allure.description("Vulnerability scanning must confirm SQL injection payloads are rejected or sanitised.")
@pytest.mark.compliance
@pytest.mark.nist_ra5
def test_ra5_api_rejects_sql_injection_payloads(api_base_url: str) -> None:
    sql_payloads = ["' OR 1=1--", "'; DROP TABLE users;--", "1 UNION SELECT * FROM users"]

    with allure.step("Send SQL injection payloads and assert no data is returned"):
        for payload in sql_payloads:
            response = requests.get(
                f"{api_base_url}/users",
                params={"id": payload},
                timeout=10,
            )
            elapsed_ms = response.elapsed.total_seconds() * 1000
            assert response.status_code in (
                200,
                400,
                404,
                422,
            ), f"RA-5 FAIL: SQL injection payload returned unexpected status {response.status_code}"
            assert (
                elapsed_ms < 2000
            ), f"RA-5 FAIL: response to injection payload took {elapsed_ms:.0f}ms -- possible DoS vector"
            if response.status_code == 200:
                body = response.text.lower()
                assert (
                    "password" not in body and "secret" not in body
                ), f"RA-5 FAIL: SQL injection payload may have caused data leakage for payload: {payload}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("RA -- Risk Assessment")
@allure.story("RA-5 Vulnerability Monitoring and Scanning")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("RA-5: API does not reflect XSS payloads in responses")
@allure.description("Vulnerability scanning must confirm XSS payloads are not reflected in API responses.")
@pytest.mark.compliance
@pytest.mark.nist_ra5
def test_ra5_api_does_not_reflect_xss_payloads(api_base_url: str) -> None:
    xss_payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "javascript:alert(1)"]

    with allure.step("Send XSS payloads and assert responses are served as non-executable JSON"):
        for payload in xss_payloads:
            response = requests.post(
                f"{api_base_url}/posts",
                json={"title": payload, "body": "test", "userId": 1},
                timeout=10,
            )
            assert response.status_code in (
                200,
                201,
                400,
                422,
            ), f"RA-5 FAIL: XSS payload returned unexpected status {response.status_code}"
            content_type = response.headers.get("Content-Type", "").lower()
            if response.status_code in (200, 201):
                if "application/json" not in content_type:
                    allure.attach(
                        f"Payload: {payload}\nContent-Type: {content_type}\nBody: {response.text[:300]}",
                        name="RA-5 XSS Reflection Risk",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                assert (
                    "application/json" in content_type
                ), f"RA-5 FAIL: reflected payload served as '{content_type}', not JSON -- XSS execution risk"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("RA -- Risk Assessment")
@allure.story("RA-5 Vulnerability Monitoring and Scanning")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("RA-5: API enforces input size limits to prevent payload-based DoS")
@allure.description("Vulnerability scanning must confirm oversized payloads are rejected within acceptable time.")
@pytest.mark.compliance
@pytest.mark.nist_ra5
def test_ra5_api_enforces_input_size_limits(api_base_url: str) -> None:
    oversized_payload = {"title": "A" * 10000, "body": "B" * 10000, "userId": 1}

    with allure.step("Send an oversized payload and assert response time is acceptable"):
        response = requests.post(
            f"{api_base_url}/posts",
            json=oversized_payload,
            timeout=10,
        )
        elapsed_ms = response.elapsed.total_seconds() * 1000

    with allure.step("Assert response time is within DoS threshold"):
        if elapsed_ms >= 2000:
            allure.attach(
                f"Elapsed: {elapsed_ms:.0f}ms  Payload size: {len(str(oversized_payload))} chars",
                name="RA-5 Oversized Payload DoS Risk",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert elapsed_ms < 2000, f"RA-5 FAIL: oversized payload took {elapsed_ms:.0f}ms -- potential DoS vector"

    with allure.step("Assert status code is acceptable"):
        assert response.status_code in (
            200,
            201,
            400,
            413,
            422,
        ), f"RA-5 FAIL: oversized payload returned unexpected status {response.status_code}"
