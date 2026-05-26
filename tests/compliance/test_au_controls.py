# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Audit and Accountability compliance tests — AU-2, AU-9, AU-12."""

import allure
import pytest
import requests


# ── AU-2: Event Logging ────────────────────────────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AU — Audit and Accountability")
@allure.story("AU-2 Event Logging")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("AU-2: Successful resource fetch produces a traceable response")
@allure.description("A successful GET must return a response body with an identifiable record ID.")
@pytest.mark.compliance
@pytest.mark.nist_au2
def test_au2_successful_fetch_produces_traceable_response(api_base_url: str) -> None:
    with allure.step("Send GET request for a known resource"):
        response = requests.get(f"{api_base_url}/posts/1", timeout=10)

    with allure.step("Assert 200 and response time"):
        assert (
            response.status_code == 200
        ), f"AU-2 FAIL: expected 200 for audit-traceable fetch, got {response.status_code}"
        assert (
            response.elapsed.total_seconds() * 1000 < 2000
        ), "AU-2 FAIL: response must arrive within 2000ms for timely event logging"

    with allure.step("Assert response contains a traceable ID field"):
        body = response.json()
        if "id" not in body:
            allure.attach(
                f"Response body: {body}",
                name="AU-2 Missing Traceable ID",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert "id" in body, "AU-2 FAIL: response must contain an 'id' field for audit traceability"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AU — Audit and Accountability")
@allure.story("AU-2 Event Logging")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("AU-2: Create event produces an auditable record with assigned ID")
@allure.description("POST must return a 201 with an assigned ID so the creation event is auditable.")
@pytest.mark.compliance
@pytest.mark.nist_au2
def test_au2_create_event_produces_auditable_record(api_base_url: str) -> None:
    payload = {"title": "AU-2 audit test", "body": "event logging validation", "userId": 1}

    with allure.step("Submit POST request to create a record"):
        response = requests.post(f"{api_base_url}/posts", json=payload, timeout=10)

    with allure.step("Assert 201 status"):
        assert response.status_code == 201, f"AU-2 FAIL: create event must return 201, got {response.status_code}"

    with allure.step("Assert response contains an assigned ID for audit trail"):
        body = response.json()
        if "id" not in body:
            allure.attach(
                f"Response body: {body}",
                name="AU-2 No Audit ID on Create",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert "id" in body, "AU-2 FAIL: create response must include an 'id' for audit trail"
        assert isinstance(body["id"], int), f"AU-2 FAIL: audit ID must be an integer, got {type(body['id']).__name__}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AU — Audit and Accountability")
@allure.story("AU-2 Event Logging")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("AU-2: Failed request returns a loggable structured error")
@allure.description("Error responses must be structured so failures can be captured in an audit log.")
@pytest.mark.compliance
@pytest.mark.nist_au2
def test_au2_failed_request_returns_loggable_error(api_base_url: str) -> None:
    with allure.step("Request a non-existent resource"):
        response = requests.get(f"{api_base_url}/posts/99999", timeout=10)

    with allure.step("Assert 404 status code is returned"):
        assert response.status_code == 404, (
            f"AU-2 FAIL: missing resource must return 404 for loggable audit event, " f"got {response.status_code}"
        )

    with allure.step("Assert response does not contain a 5xx internal error"):
        assert response.status_code < 500, "AU-2 FAIL: server must not produce 5xx errors that obscure the audit event"


# ── AU-9: Protection of Audit Information ─────────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AU — Audit and Accountability")
@allure.story("AU-9 Protection of Audit Information")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("AU-9: Audit records cannot be overwritten with arbitrary data")
@allure.description("PUT requests must not silently overwrite audit-critical fields with invalid data.")
@pytest.mark.compliance
@pytest.mark.nist_au9
def test_au9_audit_records_cannot_be_overwritten_arbitrarily(api_base_url: str) -> None:
    payload = {"id": 1, "title": "overwrite attempt", "body": "AU-9 test", "userId": 1}

    with allure.step("Attempt to overwrite record with PUT"):
        response = requests.put(f"{api_base_url}/posts/1", json=payload, timeout=10)

    with allure.step("Assert server responds with 2xx and not 5xx"):
        if response.status_code >= 500:
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:500]}",
                name="AU-9 Server Error on PUT",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert response.status_code < 500, f"AU-9 FAIL: PUT must not produce a 5xx error, got {response.status_code}"

    with allure.step("Assert updated record retains its original ID"):
        body = response.json()
        assert body.get("id") == 1, f"AU-9 FAIL: record ID must not change on update, got id={body.get('id')}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AU — Audit and Accountability")
