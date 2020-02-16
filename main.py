#!/bin/python3

import receive
import send_mail_with_attachment as send
import download
import os
import re

body_success = '''Hello!
Your downloaded video is attached.

URL: {0}
Filename: {1}

Thanks for using my service.'''

body_error = '''Hello!
Unfortunately, your video could not be downloaded.
Please try again or ask me for support.

Reason: {1}
URL: {0}

Thanks for using my service.'''

subject_error = 'youtubedlmail error'
subject_success = 'youtubedlmail video'


def line_is_youtube_link(line):
    return line is not None and (is_audio(line) or is_video(line))


def is_audio(line):
    return line.startswith('audio ')


def is_video(line):
    return line.startswith('video ')


def get_link(line):
    return re.sub(r'^(audio|video) ', '', line)

def process_mail(mail):
    for line in mail.body.splitlines():
        link = get_link(line)
        if not link.startswith('https://www.youtube.com/'):
            print('skipping wrongly formatted line ' + line)
            send.send_mail(mail.sender, subject_error, body_error.format(link, 'bad line formatting'))
            continue
        dl_as_audio = is_audio(line)
        filename = download.get_filename(link, dl_as_audio)
        if filename is None:
            print('error processing link ' + link)
            send.send_mail(mail.sender, subject_error, body_error.format(link, 'download error'))
            continue

        download.download(link, dl_as_audio)
        print('done with ' + link)
        print('named as ' + filename)
        send.send_mail_with_attachment(
            mail.sender,
            filename,
            subject_success,
            body_success.format(link, filename))
        os.remove(filename)


mails = receive.receive_and_delete_mails('youtubedlmail')

for mail in mails:
    process_mail(mail)
