import pytest


def pytest_addoption(parser):
    parser.addoption('--file1', help='The first file to check.', action='store')
    parser.addoption('--file2', help='The second file to check.', action='store')


@pytest.fixture
def file1(request):
    return request.config.getoption('--file1')


@pytest.fixture
def file2(request):
    return request.config.getoption('--file2')
