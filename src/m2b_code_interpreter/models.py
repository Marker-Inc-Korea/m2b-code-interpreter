from typing import List, Optional


class Result:
    def __init__(self, value: Optional[str]):
        self.value = value

    def __repr__(self):
        return f"Result({self.value})" if self.value is not None else "Result(None)"

    def __eq__(self, other):
        if isinstance(other, Result):
            # Normalize strings to avoid single vs double quote mismatches
            if isinstance(self.value, str) and isinstance(other.value, str):
                return self.value.strip("'\"") == other.value.strip("'\"")
            # For non-strings, fall back to direct comparison
            return self.value == other.value
        return False


class Logs:
    def __init__(self, stdout: List[str], stderr: List[str]):
        self.stdout = stdout
        self.stderr = stderr

    def normalize_output(self, output: List[str]) -> List[str]:
        """Remove trailing whitespace and deduplicate consecutive entries."""
        return [line.rstrip() for line in output if line.strip()]

    def __repr__(self):
        return f"Logs(stdout: {self.stdout}, stderr: {self.stderr})"

    def __eq__(self, other):
        if isinstance(other, Logs):
            return self.normalize_output(self.stdout) == self.normalize_output(
                other.stdout
            ) and self.normalize_output(self.stderr) == self.normalize_output(
                other.stderr
            )
        return False


class Execution:
    def __init__(self, text: Optional[Result], logs: Logs, error: Optional[dict]):
        self.texts = [text] if text is not None and text.value is not None else []
        self.text = text.value if text is not None else None
        self.logs = logs
        self.error = (
            f"ExecutionError(name='{error['name']}', value='{error['value']}', "
            f"traceback='{error['traceback']}')"
            if error
            else None
        )

    def __repr__(self):
        return (
            f"Execution(Results: {self.texts}, Logs: {self.logs}, Error: {self.error})"
        )

    def __eq__(self, other):
        if isinstance(other, Execution):
            return (
                self.texts == other.texts
                and self.logs == other.logs
                and self.error == other.error
            )
        return False
