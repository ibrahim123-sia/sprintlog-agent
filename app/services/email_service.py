import smtplib
from email.mime.text import MIMEText
from jinja2 import Template
from pathlib import Path
from app.config import settings

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "eod_email.txt"


def render_email(team_name, recipient_name, date, developer_name, completed_tasks,
                  start_time, end_time, total_hours):
    raw_template = TEMPLATE_PATH.read_text()
    template = Template(raw_template)
    rendered = template.render(
        team_name=team_name,
        recipient_name=recipient_name,
        date=date,
        developer_name=developer_name,
        completed_tasks=completed_tasks,
        start_time=start_time,
        end_time=end_time,
        total_hours=total_hours
    )
    subject_line, body = rendered.split("\n", 1)
    subject = subject_line.replace("Subject: ", "").strip()
    return subject, body.strip()


def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.smtp_user
    msg["To"] = to_email

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)