# driver.py contains the driver_program() function that is responsible for executing the code and returning the result. The function reads JSON input from stdin, executes the code, captures stdout and stderr, and then responds with the captured outputs and result in JSON format.


def driver_program():
    import sys
    import json
    from typing import Any
    from traceback import format_exc
    from contextlib import redirect_stdout, redirect_stderr
    from io import StringIO
    from textwrap import dedent

    globals: dict[str, Any] = {}  # Shared state for executed code

    def is_expression(code: str) -> bool:
        """Check if the code is a single expression."""
        try:
            compile(code, "<string>", "eval")
            return True
        except SyntaxError:
            return False

    while True:
        # Read raw input
        raw_input = input()  # Raw JSON input as a string

        # Parse the JSON command
        command = json.loads(raw_input)  # Parse JSON input
        # print(f"[DEBUG] Received command: {command}", file=sys.stderr)  # Log raw input

        # Properly dedent and strip the code
        code = dedent(command.get("code", "")).strip()
        # print(
        #     f"[DEBUG] Dedented and stripped code: {code}", file=sys.stderr
        # )  # Log cleaned code

        if not code:
            print(json.dumps({"error": "No code to execute"}), file=sys.stderr)
            continue

        # Prepare to capture stdout and stderr
        stdout_io, stderr_io = StringIO(), StringIO()
        result = None
        error_name = error_message = traceback = None

        with redirect_stdout(stdout_io), redirect_stderr(stderr_io):
            try:
                # Split code into lines
                lines = code.split("\n")
                last_line = lines[-1].strip() if lines else ""

                if len(lines) > 1 or not is_expression(last_line):
                    # Execute the full block
                    exec(code, globals)
                    # Evaluate the last line if it's not empty
                    if last_line:
                        try:
                            result = eval(last_line, globals)
                        except Exception:
                            result = None
                else:
                    # Evaluate the single-line expression
                    result = eval(last_line, globals)

            except SyntaxError as e:
                result = None
                error_name = "SyntaxError"
                error_message = str(e)
                traceback = format_exc()
            except Exception as e:
                result = None
                error_name = type(e).__name__
                error_message = str(e)
                traceback = format_exc()

        # Respond with captured outputs and result
        response = {
            "stdout": stdout_io.getvalue(),
            "stderr": stderr_io.getvalue(),
            "text": repr(result) if result is not None else None,
            "error": (
                {
                    "name": error_name,
                    "value": error_message,
                    "traceback": traceback,
                }
                if error_name
                else None
            ),
        }
        print(json.dumps(response), flush=True)
