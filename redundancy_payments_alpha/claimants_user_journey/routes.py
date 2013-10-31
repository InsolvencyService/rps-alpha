import json
from flask import Flask, render_template, url_for, session
from werkzeug.utils import redirect
from forms.claimant_contact_details import ClaimantContactDetails


app = Flask(__name__)
app.secret_key = 'something_secure_and_secret'
app.debug = True


def nav_links():
    links = [
        ('Start', url_for('start')),
        ('Personal Details', url_for('personal_details')),
        ('Employment Details', url_for('employment_details')),
    ]
    return links


@app.route('/_status', methods=['GET'])
def status():
    return "everything is ok"


@app.route('/claim-redundancy-payment', methods=['GET'])
def claim_redundancy_payment():
    return redirect(url_for('start'))


@app.route('/claim-redundancy-payment/start')
def start():
    return render_template('start.html', nav_links=nav_links())


@app.route('/claim-redundancy-payment/personal-details', methods=['GET', 'POST'])
def personal_details():
    form = ClaimantContactDetails()
    if form.validate_on_submit():
        session['user_details'] = form.data
        return redirect(url_for('employment_details'))
    return render_template('user_details.html', form=form, nav_links=nav_links())


@app.route('/claim-redundancy-payment/employment-details', methods=['GET'])
def employment_details():
    return render_template('employment_details.html', nav_links=nav_links())


@app.route('/claim-redundancy-payment/done', methods=['GET'])
def done():
    user_details_json = json.dumps(session.get('user_details'))
    return render_template('done.html', user_details=user_details_json, nav_links=nav_links())

