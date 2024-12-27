from pydoc import plain

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.v1.router import api_router
from core.database import MongoDB

app = FastAPI(**settings.fastapi_kwargs)

# Setup CORS middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# @app.on_event("startup")
# async def startup_db_client():
#     """Database connection on startup."""
#     await MongoDB.connect_to_database()
#
#
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     """Database disconnection on shutdown."""
#     await MongoDB.close_database_connection()
#

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Heddy Backend API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        db = MongoDB.get_db()
        await db.command('ping')
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": str(e)
        }

from email import contentmanager
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# settings.SMTP_HOST
# settings.SMTP_USER
# settings.SMTP_PASSWORD
# settings.EMAILS_FROM_EMAIL
# settings.EMAILS_FROM_NAME

context = ssl.create_default_context()

def load_email_template(template_path: str) -> str:
    """이메일 템플릿 파일을 로드합니다."""
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()

def email():
    # content
    auth_code = "1798399"
    email_form = load_email_template("resource/html/eamil_form.html")
    email_form = email_form.replace("{auth_code}", auth_code)
    text = "안녕하세요"
    # header
    message = MIMEMultipart("alternative")
    message["Subject"] = "이메일 인증을 완료해주세요"
    message["From"] = "heddy@heddy.com"
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

if __name__ == "__main__":
    email()
