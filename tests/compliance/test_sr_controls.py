# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
"""NIST 800-53 Supply Chain Risk Management compliance tests -- SR-3, SR-5."""

import allure
import pytest
import requests

# -- SR-3: Supply Chain Controls and Processes ---------------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SR -- Supply Chain Risk Management")
@allure.story("SR-3 Supply Chain Controls and Processes")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SR-3: Every component traces to a validated source -- all posts reference a known user")
@allure.description(
    "Supply chain controls require traceable provenance -- every component must originate from a validated source."
)
@pytest.mark.compliance
@pytest.mark.nist_sr3
def test_sr3_all_posts_trace_to_validated_source(api_base_url: str) -> None:
    with allure.step("Retrieve the validated source inventory (users)"):
        users_response = requests.get(f"{api_base_url}/users", timeout=10)
        assert users_response.status_code == 200, f"SR-3 FAIL: expected 200, got {users_response.status_code}"
        valid_user_ids = {u.get("id") for u in users_response.json()}

    with allure.step("Retrieve all downstream components (posts)"):
        posts_response = requests.get(f"{api_base_url}/posts", timeout=10)
        elapsed_ms = posts_response.elapsed.total_seconds() * 1000
        assert posts_response.status_code == 200, f"SR-3 FAIL: expected 200, got {posts_response.status_code}"
        assert elapsed_ms < 2000, f"SR-3 FAIL: response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert every component traces to a validated source"):
        untraceable = [
            {"post_id": p.get("id"), "userId": p.get("userId")}
            for p in posts_response.json()
            if p.get("userId") not in valid_user_ids
        ]
        if untraceable:
            allure.attach(
                f"Components without a validated source:\n{untraceable[:5]}",
                name="SR-3 Untraceable Components",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not untraceable
        ), f"SR-3 FAIL: {len(untraceable)} component(s) do not trace to a validated source: {untraceable[:5]}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SR -- Supply Chain Risk Management")
@allure.story("SR-3 Supply Chain Controls and Processes")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SR-3: No orphaned components in the supply chain -- all comments reference a known post")
@allure.description(
    "Supply chain controls reject orphaned components -- every comment must reference an existing post."
)
@pytest.mark.compliance
@pytest.mark.nist_sr3
def test_sr3_no_orphaned_components_in_supply_chain(api_base_url: str) -> None:
    with allure.step("Retrieve the upstream component inventory (posts)"):
        posts_response = requests.get(f"{api_base_url}/posts", timeout=10)
        assert posts_response.status_code == 200, f"SR-3 FAIL: expected 200, got {posts_response.status_code}"
        valid_post_ids = {p.get("id") for p in posts_response.json()}

    with allure.step("Retrieve all dependent components (comments)"):
        comments_response = requests.get(f"{api_base_url}/comments", timeout=10)
        elapsed_ms = comments_response.elapsed.total_seconds() * 1000
        assert comments_response.status_code == 200, f"SR-3 FAIL: expected 200, got {comments_response.status_code}"
        assert elapsed_ms < 2000, f"SR-3 FAIL: response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert no dependent component is orphaned"):
        orphaned = [
            {"comment_id": c.get("id"), "postId": c.get("postId")}
            for c in comments_response.json()
            if c.get("postId") not in valid_post_ids
        ]
        if orphaned:
            allure.attach(
                f"Orphaned components:\n{orphaned[:5]}",
                name="SR-3 Orphaned Components",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not orphaned, f"SR-3 FAIL: {len(orphaned)} orphaned component(s) in the supply chain: {orphaned[:5]}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SR -- Supply Chain Risk Management")
@allure.story("SR-3 Supply Chain Controls and Processes")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SR-3: Supply chain components present a consistent, controlled structure")
@allure.description(
    "Supply chain controls require uniform components -- every component must expose the same controlled schema."
)
@pytest.mark.compliance
@pytest.mark.nist_sr3
def test_sr3_components_present_consistent_structure(api_base_url: str) -> None:
    controlled_fields = {"userId", "id", "title", "body"}

    with allure.step("Retrieve supply chain components (posts)"):
        response = requests.get(f"{api_base_url}/posts", timeout=10)
        assert response.status_code == 200, f"SR-3 FAIL: expected 200, got {response.status_code}"

    with allure.step("Assert every component conforms to the controlled structure"):
        nonconforming = [
            {"post_id": p.get("id"), "missing": list(controlled_fields - p.keys())}
            for p in response.json()
            if controlled_fields - p.keys()
        ]
        if nonconforming:
            allure.attach(
                f"Components with an uncontrolled structure:\n{nonconforming[:5]}",
                name="SR-3 Structure Drift",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not nonconforming
        ), f"SR-3 FAIL: {len(nonconforming)} component(s) deviate from the controlled structure: {nonconforming[:5]}"


