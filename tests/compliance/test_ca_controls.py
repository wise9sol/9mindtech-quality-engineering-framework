# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Assessment, Authorization, and Monitoring compliance tests -- CA-2, CA-7, CA-9."""

import allure
import pytest
import requests

# -- CA-2: Control Assessments --------------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CA -- Assessment, Authorization, and Monitoring")
@allure.story("CA-2 Control Assessments")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CA-2: API security controls respond within assessment thresholds")
@allure.description("Security controls must respond within 2000ms to be assessable under CA-2.")
@pytest.mark.compliance
@pytest.mark.nist_ca2
def test_ca2_security_controls_respond_within_threshold(api_base_url: str) -> None:
    with allure.step("Request the user endpoint to assess response control"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000

    with allure.step("Assert status code is assessable"):
        assert (
            response.status_code == 200
        ), f"CA-2 FAIL: security control assessment requires 200, got {response.status_code}"

    with allure.step("Assert response time is within assessment threshold"):
        if elapsed_ms >= 2000:
            allure.attach(
                f"Elapsed: {elapsed_ms:.0f}ms  Threshold: 2000ms",
                name="CA-2 Latency Breach",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            elapsed_ms < 2000
        ), f"CA-2 FAIL: security control must respond within 2000ms for assessment, took {elapsed_ms:.0f}ms"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CA -- Assessment, Authorization, and Monitoring")
@allure.story("CA-2 Control Assessments")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CA-2: Authentication control returns assessable status codes")
@allure.description("The authentication control must return a documented, assessable HTTP status code.")
@pytest.mark.compliance
@pytest.mark.nist_ca2
def test_ca2_authentication_control_returns_assessable_status(api_base_url: str) -> None:
    assessable_codes = {200, 201, 400, 401, 403, 404, 405, 422, 429, 500}

    with allure.step("Request a protected resource to assess auth control"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)

    with allure.step("Assert response code is in the documented assessable set"):
        if response.status_code not in assessable_codes:
            allure.attach(
                f"Status: {response.status_code}\nAssessable codes: {assessable_codes}",
                name="CA-2 Undocumented Status Code",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            response.status_code in assessable_codes
        ), f"CA-2 FAIL: control returned undocumented status {response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CA -- Assessment, Authorization, and Monitoring")
@allure.story("CA-2 Control Assessments")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("CA-2: Error responses include assessable diagnostic information")
@allure.description("Error responses must include a body to support control assessment and audit.")
@pytest.mark.compliance
@pytest.mark.nist_ca2
def test_ca2_error_responses_include_diagnostic_body(api_base_url: str) -> None:
    with allure.step("Request a non-existent resource to trigger an error response"):
        response = requests.get(f"{api_base_url}/users/99999", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000

    with allure.step("Assert 404 status"):
        assert response.status_code == 404, f"CA-2 FAIL: expected 404 for missing resource, got {response.status_code}"

    with allure.step("Assert response time within threshold"):
        assert elapsed_ms < 2000, f"CA-2 FAIL: error response must return within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert response body is present for assessment"):
        body = response.text.strip()
        if not body:
            allure.attach(
                "Error response body is empty -- cannot assess control failure details",
                name="CA-2 Empty Error Body",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert body, "CA-2 FAIL: error response must include a body for assessment"


# -- CA-7: Continuous Monitoring ------------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CA -- Assessment, Authorization, and Monitoring")
@allure.story("CA-7 Continuous Monitoring")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CA-7: API endpoints are continuously reachable within latency bounds")
@allure.description("Continuous monitoring requires endpoints to be reachable within defined latency thresholds.")
@pytest.mark.compliance
@pytest.mark.nist_ca7
def test_ca7_api_endpoints_are_continuously_reachable(api_base_url: str) -> None:
    endpoints = ["/users", "/posts", "/comments"]

    with allure.step("Probe each monitored endpoint"):
        failures = []
        for endpoint in endpoints:
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

    with allure.step("Assert all monitored endpoints passed"):
        if failures:
            allure.attach(
                f"Failed endpoints:\n{failures}",
                name="CA-7 Monitoring Failures",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not failures
        ), f"CA-7 FAIL: continuous monitoring detected {len(failures)} endpoint failure(s): {failures}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CA -- Assessment, Authorization, and Monitoring")
