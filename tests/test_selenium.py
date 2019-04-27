import pytest
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


def test_alert_exists(web):
    """ Verify we can detect an alert popup"""
    web.open_url(f"{HOST}/alert")
    result = web.check_for_alert()  # Alert has to be removed, otherwise the call to close the browser fails
    assert result


def test_alert_does_not_exist(web):
    """ Verify we can detect an alert does not exist"""
    web.open_url(f"{HOST}/")
    result = web.check_for_alert()  # Alert has to be removed, otherwise the call to close the browser fails
    assert not result


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
    assert web.wait_for_element_removal("output", "id")  # Returns true if removed


def test_wait_for_expected_conditions_(web):
    """ Test dynamically waiting for an element to be deleted """
    url = f"{HOST}/remove_element"
    web.open_url(url)
    element = web.wait_for_element_removal("output", "id")  # Returns true if removed
    assert element


def test_click_and_hold(web):
    """ Verify left click and hold on element for specific amount of time """
    time_to_hold = 2
    web.open_url(f"{HOST}/drag")
    web.click_hold(time_to_hold, "block1", "id")
    seconds = float(web.get_text("separator", "id"))  # Read time

    # Verify time down is within range, it is written to an element on the web page
    assert seconds >= time_to_hold < time_to_hold + 1


def test_right_click(web):
    """ Verify Javascript on the web page registers a right click """
    web.open_url(f"{HOST}/keypress")
    web.right_click("right_click", "id")
    verify(web.get_text, ("right_click", "id"), "executed")


def test_double_click(web):
    """ Verify a double click is registered """
    web.open_url(f"{HOST}/keypress")
    web.double_click("double_click", "id")
    verify(web.get_text, ("double_click", "id"), "executed")


def test_mouse_hover(web):
    """ Verify the mouse pointer is moved onto an element """
    web.open_url(f"{HOST}/keypress")
    web.mouse_hover("hover", "id")
    verify(web.get_text, ("hover", "id"), "executed")


def test_drag_drop(web):
    """ Verify an element can be dragged onto another element """
    web.open_url(f"{HOST}/drag")
    web.click("block1", "id")  # Stores the current position in the element
    position1 = int(web.get_text("position", "id"))
    web.drag_drop("block1", "id", "block2", "id")  # Drag to another element
    position2 = int(web.get_text("position", "id"))
    assert position2 > position1


@pytest.mark.xfail(reason="Haven't found way to intercept keypresses in order to verify them")
def test_keyboard_shortcut(web):
    pass


@pytest.mark.parametrize("direction", ["up", "left"])
def test_scroll1(web, direction):
    """ Test scrolling the web page in two directions """
    # Load the page which will be automatically scrolled, if we need to scroll up or left
    pre_scroll = ""
    if direction == "up":
        pre_scroll = "down"
    elif direction == "left":
        pre_scroll = "right"

    web.open_url(f"{HOST}/long?{pre_scroll}")
    web.scroll_page(direction)
    assert int(web.get_text("scroll", "id")) == 0


@pytest.mark.parametrize("direction", ["down", "right"])
def test_scroll2(web, direction):
    """ Test scrolling the web page in two directions """

    web.open_url(f"{HOST}/long")
    web.scroll_page(direction)
    assert int(web.get_text("scroll", "id")) > 0


def test_nav_back(web):
    web.open_url(f"{HOST}/link")  # Link page
    web.click("Go To Root", "link text")  # Root page
    web.page_navigation("back")
    web.click("Go To Root", "link text")  # Verify we're back on the link page. Exception if this link doesn't exist


def test_nav_forward(web):
    web.open_url(f"{HOST}/link")
    web.click("Go To Root", "link text")
    web.page_navigation("back")  # Move back to previous page
    web.page_navigation("forward")  # Move forward, should be back on root page
    verify(web.get_text, ("default", "id"), "Naught, but disappointment thou shalt find within this realm.")


def test_nav_refresh(web):
    """ Verify the web page is refreshed """
    web.open_url(f"{HOST}/drag")
    web.click("block1", "id")  # Stores the current position in the element
    position1 = int(web.get_text("position", "id"))
    web.drag_drop("block1", "id", "block2", "id")  # Drag to another element

    web.page_navigation("refresh")
    web.click("block1", "id")  # Stores the current position in the element
    position2 = int(web.get_text("position", "id"))
    assert position1 == position2  # If page was refreshed, element should be back in original position


@pytest.mark.parametrize("name", ["hor200", "ver200"])
def test_scroll_to_element(web, name):
    """ Verify we can scroll to an element horizontally and vertically """
    web.open_url(f"{HOST}/long")
    web.scroll_to_element(name, "id")
    web.mouse_hover(name, "id")  # Raises exception if element is not visible
