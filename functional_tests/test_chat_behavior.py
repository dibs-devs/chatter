from channels.testing import ChannelsLiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import time
import os

from .data_setup_for_tests import set_up_data

from django_chatter.models import Room

MAX_WAIT = 5

class ChatterFunctionalTest(ChannelsLiveServerTestCase):
    serve_static = True

    # Not sure why this is still a thing:
    # https://github.com/django/channels/issues/614
    def _pre_setup(self):
        from django.db import connections
        connections.close_all()

        super()._pre_setup()

    def setUp(self):
        set_up_data()

        # To run Chrome in CI environments.
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("window-size=1200x600")
        if (os.environ.get('SELENIUM_VISUAL', None) == '1'):
            self.browser = webdriver.Chrome()
            self.browser.set_window_size(1600, 900)
        else:
            self.browser = webdriver.Chrome(options = chrome_options)

        self.domain_home = 'http://localhost' + ':' + \
                self.live_server_url.split(':')[-1]

    def tearDown(self):
        self.browser.quit()

    def test_get_homepage_url(self):
        print ("test getting homepage and sending message")
        self.browser.get(self.domain_home)
        username_field = self.browser.find_element_by_id('id_username')
        password_field = self.browser.find_element_by_id('id_password')
        send_button = self.browser.find_element_by_css_selector("input[type='submit']")
        username_field.send_keys("user0")
        password_field.send_keys("dummypassword")
        send_button.click()
        self.wait_for(lambda:
            self.assertEqual(
                self.browser.title,
                "Notes to Yourself | Chatter")
        )


    # An explicit wait method that waits for page to fully load before
    # the assertion function it's running passes. Throws exception
    def wait_for(self, function):
        start_time = time.time()
        while True:
            try:
                return function()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
