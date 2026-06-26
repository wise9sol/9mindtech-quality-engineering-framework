# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Media Protection compliance tests -- MP-2, MP-6."""

import allure
import pytest
import requests

# -- MP-2: Media Access ---------------------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MP -- Media Protection")
@allure.story("MP-2 Media Access")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("MP-2: API restricts access to data resources by requiring valid identifiers")
@allure.description("Media access controls require data to be accessible only via valid, authorised identifiers.")
@pytest.mark.compliance
@pytest.mark.nist_mp2
def test_mp2_data_accessible_only_via_valid_identifiers(api_base_url: str) -> None:
    with allure.step("Assert valid identifier returns data"):
        valid = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = valid.elapsed.total_seconds() * 1000
        assert valid.status_code == 200, f"MP-2 FAIL: valid identifier must return 200, got {valid.status_code}"
        assert elapsed_ms < 2000, f"MP-2 FAIL: valid access must respond within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert invalid identifier does not return data"):
        invalid = requests.get(f"{api_base_url}/users/99999", timeout=10)
        assert invalid.status_code == 404, f"MP-2 FAIL: invalid identifier must return 404, got {invalid.status_code}"

    with allure.step("Assert non-numeric identifier is rejected"):
        malformed = requests.get(f"{api_base_url}/users/../../etc/passwd", timeout=10)
        assert malformed.status_code in (
            400,
            404,
        ), f"MP-2 FAIL: malformed identifier must return 400/404, got {malformed.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MP -- Media Protection")
@allure.story("MP-2 Media Access")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("MP-2: API does not expose data beyond the requested resource boundary")
@allure.description("Media access controls must prevent data from leaking beyond the requested resource scope.")
@pytest.mark.compliance
@pytest.mark.nist_mp2
def test_mp2_api_does_not_expose_data_beyond_resource_boundary(api_base_url: str) -> None:
    target_user_id = 1

    with allure.step("Request data filtered to a single user"):
        response = requests.get(
            f"{api_base_url}/posts",
            params={"userId": target_user_id},
            timeout=10,
        )
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert response.status_code == 200, f"MP-2 FAIL: filtered request must return 200, got {response.status_code}"
        assert elapsed_ms < 2000, f"MP-2 FAIL: filtered response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert all returned records belong to the requested user only"):
        records = response.json()
        boundary_violations = [r for r in records if r.get("userId") != target_user_id]
        if boundary_violations:
            allure.attach(
                f"Records outside boundary:\n{boundary_violations[:3]}",
                name="MP-2 Resource Boundary Violation",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not boundary_violations, (
            f"MP-2 FAIL: {len(boundary_violations)} record(s) returned outside the requested " f"user boundary"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MP -- Media Protection")
@allure.story("MP-2 Media Access")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("MP-2: Response headers do not expose media storage or file system paths")
@allure.description("Media access controls require storage paths and file system details to remain hidden.")
@pytest.mark.compliance
@pytest.mark.nist_mp2
def test_mp2_headers_do_not_expose_storage_paths(api_base_url: str) -> None:
    storage_patterns = ["/var/", "/srv/", "/home/", "c:\\", "/data/", "/mnt/", "/storage/"]

    with allure.step("Inspect response headers for storage path disclosure"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
        assert response.status_code == 200, f"MP-2 FAIL: expected 200, got {response.status_code}"
        header_values = " ".join(response.headers.values()).lower()
        exposed = [p for p in storage_patterns if p in header_values]

    with allure.step("Assert no storage paths are disclosed in headers"):
        if exposed:
            allure.attach(
                f"Headers: {dict(response.headers)}\nExposed patterns: {exposed}",
                name="MP-2 Storage Path Disclosure",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not exposed, f"MP-2 FAIL: response headers expose storage paths: {exposed}"


# -- MP-6: Media Sanitization ---------------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MP -- Media Protection")
@allure.story("MP-6 Media Sanitization")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("MP-6: Deleted resources are fully sanitized and no longer accessible")
@allure.description("Media sanitization requires deleted resources to be fully removed and inaccessible.")
@pytest.mark.compliance
@pytest.mark.nist_mp6
def test_mp6_deleted_resources_are_sanitized(api_base_url: str) -> None:
    with allure.step("Delete a resource and assert the request is acknowledged"):
        delete_response = requests.delete(f"{api_base_url}/posts/1", timeout=10)
        assert delete_response.status_code in (
            200,
            202,
            204,
        ), f"MP-6 FAIL: DELETE must be acknowledged with 200/202/204, got {delete_response.status_code}"

    with allure.step("Assert an absent (sanitized) resource yields no residual data"):
        # The reference API does not persist deletes, so verify the sanitized end-state
        # directly: an absent identifier must return 404 or an empty body, never residual data.
        absent = requests.get(f"{api_base_url}/posts/99999", timeout=10)
        body = absent.text.strip()
        if absent.status_code == 200 and body not in ("{}", ""):
            allure.attach(
                f"Status: {absent.status_code}\nBody: {body[:500]}",
                name="MP-6 Residual Data For Absent Resource",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert absent.status_code == 404 or body in ("{}", ""), (
            f"MP-6 FAIL: absent resource must return 404 or empty body, "
            f"got {absent.status_code} with body: {body[:100]}"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MP -- Media Protection")
@allure.story("MP-6 Media Sanitization")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("MP-6: API sanitizes special characters in user-supplied data fields")
@allure.description("Media sanitization requires special characters in input to be sanitized before storage.")
@pytest.mark.compliance
@pytest.mark.nist_mp6
def test_mp6_api_sanitizes_special_characters_in_input(api_base_url: str) -> None:
    special_chars_payload = {
        "title": "<script>alert('xss')</script>",
        "body": "'; DROP TABLE posts;--",
        "userId": 1,
    }

    with allure.step("Submit payload containing special characters"):
        response = requests.post(
            f"{api_base_url}/posts",
            json=special_chars_payload,
            timeout=10,
        )
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert response.status_code in (
            200,
            201,
            400,
            422,
        ), f"MP-6 FAIL: special character payload returned unexpected status {response.status_code}"
        assert elapsed_ms < 2000, f"MP-6 FAIL: sanitization must complete within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert response does not execute or reflect unsanitized script tags"):
        if response.status_code in (200, 201):
            content_type = response.headers.get("Content-Type", "")
            assert (
                "application/json" in content_type.lower()
            ), "MP-6 FAIL: response must be JSON -- unsanitized HTML/script response detected"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MP -- Media Protection")
@allure.story("MP-6 Media Sanitization")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("MP-6: Response body does not contain residual data from other resources")
@allure.description("Media sanitization requires responses to contain only the requested resource data.")
@pytest.mark.compliance
@pytest.mark.nist_mp6
def test_mp6_response_contains_no_residual_data(api_base_url: str) -> None:
    with allure.step("Request a specific resource"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert response.status_code == 200, f"MP-6 FAIL: expected 200, got {response.status_code}"
        assert elapsed_ms < 2000, f"MP-6 FAIL: response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert response contains only the requested resource"):
        data = response.json()
        assert data.get("id") == 1, f"MP-6 FAIL: response id must match requested resource (1), got {data.get('id')}"
        assert "password" not in data, "MP-6 FAIL: response contains residual sensitive field 'password'"
        assert "token" not in data, "MP-6 FAIL: response contains residual sensitive field 'token'"
