import pytest
import logging
from time import sleep
from tenacity import retry, wait_fixed, stop_after_attempt

"""
    Tests web_automation.py. However, we have to use some of it's functions in order to test other functions.
"""

HOST = "http://localhost:5000"
DEFAULT_VALUE = "default value"


def verify(func, args, expected_result, wait_time=1, attempts=10):
    """ Executes the provided function with arguments, and asserts against the expected result until
        found or times out.

        Args:
            func (obj): Function to execute
            args (tuple): Arguments to pass to function
            expected_result (any): What the function should return
            wait_time (int): Time in seconds to wait between retries
            attempts (int): Number of attempts to assert result
    """

    @retry(wait=wait_fixed(wait_time), stop=stop_after_attempt(attempts))
    def _verify(func, args, expected_result):
        assert func(*args) == expected_result

    _verify(func, args, expected_result)


def verify_standard(web):
    """ Check against standard text output """
    verify(web.get_text, ("output", "id"), "Passed")


def test_click_button(web):
    """ Verify we can press an <input type=button> with an ID """

    web.open_url(f"{HOST}/button")
    web.click("button1", "id")
    verify_standard(web)


def test_alert_text(web):
    """ Verify text in an alert popup """
    text = "This is an alert"
    web.open_url(f"{HOST}/alert")
    verify(web.get_alert_text, (), text)
    web.accept_alert()  # Alert has to be dismissed, otherwise the call to close the browser fails


def test_alert_dismiss(web):
    """ Verify text in an alert popup """
    web.open_url(f"{HOST}/alert")
    web.accept_alert()  # Alert has to be removed, otherwise the call to close the browser fails
    text = "This is an alert"
    verify(web.get_alert_text, (), text)  # !!!!!!need to have a check for NO element exists


def test_body_text(web):
    """ Read text from body """
    assert_text = "Awesome sauce"
    web.open_url(f"{HOST}/params?value={assert_text}")  # This web page will display any text given to it
    verify(web.get_text, ("text", "id"), assert_text)


def test_read_text_from_textbox(web):
    """ Verify we can read text from a textbox """
    web.open_url(f"{HOST}/text_entry")
    verify(web.get_text, ("text1", "id"), DEFAULT_VALUE)


def test_text_entry(web):
    """ Enter text into input text box """
    text = "Zebra"
    web.open_url(f"{HOST}/text_entry")
    web.text_entry(text, "text1", "id")
    verify(web.get_text, ("text1", "id"), text)


def test_get_url(web):
    """ Read URL from address bar """
    url = f"{HOST}/params?value=random_task"
    web.open_url(url)  # This web page will display any text given to it
    verify(web.get_url, (), url)


def test_wait_for_element(web):
    """ Test dynamically waiting for an element to appear """
    url = f"{HOST}/delayed_element"
    web.open_url(url)
    element = web.wait_for_element("output", "id")  # Should return the element's object if found
    assert element


def test_wait_for_element_removal(web):
    """ Test dynamically waiting for an element to be deleted """
    url = f"{HOST}/remove_element"
    web.open_url(url)
    element = web.wait_for_element_removal("output", "id")  # Returns true if removed
    assert element
