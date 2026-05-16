import time
from behave import given, then, when
from web.models import Country, Review, WebUser


@given(u'a country "{country_iso}" exists')
def step_impl(context, country_iso):
    Country.objects.get_or_create(
        country_iso=country_iso, defaults={"country_name": "Spain"}
    )


@given(u'a registered user "{username}" exists')
def step_impl(context, username):
    country = Country.objects.first()
    user, created = WebUser.objects.get_or_create(
        username=username,
        email=f"{username}@strike1v1.com",
        defaults={"user_country": country},
    )
    if created:
        user.set_password("securepassword123")
        user.save()


@given(u'I log in as "{username}"')
def step_impl(context, username):
    context.browser.visit(context.get_url("login"))
    context.browser.fill("username", username)
    context.browser.fill("password", "securepassword123")
    context.browser.find_by_css('button[type="submit"]').first.click()
    time.sleep(0.5)


@given(
    u'"{reviewer}" has reviewed "{reviewee}" with title "{title}", rating "{rating}", description "{desc}"'
)
def step_impl(context, reviewer, reviewee, title, rating, desc):
    reviewer_obj = WebUser.objects.get(username=reviewer)
    reviewee_obj = WebUser.objects.get(username=reviewee)
    Review.objects.create(
        reviewer=reviewer_obj,
        reviewer_name=reviewer_obj.username,
        reviewee=reviewee_obj,
        title=title,
        rating=int(rating),
        description=desc,
    )


@when(u'I visit the review page for "{username}"')
def step_impl(context, username):
    url = context.get_url("web:user_reviews_list", username=username)
    context.browser.visit(url)
    time.sleep(0.3)


@when(u'I click to view my review details')
def step_impl(context):
    reviewer = WebUser.objects.get(username="player1")
    reviewee = WebUser.objects.get(username="player2")
    review = Review.objects.get(reviewer=reviewer, reviewee=reviewee)
    detail_url = f"/reviews/{reviewee.username}/{review.pk}/"
    context.browser.visit(context.get_url(detail_url))
    time.sleep(0.3)


@when(u'I visit the review detail page of "{reviewer_name}" on "{reviewee_name}"')
def step_impl(context, reviewer_name, reviewee_name):
    reviewer = WebUser.objects.get(username=reviewer_name)
    reviewee = WebUser.objects.get(username=reviewee_name)
    review = Review.objects.get(reviewer=reviewer, reviewee=reviewee)
    url = f"/reviews/{reviewee.username}/{review.pk}/"
    context.browser.visit(context.get_url(url))
    time.sleep(0.3)


@when(u'I click on "{text}" button')
def step_impl(context, text):
    time.sleep(0.3)
    if text.lower() == "modify":
        context.browser.find_by_css('button[onclick*="edit-mode"]').first.click()
        time.sleep(0.3)
    elif text.lower() == "delete":
        context.browser.find_by_css("#read-mode button.xp-btn-red").first.click()
    else:
        button = context.browser.find_by_text(text).first.click()
        time.sleep(0.3)


@then(u'I see the header "{expected_text}"')
def step_impl(context, expected_text):
    time.sleep(0.3)
    assert context.browser.is_text_present(expected_text)


@then(u'I should see the text "{expected_text}"')
def step_impl(context, expected_text):
    time.sleep(0.3)
    assert context.browser.is_text_present(expected_text)


@then(u'I should not see the option to write a review')
def step_impl(context):
    time.sleep(0.3)
    assert context.browser.is_element_not_present_by_text("+ WRITE A REVIEW")


@then(u'I should not see the "{button_text}" button')
def step_impl(context, button_text):
    time.sleep(0.3)
    assert context.browser.is_element_not_present_by_text(button_text)


@then(u'I should be redirected to the review page of "{username}"')
def step_impl(context, username):
    time.sleep(0.3)
    assert f"/reviews/{username}/" in context.browser.url
