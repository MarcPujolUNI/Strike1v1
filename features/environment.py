import re
import os
from unittest.mock import patch, MagicMock
from splinter.browser import Browser

def chrome_browser(headless=True):
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")  # recommended headless mode
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    prefs = {
        "credentials_enable_service": False,  # disable password manager
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return Browser("chrome", options=chrome_options)

def firefox_browser(headless=True):
    return Browser("firefox", headless=headless)

def before_all(context):
    context.browser = chrome_browser(headless=True)
    # Alternatively, use `firefox_browser` and headless=False to see the browser while testing

    # Mock to ask for the request of the flag
    context.mock_requests = patch('requests.get')
    context.mock_get = context.mock_requests.start()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'<svg><rect width="1" height="1"/></svg>'
    context.mock_get.return_value = mock_response

def before_scenario(context, scenario):
    from django.test import LiveServerTestCase
    context.test_case_class = LiveServerTestCase
    context.fixtures = ['country_fixture.json']

def after_all(context):
    if hasattr(context, 'browser') and context.browser:
        context.browser.quit()

    if hasattr(context, 'mock_requests'):
        context.mock_requests.stop()

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    return text

def after_step(context, step):
    if step.status == "failed" and hasattr(context, 'browser'):
        feature = slugify(context.feature.name)
        scenario = slugify(context.scenario.name)
        step_name = slugify(step.name)
        os.makedirs("screenshots", exist_ok=True)
        filename = f"screenshots/{feature}__{scenario}__{step_name}.png"
        try:
            context.browser.driver.save_screenshot(filename)
        except Exception:
            pass