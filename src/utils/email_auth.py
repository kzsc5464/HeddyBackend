import smtplib, ssl
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import settings

context = ssl.create_default_context()

def load_email_template(template_path: str) -> str:
    """이메일 템플릿 파일을 로드합니다."""
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def email(email_id):
    auth_code = ''.join(random.choices('0123456789', k=7))
    # content
    email_form = load_email_template("resource/html/eamil_form.html")
    email_form = email_form.replace("{to_email}", email_id)
    email_form = email_form.replace("{auth_code}", auth_code)
    text = "안녕하세요"
    # header
    message = MIMEMultipart("alternative")
    message["Subject"] = "이메일 인증을 완료해주세요"
    message["From"] = email_id
    message["To"] = settings.EMAILS_FROM_EMAIL
    # add content
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(email_form, "html")
    # set message
    message.attach(part1)
    message.attach(part2)
    # send email
    with smtplib.SMTP_SSL(settings.SMTP_HOST, port=465) as smtp:
        smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        smtp.sendmail(
            settings.EMAILS_FROM_EMAIL,
            settings.EMAILS_FROM_EMAIL,
            message.as_string())
    return auth_code