import string
import unittest
from hamcrest import assert_that, has_item, has_entry, has_items
from mock import patch

import claim_service.api as claims_api
from claim_service.discrepancies import find_discrepancies_in_claim


class TestSummariseClaims(unittest.TestCase):
    @patch('claim_service.api.cabinet_api')
    def test_returns_summary_of_claims(self, mock_cabinet):
        #Given that the database returns some claims.
        employee_information = {
            'employee_national_insurance_number': 'XX223344X',
            'employee_date_of_birth': '01/01/1990',
            'employee_title': 'Mr',
            'employee_surname': 'SURNAME',
            'employee_forenames': 'FORENAMES',
            'employer_name': 'Widgets Inc',
            'employee_basic_weekly_pay': '300.5'
        }

        claimant_information = {
            'nino': 'AB112233Z'
        }

        claimant_information_2 = {
            'nino': 'AB112233X'
        }

        claim_1 = (claimant_information, employee_information)
        claim_2 = (claimant_information_2, employee_information)

        mock_cabinet.get_claims.return_value = [
            claim_1,
            claim_2
        ]

        #When we call summarise claims on the claim service
        claim_summary = claims_api.summarise_claims()

        #Then we should get back a list summarising the claim
        assert_that(claim_summary, has_items(
            has_entry('nino', 'AB112233Z'),
            has_entry('nino', 'AB112233X')
        ))


def _initials(claimant_information):
    initials = None
    forenames = claimant_information.get('forenames')
    if forenames:
        first_letters = [name[0] for name in forenames.split(' ')]
        initials = string.join(first_letters)
    return initials


def summarise_claim(claim):
    claimant_information = claim[0]
    claim_summary = {
        'discrepancy': bool(find_discrepancies_in_claim(claim)),
        'surname': claimant_information.get('surname'),
        'initials': (_initials(claimant_information)),
        'nino': claimant_information.get('nino'),
        'date_of_birth': claimant_information.get('date_of_birth'),
        'date_submitted': claim[2]
    }
    return claim_summary


class TestSummariseClaim(unittest.TestCase):
    def test_summarising_a_claim_with_discrepancies(self):
        #Given that we have a claim
        employee_information = {
            'employee_national_insurance_number': 'XX223344X',
            'employee_date_of_birth': '01/01/1990',
            'employee_title': 'Mr',
            'employee_surname': 'SURNAME',
            'employee_forenames': 'FORENAMES',
            'employer_name': 'Widgets Inc',
            'employee_basic_weekly_pay': '300.5'
        }

        claimant_information = {
            'nino': 'AB112233Z',
            'gross_rate_of_pay': '250.5',
            'surname': 'Rogers',
            'forenames': 'Steve James',
            'date_of_birth': '01/12/1970'
        }

        date_submitted = '01/10/2013'

        claim = (claimant_information, employee_information, date_submitted)

        #When we call summarise claim on the claim service
        claim_summary = summarise_claim(claim)

        #Then we should get back a summary of the claim
        assert_that(claim_summary, has_entry('discrepancy', True))
        assert_that(claim_summary, has_entry('surname', 'Rogers'))
        assert_that(claim_summary, has_entry('initials', 'S J'))
        assert_that(claim_summary, has_entry('date_of_birth', '01/12/1970'))
        assert_that(claim_summary, has_entry('date_submitted', '01/10/2013'))

    def test_summarising_a_claim_with_no_discrepancies(self):
        #Given that we have a claim
        employee_information = {
            'employee_national_insurance_number': 'XX223344X',
            'employee_date_of_birth': '01/01/1990',
            'employee_title': 'Mr',
            'employee_surname': 'SURNAME',
            'employee_forenames': 'FORENAMES',
            'employer_name': 'Widgets Inc',
            'employee_basic_weekly_pay': '250.5'
        }

        claimant_information = {
            'nino': 'AB112233Z',
            'gross_rate_of_pay': '250.5'
        }

        date_submitted = '01/10/2013'

        claim = (claimant_information, employee_information, date_submitted)

        #When we call summarise claim on the claim service
        claim_summary = summarise_claim(claim)

        #Then we should get back a summary of the claim
        assert_that(claim_summary, has_entry('discrepancy', False))