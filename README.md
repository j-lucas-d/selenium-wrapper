# selenium-wrapper

## Purpose

I use this as the basis for writing web page automated tests.

## Wrapper Functions
- init(browser_name, headless, binary)
- open_url()
- get_url()
- text_entry()
- get_text()
- click()
- wait_for_element()
- smart_wait()
- accept_alert()
- get_alert_text()
- click_hold()
- right_click()
- double_click()
- mouse_hover()
- drag_drop()
- keyboard_shortcut()
- scroll_page()
- scroll_to_element()
- page_navigation()
- close()

## Requirements

Firefox and/or Chromium

geckodriver: https://github.com/mozilla/geckodriver/releases

chromedriver: apt-get install chromium-chromedriver OR https://sites.google.com/a/chromium.org/chromedriver/downloads

## Note
1. Selenium is finicky with browser versions. The driver and browser versions must always match
2. Currently only working / tested for Linux with Firefox and Chromium

## Todo

1. Parametrize web() in fixtures.py to test against multiple browsers
2. Add support for Edge
3. Test against chromium
