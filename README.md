# m2b-code-interpreter: E2B-Style Sandbox using Modal

[EXPERIMENTAL] `m2b-code-interpreter` is a Python package that replicates the E2B sandbox experience using Modal's robust sandboxing infrastructure. It provides a stateful, isolated environment for executing Python code, allowing for persistent variable states across executions.


## Features

- **Stateful Code Execution**: Variables and states persist across multiple code executions.
- **E2B-Style Interface**: Access outputs (`logs.stdout`) and evaluation results (`text`) seamlessly.
- **Secure Environment**: Executes code in a Modal sandbox for isolation and safety.


## Quickstart

1. Create a Sandbox
```python
from m2b_code_interpreter import Sandbox

# Initialize the sandbox
sbx = Sandbox()

# Run some code
execution = sbx.run_code("print('hello world')")

print(execution.logs.stdout[0])  # hello world\n

# Clean up the sandbox
sandbox.kill()
```

2. Stateful Execution
```python
# Run multiple pieces of code while maintaining state
sandbox.run_code("x = 10")
sandbox.run_code("y = 20")
execution = sandbox.run_code("x + y")
print(execution.text)  # 30
```

3. Connect to OpenAI
```python
# pip install openai m2b-code-interpreter
from openai import OpenAI
from m2b_code_interpreter import Sandbox

# Create OpenAI client
client = OpenAI()
system = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."
prompt = "Calculate how many r's are in the word 'strawberry'"

# Send messages to OpenAI API
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ],
)

# Extract the code from the response
code = response.choices[0].message.content

# Execute code in M2B Sandbox
if code:
    with Sandbox() as sandbox:
        execution = sandbox.run_code(code)
        result = execution.text

    print(result)  # 3

```

## Integration with Modal

`m2b-code-interpreter` leverages Modal’s sandbox API. Ensure you have Modal set up and properly configured.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Before use

`m2b-code-interpreter` does not provide all the features of e2b's code interpreter, and Modal's Sandbox does not behave the same as e2b's implementation of Sandbox(jupyter-like execution). You can try out simple examples, but be aware that this package is experimental and not intended to replace e2b.

## Acknowledgements
- E2B: Inspiration for the interface design.
- Modal: Underlying sandboxing technology.

## Contact

For questions or feedback, please contact here.
