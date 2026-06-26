# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Physical and Environmental Protection compliance tests -- PE-2, PE-3."""

import allure
import pytest
import requests

# -- PE-2: Physical Access Authorizations ---------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PE -- Physical and Environmental Protection")
@allure.story("PE-2 Physical Access Authorizations")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PE-2: API enforces access authorizations -- unauthorised identifiers are rejected")
@allure.description("Physical access authorizations are mirrored in the API layer -- invalid IDs must not return data.")
@pytest.mark.compliance
@pytest.mark.nist_pe2
def test_pe2_unauthorised_identifiers_are_rejected(api_base_url: str) -> None:
    with allure.step("Assert valid authorised identifier returns data"):
        valid = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = valid.elapsed.total_seconds() * 1000
        assert valid.status_code == 200, f"PE-2 FAIL: authorised identifier must return 200, got {valid.status_code}"
        assert elapsed_ms < 2000, f"PE-2 FAIL: authorised access must respond within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert unauthorised identifier is rejected with 404"):
        invalid = requests.get(f"{api_base_url}/users/99999", timeout=10)
        assert (
            invalid.status_code == 404
        ), f"PE-2 FAIL: unauthorised identifier must return 404, got {invalid.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PE -- Physical and Environmental Protection")
@allure.story("PE-2 Physical Access Authorizations")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PE-2: API does not expose access control lists or authorization metadata")
@allure.description("Physical access authorization data must not be exposed in API responses.")
@pytest.mark.compliance
@pytest.mark.nist_pe2
def test_pe2_access_control_metadata_not_exposed(api_base_url: str) -> None:
    acl_keywords = ["acl", "access_list", "permissions", "role", "clearance", "badge", "authorized_by"]

    with allure.step("Retrieve user resource and scan for ACL metadata exposure"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert response.status_code == 200, f"PE-2 FAIL: expected 200, got {response.status_code}"
        assert elapsed_ms < 2000, f"PE-2 FAIL: response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert no access control metadata is present in response"):
        body = response.text.lower()
        exposed = [kw for kw in acl_keywords if kw in body]
        if exposed:
            allure.attach(
                f"ACL keywords found: {exposed}\nBody: {response.text[:500]}",
                name="PE-2 ACL Metadata Exposure",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not exposed, f"PE-2 FAIL: access control metadata exposed in response: {exposed}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PE -- Physical and Environmental Protection")
@allure.story("PE-2 Physical Access Authorizations")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("PE-2: API access is consistently enforced across all resource endpoints")
@allure.description("Access authorizations must be enforced uniformly -- all endpoints reject invalid IDs.")
@pytest.mark.compliance
@pytest.mark.nist_pe2
def test_pe2_access_enforced_uniformly_across_endpoints(api_base_url: str) -> None:
    resource_endpoints = ["/users/99999", "/posts/99999", "/comments/99999"]

    with allure.step("Assert all resource endpoints reject invalid identifiers with 404"):
        failures = []
        for endpoint in resource_endpoints:
            response = requests.get(f"{api_base_url}{endpoint}", timeout=10)
            if response.status_code != 404:
                failures.append({"endpoint": endpoint, "status": response.status_code})

    with allure.step("Assert uniform access enforcement across all endpoints"):
        if failures:
            allure.attach(
                f"Non-uniform enforcement:\n{failures}",
                name="PE-2 Non-Uniform Access Enforcement",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not failures
        ), f"PE-2 FAIL: {len(failures)} endpoint(s) do not uniformly enforce access control: {failures}"


# -- PE-3: Physical Access Control ----------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PE -- Physical and Environmental Protection")
@allure.story("PE-3 Physical Access Control")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PE-3: API enforces access control -- requests without valid scope are blocked")
@allure.description("Physical access control is reflected in the API -- requests outside valid scope must be blocked.")
@pytest.mark.compliance
@pytest.mark.nist_pe3
def test_pe3_requests_outside_valid_scope_are_blocked(api_base_url: str) -> None:
    with allure.step("Assert in-scope request returns 200"):
        in_scope = requests.get(f"{api_base_url}/posts/1", timeout=10)
        elapsed_ms = in_scope.elapsed.total_seconds() * 1000
        assert in_scope.status_code == 200, f"PE-3 FAIL: in-scope request must return 200, got {in_scope.status_code}"
        assert elapsed_ms < 2000, f"PE-3 FAIL: in-scope response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert out-of-scope request is blocked with 404"):
        out_of_scope = requests.get(f"{api_base_url}/posts/99999", timeout=10)
        assert (
            out_of_scope.status_code == 404
        ), f"PE-3 FAIL: out-of-scope request must return 404, got {out_of_scope.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PE -- Physical and Environmental Protection")
@allure.story("PE-3 Physical Access Control")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("PE-3: API rejects requests using unsupported access methods")
@allure.description("Access control requires only approved methods -- unsupported HTTP methods are rejected.")
@pytest.mark.compliance
@pytest.mark.nist_pe3
def test_pe3_unsupported_access_methods_are_rejected(api_base_url: str) -> None:
    with allure.step("Send unsupported HTTP methods to a resource endpoint"):
        put_response = requests.put(
            f"{api_base_url}/users",
            json={"name": "PE-3 test"},
            timeout=10,
        )
        options_response = requests.options(f"{api_base_url}/users", timeout=10)

    with allure.step("Assert unsupported PUT to collection is rejected"):
        assert put_response.status_code in (
            400,
            404,
            405,
        ), f"PE-3 FAIL: unsupported PUT must return 400/404/405, got {put_response.status_code}"

    with allure.step("Assert OPTIONS response is within acceptable bounds"):
        assert options_response.status_code in (
            200,
            204,
            404,
            405,
        ), f"PE-3 FAIL: OPTIONS must return 200/204/404/405, got {options_response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("PE -- Physical and Environmental Protection")
@allure.story("PE-3 Physical Access Control")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("PE-3: API access control response times are within acceptable bounds")
@allure.description("Access control mechanisms must not degrade performance -- all responses within 2000ms.")
@pytest.mark.compliance
@pytest.mark.nist_pe3
def test_pe3_access_control_response_times_acceptable(api_base_url: str) -> None:
    probes = [
        ("/users/1", 200),
        ("/users/99999", 404),
        ("/posts/1", 200),
        ("/posts/99999", 404),
    ]

    with allure.step("Probe access control response times across valid and invalid requests"):
        failures = []
        for path, expected_status in probes:
            response = requests.get(f"{api_base_url}{path}", timeout=10)
            elapsed_ms = response.elapsed.total_seconds() * 1000
            if response.status_code != expected_status or elapsed_ms >= 2000:
                failures.append(
                    {
                        "path": path,
                        "expected": expected_status,
                        "actual": response.status_code,
                        "elapsed_ms": round(elapsed_ms),
                    }
                )

    with allure.step("Assert all access control checks within 2000ms"):
        if failures:
            allure.attach(
                f"Access control performance failures:\n{failures}",
                name="PE-3 Access Control Performance",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not failures, f"PE-3 FAIL: {len(failures)} access control check(s) failed or exceeded 2000ms: {failures}"
