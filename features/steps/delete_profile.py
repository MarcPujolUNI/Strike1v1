import time
from behave import when, then


@when(u'I click on the delete account trigger button')
def step_impl(context):
    delete_trigger = context.browser.find_by_css('button[onclick="toggleDeleteModal(true)"]').first
    assert delete_trigger, "Delete account trigger button not found"
    delete_trigger.click()


@when(u'I confirm the account deletion inside the modal')
def step_impl(context):
    modal_container = context.browser.find_by_id('delete-modal').first
    assert modal_container, "Delete confirmation modal not found in DOM"

    confirm_button = modal_container.find_by_css('form button[type="submit"]').first
    assert confirm_button, "Confirmation button not found inside modal form"
    confirm_button.click()