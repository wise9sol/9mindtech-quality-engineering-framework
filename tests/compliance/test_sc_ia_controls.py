# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 System Protection and Identification compliance tests — SC-8, SC-28, IA-2, IA-5."""

import os
import re

import allure
import pytest
import requests


# ── SC-8: Transmission Confidentiality and Integrity ──────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SC — System and Communications Protection")
@allure.story("SC-8 Transmission Confidentiality and Integrity")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("SC-8: API_BASE_URL uses HTTPS to enforce encrypted transmission")
@allure.description("Unencrypted transmission violates SC-8. All URLs must use the https scheme.")
@pytest.mark.compliance
@pytest.mark.nist_sc8
def test_sc8_api_base_url_uses_https() -> None:
    with allure.step("Read API_BASE_URL from environment"):
        url = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

    with allure.step("Assert URL scheme is https"):
        if not url.startswith("https://"):
            allure.attach(
                f"API_BASE_URL={url}",
                name="SC-8 Insecure Transmission URL",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert url.startswith(
            "https://"
        ), f"SC-8 FAIL: API_BASE_URL must use HTTPS to protect transmission, got '{url}'"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SC — System and Communications Protection")
@allure.story("SC-8 Transmission Confidentiality and Integrity")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("SC-8: TLS handshake succeeds with strict certificate verification")
@allure.description("A successful TLS handshake with verify=True confirms valid certificate chain.")
@pytest.mark.compliance
@pytest.mark.nist_sc8
def test_sc8_tls_handshake_succeeds_with_strict_verification(api_base_url: str) -> None:
    with allure.step("Send HTTPS request with TLS certificate verification enabled"):
        try:
            response = requests.get(f"{api_base_url}/posts/1", verify=True, timeout=10)
        except requests.exceptions.SSLError as exc:
            allure.attach(
                str(exc),
                name="SC-8 TLS Handshake Failure",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.fail(f"SC-8 FAIL: TLS handshake failed with strict verification — {exc}")

    with allure.step("Assert 200 response over verified TLS"):
        assert response.status_code == 200, f"SC-8 FAIL: HTTPS request must return 200, got {response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SC — System and Communications Protection")
@allure.story("SC-8 Transmission Confidentiality and Integrity")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SC-8: Response is served over HTTPS as confirmed by the effective URL")
@allure.description("The final URL after any redirects must still use the https scheme.")
@pytest.mark.compliance
@pytest.mark.nist_sc8
def test_sc8_effective_url_remains_https_after_any_redirects(api_base_url: str) -> None:
    with allure.step("Send request and capture effective URL"):
        response = requests.get(f"{api_base_url}/posts/1", timeout=10)
        effective_url = response.url

    with allure.step("Assert the effective URL after redirects is still HTTPS"):
        if not effective_url.startswith("https://"):
            allure.attach(
                f"Effective URL: {effective_url}",
                name="SC-8 Redirect to HTTP",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert effective_url.startswith(
            "https://"
        ), f"SC-8 FAIL: effective URL must use HTTPS after redirects, got '{effective_url}'"


# ── SC-28: Protection of Information at Rest ──────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SC — System and Communications Protection")
@allure.story("SC-28 Protection of Information at Rest")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SC-28: Response body does not contain plaintext credential patterns")
@allure.description("Plaintext passwords in API responses indicate data-at-rest protection failure.")
@pytest.mark.compliance
@pytest.mark.nist_sc28
def test_sc28_response_does_not_contain_plaintext_credentials(api_base_url: str) -> None:
    credential_pattern = re.compile(r'(password|passwd|pwd)\s*[=:]\s*["\']?[^\s"\']{4,}', re.IGNORECASE)

    with allure.step("Fetch user list and scan for plaintext credential patterns"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"SC-28 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert no plaintext credential pattern is present in the response"):
        matches = credential_pattern.findall(response.text)
        if matches:
            allure.attach(
                f"Matches found: {matches}\nBody excerpt: {response.text[:500]}",
                name="SC-28 Plaintext Credentials",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not matches, f"SC-28 FAIL: response must not contain plaintext credentials, found: {matches}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SC — System and Communications Protection")
@allure.story("SC-28 Protection of Information at Rest")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SC-28: Response body does not contain credit card number patterns")
@allure.description("PCI-DSS and SC-28 both prohibit unmasked credit card numbers in API responses.")
@pytest.mark.compliance
@pytest.mark.nist_sc28
def test_sc28_response_does_not_contain_credit_card_patterns(api_base_url: str) -> None:
    cc_pattern = re.compile(r"\b(?:\d[ -]?){13,16}\b")

    with allure.step("Fetch user and post data and scan for credit card patterns"):
        responses = [
            requests.get(f"{api_base_url}/users", timeout=10),
            requests.get(f"{api_base_url}/posts", timeout=10),
        ]

    with allure.step("Assert no credit card pattern appears in any response"):
        for resp in responses:
            matches = cc_pattern.findall(resp.text)
            if matches:
                allure.attach(
                    f"URL: {resp.url}\nMatches: {matches[:5]}",
                    name="SC-28 Credit Card Pattern",
                    attachment_type=allure.attachment_type.TEXT,
                )
            assert not matches, f"SC-28 FAIL: response from {resp.url} must not contain credit card patterns"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SC — System and Communications Protection")
@allure.story("SC-28 Protection of Information at Rest")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SC-28: Response body does not contain US Social Security Number patterns")
@allure.description("SSNs in API responses indicate a failure to protect PII at rest.")
@pytest.mark.compliance
@pytest.mark.nist_sc28
def test_sc28_response_does_not_contain_ssn_patterns(api_base_url: str) -> None:
    ssn_pattern = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

    with allure.step("Fetch user data and scan for SSN patterns"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        assert response.status_code == 200, f"SC-28 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert no SSN pattern is present in the response body"):
        matches = ssn_pattern.findall(response.text)
        if matches:
            allure.attach(
                f"SSN patterns found: {matches}",
                name="SC-28 SSN Exposure",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not matches, f"SC-28 FAIL: response must not contain SSN patterns, found {len(matches)} match(es)"


# ── IA-2: Identification and Authentication ───────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA — Identification and Authentication")
@allure.story("IA-2 Identification and Authentication")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IA-2: Request with a malformed Authorization header is handled safely")
@allure.description("Malformed auth tokens must not cause 5xx errors or expose internal details.")
@pytest.mark.compliance
@pytest.mark.nist_ia2
def test_ia2_malformed_auth_header_handled_safely(api_base_url: str) -> None:
    bad_token = "Bearer INVALID.TOKEN.VALUE"

    with allure.step("Send request with a malformed Authorization header"):
        response = requests.get(
            f"{api_base_url}/posts/1",
            headers={"Authorization": bad_token},
            timeout=10,
        )

    with allure.step("Assert server does not return 5xx for a malformed token"):
        if response.status_code >= 500:
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:500]}",
                name="IA-2 5xx on Bad Token",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            response.status_code < 500
        ), f"IA-2 FAIL: malformed auth header must not produce 5xx, got {response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA — Identification and Authentication")
