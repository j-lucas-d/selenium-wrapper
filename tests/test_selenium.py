import pytest
from time import sleep


def test_form_button(web):
    """ Verify we can press an <input type=button> with an ID """

    web.open_url("http://localhost:5000/button")
    web.click("button1", "id")
    # web() will fail if button is not found


def test_alert(web):
    """ Verify text in an alert, and the button can be accepted """
    web.open_url("http://localhost:5000/alert")
    text = web.get_alert_text()
    web.accept_alert()
    assert text == "This is an alert"


def test_body_text(web):
    assert_text = "Awesome sauce"
    web.open_url(f"http://localhost:5000/params?value={assert_text}")
    text = web.get_text("text", "id")
    assert text == assert_text
    sleep(3)
