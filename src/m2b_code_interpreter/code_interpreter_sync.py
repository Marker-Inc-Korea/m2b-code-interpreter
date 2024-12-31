# code_intepretor_sync.py
import json
import inspect

import modal

from .driver import driver_program
from .exceptions import SandboxError
from .models import Execution, Logs, Result


class Sandbox:
    def __init__(self):
        try:
            driver_program_text = inspect.getsource(driver_program)
            driver_program_command = f"{driver_program_text}\ndriver_program()"
            self.sandbox = modal.Sandbox.create(
                image=modal.Image.debian_slim().pip_install("pandas"),
                app=modal.App.lookup("e2b-style", create_if_missing=True),
            )
            self.process = self.sandbox.exec("python", "-c", driver_program_command)
        except Exception as e:
            raise SandboxError(f"Failed to initialize Sandbox: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.kill()

    def run_code(self, code: str) -> Execution:
        try:
            # Send code to the driver program
            self.process.stdin.write(json.dumps({"code": code}))
            self.process.stdin.write("\n")
            self.process.stdin.drain()

            # Read the response from stdout
            response = json.loads(next(iter(self.process.stdout)).strip())

            # Construct the Execution object
            text = Result(response["text"])
            logs = Logs(
                stdout=response["stdout"].splitlines(keepends=True),
                stderr=response["stderr"].splitlines(keepends=True),
            )
            error = response.get("error")

            return Execution(text=text, logs=logs, error=error)
        except Exception as e:
            raise SandboxError(f"Failed to execute code: {e}")

    def kill(self):
        try:
            if self.sandbox:
                self.sandbox.terminate()
        except Exception as e:
            raise SandboxError(f"Failed to terminate Sandbox: {e}")
