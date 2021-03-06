import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from fastapi.templating import Jinja2Templates
from models.config import SendGridConfig, EmailSettings
import controllers.email_template as email_template_controler
import controllers.s3 as s3_controller
from models.email_template import EmailTrigger

cfg = SendGridConfig()
email_cfg = EmailSettings()
API_KEY = cfg.sendgrid_api_key

email_templates = Jinja2Templates(directory="static/templates/email")


def send_email(to: str, subject: str, template: str):
    sg = sendgrid.SendGridAPIClient(api_key=API_KEY)
    from_email = Email(cfg.sendgrid_sender)  # Change to your verified sender
    to_email = To(to)  # Change to your recipient
    content = Content("text/html", template)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)


def send_verification_email(email: str, verify_url: str):
    subject = "Please Verify Your Email"
    template = email_templates.get_template("verify.html").render(
        verify_url=verify_url, **email_cfg.dict()
    )
    send_email(email, subject, template)


def send_password_reset_email(email: str, reset_url: str):
    template = email_template_controler.get_email_template_by_trigger(
        EmailTrigger.password_reset.value
    )
    file = s3_controller.download_file(template.object_id)
    print(file)
    subject = "Password Reset"
    template = email_templates.get_template("password_reset.html").render(
        reset_url=reset_url
    )
    # send_email(email, subject, template)
