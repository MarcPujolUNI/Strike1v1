import time
from behave import then


@then(u'The navigation link should display "DASHBOARD"')
def step_impl(context):
    time.sleep(0.3)
    link = context.browser.find_by_css("a.nav-link-center").first
    assert "DASHBOARD" in link.text.strip().upper()


@then(u'I should see my competitive status summary')
def step_impl(context):
    time.sleep(0.3)
    assert context.browser.is_text_present("Dashboard - Player: test")
    assert context.browser.is_text_present("TOTAL WINS")
    assert context.browser.is_text_present("TOTAL LOSSES")
    assert context.browser.is_text_present("COMBAT K/D")
