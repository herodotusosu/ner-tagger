import pytest


def pytest_addoption(parser):
    parser.addoption('--file1', help='The first file to check.', action='store')
    parser.addoption('--col1', help='The column to compare for the first file',
                     action='store')
    parser.addoption('--file2', help='The second file to check.', action='store')
    parser.addoption('--col2', help='The column to compare for the second file',
                     action='store')


@pytest.fixture
def file1(request):
    return request.config.getoption('--file1')


@pytest.fixture
def file2(request):
    return request.config.getoption('--file2')


@pytest.fixture
def column1(request):
    return request.config.getoption('--col1')


@pytest.fixture
def column2(request):
    return request.config.getoption('--col2')