@allure.story("IA-2 Identification and Authentication")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IA-2: Repeated authentication failures do not expose internal error details")
@allure.description("Five consecutive bad-token requests must not trigger a 5xx or leak internals.")
@pytest.mark.compliance
@pytest.mark.nist_ia2
def test_ia2_repeated_auth_failures_do_not_expose_internals(api_base_url: str) -> None:
    bad_tokens = [
        "Bearer eyJinvalid1",
        "Bearer eyJinvalid2",
        "Bearer eyJinvalid3",
        "Bearer eyJinvalid4",
        "Bearer eyJinvalid5",
    ]

    with allure.step("Send 5 consecutive requests with invalid tokens"):
        statuses = []
        for token in bad_tokens:
            resp = requests.get(
                f"{api_base_url}/posts/1",
                headers={"Authorization": token},
                timeout=10,
            )
            statuses.append(resp.status_code)
            if resp.status_code >= 500:
                allure.attach(
                    f"Token: {token}\nStatus: {resp.status_code}\nBody: {resp.text[:300]}",
                    name="IA-2 Lockout 5xx Leak",
                    attachment_type=allure.attachment_type.TEXT,
                )

    with allure.step("Assert no 5xx response was returned across all attempts"):
        server_errors = [s for s in statuses if s >= 500]
        assert not server_errors, (
            f"IA-2 FAIL: repeated auth failures must not expose 5xx errors, " f"got: {server_errors}"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA — Identification and Authentication")
@allure.story("IA-2 Identification and Authentication")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("IA-2: Empty Authorization header value is handled without server crash")
@allure.description("An empty auth header must return a safe client-error status, not a server error.")
@pytest.mark.compliance
@pytest.mark.nist_ia2
def test_ia2_empty_auth_header_does_not_crash_server(api_base_url: str) -> None:
    with allure.step("Send request with an empty Authorization header value"):
        response = requests.get(
            f"{api_base_url}/posts/1",
            headers={"Authorization": ""},
            timeout=10,
        )

    with allure.step("Assert no 5xx response is returned"):
        if response.status_code >= 500:
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:300]}",
                name="IA-2 Empty Auth 5xx",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            response.status_code < 500
        ), f"IA-2 FAIL: empty auth header must not produce 5xx, got {response.status_code}"