# -- SR-5: Acquisition Strategies, Tools, and Methods --------------------------


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SR -- Supply Chain Risk Management")
@allure.story("SR-5 Acquisition Strategies, Tools, and Methods")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SR-5: Acquired resources conform to the defined acquisition schema")
@allure.description("Acquisition methods define accepted criteria -- every acquired resource must satisfy the schema.")
@pytest.mark.compliance
@pytest.mark.nist_sr5
def test_sr5_acquired_resource_conforms_to_acquisition_schema(api_base_url: str) -> None:
    acquisition_schema = {"id", "name", "username", "email", "address", "phone", "website", "company"}

    with allure.step("Acquire a resource through the defined acquisition method"):
        response = requests.get(f"{api_base_url}/users/1", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert response.status_code == 200, f"SR-5 FAIL: expected 200, got {response.status_code}"
        assert elapsed_ms < 2000, f"SR-5 FAIL: response must be within 2000ms, took {elapsed_ms:.0f}ms"

    with allure.step("Assert the acquired resource satisfies the acquisition schema"):
        missing = acquisition_schema - response.json().keys()
        if missing:
            allure.attach(
                f"Acquisition schema: {acquisition_schema}\nMissing: {missing}",
                name="SR-5 Acquisition Schema Gap",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert not missing, f"SR-5 FAIL: acquired resource does not satisfy the acquisition schema: {missing}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SR -- Supply Chain Risk Management")
@allure.story("SR-5 Acquisition Strategies, Tools, and Methods")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("SR-5: Acquisition method rejects untrusted resources -- unknown components are not supplied")
@allure.description(
    "Acquisition strategies bar untrusted sources -- requests for unknown components must not return data."
)
@pytest.mark.compliance
@pytest.mark.nist_sr5
def test_sr5_acquisition_rejects_untrusted_resources(api_base_url: str) -> None:
    untrusted_ids = [99999, 123456, 0]

    with allure.step("Attempt to acquire untrusted (non-existent) components"):
        supplied = []
        for resource_id in untrusted_ids:
            response = requests.get(f"{api_base_url}/users/{resource_id}", timeout=10)
            if response.status_code == 200 and response.json():
                supplied.append({"id": resource_id, "status": response.status_code})

    with allure.step("Assert the acquisition method supplied no untrusted component"):
        if supplied:
            allure.attach(
                f"Untrusted components supplied:\n{supplied}",
                name="SR-5 Untrusted Acquisition",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert (
            not supplied
        ), f"SR-5 FAIL: acquisition method supplied {len(supplied)} untrusted component(s): {supplied}"


@allure.epic("NIST 800-53 Compliance")
@allure.feature("SR -- Supply Chain Risk Management")
@allure.story("SR-5 Acquisition Strategies, Tools, and Methods")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SR-5: Acquisition is repeatable -- the same method yields a consistent component")
@allure.description(
    "Acquisition methods must be deterministic -- repeated acquisition of a component must be consistent."
)
@pytest.mark.compliance
@pytest.mark.nist_sr5
def test_sr5_acquisition_method_is_repeatable(api_base_url: str) -> None:
    with allure.step("Acquire the same component twice through the defined method"):
        first = requests.get(f"{api_base_url}/users/1", timeout=10)
        second = requests.get(f"{api_base_url}/users/1", timeout=10)
        assert first.status_code == 200, f"SR-5 FAIL: first acquisition expected 200, got {first.status_code}"
        assert second.status_code == 200, f"SR-5 FAIL: second acquisition expected 200, got {second.status_code}"

    with allure.step("Assert repeated acquisition yields a consistent component"):
        if first.json() != second.json():
            allure.attach(
                f"First:\n{first.json()}\n\nSecond:\n{second.json()}",
                name="SR-5 Acquisition Drift",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert first.json() == second.json(), "SR-5 FAIL: acquisition method is not repeatable -- component drifted"
