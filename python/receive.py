import smtplib
import time
import imaplib
import email
import os
import configuration as conf

class YoutubeMail:
    sender: str
    body: str

    def __init__(self, sender, body):
        self.sender = sender
        self.body = body

def receive_and_delete_mails(subject_filter):
    try:
        mail_list = []
        mail = imaplib.IMAP4_SSL(conf.imap_server, conf.imap_port)
        mail.login(conf.user, conf.password)
        mail.select()
    
        _, msgnums = mail.search(None, 'ALL')
    
        for num in msgnums[0].split():
            _, data = mail.fetch(num, '(RFC822)')
    
            msg = email.message_from_bytes(data[0][1])
            email_subject = msg['subject']
            email_from = msg['from']
            email_body = msg.get_payload()
    
            if email_subject == subject_filter:
                mail_list.append(YoutubeMail(email_from, email_body))
            mail.store(num, '+FLAGS', '\\Deleted')
        mail.expunge()
        mail.close()
        mail.logout()
        return mail_list
    except Exception as e:
        print(str(e))
