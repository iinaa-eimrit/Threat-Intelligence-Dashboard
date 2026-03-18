import smtplib
import requests
from email.mime.text import MIMEText

def send_email_alert(to, subject, body, smtp_server, smtp_port, smtp_user, smtp_pass):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [to], msg.as_string())

def send_slack_alert(webhook_url, message):
    requests.post(webhook_url, json={'text': message})

def send_webhook_alert(webhook_url, payload):
    requests.post(webhook_url, json=payload)
