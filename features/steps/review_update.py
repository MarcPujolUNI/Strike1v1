import time
from behave import then, when


@when(
    u'I update the review form with title "{title}", rating "{rating}", and description "{desc}"'
)
def step_impl(context, title, rating, desc):
    time.sleep(0.3)
    context.browser.fill("title", title)
    context.browser.fill("description", desc)
    context.browser.find_by_css(f'#edit-mode span.star-rating[data-value="{rating}"]').first.click()


@when(u'I save the modifications')
def step_impl(context):
    context.browser.find_by_css('#edit-mode button[type="submit"]').first.click()
    time.sleep(0.5)


@then(u'I should see the updated review title "{title}" on the review detail page')
def step_impl(context, title):
    time.sleep(0.3)
    assert context.browser.is_text_present(title.upper())
