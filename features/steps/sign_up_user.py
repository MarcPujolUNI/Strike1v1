import time
from behave import given, when, then
from django.contrib.auth import get_user_model
from web.models import Country, CounterUser

WebUser = get_user_model()

@given('a country exists with id {country_id:d} and name "{name}" and iso "{iso}"')
def step_impl(context, country_id, name, iso):
    Country.objects.get_or_create(
        country_id=country_id,
        defaults={'country_name': name, 'country_iso': iso}
    )

@when('I navigate to the registration page')
def step_impl(context):
    context.browser.visit(context.get_url('signup'))

@when('I fill out the sign up form with data:')
def step_impl(context):
    for row in context.table:
        context.browser.fill('username', row['username'])
        context.browser.fill('email', row['email'])
        context.browser.fill('password1', row['password'])
        context.browser.fill('password2', row['password'])
        context.browser.select('user_country', str(row['user_country']))

@when('I submit the registration form')
def step_impl(context):
    context.browser.find_by_xpath("//button[@type='submit']").first.click()

@then('I should be redirected to the login page')
def step_impl(context):
    current_url = context.browser.url
    assert 'login' in current_url.lower(), f"Expected login page, but current URL is: {current_url}"

@then('A WebUser with username "{username}" should exist in the database')
def step_impl(context, username):
    assert WebUser.objects.filter(username=username).exists()

@then('A CounterUser profile for "{username}" should be automatically initialized')
def step_impl(context, username):
    assert CounterUser.objects.filter(user__username=username).exists()