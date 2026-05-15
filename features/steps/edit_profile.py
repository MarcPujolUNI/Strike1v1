import time, os
from behave import given, when, then

from Strike1v1 import settings


@given(u'I am logged in as "{username}" with password "{password}"')
def step_impl(context, username, password):
    context.browser.visit(context.get_url('login'))
    context.browser.fill('username', username)
    context.browser.fill('password', password)
    context.browser.find_by_css('button[type="submit"]').first.click()

@when(u'I navigate to the profile page')
def step_impl(context):
    context.browser.visit(context.get_url('web:profile'))

@when(u'I click on the "{button_text}" button')
def step_impl(context, button_text):
    if "Profile" in button_text:
        context.browser.find_by_id('edit-profile-btn').first.click()
    else:
        context.browser.find_by_id('edit-password-btn').first.click()

@when(u'I fill in the profile username with "{new_username}"')
def step_impl(context, new_username):
    field = context.browser.find_by_name('username').first
    field.clear()
    field.fill(new_username)

@when(u'I fill in the profile email with "{new_email}"')
def step_impl(context, new_email):
    field = context.browser.find_by_name('email').first
    field.clear()
    field.fill(new_email)

@when(u'I select "{map_name}" as my favourite map')
def step_impl(context, map_name):
    context.browser.find_by_name('favourite_map').last.find_by_text(map_name).click()

@when(u'I click the "{button_text}" button')
def step_impl(context, button_text):
    if "Save" in button_text:
        button = context.browser.find_by_css('#save-button-container button').first
    else:
        button = context.browser.find_by_css('#password-save-container button').first
    button.click()

@then(u'I should see a success message "{expected_message}"')
def step_impl(context, expected_message):
    time.sleep(0.5)
    page_text = context.browser.find_by_tag('body').first.text.lower()
    assert expected_message.lower() in page_text

@then(u'the username input should have "{expected_username}"')
def step_impl(context, expected_username):
    assert context.browser.find_by_name('username').first.value == expected_username

@when(u'I fill in the password change form with old "{old_p}" and new "{new_p}"')
def step_impl(context, old_p, new_p):
    context.browser.fill('old_password', old_p)
    context.browser.fill('new_password1', new_p)
    context.browser.fill('new_password2', new_p)


@when(u'I upload a new profile picture asset "{filename}"')
def step_impl(context, filename):
    asset_path = os.path.join(settings.BASE_DIR, 'features', 'steps', 'assets', filename)
    assert os.path.exists(asset_path), f"I didn't find the route: {asset_path}"

    file_input = context.browser.find_by_name('user_image').first
    file_input.type(asset_path)