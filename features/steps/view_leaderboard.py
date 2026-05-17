import time
from behave import given, then, when
from django.contrib.auth import get_user_model
from web.models import CounterUser, Country

User = get_user_model()


@given(u'the following countries exist:')
def step_impl(context):
    for row in context.table:
        Country.objects.update_or_create(
            country_iso=row["country_iso"],
            defaults={
                "country_name": row["country_name"],
                "flag_image": f"country_flags/{row['country_iso']}.png",
            },
        )


@given(u'the following players exist with scores:')
def step_impl(context):
    for row in context.table:
        country = Country.objects.get(country_iso=row["country_iso"])
        user, created = User.objects.get_or_create(
            username=row["username"],
            defaults={
                "email": f"{row['username']}@gmail.com",
                "user_country": country,
            },
        )
        if created:
            user.set_password("pass123")
            user.save()

        stats, _ = CounterUser.objects.get_or_create(user=user)
        stats.score = int(row["score"])
        stats.save()


@when(u'I navigate to the leaderboard page')
def step_impl(context):
    context.browser.visit(context.get_url("web:leaderboard"))
    time.sleep(0.3)


@when(u'I filter the leaderboard by country "{country_name}"')
def step_impl(context, country_name):
    search_input = context.browser.find_by_css('#country-ajax-input').first
    search_input.fill(country_name)

    time.sleep(0.6)

    context.browser.is_element_present_by_css('#country-ajax-results div', wait_time=3)
    results = context.browser.find_by_css('#country-ajax-results div')
    results.first.click()

    apply_btn = context.browser.find_by_css('#submit-country-search-btn').first
    apply_btn.click()

    time.sleep(0.5)


@then(u'I should see "LEADERBOARD" in the header')
def step_impl(context):
    time.sleep(0.3)
    assert context.browser.is_text_present("LEADERBOARD")


@then(u'the players should be listed in this order:')
def step_impl(context):
    time.sleep(0.3)
    elements = context.browser.find_by_css('span[data-testid="player-name"]')
    actual_names = [
        el.text.strip().lower() for el in elements if el.text.strip()
    ]
    expected_names = [row["username"].lower() for row in context.table]

    assert len(actual_names) >= len(expected_names)
    for i, name in enumerate(expected_names):
        assert actual_names[i] == name


@then(u'I should not see "{username}"')
def step_impl(context, username):
    time.sleep(0.3)
    assert not context.browser.is_text_present(username)
