import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configuration as conf


def _create_message(receiver, subject, body):
    message = MIMEMultipart()
    message['From'] = conf.sender
    message['To'] = receiver
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(body, 'plain'))

    return message


def _add_attachment(msg, filename):
    with open(filename, 'rb') as attachment:
        # The content type 'application/octet-stream' means that a MIME
        # attachment is a binary file
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    # Encode to base64
    encoders.encode_base64(part)

    # Add header
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= "{filename}"',
    )

    # Add attachment to your message
    msg.attach(part)


def _send(msg):
    with smtplib.SMTP(conf.smtp_server, conf.smtp_port) as s:
        s.starttls()
        s.ehlo()
        s.login(conf.user, conf.password)
        s.send_message(msg)


def send_mail_with_attachment(receiver, attachment, subject, body):
    msg = _create_message(receiver, subject, body)
    _add_attachment(msg, attachment)
    _send(msg)

def send_mail(receiver, subject, body):
    msg = _create_message(receiver, subject, body)
    _send(msg)
