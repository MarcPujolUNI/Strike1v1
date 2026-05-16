import time
from behave import then, when


@when(u'I navigate to the play page')
def step_impl(context):
    context.browser.visit(context.get_url("web:play"))
    time.sleep(0.3)


@then(u'I should see the header "{text}"')
def step_impl(context, text):
    time.sleep(0.3)
    assert context.browser.is_text_present(text)


@then(u'I should see a button with text "{text}"')
def step_impl(context, text):
    time.sleep(0.3)
    button = context.browser.find_by_xpath(
        "//button[contains(translate(., 'match', 'MATCH'), 'MATCH')]"
    ).first
    assert button.visible
    assert text.upper() in button.text.upper()


@then(u'I click on the matchmaking button')
def step_impl(context):
    time.sleep(0.3)
    context.browser.find_by_xpath(
        "//button[contains(translate(., 'match', 'MATCH'), 'MATCH')]"
    ).first.click()
    time.sleep(0.5)
