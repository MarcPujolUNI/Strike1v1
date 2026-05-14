from behave import when, then

URL_MAP = {
    "Terms of Service": "web:tos",
    "Privacy Policy": "web:privacy",
    "Cookie Policy": "web:cookies"
}

def assert_text_in_page(context, text):
    page_text = context.browser.find_by_tag('body').text.upper()
    assert text.upper() in page_text, f"Expected text '{text}' not found (searched as '{text.upper()}')"

@when(u'I navigate to the "{page_name}" page')
def step_impl(context, page_name):
    url_name = URL_MAP.get(page_name)
    context.browser.visit(context.get_url(url_name))

@then(u'I should see "{text}" in the title')
def step_impl(context, text):
    assert_text_in_page(context, text)

@then(u'I should see the educational disclaimer')
def step_impl(context):
    assert_text_in_page(context, "EDUCATIONAL")
    assert_text_in_page(context, "DISCLAIMER")
    assert_text_in_page(context, "TECHNICAL DEMONSTRATION")

@then(u'I should see how academic data is handled')
def step_impl(context):
    assert_text_in_page(context, "DATA HANDLING")
    assert_text_in_page(context, "ACADEMIC BEST PRACTICES")
    assert_text_in_page(context, "THIRD-PARTY")

@then(u'I should see information about session tokens')
def step_impl(context):
    assert_text_in_page(context, "SESSION TOKENS")
    assert_text_in_page(context, "CSRF PROTECTION")
    assert_text_in_page(context, "STRICTLY NECESSARY")