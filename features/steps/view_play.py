from behave import when, then
import time


@when(u'I navigate to the play page')
def step_impl(context):
    context.browser.visit(context.get_url('web:play'))


@then(u'I should see the header "{text}"')
def step_impl(context, text):
    assert context.browser.is_text_present(text, wait_time=5)


@then(u'I should see a button with text "{text}"')
def step_impl(context, text):
    button = context.browser.find_by_xpath("//button[contains(translate(., 'match', 'MATCH'), 'MATCH')]").first
    assert button.visible

    actual_text = button.text.upper()
    expected_text = text.upper()
    assert expected_text in actual_text


@then(u'I click on the matchmaking button')
def step_impl(context):
    context.browser.find_by_xpath("//button[contains(translate(., 'match', 'MATCH'), 'MATCH')]").first.click()