from behave import then


@then('The navigation link should display "DASHBOARD"')
def step_impl(context):
    context.browser.is_element_present_by_css('a.nav-link-center')
    assert context.browser.find_by_css('a.nav-link-center').first.text == "DASHBOARD"


@then('I should see my competitive status summary')
def step_impl(context):
    assert context.browser.is_text_present('Dashboard - Player: test')
    assert context.browser.is_text_present('TOTAL WINS')
    assert context.browser.is_text_present('TOTAL LOSSES')
    assert context.browser.is_text_present('COMBAT K/D')