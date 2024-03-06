import pytest

from src.config import config


@pytest.fixture
def get_data():
    return config()


def test_config(get_data):
    params = config()
    assert get_data == params
