import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--name", action="store", default="httpbin", help="Name of the kubernetes deployment"
    )


@pytest.fixture
def deployment_name(request):
    return request.config.getoption("--name")