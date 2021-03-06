from hamcrest import *
from birmingham_cabinet import api
from claimants_user_journey.routes import app
from BeautifulSoup import BeautifulSoup


@given('the IP has provided the employee details')
def step(context):
    employee_details = {}
    for key, value in context.table:
        employee_details[key] = value
    api.add_rp14a_form(employee_details)
    context.nino = employee_details['employee_national_insurance_number']

def parse_csrf_token(response):
    # in order to post form data back to the app
    # we need to also send back the csrf token
    page = BeautifulSoup(response.data)
    csrf_token = page.find('input', id='csrf_token')['value']
    return csrf_token

@given('the claimant is matched to the employee details')
def step(context):
    context.app = app.test_client()
    get_the_page = context.app.get('/claim-redundancy-payment/personal-details/')
    response = context.app.post(
        '/claim-redundancy-payment/personal-details/',
        data={
            'forenames': 'John',
            'surname': 'Smith',
            'title': 'Mr',
            'other': '',
            'building_number': '0',
            'street': 'Fake Street',
            'district': '9',
            'town_or_city': 'Fake Town',
            'county': 'Not-a-county',
            'postcode': 'XXXXXX',
            'email': 'foo@bar.com',
            'telephone_number': '000000 000 000',
            'nino': context.nino,
            'date_of_birth': [
                '1',
                '2',
                '1983'
            ],
            'csrf_token': parse_csrf_token(get_the_page)
        },
        follow_redirects=True
    )
    assert_that(response.status_code, is_(200))
    page = BeautifulSoup(response.data)
    assert_that(page.find('h1').text, is_('Claim Redundancy Payment'))

@when('the claimant enters the valid wage details')
def step(context):
    wages_details = {}
    for key, value in context.table:
        if key == 'wage_owed_from':
            wages_details[key] = value.split('/')
        elif key == 'wage_owed_to':
            wages_details[key] = value.split('/')
        else:
            wages_details[key] = value

    get_the_page = context.app.get('/claim-redundancy-payment/wage-details/')
    wages_details.update({'csrf_token': parse_csrf_token(get_the_page)})
    response = context.app.post(
        '/claim-redundancy-payment/wage-details/',
        data=wages_details,
        follow_redirects=True
    )
    assert_that(response.status_code, is_(200))
    context.followup_response = response

@when('the claimant enters the valid arrears of pay details')
def step(context):
    arrears_pay_details = {}
    for key, value in context.table:
        if key == 'wage_owed_from':
            arrears_pay_details[key] = value.split('/')
        elif key == 'wage_owed_to':
            arrears_pay_details[key] = value.split('/')
        else:
            arrears_pay_details[key] = value

    get_the_page = context.app.get('/claim-redundancy-payment/wages-owed-details/')
    arrears_pay_details.update({'csrf_token': parse_csrf_token(get_the_page)})
    response = context.app.post(
        '/claim-redundancy-payment/wages-owed-details/',
        data=arrears_pay_details,
        follow_redirects=True
    )
    assert_that(response.status_code, is_(200))
    context.followup_response = response


@then('the claimant should see a discrepancy on wage owed in arrears')
def step(context):
    page = BeautifulSoup(context.followup_response.data)
    assert_that(page.find('h2').text, is_('Please enter details of any unpaid wages'))
    question_element = page.find(id="gross_amount_owed_question")
    assert_that(question_element['class'], contains_string('discrepancy'))


@then('the claimant should see a discrepancy on gross rate of pay')
def step(context):
    discrepancy_html = context.followup_response.data
    page = BeautifulSoup(discrepancy_html)
    assert_that(page.find('h2').text, is_('Please enter your wage details'))
    question_element = page.find(id="gross_rate_of_pay_question")
    assert_that(question_element['class'], contains_string('discrepancy'))


@then('not see a discrepancy on frequency of work')
def step(context):
    discrepancy_html = context.followup_response.data
    page = BeautifulSoup(discrepancy_html)
    question_element = page.find(id="normal_days_of_work_question")
    assert_that(question_element['class'], is_not(contains_string('discrepancy')))

@then('see a call to action box at the top of the screen')
def step(context):
    if context.followup_response:
        discrepancy_html = context.followup_response.data
    page = BeautifulSoup(discrepancy_html)
    call_to_action_elements = page.findAll("div", {"class" : "call-to-action group discrepancy-summary"})
    assert_that(call_to_action_elements, not empty())


@then('the claimant should see the next page of the form')
def step(context):
    page = BeautifulSoup(context.followup_response.data)
    assert_that(page.find('h2').text, contains_string('Please enter details of any unpaid wages'))

@then('the page should not have a call to action box at the top of the screen')
def step(context):
    discrepancy_html = context.response.data
    page = BeautifulSoup(discrepancy_html)
    call_to_action_elements = page.findAll("div", {"class" : "call-to-action group discrepancy-summary"})
    assert_that(call_to_action_elements, empty())


