import time
from behave import given, when, then
from django.contrib.auth import get_user_model
from web.models import Country, CounterUser

User = get_user_model()


@given('I am an anonymous user on the landing page')
def step_impl(context):
    context.browser.visit(context.get_url('web:index'))


@given('A WebUser exists with username "{username}" and password "{password}"')
def step_impl(context, username, password):
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, email=f"{username}@gmail.com", password=password)
        spain = Country.objects.filter(country_id=68).first()
        if spain and hasattr(user, 'user_country'):
            user.user_country = spain
            user.save()
        CounterUser.objects.get_or_create(user=user)


@when('I navigate to the login page')
def step_impl(context):
    base_url = context.test.live_server_url
    context.browser.visit(f"{base_url}/accounts/login/")


@when('I fill out the login form with username "{username}" and password "{password}"')
def step_impl(context, username, password):
    context.browser.fill('username', username)
    context.browser.fill('password', password)


@when('I submit the login form')
def step_impl(context):
    context.browser.find_by_css('button[type="submit"]').first.click()


@then('I should be redirected to the landing page')
def step_impl(context):
    base_url = context.test.live_server_url
    assert context.browser.url == f"{base_url}/", \
        f"Expected landing page, but current URL is: {context.browser.url}"


@then('I should see a welcome message or my dashboard')
def step_impl(context):
    assert not context.browser.is_text_present('LOGIN'), "Login button is still present"


@when('I click on the logout button')
def step_impl(context):
    dropdown_trigger = context.browser.find_by_css('#profile-dropdown-container button').first
    assert dropdown_trigger, "No se encontró el botón para abrir el menú de perfil"
    dropdown_trigger.click()

    logout_button = context.browser.find_by_css('#profile-menu button[type="submit"]').first
    assert logout_button, "Logout button not found inside the dropdown menu"
    logout_button.click()


@then('I should see the "Login" and "Sign Up" button again on the header')
def step_impl(context):
    login_link = context.browser.find_by_css('a[href*="/accounts/login/"]')
    signup_link = context.browser.find_by_css('a[href*="/accounts/signup/"]')
    assert not login_link.is_empty() or not signup_link.is_empty(), "Public authentication links not found after logout"