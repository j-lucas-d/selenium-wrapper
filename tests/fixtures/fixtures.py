import pytest
import threading
import sys

sys.path.append(".")  # This puts the root of this repository on the Python path
from test_data import web_server
from src.web_automation import WebAutomation


@pytest.fixture(autouse=True, scope="session")
def start_web_server():
    """ Starts a sample web server """
    t = threading.Thread(target=web_server.app.run)
    t.daemon = True
    t.start()


# TODO: This should be parametrized to test both browsers
@pytest.fixture(scope="function")
def web(request):
    obj = WebAutomation(browser_name="firefox", headless=False)

    def _teardown():
        obj.close()

    request.addfinalizer(_teardown)

    return obj
