""" Performs web page automation either in a visible browser, or a headless one (invisible) """

import logging
from time import time, sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions


class WebAutomation:
    def __init__(self, browser_name="firefox", headless=False, executable=None):
        """ Returns browser object with which to interface
            
            Args:
                browser_name (str): "firefox" or "chrome"
                headless (bool): True = Do not show browser; False = Show browser during automation
                binary (str): Optional, if set, should be a direct path to the browser executable
        """

        self.browser_name = browser_name.lower()
        self.headless = headless
        self.webdriver_wait = 20  # How long to wait for elements to appear and events to occur in seconds
        self.executable = executable
        self.launch_browser()

    def launch_browser(self):
        """ Launch browser and create instance. Sets self.selenium_driver """

        try:
            # Chrome
            if self.browser_name == "chrome":
                self.start_chrome()

            # Firefox
            elif self.browser_name == "firefox":
                self.start_firefox()
        except:
            logging.error("Error starting web browser")
            raise

    def start_chrome(self):
        """ Configure and start Chrome """

        # Setup browser options
        options = webdriver.chrome.options.Options()  # Create options object
        options.add_argument(
            "--disable-extensions"
        )  # Don't want user's extensions interfering
        options.add_argument("--no-sandbox")  # Set sandbox argument

        # Enable headless operation if desired
        if self.headless:
            options.add_argument(
                "--headless"
            )

        # If user specifies an exact location, use it instead of the $PATH variable
        if self.executable:
            options.binary_location = (
                self.executable
            )

        # Set Capabilities
        cap = webdriver.common.desired_capabilities.DesiredCapabilities.CHROME
        cap["loggingPrefs"] = {"browser": "ALL"}

        # Create instance
        self.selenium_driver = webdriver.Chrome(options=options, desired_capabilities=cap)  # Create instance
        self.selenium_driver.implicitly_wait(self.webdriver_wait)  # Sets wait time
        self.selenium_driver.maximize_window()  # Maximize window

    def start_firefox(self):
        """ Configure and start Firefox """

        # Setup browser options
        options = webdriver.firefox.options.Options()  # Create options object
        options.add_argument(
            "--safe-mode"
        )  # Don't want user's extensions interfering

        # Enable headless operation if desired
        if self.headless:
            options.add_argument("--headless")

        # Create instance
        try:
            # If user specifies an exact location, use it instead of the $PATH variable
            self.selenium_driver = webdriver.Firefox(options=options, firefox_binary=self.executable)
        except exceptions.WebDriverException:
            logging.error(
                "Error creating Selenium driver. Your web browser or browser driver may be out of date. Updating both should fix this.")
            raise
        self.selenium_driver.implicitly_wait(self.webdriver_wait)
        self.selenium_driver.maximize_window()

    def _find_element(self, element_id, element_type):
        """ When provided an identifier, returns the element object which can be used by Selenium functions

            Exits with an exception if not found within the self.webdriver_wait timeout.

            Args:
                element_id (str): Name/ID/XPATH/etc of element
                element_type (str): Valid element type (see path_types below)

            Returns:
                element object
        """

        # Get object for the provided identifier
        path_types = {
            "id": self.selenium_driver.find_element_by_id,
            "xpath": self.selenium_driver.find_element_by_xpath,
            "link text": self.selenium_driver.find_element_by_link_text,
            "partial link text": self.selenium_driver.find_element_by_partial_link_text,
            "name": self.selenium_driver.find_element_by_name,
            "class name": self.selenium_driver.find_element_by_class_name,
            "css selector": self.selenium_driver.find_element_by_css_selector,
            "tag name": self.selenium_driver.find_element_by_tag_name
        }

        assert element_type in path_types, "Invalid element type provided"  # Notify about user error
        element = path_types[element_type](element_id)  # Get element object
        assert element is not None, "Element was not found. Likely does not exist on Web Page."
        return element

    ####################################################################

    def wait_for_element(self, element_id, element_type, timeout=None):
        """ Wait until element appears, or timeout reached

            Args:
                element_id (str): Name/ID/XPATH/etc of element
                element_type (str): If None, we will try to automatically determine the type of element
                timeout (int): If set, driver wait is changed temporarily to "timeout". Time is in seconds

            Returns:
                True if element exists, False if not after the timeout has been reached
        """

        # Change driver wait, if user requests it
        if timeout:
            self.selenium_driver.implicitly_wait(timeout)  # Sets wait time

        # Try to access the element, and wait until it's found or timeout occurs
        try:
            result = True
            self._find_element(element_id, element_type)  # Use implicitly_wait()
        except:
            result = False
        finally:
            # Reset the wait time to default
            self.selenium_driver.implicitly_wait(self.webdriver_wait)  # Sets wait time

        return result  # Return True/False

    def wait_for_element_removal(self, element_id, element_type, timeout=20):
        """ Wait until element appears, or timeout reached

            Args:
                element_id (str): Name/ID/XPATH/etc of element
                element_type (str): If None, we will try to automatically determine the type of element
                timeout (int): If set, driver wait is changed temporarily to "timeout". Time is in seconds

            Returns:
                True if element does NOT exist
        """

        # Sets wait time to minimum, so we don't waste time after the element's removal
        self.selenium_driver.implicitly_wait(1)

        # Try to access the element, and wait until it's found or timeout occurs
        result = True
        etime = time() + timeout
        while result:
            result = self.wait_for_element(element_id, element_type, timeout=1)  # Check for elements existence
            if result:
                sleep(1)
                if time() > etime:  # Timeout reached
                    break

        # Reverse result, to make it more obvious that the test was successful
        result = [True, False][result]

        # Reset to default wait time
        self.selenium_driver.implicitly_wait(self.webdriver_wait)

        return result  # Return True/False

    def smart_wait(self, url=None, is_in=None):
        """ Wait for element to become visible

            Available Conditions: https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html

            "wait" instance creates an exception if it fails to find the specified parameter

            Args (must pick only one):
                url (str): Waits for URL to change
                is_in (str): Waits until URL contains the provided string
        """

        # Set time to wait, using default wait time
        wait = WebDriverWait(self.selenium_driver, self.webdriver_wait)

        # Wait depending on which type user selected
        if url:
            wait.until(EC.url_changes(url))
        if is_in:
            wait.until(EC.url_contains(is_in))

    def open_url(self, url):
        """ Go to URL in browser, and wait for page to load per the self.webdriver_wait time """
        self.selenium_driver.get(url)

    def text_entry(self, text, element_id, element_type):
        """ Enter text into a text box

            Args:
                text (string): text to enter into the text box
                element_id (string): Name/ID/XPATH/etc of element
                element_type (string): When None, searches every element type, but is not recommended.
                                       Set it to the type you expect. Eg: "id"
        """

        element = self._find_element(element_id, element_type)  # Get element object
        element.click()  # Set focus
        element.clear()  # Remove any existing text
        element.send_keys(text)  # Enter text

    def click(self, element_id, element_type):
        """ Click on anything which has an identifiable name

            Args:
                element_id (string): Name/ID/XPATH/etc of element
                element_type (string): When None, searches every element type, but is not recommended.
                                       Set it to the type you expect. Eg: "id"
        """

        element = self._find_element(element_id, element_type)  # Get element object
        element.click()  # Click on object

    def get_text(self, element_id, element_type):
        """ Retrieves text from a tag or textbox and returns it """
        element = self._find_element(element_id, element_type)  # Get element object
        value = element.get_attribute("value")  # Try to read as a textbox first, produces None if not a textbox
        if value is None:
            return element.text  # Should be a tag, so return it's text
        return value

    def get_url(self):
        """ Return the current URL from the address bar

            Returns:
                URL (string)
        """
        return self.selenium_driver.current_url

    def accept_alert(self):
        """ Accept an alert """
        alert = self.selenium_driver.switch_to.alert
        alert.accept()

    def get_alert_text(self):
        """ Return text from an alert """
        alert = self.selenium_driver.switch_to.alert
        return alert.text

    def click_hold(self, element_id, element_type):
        """ Left click and hold - UNTESTED """
        element = self._find_element(element_id, element_type)  # Get element object
        action = ActionChains(self.selenium_driver).click_and_hold(element)
        action.perform()

    def right_click(self, element_id, element_type):
        """ Right (context) click - UNTESTED """
        element = self._find_element(element_id, element_type)  # Get element object
        action = ActionChains(self.selenium_driver).context_click(element)
        action.perform()

    def double_click(self, element_id, element_type):
        """ Double left click - UNTESTED """
        element = self._find_element(element_id, element_type)  # Get element object
        action = ActionChains(self.selenium_driver).double_click(element)
        action.perform()

    def mouse_hover(self, element_id, element_type):
        """ Hover mouse over element - UNTESTED """
        element = self._find_element(element_id, element_type)  # Get element object
        action = ActionChains(self.selenium_driver).move_to_element(element)
        action.perform()

    def drag_drop(self, src_element_id, src_element_type, dst_element_id, dst_element_type):
        """ Hover mouse over element - UNTESTED """
        src_element = self._find_element(src_element_id, src_element_type)  # Get element object
        dst_element = self._find_element(dst_element_id, dst_element_type)  # Get element object
        action = ActionChains(self.selenium_driver).drag_and_drop(src_element, dst_element)
        action.perform()

    def keyboard_shortcut(self, character, control=False, alt=False, shift=False):
        """ Send any key press - UNTESTED """
        key_combo = ""
        if control:
            key_combo += Keys.CONTROL
        if alt:
            key_combo += Keys.ALT
        if shift:
            key_combo += Keys.SHIFT
        key_combo += character

        self.selenium_driver.find_element_by_tag_name('body').send_keys(key_combo)

    def scroll_page(self):
        """ Scroll web page - UNTESTED """
        window_name = 'window'
        scroll_window = ""
        vertical = 750
        horizontal = 0
        self.selenium_driver.execute_script(f"{window_name}.scrollBy({horizontal}, {vertical})", scroll_window)

    def scroll_to_element(self, element_id, element_type):
        """ Move element until in view - UNTESTED """
        self.mouse_hover(element_id, element_type)

    def page_navigation(self, command):
        """ Various actions outside the web page - UNTESTED """
        if command == 'back':
            self.selenium_driver.back()
        elif command == 'forward':
            self.selenium_driver.forward()
        elif command == 'refresh':
            self.selenium_driver.refresh()

    def close(self):
        """ Shut down the web browser driver. Failure to call this will result in zombie processes """
        self.selenium_driver.close()
