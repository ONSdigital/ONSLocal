from unittest.mock import patch
import pytest
from io import StringIO
from contextlib import redirect_stdout
from Shared.decorators import time_func


@time_func
def sample_function():
    return "Hello, World!"


def test_time_func():
    # Mock time.time to control the start and end times
    with patch('time.time', side_effect=[1, 2]):
        # Capture the output of the print statement
        with StringIO() as buf, redirect_stdout(buf):
            result = sample_function()
            output = buf.getvalue()

    # Assert the function result
    assert result == "Hello, World!"

    # Assert the printed output
    assert "Function 'sample_function' took 1.0000 seconds to execute." in output
