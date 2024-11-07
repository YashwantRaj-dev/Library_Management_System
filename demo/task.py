from celery import Celery
from celery.schedules import crontab
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import time
from models.user import User, Book, BookRequest
from datetime import datetime, timedelta, timezone
from config import app as flask_app  # Import the Flask app correctly
from fpdf import FPDF, HTMLMixin
from html import unescape
import pdfkit
# from weasyprint import HTML

app = Celery('task', broker = 'redis://127.0.0.1:6379')
app.conf.enable_utc = False 
app.conf.timezone = 'Asia/Kolkata'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=17, minute=15),  # Schedule at 5 PM
        send_daily_reminder.s()
    )
    sender.add_periodic_task(
        crontab(hour=17, minute=15, day_of_month='01'),  # Schedule on the first day of each month
        send_monthly_activity_report.s()
    )

@app.task
def send_daily_reminder():
    with flask_app.app_context():
        users = User.query.all()
        for user in users:
            if (user.email.endswith('@gmail.com') or user.email.endswith('.ac.in') or user.email.endswith('.com')) and (user.last_visit is None or user.last_visit.replace(tzinfo=timezone.utc).date() < datetime.now(timezone.utc).date()):
                send_email(user.email, "Daily Reminder", "Please visit the app today!")

def send_email(receiver, subject, message):
    sender = 'yashwantraj159@gmail.com'
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'yashwantraj159@gmail.com'
    smtp_password = 'vzfvpliksmonadwu'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, receiver, msg.as_string())
        
@app.task
def send_monthly_activity_report():
    with flask_app.app_context():
        users = User.query.all()
        for user in users:
            report_html = generate_html_report(user)
            # report_pdf = generate_pdf_report(report_html)
            if (user.email.endswith('@gmail.com') or user.email.endswith('.ac.in')):
                # send_email2(user.email, "Monthly Activity Report", "Please find your monthly activity report attached.", report_pdf)
                send_email(user.email, "Monthly Activity Report", report_html)

def generate_html_report(user):
    # Generate the HTML content for the report
    current_access_books = BookRequest.query.filter_by(user_id=user.id, status='granted').all()
    current_access_titles = [req.book.title for req in current_access_books]
    
    # Get the completed books for the user
    completed_books = BookRequest.query.filter_by(user_id=user.id, is_completed=True).all()
    completed_titles = [req.book.title for req in completed_books]
    
    report_html = f"""
    <html>
        <body>
            <h1>Monthly Activity Report for {user.username}</h1>
            <!-- Add more sections as needed -->
            <h2>No. of Books with Current Access: {len(current_access_titles)}</h2>
            {"<p>" + ", ".join(current_access_titles) + "</p>" if current_access_titles else "<p>No current access</p>"}
            <h2>No. of Books Completed: {len(completed_titles)}</h2>
            {"<p>" + ", ".join(completed_titles) + "</p>" if completed_titles else "<p>No books completed</p>"}
        </body>
    </html>
    """
    return report_html

pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

def generate_pdf_report(report_html):
    pdf_file_path = "sample.pdf" 
    # pdf_file_path = f"/tmp/monthly_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    try:
        pdfkit.from_file(report_html, pdf_file_path, configuration=pdfkit_config)
    except IOError as e:
        print(f"wkhtmltopdf failed: {e}")
        with open("wkhtmltopdf_error.log", "w") as error_log:
            error_log.write(str(e))
        raise
    return pdf_file_path


# def generate_pdf_report(report_html):
#     pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
#     pdf_file_path = f"/tmp/monthly_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
#     pdfkit.from_string(report_html, pdf_file_path, configuration=pdfkit_config)
#     return pdf_file_path

# def generate_pdf_report(report_html):
#     pdf_file_path = f"/tmp/monthly_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
#     HTML(string=report_html).write_pdf(pdf_file_path)
#     return pdf_file_path

def send_email2(receiver, subject, message, attachment_path):
    sender = 'yashwantraj159@gmail.com'
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    with open(attachment_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'yashwantraj159@gmail.com'
    smtp_password = 'vzfvpliksmonadwu'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, receiver, msg.as_string())
        
# class PDF(FPDF, HTMLMixin):
#     def write_html(self, html):
#         super().write_html(html) 
