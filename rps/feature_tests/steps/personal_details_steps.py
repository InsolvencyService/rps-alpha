from behave import *
from hamcrest import *
from claimants_user_journey import routes
from BeautifulSoup import BeautifulSoup

test_client = routes.app.test_client()


def parse_csrf_token(response):
    # in order to post form data back to the app
    # we need to also send back the csrf token
    page = BeautifulSoup(response.data)
    csrf_token = page.find('input', id='csrf_token')['value']
    return csrf_token


@given('a claimant with the personal details')
def step(context):
    context.form_data = {}
    for row in context.table:
        if row['DETAILS'] == 'date_of_birth':
            context.form_data['date_of_birth'] = row['VALUE'].split('/')
        else:
            context.form_data[row['DETAILS']] = row['VALUE']


@when('enters their details')
def step(context):
    context.response = test_client.post(
        '/claim-redundancy-payment/personal-details/',
        data=context.form_data,
        follow_redirects=False
    )


@then('the claimant should be sent to {url}')
def step(context, url):
    assert_that(context.response.status, is_('302 FOUND'))
    headers = context.response.headers
    redirect_path = headers['Location']
    assert_that(redirect_path, contains_string(url))

@then('they are shown their employee record')
def step(context):
    page = BeautifulSoup(context.response.data)
    assert_that(page.find('h1').text, is_('Your Employee Record'))

@then('they are shown a message telling them to contact their IP')
def step(context):
    page = BeautifulSoup(context.response.data)
    assert_that(page.find('h1').text, is_('No Employee Record Found'))
