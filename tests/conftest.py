import pytest


def pytest_addoption(parser):
    parser.addoption('--test-config-file', action='store', dest='TEST_CONFIG_FILE')
    

@pytest.fixture
def config_file(request):
    return request.config.getoption('TEST_CONFIG_FILE')