@allure.story("CA-7 Continuous Monitoring")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CA-7: Security-relevant headers are present on every monitored response")
@allure.description("Continuous monitoring must verify security headers are consistently present.")
@pytest.mark.compliance
@pytest.mark.nist_ca7
def test_ca7_security_headers_present_on_monitored_responses(api_base_url: str) -> None:
    with allure.step("Fetch a monitored response"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert response.status_code == 200, f"CA-7 FAIL: monitored endpoint must return 200, got {response.status_code}"
        assert elapsed_ms < 2000, f"CA-7 FAIL: monitored response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert Content-Type is present as a baseline security header"):
        content_type = response.headers.get("Content-Type", "")
        if not content_type:
            allure.attach(
                f"Headers: {dict(response.headers)}",
                name="CA-7 Missing Content-Type",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert content_type, "CA-7 FAIL: Content-Type header must be present on monitored responses"

    with allure.step("Assert response body is parseable JSON"):
        try:
            response.json()
        except ValueError as exc:
            allure.attach(
                f"Body: {response.text[:500]}",
                name="CA-7 Non-JSON Response",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(f"CA-7 FAIL: monitored response must return parseable JSON -- {exc}")


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CA -- Assessment, Authorization, and Monitoring")
@allure.story("CA-7 Continuous Monitoring")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("CA-7: Monitoring detects response schema drift over repeated requests")
@allure.description("Repeated requests must return a consistent schema; drift signals a control change.")
@pytest.mark.compliance
@pytest.mark.nist_ca7
def test_ca7_schema_consistent_across_monitoring_samples(api_base_url: str) -> None:
    with allure.step("Collect two monitoring samples from the same endpoint"):
        r1 = requests.get(f"{api_base_url}/users/1", timeout=10)
        r2 = requests.get(f"{api_base_url}/users/1", timeout=10)
        assert r1.status_code == 200, f"CA-7 FAIL: sample 1 must return 200, got {r1.status_code}"
        assert r2.status_code == 200, f"CA-7 FAIL: sample 2 must return 200, got {r2.status_code}"

    with allure.step("Assert schemas match across both samples"):
        keys1 = set(r1.json().keys())
        keys2 = set(r2.json().keys())
        drift = keys1.symmetric_difference(keys2)
        if drift:
            allure.attach(
                f"Sample 1 keys: {keys1}\nSample 2 keys: {keys2}\nDrift: {drift}",
                name="CA-7 Schema Drift Detected",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not drift, f"CA-7 FAIL: schema drift detected between monitoring samples -- changed keys: {drift}"


# -- CA-9: Internal System Connections ------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CA -- Assessment, Authorization, and Monitoring")
@allure.story("CA-9 Internal System Connections")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CA-9: Internal API connections use HTTPS")
@allure.description("All internal system connections must use HTTPS to protect data in transit.")
@pytest.mark.compliance
@pytest.mark.nist_ca9
def test_ca9_internal_connections_use_https(api_base_url: str) -> None:
    with allure.step("Assert internal connection URL uses HTTPS"):
        if not api_base_url.startswith("https://"):
            allure.attach(
                f"api_base_url={api_base_url}",
                name="CA-9 Insecure Connection",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert api_base_url.startswith(
            "https://"
        ), f"CA-9 FAIL: internal system connections must use HTTPS, got '{api_base_url}'"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CA -- Assessment, Authorization, and Monitoring")
@allure.story("CA-9 Internal System Connections")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CA-9: Internal connection responds with approved status codes only")
@allure.description("Internal system connections must return only approved, documented status codes.")
@pytest.mark.compliance
@pytest.mark.nist_ca9
def test_ca9_internal_connection_returns_approved_status(api_base_url: str) -> None:
    approved_codes = {200, 201, 204, 400, 401, 403, 404, 422, 429}

    with allure.step("Establish internal connection to the primary resource endpoint"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000

    with allure.step("Assert response is within latency bounds"):
        assert elapsed_ms < 2000, f"CA-9 FAIL: internal connection must respond within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert status code is in the approved set"):
        if response.status_code not in approved_codes:
            allure.attach(
                f"Status: {response.status_code}\nApproved: {approved_codes}",
                name="CA-9 Unapproved Status Code",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            response.status_code in approved_codes
        ), f"CA-9 FAIL: internal connection returned unapproved status {response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CA -- Assessment, Authorization, and Monitoring")
@allure.story("CA-9 Internal System Connections")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("CA-9: Internal connections return consistent data across multiple requests")
@allure.description("Internal system connections must return stable, consistent data to support system integrity.")
@pytest.mark.compliance
@pytest.mark.nist_ca9
def test_ca9_internal_connection_data_is_consistent(api_base_url: str) -> None:
    with allure.step("Make two sequential internal connection requests"):
        r1 = requests.get(f"{api_base_url}/users/1", timeout=10)
        r2 = requests.get(f"{api_base_url}/users/1", timeout=10)
        assert r1.status_code == 200, f"CA-9 FAIL: connection 1 must return 200, got {r1.status_code}"
        assert r2.status_code == 200, f"CA-9 FAIL: connection 2 must return 200, got {r2.status_code}"

    with allure.step("Assert both connections returned identical data"):
        data1 = r1.json()
        data2 = r2.json()
        if data1 != data2:
            allure.attach(
                f"Connection 1: {data1}\nConnection 2: {data2}",
                name="CA-9 Data Inconsistency",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert data1 == data2, "CA-9 FAIL: internal connections must return consistent data -- mismatch detected"
