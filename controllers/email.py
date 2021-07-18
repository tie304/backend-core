import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, BaseLoader

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
    try:
        template = email_template_controler.get_email_template_by_trigger(
            EmailTrigger.password_reset
        )
    except ValueError:
        template = f"<a href='{verify_url}'>Click Here To Verify Your Email</a>"
        send_email(email, "Please Verify Your Email.", template)
        return

    data = s3_controller.download_file(template.object_id)
    rtemplate = Environment(loader=BaseLoader()).from_string(data.decode("utf-8"))
    rendered_template = rtemplate.render(
        reset_url=reset_url, **template.field_value_map
    )

    subject = template.email_subject
    send_email(email, subject, rendered_template)


def send_password_reset_email(email: str, reset_url: str):
    try:
        template = email_template_controler.get_email_template_by_trigger(
            EmailTrigger.password_reset
        )
    except ValueError:
        template = f"<a href='{reset_url}'>Click here to reset your password</a>"
        send_email(email, "Password Reset", template)
        return

    data = s3_controller.download_file(template.object_id)

    subject = template.email_subject
    rtemplate = Environment(loader=BaseLoader()).from_string(data.decode("utf-8"))
    rendered_template = rtemplate.render(
        reset_url=reset_url, **template.field_value_map
    )
    send_email(email, subject, rendered_template)
