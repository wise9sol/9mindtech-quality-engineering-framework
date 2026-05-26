# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 System and Information Integrity tests — SI-2, SI-10, SI-12."""

import re

import allure
import pytest
import requests


# ── SI-2: Flaw Remediation ─────────────────────────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SI — System and Information Integrity")
@allure.story("SI-2 Flaw Remediation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SI-2: Server header does not expose version information")
@allure.description("Server version disclosure enables targeted exploitation of known CVEs.")
@pytest.mark.compliance
@pytest.mark.nist_si2
def test_si2_server_header_does_not_expose_version(api_base_url: str) -> None:
    with allure.step("Send GET request and inspect response headers"):
        response = requests.get(f"{api_base_url}/posts/1", timeout=10)
        assert response.status_code == 200, f"SI-2 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert Server header does not contain a version string"):
        server = response.headers.get("Server", "")
        version_pattern = re.compile(r"\d+\.\d+")
        if version_pattern.search(server):
            allure.attach(
                f"Server header: {server}",
                name="SI-2 Version Disclosure",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not version_pattern.search(
            server
        ), f"SI-2 FAIL: Server header must not disclose a version, found '{server}'"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SI — System and Information Integrity")
@allure.story("SI-2 Flaw Remediation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SI-2: 404 response does not leak stack traces or file paths")
@allure.description("Error responses must not expose implementation details exploitable by attackers.")
@pytest.mark.compliance
@pytest.mark.nist_si2
def test_si2_404_does_not_leak_stack_traces(api_base_url: str) -> None:
    with allure.step("Request a non-existent endpoint"):
        response = requests.get(f"{api_base_url}/posts/99999", timeout=10)
        assert response.status_code == 404, f"SI-2 FAIL: expected 404, got {response.status_code}"

    with allure.step("Assert response body contains no stack trace indicators"):
        body = response.text.lower()
        indicators = ("traceback", "stack trace", "exception", "at line", "syntaxerror")
        for indicator in indicators:
            if indicator in body:
                allure.attach(
                    f"Indicator '{indicator}' found:\n{response.text[:500]}",
                    name="SI-2 Stack Trace Leak",
                    attachment_type=allure.attachment_type.TEXT,
                )
            assert indicator not in body, f"SI-2 FAIL: 404 response must not contain '{indicator}'"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SI — System and Information Integrity")
@allure.story("SI-2 Flaw Remediation")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SI-2: Response includes a Content-Type header")
@allure.description("Missing Content-Type enables MIME-sniffing attacks indicating unpatched behaviour.")
@pytest.mark.compliance
@pytest.mark.nist_si2
def test_si2_response_includes_content_type_header(api_base_url: str) -> None:
    with allure.step("Send GET request"):
        response = requests.get(f"{api_base_url}/posts/1", timeout=10)
        assert response.status_code == 200, f"SI-2 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert Content-Type header is present and specifies JSON"):
        content_type = response.headers.get("Content-Type", "")
        if not content_type:
            allure.attach(
                f"Headers: {dict(response.headers)}",
                name="SI-2 Missing Content-Type",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert content_type, "SI-2 FAIL: Content-Type header must be present"
        assert (
            "application/json" in content_type
        ), f"SI-2 FAIL: Content-Type must specify application/json, got '{content_type}'"


# ── SI-10: Information Input Validation ───────────────────────────────────────


@pytest.mark.parametrize(
    "label,payload",
    [
        (
            "sql_injection",
            {"title": "'; DROP TABLE posts; --", "body": "sql injection attempt", "userId": 1},
        ),
        (
            "xss_script_tag",
            {"title": "<script>alert('xss')</script>", "body": "xss attempt", "userId": 1},
        ),
        (
            "oversized_title",
            {"title": "A" * 10000, "body": "overflow attempt", "userId": 1},
        ),
        (
            "null_title",
            {"title": None, "body": "null field attempt", "userId": 1},
        ),
        (
            "empty_title",
            {"title": "", "body": "empty field attempt", "userId": 1},
        ),
    ],
)
@allure.epic("NIST 800-53 Compliance")
@allure.feature("SI — System and Information Integrity")
@allure.story("SI-10 Information Input Validation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SI-10: API handles malicious input without crashing or leaking internals")
@allure.description(
    "Every form of malicious or malformed input must be handled safely — "
    "no 5xx errors and no stack trace disclosure."
)
@pytest.mark.compliance
@pytest.mark.nist_si10
def test_si10_api_handles_malicious_input_safely(label: str, payload: dict, api_base_url: str) -> None:
    with allure.step(f"Submit POST with malicious payload: {label}"):
        allure.attach(
            str(payload),
            name=f"SI-10 Payload ({label})",
            attachment_type=allure.attachment_type.TEXT,
        )
        response = requests.post(f"{api_base_url}/posts", json=payload, timeout=10)

    with allure.step("Assert server does not return a 5xx error"):
        if response.status_code >= 500:
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:500]}",
                name=f"SI-10 Server Error ({label})",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert response.status_code < 500, (
            f"SI-10 FAIL: malicious input '{label}' must not cause a 5xx error, " f"got {response.status_code}"
        )

    with allure.step("Assert response body does not contain a stack trace"):
        body_lower = response.text.lower()
        for indicator in ("traceback", "exception", "stack trace"):
            assert indicator not in body_lower, f"SI-10 FAIL: response for '{label}' must not leak '{indicator}'"


