import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

sender = 'yashwantraj159@gmail.com'
recipient = 'rajyashwant0641@gmail.com'
subject = 'Test email with attachment'
message = 'This is a test email'

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = subject
msg.attach(MIMEText(message))

filename = 'check.py'
path = os.path.join(os.getcwd(), filename)
with open(path, 'rb') as f:
    attachment = MIMEApplication(f.read(),_subtype='pdf')
    attachment.add_header('Content-Disposition','attachment',filename=filename)
    msg.attach(attachment)
    
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'yashwantraj159@gmail.com'
smtp_password = 'vzfvpliksmonadwu'

with smtplib.SMTP(smtp_server,smtp_port) as server:
    server.starttls()
    server.login(smtp_username,smtp_password)
    server.sendmail(sender,recipient,msg.as_string())

#def send_email(sender,receiver,subject,message,attachment):
 
def send_email(sender,receiver,subject,message):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message))
    # filename = attachment
    # path = os.path.join(os.getcwd(),filename)
    # with open(path,'rb') as f:
    #     attachment = MIMEApplication(f.read(),_subtype='pdf')
    #     attachment.add_header('Content-Disposition','attachment',filename=filename)
    #     msg.attach(attachment)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'yashwantraj159@gmail.com'
    smtp_password = 'vzfvpliksmonadwu'

    with smtplib.SMTP(smtp_server,smtp_port) as server:
        server.starttls()
        server.login(smtp_username,smtp_password)
        server.sendmail(sender,receiver,msg.as_string())
