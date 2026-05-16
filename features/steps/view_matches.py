import time
from datetime import timedelta
from behave import given, then, when
from django.contrib.auth import get_user_model
from django.utils import timezone
from web.models import CounterUser, Country, Match


@when(u'I navigate to the match history page')
def step_impl(context):
    context.browser.visit(context.get_url("web:matches"))
    time.sleep(0.3)


@then(u'I should see a message "{expected_message}"')
def step_impl(context, expected_message):
    time.sleep(0.3)
    empty_cell = context.browser.find_by_css("td.text-footer-text").first
    assert expected_message.lower() in empty_cell.text.lower()


@given(u'The user has "{count:d}" recorded matches on map "{map_name}"')
def step_impl(context, count, map_name):
    user_model = get_user_model()
    user = user_model.objects.get(username="tester")
    counter_user = CounterUser.objects.get(user=user)

    country, _ = Country.objects.get_or_create(
        country_iso="ES", defaults={"country_name": "Spain"}
    )
    rival, _ = user_model.objects.get_or_create(
        username="rival_player",
        defaults={"email": "rival@strike.com", "user_country": country},
    )
    rival_counter, _ = CounterUser.objects.get_or_create(
        user=rival, defaults={"score": 1000}
    )

    for i in range(count):
        is_even = i % 2 == 0
        Match.objects.create(
            winner=counter_user if is_even else rival_counter,
            winner_name=(
                counter_user.user.username
                if is_even
                else rival_counter.user.username
            ),
            loser=rival_counter if is_even else counter_user,
            loser_name=(
                rival_counter.user.username
                if is_even
                else counter_user.user.username
            ),
            score_display="10-7" if is_even else "10-8",
            duration=timedelta(minutes=20),
            date=timezone.now() - timedelta(hours=i),
        )


@then(u'I should see a list of "{expected_count:d}" matches')
def step_impl(context, expected_count):
    time.sleep(0.3)
    match_rows = context.browser.find_by_css("tbody tr")
    assert len(match_rows) == expected_count


@then(u'I should see the pagination controls')
def step_impl(context):
    time.sleep(0.3)
    assert context.browser.find_by_xpath(
        "//div[contains(text(), 'PAGE 1 / 2')]"
    )
    assert context.browser.find_by_xpath(
        "//div[contains(., 'Total: 12 Matches')]"
    )
    assert context.browser.find_by_css('a[href="?page=2"]')
