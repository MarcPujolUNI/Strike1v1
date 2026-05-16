from datetime import timedelta
from behave import given, when, then
from django.utils import timezone
from django.contrib.auth import get_user_model
from web.models import CounterUser, Match, Country


@when(u'I navigate to the match history page')
def step_impl(context):
    context.browser.visit(context.get_url('web:matches'))


@then(u'I should see a message "{expected_message}"')
def step_impl(context, expected_message):
    empty_cell = context.browser.find_by_css('td.text-footer-text').first
    assert empty_cell, "Empty history cell not found in the table"
    assert expected_message.lower() in empty_cell.text.lower(), f"Expected '{expected_message}', but found '{empty_cell.text}'"


@given(u'The user has "{count:d}" recorded matches on map "{map_name}"')
def step_impl(context, count, map_name):
    user_model = get_user_model()
    user = user_model.objects.get(username="tester")
    counter_user = CounterUser.objects.get(user=user)

    country, _ = Country.objects.get_or_create(country_iso="ES", defaults={"country_name": "Spain"})
    rival, _ = user_model.objects.get_or_create(username="rival_player",
                                                defaults={"email": "rival@strike.com", "user_country": country})
    rival_counter, _ = CounterUser.objects.get_or_create(user=rival, defaults={"score": 1000})

    for i in range(count):
        is_even = i % 2 == 0
        Match.objects.create(
            winner=counter_user if is_even else rival_counter,
            winner_name=counter_user.user.username if is_even else rival_counter.user.username,
            loser=rival_counter if is_even else counter_user,
            loser_name=rival_counter.user.username if is_even else counter_user.user.username,
            score_display="10-7" if is_even else "10-8",
            duration=timedelta(minutes=20),
            date=timezone.now() - timedelta(hours=i)
        )


@then(u'I should see a list of "{expected_count:d}" matches')
def step_impl(context, expected_count):
    match_rows = context.browser.find_by_css('tbody tr')
    assert len(match_rows) == expected_count, f"Expected {expected_count} matches visible, but found {len(match_rows)}"


@then(u'I should see the pagination controls')
def step_impl(context):
    assert context.browser.find_by_xpath(
        "//div[contains(text(), 'PAGE 1 / 2')]"), "Pagination text 'PAGE 1 / 2' not found."
    assert context.browser.find_by_xpath(
        "//div[contains(., 'Total: 12 Matches')]"), "Total matches count indicator not found."
    assert context.browser.find_by_css('a[href="?page=2"]'), "Link button to page 2 (?page=2) not found."
