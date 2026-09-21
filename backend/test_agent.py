from backend.harness.agent import Agent


def main():

    agent = Agent()

    task = (
        "Analyze an inspection report "
        "and prepare an approval note."
    )

    result = agent.run(task)

    print("\n==============================")
    print(" AGENT TEST")
    print("==============================")

    print("\nTASK:")
    print(result["task"])

    print("\nPLAN:")

    for index, step in enumerate(
        result["plan"],
        start=1
    ):
        print(f"{index}. {step}")

    print("\nEXECUTION:")

    for item in result["execution"]:

        print(
            f"{item['step']}. "
            f"{item['action']}"
        )

        print(
            f"   → {item['result']}"
        )


if __name__ == "__main__":
    main()