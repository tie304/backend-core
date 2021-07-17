from depends import get_database

from models.email_template import EmailTemplate
from models.email_template import EmailTemplateValueMap

def create_email_template(template_name: str, fields: list, object_id: str, user_id: str):
    session = get_database()
    email_template = EmailTemplate(template_name=template_name,user_id=user_id, fields=fields, object_id=object_id)
    session.add(email_template)
    session.commit()
    session.refresh(email_template) 
    session.close()
    return email_template

def get_by_id(template_id: int) -> EmailTemplate:
    session = get_database()
    template = session.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
    session.close()
    return template



def create_email_template_mapping():
    pass


