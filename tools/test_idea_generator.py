import textwrap


def generate_test_ideas(feature_description):
    ideas = {
        "positive_cases": [],
        "negative_cases": [],
        "edge_cases": [],
        "api_checks": [],
        "ui_checks": []
    }

    ideas["positive_cases"].append(
        f"Verify {feature_description} works with valid inputs."
    )

    ideas["negative_cases"].append(
        f"Verify {feature_description} fails with invalid inputs."
    )

    ideas["edge_cases"].append(
        f"Test boundary conditions related to {feature_description}."
    )

    ideas["api_checks"].append(
        f"Validate API responses and status codes related to {feature_description}."
    )

    ideas["ui_checks"].append(
        f"Verify UI elements and user interactions for {feature_description}."
    )

    return ideas


def print_test_plan(feature_description):
    ideas = generate_test_ideas(feature_description)

    print("\nAI-Assisted Test Plan\n")

    for category, tests in ideas.items():
        print(f"\n{category.upper()}:\n")
        for test in tests:
            print(textwrap.fill(f"- {test}", width=80))


if __name__ == "__main__":
    feature = input("Describe the feature to test: ")
    print_test_plan(feature)

    if __name__ == "__main__":
        feature = input("Describe the feature to test: ").strip()

        if not feature:
            print("Please enter a feature description.")
        else:
            print_test_plan(feature)