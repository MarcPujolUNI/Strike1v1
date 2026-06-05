import time
from behave import given, then, when
from django.contrib.auth import get_user_model
from web.models import Country, CounterUser

User = get_user_model()


@given(u'I am an anonymous user on the landing page')
def step_impl(context):
    context.browser.visit(context.get_url("web:index"))
    time.sleep(0.3)


@given(u'A WebUser exists with username "{username}" and password "{password}"')
def step_impl(context, username, password):
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username, email=f"{username}@gmail.com", password=password
        )
        spain = Country.objects.filter(country_id=68).first()
        if spain and hasattr(user, "user_country"):
            user.user_country = spain
            user.save()
        CounterUser.objects.get_or_create(user=user)


@when(u'I navigate to the login page')
def step_impl(context):
    context.browser.visit(f"{context.test.live_server_url}/accounts/login/")
    time.sleep(0.3)


@when(u'I fill out the login form with username "{username}" and password "{password}"')
def step_impl(context, username, password):
    context.browser.fill("username", username)
    context.browser.fill("password", password)


@when(u'I submit the login form')
def step_impl(context):
    context.browser.find_by_css('button[type="submit"]').first.click()
    time.sleep(0.5)


@then(u'I should be redirected to the landing page')
def step_impl(context):
    time.sleep(0.3)
    assert context.browser.url == f"{context.test.live_server_url}/"


@then(u'I should see a welcome message or my dashboard')
def step_impl(context):
    time.sleep(0.3)
    assert not context.browser.is_text_present("LOGIN")


@when(u'I click on the logout button')
def step_impl(context):
    time.sleep(0.2)
    context.browser.find_by_css("#profile-dropdown-container button").first.click()
    time.sleep(0.2)
    context.browser.find_by_css('#profile-menu button[type="submit"]').first.click()
    time.sleep(0.5)


@then(u'I should see the "Login" and "Sign Up" button again on the header')
def step_impl(context):
    time.sleep(0.3)
    login_link = context.browser.find_by_css('a[href*="/accounts/login/"]')
    signup_link = context.browser.find_by_css('a[href*="/accounts/signup/"]')
    assert not login_link.is_empty() or not signup_link.is_empty()
