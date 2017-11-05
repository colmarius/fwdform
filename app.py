import os
from uuid import uuid4

import sendgrid
from sendgrid.helpers.mail import Mail, Email, Content
from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, abort

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
db = SQLAlchemy(app)


class User(db.Model):

    def __init__(self, email):
        self.email = email
        self.uuid = str(uuid4())

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    uuid = db.Column(db.String(36), unique=True)


def build_email(from_email, subject, to_email, message):
    """Sent email with Sendgrid"""
    mail = Mail(
        from_email=Email(from_email),
        subject=subject,
        to_email=Email(to_email),
        content=Content("text/plain", message)
    )
    return mail


@app.route('/')
def index():
    return redirect('http://colmarius.github.io/fwdform')


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if user:
        return ('Email already registered', 403)
    user = User(email)
    db.session.add(user)
    db.session.commit()
    return "Token: {}".format(user.uuid)


@app.route('/user/<uuid>', methods=['POST'])
def forward(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    if not user:
        return ('User not found', 406)
    mail = build_email(
        from_email=request.form['email'],
        subject=request.form['subject'],
        to_email=user.email,
        message=request.form['message']
    )
    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code != 202:
        abort(500)
    if 'next' in request.form:
        return redirect(request.form['next'])
    return 'Your message was sent successfully'


@app.errorhandler(400)
def bad_parameters(e):
    return ('<p>Missing information. Press the back button to complete '
            'the empty fields.</p><p><i>Developers: we were expecting '
            'the parameters "subject", "email" and "message". You might '
            'also consider using JS validation.</i>', 400)


@app.errorhandler(500)
def error(err):
    return ("Sorry, something went wrong: {}!".format(err), 500)
