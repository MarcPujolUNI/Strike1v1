import time
from behave import then, when


@when(u'I confirm the deletion by clicking "Yes, Delete Review" button')
def step_impl(context):
    time.sleep(0.3)
    button = context.browser.find_by_css('#delete-modal form button[type="submit"]').first
    button.click()


@then(u'I should not see "{text}" in the reviews list')
def step_impl(context, text):
    time.sleep(0.3)
    assert context.browser.is_text_not_present(text)
