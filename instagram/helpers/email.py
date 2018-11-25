import sendgrid
import os
from sendgrid.helpers.mail import *
import config

config = eval(os.environ['APP_SETTINGS'])

def send_email(from_email, to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(apikey=config.SENDGRID_API_KEY)
    from_email = Email(from_email)
    to_email = Email(to_email)
    subject = subject
    content = Content("text/plain", content)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    # print(response.status_code)
    # print(response.body)
    # print(response.headers)

    return str(response.status_code) == '202'
