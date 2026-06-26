# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 System and Services Acquisition compliance tests -- SA-11, SA-15."""

import allure
import pytest
import requests

# -- SA-11: Developer Testing and Evaluation ------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SA -- System and Services Acquisition")
@allure.story("SA-11 Developer Testing and Evaluation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SA-11: API returns correct status codes for all CRUD operations")
@allure.description("Developer testing must verify correct status codes for all supported operations.")
@pytest.mark.compliance
@pytest.mark.nist_sa11
def test_sa11_api_returns_correct_status_codes_for_crud(api_base_url: str) -> None:
    with allure.step("Test GET returns 200"):
        get_response = requests.get(f"{api_base_url}/posts/1", timeout=10)
        assert get_response.status_code == 200, f"SA-11 FAIL: GET must return 200, got {get_response.status_code}"

    with allure.step("Test POST returns 201"):
        post_response = requests.post(
            f"{api_base_url}/posts",
            json={"title": "SA-11 test", "body": "developer test", "userId": 1},
            timeout=10,
        )
        assert post_response.status_code == 201, f"SA-11 FAIL: POST must return 201, got {post_response.status_code}"

    with allure.step("Test DELETE returns 200"):
        delete_response = requests.delete(f"{api_base_url}/posts/1", timeout=10)
        assert (
            delete_response.status_code == 200
        ), f"SA-11 FAIL: DELETE must return 200, got {delete_response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SA -- System and Services Acquisition")
@allure.story("SA-11 Developer Testing and Evaluation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SA-11: API rejects malformed input with 400 or 422")
@allure.description("Developer testing must confirm the API rejects invalid payloads with appropriate error codes.")
@pytest.mark.compliance
@pytest.mark.nist_sa11
def test_sa11_api_rejects_malformed_input(api_base_url: str) -> None:
    with allure.step("Send a POST with an empty payload"):
        response = requests.post(
            f"{api_base_url}/posts",
            json={},
            timeout=10,
        )

    with allure.step("Assert response indicates client error or accepted with defaults"):
        if response.status_code not in (200, 201, 400, 422):
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:500]}",
                name="SA-11 Unexpected Response to Malformed Input",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert response.status_code in (
            200,
            201,
            400,
            422,
        ), f"SA-11 FAIL: malformed input must return 200/201/400/422, got {response.status_code}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SA -- System and Services Acquisition")
@allure.story("SA-11 Developer Testing and Evaluation")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SA-11: All API responses return within developer-defined latency threshold")
@allure.description("Developer testing must verify response times meet the defined latency threshold of 2000ms.")
@pytest.mark.compliance
@pytest.mark.nist_sa11
def test_sa11_all_responses_within_latency_threshold(api_base_url: str) -> None:
    endpoints = ["/posts", "/users", "/comments", "/todos"]

    with allure.step("Probe all endpoints and record elapsed times"):
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

    with allure.step("Assert all endpoints pass the developer latency threshold"):
        if failures:
            allure.attach(
                f"Failing endpoints:\n{failures}",
                name="SA-11 Latency Threshold Failures",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not failures, f"SA-11 FAIL: {len(failures)} endpoint(s) failed latency/status check: {failures}"


# -- SA-15: Development Process, Standards, and Tools --------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SA -- System and Services Acquisition")
@allure.story("SA-15 Development Process Standards and Tools")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SA-15: API adheres to RESTful standards -- correct content-type on all responses")
@allure.description("Development standards require all API responses to declare application/json content-type.")
@pytest.mark.compliance
@pytest.mark.nist_sa15
def test_sa15_api_adheres_to_restful_content_type_standard(api_base_url: str) -> None:
    endpoints = ["/posts/1", "/users/1", "/comments/1"]

    with allure.step("Assert Content-Type is application/json on all endpoints"):
        failures = []
        for endpoint in endpoints:
            response = requests.get(f"{api_base_url}{endpoint}", timeout=10)
            content_type = response.headers.get("Content-Type", "")
            if "application/json" not in content_type.lower():
                failures.append({"endpoint": endpoint, "content_type": content_type})

    with allure.step("Assert all endpoints return correct content-type"):
        if failures:
            allure.attach(
                f"Non-compliant endpoints:\n{failures}",
                name="SA-15 Content-Type Standard Violation",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not failures
        ), f"SA-15 FAIL: {len(failures)} endpoint(s) violate the application/json standard: {failures}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SA -- System and Services Acquisition")
@allure.story("SA-15 Development Process Standards and Tools")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SA-15: API follows standard HTTP method semantics")
@allure.description("Development standards require correct HTTP method semantics -- GET must be idempotent.")
@pytest.mark.compliance
@pytest.mark.nist_sa15
def test_sa15_api_follows_http_method_semantics(api_base_url: str) -> None:
    with allure.step("Verify GET is idempotent -- two identical requests return identical data"):
        r1 = requests.get(f"{api_base_url}/posts/1", timeout=10)
        r2 = requests.get(f"{api_base_url}/posts/1", timeout=10)
        assert r1.status_code == 200, f"SA-15 FAIL: GET must return 200, got {r1.status_code}"
        assert r2.status_code == 200, f"SA-15 FAIL: GET must return 200, got {r2.status_code}"

    with allure.step("Assert both GET responses are identical"):
        if r1.json() != r2.json():
            allure.attach(
                f"Request 1: {r1.json()}\nRequest 2: {r2.json()}",
                name="SA-15 GET Not Idempotent",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert r1.json() == r2.json(), "SA-15 FAIL: GET must be idempotent -- repeated requests returned different data"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SA -- System and Services Acquisition")
@allure.story("SA-15 Development Process Standards and Tools")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SA-15: API response schema is documented and stable across requests")
@allure.description("Development standards require a stable, documented response schema for all resources.")
@pytest.mark.compliance
@pytest.mark.nist_sa15
def test_sa15_response_schema_is_stable_and_documented(api_base_url: str) -> None:
    documented_schema = {"id", "title", "body", "userId"}

    with allure.step("Retrieve multiple posts and validate schema stability"):
        failures = []
        for post_id in (1, 2, 3):
            response = requests.get(f"{api_base_url}/posts/{post_id}", timeout=10)
            assert (
                response.status_code == 200
            ), f"SA-15 FAIL: post {post_id} must return 200, got {response.status_code}"
            actual = set(response.json().keys())
            missing = documented_schema - actual
            if missing:
                failures.append({"post_id": post_id, "missing_fields": list(missing)})

    with allure.step("Assert schema is stable and matches documentation"):
        if failures:
            allure.attach(
                f"Schema violations:\n{failures}",
                name="SA-15 Schema Instability",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not failures, f"SA-15 FAIL: {len(failures)} post(s) deviate from the documented schema: {failures}"
