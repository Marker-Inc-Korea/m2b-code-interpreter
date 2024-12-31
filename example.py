from m2b_code_interpreter import Sandbox

sbx = Sandbox()
execution = sbx.run_code("print('hello world')")  # Execute Python inside the sandbox

print(execution.logs.stdout[0])  # hello world\n
