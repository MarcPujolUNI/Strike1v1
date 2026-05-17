import time
from behave import then, when


@when(u'I click the write a review button')
def step_impl(context):
    time.sleep(0.3)
    context.browser.find_by_css(".xp-btn-blue").first.click()
    time.sleep(0.5)


@when(u'I fill in the review form with title "{title}", rating "{rating}", and description "{desc}"')
def step_impl(context, title, rating, desc):
    context.browser.fill("title", title)
    context.browser.fill("description", desc)
    context.browser.find_by_css(f'span.star-rating[data-value="{rating}"]').first.click()


@when(u'I submit the review form')
def step_impl(context):
    context.browser.find_by_css('#review-form-container button[type="submit"]').first.click()
    time.sleep(0.5)


@then(u'I should see my review with title "{expected_title}" in the "Your review" section')
def step_impl(context, expected_title):
    time.sleep(0.3)
    assert context.browser.is_text_present(
        "YOUR REVIEW"
    ) or context.browser.is_text_present("Your Review")
    assert context.browser.is_text_present(
        expected_title
    ) or context.browser.is_text_present(expected_title.upper())
