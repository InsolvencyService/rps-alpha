from datetime import date
import re
from wtforms import TextField, Form, SelectField, ValidationError, Field
from wtforms.validators import AnyOf, DataRequired
from wtforms.widgets.core import HTMLString
from claimants_user_journey.forms.validators import DateOfBirthValidator, RequiredIfFieldHasValue, convert_string_to_date


class CurrencyField(TextField):
    """This is a subtype of the WTForm Text field which appends
    a pound-sign to the html.

    It does this as a monkey patch to the wtform.
    """
    def __call__(self, **kwargs):
        """See the depths of the __call__ method in Field
        to understand what is going on.
        """
        html = '&pound;' + self.widget(self, **kwargs)
        return HTMLString(html)

def blank_and_number_range_tuples(min, max_plus_one):
    lst = [('','')]
    lst += [(str(x), str(x)) for x in xrange(min, max_plus_one)]
    return lst


class CustomDateWidget(object):
    def __init__(self, error_class=u'has_errors'):
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)

        if type(field.data) == list and len(field.data) == 3:
            date_parts = field.data
        else:
            date_parts = ['','','']

        #Day drop down list
        html = ["<select id=\"%s-day\" name=\"%s\">" % (field.id, field.name)]
        for x in xrange(0, 32):
            if x == 0:
                val = ""
            else:
                val = str(x)

            if val == date_parts[0]:
                html.append("<option value=\"%s\" selected>%s</option>" % (val, val))
            else:
                html.append("<option value=\"%s\">%s</option>" % (val, val))
        html.append('</select>')

        #Month drop down list
        month_options = (
            '',
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December'
        )
        html.append("<select id=\"%s-month\" name=\"%s\">" % (field.id, field.name))
        for form_val, user_val in enumerate(month_options):
            if str(form_val) == date_parts[1]:
                html.append("<option value=\"%s\" selected>%s</option>" % (form_val, user_val))
            else:
                html.append("<option value=\"%s\">%s</option>" % (form_val, user_val))
        html.append('</select>')

        #Year text field
        html.append("<input id=\"%s-year\" name=\"%s\" type=\"text\" value=\"%s\">" % (field.id, field.name, date_parts[2]))

        return HTMLString(''.join(html))


class CustomDateField(Field):
    widget = CustomDateWidget()

    def _value(self):
        if self.data:
            return self.data
        else:
            return ['','','']

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist
        else:
            self.data = ['', '', '']
