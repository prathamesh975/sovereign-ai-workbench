from typing import Callable, List


class ExecutionLoop:
    """
    Executes the steps created by the Planner.
    """

    def __init__(self):

        self.history = []

    def execute(
        self,
        plan: List[str],
        step_handler: Callable[[str], str]
    ):

        results = []

        for index, step in enumerate(plan, start=1):

            result = step_handler(step)

            execution_record = {
                "step": index,
                "action": step,
                "result": result
            }

            self.history.append(
                execution_record
            )

            results.append(
                execution_record
            )

        return results

    def get_history(self):

        return self.history