# ── SI-12: Information Management and Retention ───────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SI — System and Information Integrity")
@allure.story("SI-12 Information Management and Retention")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SI-12: DELETE returns an appropriate status confirming removal")
@allure.description("A deletion must return a 2xx status confirming the retention policy was applied.")
@pytest.mark.compliance
@pytest.mark.nist_si12
def test_si12_delete_returns_appropriate_status(api_base_url: str) -> None:
    with allure.step("Send DELETE for record id=1"):
        response = requests.delete(f"{api_base_url}/posts/1", timeout=10)

    with allure.step("Assert 2xx status confirming deletion was processed"):
        if not (200 <= response.status_code < 300):
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:200]}",
                name="SI-12 DELETE Status",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert 200 <= response.status_code < 300, (
            f"SI-12 FAIL: delete must return 2xx to confirm retention action, " f"got {response.status_code}"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SI — System and Information Integrity")
@allure.story("SI-12 Information Management and Retention")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SI-12: Record response does not include unexpected sensitive retention fields")
@allure.description("Responses must not expose internal retention metadata such as raw timestamps or checksums.")
@pytest.mark.compliance
@pytest.mark.nist_si12
def test_si12_response_does_not_include_unexpected_sensitive_fields(api_base_url: str) -> None:
    with allure.step("Fetch a single record"):
        response = requests.get(f"{api_base_url}/posts/1", timeout=10)
        assert response.status_code == 200, f"SI-12 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert no unexpected internal fields are present"):
        body = response.json()
        forbidden = {"__v", "_class", "deleted_at", "checksum", "internal_id"}
        exposed = forbidden & body.keys()
        if exposed:
            allure.attach(
                f"Exposed fields: {exposed}\nRecord: {body}",
                name="SI-12 Unexpected Fields",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not exposed, f"SI-12 FAIL: response must not expose internal fields, found {exposed}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SI — System and Information Integrity")
@allure.story("SI-12 Information Management and Retention")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SI-12: Record list is bounded to prevent excessive data retention exposure")
@allure.description("An unbounded list response violates information retention scoping requirements.")
@pytest.mark.compliance
@pytest.mark.nist_si12
def test_si12_record_list_is_bounded(api_base_url: str) -> None:
    with allure.step("Fetch the full post list"):
        response = requests.get(f"{api_base_url}/posts", timeout=10)
        assert response.status_code == 200, f"SI-12 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert the list contains a finite, positive number of records"):
        records = response.json()
        assert len(records) > 0, "SI-12 FAIL: record list must not be empty"
        assert len(records) <= 10000, f"SI-12 FAIL: record list must be bounded, returned {len(records)} records"