# ── IA-5: Authenticator Management ────────────────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA — Identification and Authentication")
@allure.story("IA-5 Authenticator Management")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("IA-5: ANTHROPIC_API_KEY is present in the environment")
@allure.description("A missing API key means authenticator provisioning has failed.")
@pytest.mark.compliance
@pytest.mark.nist_ia5
def test_ia5_api_key_is_present_in_environment() -> None:
    with allure.step("Read ANTHROPIC_API_KEY from environment"):
        key = os.getenv("ANTHROPIC_API_KEY", "")

    with allure.step("Assert the key is set and non-empty"):
        if not key:
            allure.attach(
                "ANTHROPIC_API_KEY is not set or is empty.",
                name="IA-5 Missing Authenticator",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert key, "IA-5 FAIL: ANTHROPIC_API_KEY must be set for authenticator management compliance"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA — Identification and Authentication")
@allure.story("IA-5 Authenticator Management")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IA-5: API key meets minimum length requirement")
@allure.description("Short API keys are brute-forceable. Minimum 20 characters enforces key strength.")
@pytest.mark.compliance
@pytest.mark.nist_ia5
def test_ia5_api_key_meets_minimum_length() -> None:
    min_length = 20

    with allure.step("Read ANTHROPIC_API_KEY from environment"):
        key = os.getenv("ANTHROPIC_API_KEY", "")
        if not key:
            pytest.skip("ANTHROPIC_API_KEY not set — skipping length check")

    with allure.step(f"Assert key length >= {min_length} characters"):
        if len(key) < min_length:
            allure.attach(
                f"Key length: {len(key)}  Minimum: {min_length}",
                name="IA-5 Key Too Short",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert len(key) >= min_length, f"IA-5 FAIL: API key must be at least {min_length} characters, got {len(key)}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("IA — Identification and Authentication")
@allure.story("IA-5 Authenticator Management")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("IA-5: API key does not appear in any API response body")
@allure.description("An API key present in a response body indicates a credential leak in transit.")
@pytest.mark.compliance
@pytest.mark.nist_ia5
def test_ia5_api_key_not_present_in_response_body(api_base_url: str) -> None:
    with allure.step("Read ANTHROPIC_API_KEY from environment"):
        key = os.getenv("ANTHROPIC_API_KEY", "")
        if not key:
            pytest.skip("ANTHROPIC_API_KEY not set — skipping leak check")

    with allure.step("Fetch several API resources"):
        endpoints = ["/posts/1", "/users/1", "/comments/1"]
        for path in endpoints:
            resp = requests.get(f"{api_base_url}{path}", timeout=10)

            with allure.step(f"Scan {path} response for API key"):
                if key in resp.text:
                    allure.attach(
                        f"API key found in response from {path}",
                        name="IA-5 Key Leak",
                        attachment_type=allure.attachment_type.TEXT,
                    )
                assert key not in resp.text, f"IA-5 FAIL: API key must not appear in response body from {path}"
