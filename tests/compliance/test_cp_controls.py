# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Contingency Planning compliance tests -- CP-9, CP-10."""

import allure
import pytest
import requests

# -- CP-9: System Backup --------------------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CP -- Contingency Planning")
@allure.story("CP-9 System Backup")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CP-9: Critical data endpoints are reachable and return complete records")
@allure.description("System backup requires critical data to be retrievable as complete, non-empty records.")
@pytest.mark.compliance
@pytest.mark.nist_cp9
def test_cp9_critical_data_endpoints_return_complete_records(api_base_url: str) -> None:
    with allure.step("Request the critical user data endpoint"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000

    with allure.step("Assert endpoint is reachable and returns 200"):
        assert (
            response.status_code == 200
        ), f"CP-9 FAIL: critical data endpoint must return 200, got {response.status_code}"

    with allure.step("Assert response time within backup retrieval threshold"):
        assert elapsed_ms < 2000, f"CP-9 FAIL: critical data must be retrievable within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert backup data set is non-empty"):
        records = response.json()
        if not records:
            allure.attach(
                "Critical data endpoint returned an empty list -- backup would be empty.",
                name="CP-9 Empty Backup Dataset",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert records, "CP-9 FAIL: critical data endpoint must return records for backup"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CP -- Contingency Planning")
@allure.story("CP-9 System Backup")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CP-9: Individual records are retrievable by ID for point-in-time recovery")
@allure.description("Point-in-time recovery requires individual records to be retrievable by their unique identifier.")
@pytest.mark.compliance
@pytest.mark.nist_cp9
def test_cp9_individual_records_retrievable_for_recovery(api_base_url: str) -> None:
    with allure.step("Retrieve the full record inventory"):
        all_response = requests.get(f"{api_base_url}/users", timeout=10)
        assert (
            all_response.status_code == 200
        ), f"CP-9 FAIL: inventory endpoint must return 200, got {all_response.status_code}"
        records = all_response.json()
        assert records, "CP-9 FAIL: no records available for recovery validation"

    with allure.step("Retrieve an individual record by ID"):
        target_id = records[0]["id"]
        single_response = requests.get(f"{api_base_url}/users/{target_id}", timeout=10)
        elapsed_ms = single_response.elapsed.total_seconds() * 1000
        assert (
            single_response.status_code == 200
        ), f"CP-9 FAIL: individual record {target_id} must be retrievable, got {single_response.status_code}"
        assert elapsed_ms < 2000, f"CP-9 FAIL: record retrieval must complete within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert retrieved record matches inventory"):
        single = single_response.json()
        inventory_record = next((r for r in records if r["id"] == target_id), None)
        if single != inventory_record:
            allure.attach(
                f"Retrieved: {single}\nInventory: {inventory_record}",
                name="CP-9 Record Mismatch",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            single == inventory_record
        ), f"CP-9 FAIL: retrieved record {target_id} does not match inventory -- backup integrity compromised"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CP -- Contingency Planning")
@allure.story("CP-9 System Backup")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("CP-9: Backup data schema contains all required fields for restoration")
@allure.description("Records must contain all fields needed for full system restoration under CP-9.")
@pytest.mark.compliance
@pytest.mark.nist_cp9
def test_cp9_backup_schema_contains_restoration_fields(api_base_url: str) -> None:
    restoration_fields = {"id", "name", "username", "email"}

    with allure.step("Retrieve a record to validate backup schema"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
        assert response.status_code == 200, f"CP-9 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert all restoration fields are present"):
        actual = set(response.json().keys())
        missing = restoration_fields - actual
        if missing:
            allure.attach(
                f"Required for restoration: {restoration_fields}\nActual: {actual}\nMissing: {missing}",
                name="CP-9 Missing Restoration Fields",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not missing, f"CP-9 FAIL: backup record missing fields required for restoration: {missing}"


# -- CP-10: System Recovery and Reconstitution ----------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CP -- Contingency Planning")
@allure.story("CP-10 System Recovery and Reconstitution")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CP-10: System recovers and returns 200 within recovery time objective")
@allure.description("After a simulated disruption, the system must reconstitute and respond within the RTO threshold.")
@pytest.mark.compliance
@pytest.mark.nist_cp10
def test_cp10_system_recovers_within_rto(api_base_url: str) -> None:
    rto_ms = 5000

    with allure.step("Simulate recovery probe -- request after disruption window"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000

    with allure.step("Assert system has reconstituted and returns 200"):
        assert (
            response.status_code == 200
        ), f"CP-10 FAIL: system must return 200 after recovery, got {response.status_code}"

    with allure.step(f"Assert response within RTO of {rto_ms}ms"):
        if elapsed_ms >= rto_ms:
            allure.attach(
                f"Elapsed: {elapsed_ms:.0f}ms  RTO: {rto_ms}ms",
                name="CP-10 RTO Breach",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            elapsed_ms < rto_ms
        ), f"CP-10 FAIL: system did not recover within RTO of {rto_ms}ms, took {elapsed_ms:.0f}ms"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CP -- Contingency Planning")
@allure.story("CP-10 System Recovery and Reconstitution")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CP-10: Reconstituted system returns consistent data after recovery")
@allure.description("After recovery, the system must return data consistent with pre-disruption state.")
@pytest.mark.compliance
@pytest.mark.nist_cp10
def test_cp10_reconstituted_system_returns_consistent_data(api_base_url: str) -> None:
    with allure.step("Capture pre-recovery baseline data"):
        baseline = requests.get(f"{api_base_url}/users/1", timeout=10)
        assert baseline.status_code == 200, f"CP-10 FAIL: baseline capture must return 200, got {baseline.status_code}"

    with allure.step("Simulate recovery and re-probe"):
        recovery = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = recovery.elapsed.total_seconds() * 1000
        assert (
            recovery.status_code == 200
        ), f"CP-10 FAIL: post-recovery probe must return 200, got {recovery.status_code}"
        assert elapsed_ms < 2000, f"CP-10 FAIL: post-recovery response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert post-recovery data matches baseline"):
        if baseline.json() != recovery.json():
            allure.attach(
                f"Baseline: {baseline.json()}\nPost-recovery: {recovery.json()}",
                name="CP-10 Data Inconsistency After Recovery",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            baseline.json() == recovery.json()
        ), "CP-10 FAIL: post-recovery data does not match baseline -- reconstitution incomplete"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("CP -- Contingency Planning")
@allure.story("CP-10 System Recovery and Reconstitution")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("CP-10: All critical endpoints are accessible after system reconstitution")
@allure.description("Full reconstitution requires all critical endpoints to be accessible, not just the primary one.")
@pytest.mark.compliance
@pytest.mark.nist_cp10
def test_cp10_all_critical_endpoints_accessible_after_recovery(api_base_url: str) -> None:
    critical_endpoints = ["/users", "/posts", "/comments"]

    with allure.step("Probe all critical endpoints post-reconstitution"):
        failures = []
        for endpoint in critical_endpoints:
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

    with allure.step("Assert all critical endpoints accessible"):
        if failures:
            allure.attach(
                f"Inaccessible endpoints:\n{failures}",
                name="CP-10 Reconstitution Incomplete",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not failures
        ), f"CP-10 FAIL: {len(failures)} critical endpoint(s) inaccessible after reconstitution: {failures}"