@allure.story("AU-9 Protection of Audit Information")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("AU-9: Audit record list is bounded and does not expose unlimited data")
@allure.description("The record list must return a bounded, finite set to prevent bulk audit export.")
@pytest.mark.compliance
@pytest.mark.nist_au9
def test_au9_audit_record_list_is_bounded(api_base_url: str) -> None:
    with allure.step("Fetch the full post list"):
        response = requests.get(f"{api_base_url}/posts", timeout=10)
        assert response.status_code == 200, f"AU-9 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert the list has a finite, non-zero length"):
        records = response.json()
        assert len(records) > 0, "AU-9 FAIL: audit record list must not be empty"
        assert len(records) <= 10000, f"AU-9 FAIL: record list must be bounded, got {len(records)} records"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AU — Audit and Accountability")
@allure.story("AU-9 Protection of Audit Information")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("AU-9: All audit record IDs are valid positive integers")
@allure.description("Invalid record IDs undermine the integrity of the audit trail.")
@pytest.mark.compliance
@pytest.mark.nist_au9
def test_au9_audit_record_ids_are_valid_positive_integers(api_base_url: str) -> None:
    with allure.step("Fetch posts and extract IDs"):
        response = requests.get(f"{api_base_url}/posts", timeout=10)
        assert response.status_code == 200, f"AU-9 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert every record ID is a positive integer"):
        invalid = [r for r in response.json() if not isinstance(r.get("id"), int) or r["id"] <= 0]
        if invalid:
            allure.attach(
                f"Invalid records: {invalid[:5]}",
                name="AU-9 Invalid Record IDs",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not invalid, (
            f"AU-9 FAIL: all audit record IDs must be positive integers, " f"found {len(invalid)} invalid record(s)"
        )


# ── AU-12: Audit Record Generation ────────────────────────────────────────────


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AU — Audit and Accountability")
@allure.story("AU-12 Audit Record Generation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("AU-12: POST generates a new record with a system-assigned ID")
@allure.description("Each created record must receive a unique system-assigned ID for audit generation.")
@pytest.mark.compliance
@pytest.mark.nist_au12
def test_au12_post_generates_record_with_assigned_id(api_base_url: str) -> None:
    payload = {"title": "AU-12 test", "body": "audit record generation", "userId": 1}

    with allure.step("Submit POST to create a new record"):
        response = requests.post(f"{api_base_url}/posts", json=payload, timeout=10)

    with allure.step("Assert 201 and system-assigned ID"):
        assert response.status_code == 201, f"AU-12 FAIL: record generation must return 201, got {response.status_code}"
        body = response.json()
        if "id" not in body:
            allure.attach(
                f"Response: {body}",
                name="AU-12 No ID on Record",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert "id" in body, "AU-12 FAIL: generated record must contain a system-assigned 'id'"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AU — Audit and Accountability")
@allure.story("AU-12 Audit Record Generation")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("AU-12: Generated record contains all required audit fields")
@allure.description("An audit record must carry userId, id, title, and body to be complete.")
@pytest.mark.compliance
@pytest.mark.nist_au12
def test_au12_generated_record_contains_required_audit_fields(api_base_url: str) -> None:
    with allure.step("Fetch a known record to verify its audit fields"):
        response = requests.get(f"{api_base_url}/posts/1", timeout=10)
        assert response.status_code == 200, f"AU-12 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert all required audit fields are present"):
        body = response.json()
        required = {"id", "userId", "title", "body"}
        missing = required - body.keys()
        if missing:
            allure.attach(
                f"Missing fields: {missing}\nRecord: {body}",
                name="AU-12 Incomplete Audit Record",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not missing, f"AU-12 FAIL: audit record must contain {required}, missing {missing}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("AU — Audit and Accountability")
@allure.story("AU-12 Audit Record Generation")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("AU-12: DELETE returns an audit-compatible 200 status")
@allure.description("A deletion event must return 200 so it can be captured in the audit log.")
@pytest.mark.compliance
@pytest.mark.nist_au12
def test_au12_delete_returns_audit_compatible_status(api_base_url: str) -> None:
    with allure.step("Send DELETE request for record id=1"):
        response = requests.delete(f"{api_base_url}/posts/1", timeout=10)

    with allure.step("Assert 200 status for audit-compatible deletion event"):
        if response.status_code != 200:
            allure.attach(
                f"Status: {response.status_code}\nBody: {response.text[:200]}",
                name="AU-12 DELETE Status",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert response.status_code == 200, (
            f"AU-12 FAIL: delete event must return 200 for audit compatibility, " f"got {response.status_code}"
        )
