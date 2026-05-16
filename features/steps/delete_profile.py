import time
from behave import when


@when(u'I click on the delete account trigger button')
def step_impl(context):
    time.sleep(0.3)
    button = context.browser.find_by_css('button[onclick="toggleDeleteModal(true)"]').first
    button.click()


@when(u'I confirm the account deletion inside the modal')
def step_impl(context):
    time.sleep(0.3)
    button = context.browser.find_by_css('#delete-modal form button[type="submit"]').first
    button.click()
