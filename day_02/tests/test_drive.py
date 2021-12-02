import pytest

from day_02.source import solve
from helpers import current_path, stream_data


@pytest.fixture
def test_data_stream():
    return stream_data(current_path(__file__))


def test_solve(test_data_stream):
    assert solve(test_data_stream) == 150
