import logging
import pytest
from reportportal_client import RPLogger
import env


def pytest_addoption(parser):
    """Adds required parameters for Report Portal"""
    parser.addini("rp_api_key", help="Reportportal API Key", default=env.rp_api_key)
    parser.addini("rp_endpoint", help="Reportportal Endpoint", default=env.rp_endpoint)
    parser.addini("rp_project", help="Reportportal Project", default=env.rp_project)
    parser.addini("rp_mode", help="Reportportal Mode", default=env.rp_mode)
    parser.addini("rp_launch", help="Reportportal Launch", default=f"Box:{env.rp_launch}")
    parser.addini(
        "rp_launch_attributes",
        help="Reportportal Launch Attributes",
        default=["Framework:PyTest", f"Env:{env.rp_launch}"],
    )


@pytest.fixture(scope="session", autouse=True)
def rp_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.setLoggerClass(RPLogger)
    env.logger = logger
    return logger


def pytest_collection_modifyitems(items):
    for item in items:
        # Components
        if "gold_image" in item.nodeid:
            item.add_marker(pytest.mark.component("gold_image"))
        if "file_distributor" in item.nodeid:
            item.add_marker(pytest.mark.component("file_distributor"))
        if "file_processor" in item.nodeid:
            item.add_marker(pytest.mark.component("file_processor"))
        if "file_purger" in item.nodeid:
            item.add_marker(pytest.mark.component("file_purger"))
        # Test types
        if "ui_test" in item.nodeid:
            item.add_marker(pytest.mark.type("ui"))
        if "api_test" in item.nodeid:
            item.add_marker(pytest.mark.type("api"))
