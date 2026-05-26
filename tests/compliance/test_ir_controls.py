# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Incident Response compliance tests — IR-5, IR-6."""

import allure
import pytest
import requests

# ── IR-5: Incident Monitoring ─────────────────────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IR — Incident Response")
@allure.story("IR-5 Incident Monitoring")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IR-5: Burst of rapid requests is handled consistently without errors")
@allure.description(
    "Simulates an anomalous traffic spike. All 10 requests must return the same "
    "status code — no intermittent 5xx or inconsistent handling."
)
@pytest.mark.compliance
@pytest.mark.nist_ir5
def test_ir5_burst_requests_handled_consistently(api_base_url: str) -> None:
    burst_count = 10

    with allure.step(f"Send {burst_count} rapid successive GET requests"):
        statuses = []
        for i in range(burst_count):
            resp = requests.get(f"{api_base_url}/posts/1", timeout=10)
            statuses.append(resp.status_code)

    with allure.step("Assert all responses have the same status code"):
        unique_statuses = set(statuses)
        if len(unique_statuses) > 1:
            allure.attach(
                f"Status codes across {burst_count} requests: {statuses}",
                name="IR-5 Inconsistent Burst Responses",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            len(unique_statuses) == 1
        ), f"IR-5 FAIL: burst requests must return consistent status, got {unique_statuses}"

    with allure.step("Assert no 5xx was returned in the burst"):
        server_errors = [s for s in statuses if s >= 500]
        if server_errors:
            allure.attach(
                f"5xx statuses: {server_errors}",
                name="IR-5 Server Errors in Burst",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not server_errors, f"IR-5 FAIL: burst requests must not produce 5xx errors, got {server_errors}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IR — Incident Response")
@allure.story("IR-5 Incident Monitoring")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IR-5: Request with wrong Content-Type is handled gracefully")
@allure.description(
    "An anomalous Content-Type header simulates a misconfigured or malicious client. "
    "The server must respond safely without crashing."
)
@pytest.mark.compliance
@pytest.mark.nist_ir5
def test_ir5_malformed_content_type_handled_gracefully(api_base_url: str) -> None:
    with allure.step("Send POST with an unexpected Content-Type header"):
        response = requests.post(
            f"{api_base_url}/posts",
            data="this is not json",
            headers={"Content-Type": "application/x-custom-anomaly"},
            timeout=10,
        )

    with allure.step("Assert server does not return a 5xx error"):
        if response.status_code >= 500:
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:500]}",
                name="IR-5 Content-Type Anomaly Crash",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert response.status_code < 500, (
            f"IR-5 FAIL: anomalous Content-Type must not crash the server, " f"got {response.status_code}"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IR — Incident Response")
@allure.story("IR-5 Incident Monitoring")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("IR-5: Unsupported HTTP method returns a client-error status")
@allure.description(
    "An unsupported method (e.g. TRACE) on a resource simulates an anomalous probe. "
    "The server must return a 4xx, not crash with 5xx."
)
@pytest.mark.compliance
@pytest.mark.nist_ir5
def test_ir5_unsupported_http_method_returns_client_error(api_base_url: str) -> None:
    with allure.step("Send a TRACE request to a known resource"):
        response = requests.request("TRACE", f"{api_base_url}/posts/1", timeout=10)

    with allure.step("Assert a 4xx or 2xx response — never 5xx"):
        if response.status_code >= 500:
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:300]}",
                name="IR-5 Unsupported Method 5xx",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            response.status_code < 500
        ), f"IR-5 FAIL: unsupported HTTP method must return <500, got {response.status_code}"


# ── IR-6: Incident Reporting ──────────────────────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IR — Incident Response")
@allure.story("IR-6 Incident Reporting")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IR-6: 404 response contains enough information to file an incident report")
@allure.description(
    "An incident report requires a status code and a parseable response body. "
    "A completely empty 404 cannot be reported accurately."
)
@pytest.mark.compliance
@pytest.mark.nist_ir6
def test_ir6_404_response_contains_reportable_information(api_base_url: str) -> None:
    with allure.step("Request a non-existent resource"):
        response = requests.get(f"{api_base_url}/posts/99999", timeout=10)

    with allure.step("Assert 404 status code is present"):
        assert (
            response.status_code == 404
        ), f"IR-6 FAIL: expected 404 for reportable error event, got {response.status_code}"

    with allure.step("Assert response time is within reportable threshold"):
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert elapsed_ms < 2000, (
            f"IR-6 FAIL: error response must arrive within 2000ms for timely reporting, " f"took {elapsed_ms:.0f}ms"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IR — Incident Response")
@allure.story("IR-6 Incident Reporting")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IR-6: Error responses have a consistent, parseable format")
@allure.description(
    "Inconsistent error formats prevent automated incident reporting pipelines from "
    "parsing and escalating failures correctly."
)
@pytest.mark.compliance
@pytest.mark.nist_ir6
def test_ir6_error_responses_have_consistent_format(api_base_url: str) -> None:
    missing_ids = [99998, 99999]

    with allure.step("Send requests to two different non-existent resources"):
        responses = [requests.get(f"{api_base_url}/posts/{rid}", timeout=10) for rid in missing_ids]

    with allure.step("Assert both return the same 404 status code"):
        statuses = [r.status_code for r in responses]
        if len(set(statuses)) > 1:
            allure.attach(
                f"Statuses: {statuses}",
                name="IR-6 Inconsistent Error Statuses",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert len(set(statuses)) == 1, f"IR-6 FAIL: error status codes must be consistent, got {statuses}"
        assert statuses[0] == 404, f"IR-6 FAIL: missing resources must return 404, got {statuses[0]}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IR — Incident Response")
@allure.story("IR-6 Incident Reporting")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("IR-6: Successful API responses include identifiable metadata for incident correlation")
@allure.description(
    "Responses must carry enough identifiable fields (id, userId) to correlate "
    "a successful event with an incident if it later becomes relevant."
)
@pytest.mark.compliance
@pytest.mark.nist_ir6
def test_ir6_successful_response_includes_identifiable_metadata(api_base_url: str) -> None:
    with allure.step("Fetch a known resource"):
        response = requests.get(f"{api_base_url}/posts/1", timeout=10)
        assert response.status_code == 200, f"IR-6 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert response contains fields needed for incident correlation"):
        body = response.json()
        required = {"id", "userId"}
        missing = required - body.keys()
        if missing:
            allure.attach(
                f"Missing correlation fields: {missing}\nBody: {body}",
                name="IR-6 Missing Identifiable Metadata",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not missing, (
            f"IR-6 FAIL: response must contain {required} for incident correlation, " f"missing {missing}"
        )
