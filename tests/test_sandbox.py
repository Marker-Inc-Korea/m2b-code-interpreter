# test_sandbox.py is a test file that tests the Sandbox class in m2b_code_interpreter.py.

import pytest
from m2b_code_interpreter import Sandbox, Execution, Logs, Result


@pytest.fixture
def sandbox():
    sbx = Sandbox()
    yield sbx
    sbx.kill()


def test_simple_expression(sandbox):
    code_to_run = """
    'hello e2b!'
    """
    execution = sandbox.run_code(code_to_run)
    expected = Execution(
        text=Result("'hello e2b!'"),
        logs=Logs(stdout=[], stderr=[]),
        error=None,
    )
    assert execution == expected
    # Execution(Results: [Result(hello e2b!)], Logs: Logs(stdout: [], stderr: []), Error: None)


def test_print_statement(sandbox):
    code_to_run = """
    print('hello e2b!')
    """
    execution = sandbox.run_code(code_to_run)
    expected = Execution(
        text=None,
        logs=Logs(stdout=["hello e2b!\n"], stderr=[]),
        error=None,
    )
    assert execution == expected
    # Execution(Results: [], Logs: Logs(stdout: ['hello e2b!\n'], stderr: []), Error: None)


def test_variable_persistence(sandbox):
    code_to_run_1 = """
    x = 10
    y = 20
    """
    execution_1 = sandbox.run_code(code_to_run_1)
    expected_1 = Execution(
        text=None,
        logs=Logs(stdout=[], stderr=[]),
        error=None,
    )
    # assert execution_1.texts == expected_1.texts
    # assert execution_1.logs == expected_1.logs
    # assert execution_1.error == expected_1.error
    assert execution_1 == expected_1
    # Execution(Results: [], Logs: Logs(stdout: [], stderr: []), Error: None)

    code_to_run_2 = """
    x + y
    """
    execution_2 = sandbox.run_code(code_to_run_2)
    expected_2 = Execution(
        text=Result("30"),
        logs=Logs(stdout=[], stderr=[]),
        error=None,
    )
    # assert execution_2.texts == expected_2.texts
    # assert execution_2.logs == expected_2.logs
    # assert execution_2.error == expected_2.error
    assert execution_2 == expected_2
    # Execution(Results: [Result(30)], Logs: Logs(stdout: [], stderr: []), Error: None)


def test_pandas_dataframe(sandbox):
    code_to_run = """
    import pandas as pd

    # Create a DataFrame
    data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35], 'City': ['Seoul', 'Busan', 'Incheon']}
    df = pd.DataFrame(data)

    df
    """
    execution = sandbox.run_code(code_to_run)
    expected = Execution(
        text=Result(
            "      Name  Age     City\n"
            "0    Alice   25    Seoul\n"
            "1      Bob   30    Busan\n"
            "2  Charlie   35  Incheon"
        ),
        logs=Logs(stdout=[], stderr=[]),
        error=None,
    )
    assert execution == expected
