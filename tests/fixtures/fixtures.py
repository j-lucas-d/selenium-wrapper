""" Fixtures for testing """
import sys
import threading
import os
import pytest

sys.path.append(".")  # This puts the root of this repository on the Python path
from test_data import web_server  # pylint: disable=wrong-import-position
from src.web_automation import WebAutomation  # pylint: disable=wrong-import-position


@pytest.fixture(autouse=True, scope="session")
def start_web_server():
    """ Starts a sample web server """
    tid = threading.Thread(target=web_server.app.run)
    tid.daemon = True
    tid.start()


@pytest.fixture(scope="function")
def web(request):
    """ Starts the web browser with standard configuration

        Options:
            set "disable_headless" to 1 in the environment to make the browser visible
    """
    headless = True
    if os.environ.get("disable_headless"):
        headless = False

    obj = WebAutomation(browser_name="firefox", headless=headless)

    def _teardown():
        obj.close()

    request.addfinalizer(_teardown)

    return obj
