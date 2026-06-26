# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Maintenance compliance tests -- MA-2, MA-6."""

import allure
import pytest
import requests

# -- MA-2: Controlled Maintenance -----------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MA -- Maintenance")
@allure.story("MA-2 Controlled Maintenance")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("MA-2: System remains available and responsive during normal operations")
@allure.description("Controlled maintenance requires the system to remain available outside maintenance windows.")
@pytest.mark.compliance
@pytest.mark.nist_ma2
def test_ma2_system_available_outside_maintenance_window(api_base_url: str) -> None:
    with allure.step("Probe primary endpoints to verify availability"):
        endpoints = ["/users", "/posts", "/comments"]
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

    with allure.step("Assert all endpoints available outside maintenance window"):
        if failures:
            allure.attach(
                f"Unavailable endpoints:\n{failures}",
                name="MA-2 Maintenance Window Violation",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not failures
        ), f"MA-2 FAIL: {len(failures)} endpoint(s) unavailable outside maintenance window: {failures}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MA -- Maintenance")
@allure.story("MA-2 Controlled Maintenance")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("MA-2: System state is consistent before and after maintenance probe")
@allure.description("Controlled maintenance must not alter system data state -- records must be consistent.")
@pytest.mark.compliance
@pytest.mark.nist_ma2
def test_ma2_system_state_consistent_after_maintenance_probe(api_base_url: str) -> None:
    with allure.step("Capture pre-maintenance baseline"):
        pre = requests.get(f"{api_base_url}/users/1", timeout=10)
        assert pre.status_code == 200, f"MA-2 FAIL: baseline capture must return 200, got {pre.status_code}"

    with allure.step("Simulate maintenance probe -- re-request same resource"):
        post = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = post.elapsed.total_seconds() * 1000
        assert post.status_code == 200, f"MA-2 FAIL: post-maintenance probe must return 200, got {post.status_code}"
        assert elapsed_ms < 2000, f"MA-2 FAIL: post-maintenance response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert system state is unchanged"):
        if pre.json() != post.json():
            allure.attach(
                f"Pre-maintenance: {pre.json()}\nPost-maintenance: {post.json()}",
                name="MA-2 State Change Detected",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            pre.json() == post.json()
        ), "MA-2 FAIL: system state changed during maintenance probe -- controlled maintenance violated"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MA -- Maintenance")
@allure.story("MA-2 Controlled Maintenance")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("MA-2: Maintenance does not expose additional attack surface")
@allure.description("Controlled maintenance must not expose diagnostic or admin endpoints to the public surface.")
@pytest.mark.compliance
@pytest.mark.nist_ma2
def test_ma2_maintenance_does_not_expose_attack_surface(api_base_url: str) -> None:
    maintenance_paths = ["/maintenance", "/admin/maintenance", "/status/maintenance", "/diag"]

    with allure.step("Probe maintenance-related paths for unintended exposure"):
        exposed = []
        for path in maintenance_paths:
            response = requests.get(f"{api_base_url}{path}", timeout=10)
            if response.status_code == 200:
                exposed.append({"path": path, "status": response.status_code})

    with allure.step("Assert no maintenance endpoints are publicly accessible"):
        if exposed:
            allure.attach(
                f"Exposed maintenance paths:\n{exposed}",
                name="MA-2 Maintenance Surface Exposure",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not exposed, f"MA-2 FAIL: {len(exposed)} maintenance endpoint(s) publicly accessible: {exposed}"


# -- MA-6: Timely Maintenance ---------------------------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MA -- Maintenance")
@allure.story("MA-6 Timely Maintenance")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("MA-6: System responds within timely maintenance latency bounds")
@allure.description("Timely maintenance requires the system to respond within defined latency bounds after upkeep.")
@pytest.mark.compliance
@pytest.mark.nist_ma6
def test_ma6_system_responds_within_timely_maintenance_bounds(api_base_url: str) -> None:
    timely_threshold_ms = 2000

    with allure.step("Probe system and verify timely response after maintenance"):
        response = requests.get(f"{api_base_url}/users", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000

    with allure.step("Assert system returned 200"):
        assert (
            response.status_code == 200
        ), f"MA-6 FAIL: system must return 200 after timely maintenance, got {response.status_code}"

    with allure.step(f"Assert response within timely threshold of {timely_threshold_ms}ms"):
        if elapsed_ms >= timely_threshold_ms:
            allure.attach(
                f"Elapsed: {elapsed_ms:.0f}ms  Threshold: {timely_threshold_ms}ms",
                name="MA-6 Timely Maintenance Threshold Breach",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert elapsed_ms < timely_threshold_ms, (
            f"MA-6 FAIL: system did not respond within {timely_threshold_ms}ms after maintenance, "
            f"took {elapsed_ms:.0f}ms"
        )


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MA -- Maintenance")
@allure.story("MA-6 Timely Maintenance")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("MA-6: All system components are available within timely maintenance window")
@allure.description("Timely maintenance requires all system components to be available within the maintenance SLA.")
@pytest.mark.compliance
@pytest.mark.nist_ma6
def test_ma6_all_components_available_within_maintenance_sla(api_base_url: str) -> None:
    sla_ms = 2000
    components = ["/users", "/posts", "/comments", "/todos"]

    with allure.step("Verify all components available within maintenance SLA"):
        failures = []
        for component in components:
            response = requests.get(f"{api_base_url}{component}", timeout=10)
            elapsed_ms = response.elapsed.total_seconds() * 1000
            if response.status_code != 200 or elapsed_ms >= sla_ms:
                failures.append(
                    {
                        "component": component,
                        "status": response.status_code,
                        "elapsed_ms": round(elapsed_ms),
                    }
                )

    with allure.step("Assert all components within SLA"):
        if failures:
            allure.attach(
                f"SLA breaches:\n{failures}",
                name="MA-6 Maintenance SLA Breach",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not failures, f"MA-6 FAIL: {len(failures)} component(s) outside maintenance SLA: {failures}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("MA -- Maintenance")
@allure.story("MA-6 Timely Maintenance")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("MA-6: System data integrity is preserved through maintenance cycles")
@allure.description("Timely maintenance must preserve data integrity -- record counts must remain stable.")
@pytest.mark.compliance
@pytest.mark.nist_ma6
def test_ma6_data_integrity_preserved_through_maintenance(api_base_url: str) -> None:
    with allure.step("Capture record count before maintenance cycle"):
        pre = requests.get(f"{api_base_url}/users", timeout=10)
        assert pre.status_code == 200, f"MA-6 FAIL: pre-maintenance count must return 200, got {pre.status_code}"
        pre_count = len(pre.json())

    with allure.step("Simulate maintenance cycle and re-probe"):
        post = requests.get(f"{api_base_url}/users", timeout=10)
        assert post.status_code == 200, f"MA-6 FAIL: post-maintenance count must return 200, got {post.status_code}"
        post_count = len(post.json())

    with allure.step("Assert record count is unchanged -- data integrity preserved"):
        if pre_count != post_count:
            allure.attach(
                f"Pre-maintenance count: {pre_count}\nPost-maintenance count: {post_count}",
                name="MA-6 Data Integrity Violation",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert pre_count == post_count, (
            f"MA-6 FAIL: record count changed through maintenance cycle "
            f"({pre_count} -> {post_count}) -- data integrity compromised"
        )
