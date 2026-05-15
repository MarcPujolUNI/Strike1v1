from behave import then


@then('The navigation link should display "DASHBOARD"')
def step_impl(context):
    context.browser.is_element_present_by_css('a.nav-link-center', wait_time=5)
    link = context.browser.find_by_css('a.nav-link-center').first
    actual_text = link.text.strip().upper()
    assert "DASHBOARD" in actual_text, f"No se encontró 'DASHBOARD' en el texto: '{actual_text}'"

@then('I should see my competitive status summary')
def step_impl(context):
    assert context.browser.is_text_present('Dashboard - Player: test')
    assert context.browser.is_text_present('TOTAL WINS')
    assert context.browser.is_text_present('TOTAL LOSSES')
    assert context.browser.is_text_present('COMBAT K/D')