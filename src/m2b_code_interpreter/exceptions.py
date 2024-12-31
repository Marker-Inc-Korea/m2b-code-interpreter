# exceptions.py
class SandboxError(Exception):
    """Custom exception for Sandbox-related errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"SandboxError: {self.message}"
