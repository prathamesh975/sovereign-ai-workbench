import re


class Validator:

    def __init__(self):
        pass

    def validate(
        self,
        output: str,
        document_text: str,
        task: str = ""
    ):
        """
        Validate generated output against the user's task
        and the source document.

        Returns:
        {
            "passed": bool,
            "type": str,
            "issues": list
        }
        """

        issues = []

        # ==================================================
        # 1. Basic output check
        # ==================================================

        if not output or not output.strip():
            return {
                "passed": False,
                "type": "empty_output",
                "issues": [
                    "No output was generated."
                ]
            }

        output_lower = output.lower().strip()
        task_lower = (task or "").lower().strip()

        document_lower = (
            document_text.lower()
            if document_text
            else ""
        )

        # ==================================================
        # 2. Determine task type
        # ==================================================

        if any(
            keyword in task_lower
            for keyword in [
                "approval note",
                "approval",
                "approve"
            ]
        ):
            task_type = "approval"

        elif any(
            keyword in task_lower
            for keyword in [
                "maintenance recommendation",
                "maintenance recommendations",
                "recommendation",
                "recommended action",
                "recommend"
            ]
        ):
            task_type = "recommendation"

        elif any(
            keyword in task_lower
            for keyword in [
                "summarize",
                "summarise",
                "summary"
            ]
        ):
            task_type = "summary"

        elif any(
            keyword in task_lower
            for keyword in [
                "analyze",
                "analyse",
                "analysis"
            ]
        ):
            task_type = "analysis"

        else:
            task_type = "general"

        # ==================================================
        # 3. Task-specific content validation
        # ==================================================

        if task_type == "approval":

            approval_indicators = [
                "approval",
                "maintenance",
                "subject",
                "equipment",
                "inspection",
                "requested approval",
                "recommendation"
            ]

            found_indicators = sum(
                indicator in output_lower
                for indicator in approval_indicators
            )

            if found_indicators < 2:
                issues.append(
                    "Generated output does not appear to contain "
                    "enough approval-note content."
                )

        elif task_type == "recommendation":

            recommendation_indicators = [
                "recommendation",
                "recommended",
                "maintenance",
                "corrective action",
                "action",
                "should",
                "inspection finding"
            ]

            found_indicators = sum(
                indicator in output_lower
                for indicator in recommendation_indicators
            )

            if found_indicators < 2:
                issues.append(
                    "Generated output does not appear to contain "
                    "a maintenance recommendation."
                )

        elif task_type == "summary":

            summary_indicators = [
                "summary",
                "summarize",
                "inspection",
                "findings",
                "key findings",
                "overview",
                "conclusion"
            ]

            found_indicators = sum(
                indicator in output_lower
                for indicator in summary_indicators
            )

            if found_indicators < 1:
                issues.append(
                    "Generated output does not appear to contain "
                    "a meaningful summary."
                )

        elif task_type == "analysis":

            analysis_indicators = [
                "analysis",
                "finding",
                "findings",
                "cause",
                "condition",
                "assessment",
                "observation",
                "conclusion"
            ]

            found_indicators = sum(
                indicator in output_lower
                for indicator in analysis_indicators
            )

            if found_indicators < 1:
                issues.append(
                    "Generated output does not appear to contain "
                    "an analysis."
                )

        # ==================================================
        # 4. Check useful content
        # ==================================================

        words = output.split()

        if len(words) < 10:
            issues.append(
                "Generated output is too short."
            )

        # ==================================================
        # 5. Technical measurement validation
        # ==================================================

        if document_text and document_text.strip():

            measurement_pattern = (
                r"\b\d+(?:\.\d+)?\s*"
                r"(?:mm/s|mm|cm|m|°c|c|kw|mw|bar|psi|rpm|hz|"
                r"v|a|%)\b"
            )

            document_measurements = set(
                re.findall(
                    measurement_pattern,
                    document_lower
                )
            )

            output_measurements = set(
                re.findall(
                    measurement_pattern,
                    output_lower
                )
            )

            suspicious_measurements = (
                output_measurements
                - document_measurements
            )

            if suspicious_measurements:

                issues.append(
                    "Output contains measurements not found "
                    "in the source document: "
                    + ", ".join(
                        sorted(suspicious_measurements)
                    )
                )

        # ==================================================
        # 6. Unsupported approval claims
        # ==================================================

        approval_claim_patterns = [
            r"\bapproval has been granted\b",
            r"\bapproval was granted\b",
            r"\bapproved by management\b",
            r"\bapproved by the department\b",
            r"\bthe request has been approved\b",
            r"\bthe work has been approved\b",
            r"\bmaintenance has been approved\b"
        ]

        source_has_approval = False

        if document_text:

            source_has_approval = any(
                re.search(
                    pattern,
                    document_lower
                )
                for pattern in approval_claim_patterns
            )

        output_has_unsupported_approval = False

        for pattern in approval_claim_patterns:

            if re.search(
                pattern,
                output_lower
            ):
                output_has_unsupported_approval = True
                break

        if (
            output_has_unsupported_approval
            and not source_has_approval
        ):

            issues.append(
                "Output claims that an action has been "
                "approved, but the source document does "
                "not explicitly state that approval was granted."
            )

        # ==================================================
        # 7. Detect obvious empty / generic output
        # ==================================================

        generic_outputs = [
            "unable to process the document",
            "no information available",
            "cannot generate",
            "no output available"
        ]

        if any(
            phrase in output_lower
            for phrase in generic_outputs
        ):

            issues.append(
                "Generated output appears to be incomplete "
                "or generic."
            )

        # ==================================================
        # 8. Final validation result
        # ==================================================

        passed = len(issues) == 0

        return {
            "passed": passed,
            "type": task_type,
            "issues": issues
        }