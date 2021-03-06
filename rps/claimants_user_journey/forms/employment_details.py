from datetime import date
from flask_wtf import Form
from wtforms import TextField, RadioField
from wtforms.validators import Length, ValidationError
from claimants_user_journey.forms.custom_field_types import CustomDateField
from claimants_user_journey.forms.validators import CustomDateFieldValidator


class EmploymentDetails(Form):
    job_title = TextField('Job Title', validators=[Length(max=30)])
    _worker_type_options = [
        'Employed',
        'Labour-only Sub-contractor',
        'Agency Worker',
        'Fixed-term contracts worker',
        'Director or Shareholder',
        'Freelance worker',
        'Casual worker',
        'Home worker'
    ]
    type_of_worker = RadioField(
        'What type of worker were you?',
        choices = [
            ('employed', '<strong>Employed</strong></br>You were employed under a contract of employment'),
            ('labour-only sub-contractor', '<strong>Labour-only Sub-contractor</strong></br>You were self employed and paid tax and national insurance on that basis'),
            ('agency worker', '<strong>Agency Worker</strong></br>You were working for the client of an agency'),
            ('fixed term contract', '<strong>Fixed Term Contract</strong></br>Your contract was for a specific period of time i.e. it had an end date'),
            ('director or shareholder', '<strong>Director or Shareholder</strong></br>You were an office holder of the company'),
            ('freelance', '<strong>Freelance</strong></br>You worked for yourself and the business was a client'),
            ('casual worker', '<strong>Casual Worker</strong></br>You worked for the employer as and when required'),
            ('home worker', '<strong>Home Worker</strong></br>You worked from home but attended an office for meetings')
        ],
    )
    start_date = CustomDateField(label="When did you start working for this employer?", validators=[CustomDateFieldValidator()])
    end_date = CustomDateField(label="When did your employment end?", validators=[CustomDateFieldValidator(start_date_field_name='start_date')])
