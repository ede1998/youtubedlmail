# youtubedlmail

With this docker image you can download and convert youtube videos via email.

## Usage

Simply send a plain text email to the email address you configured.
The subject must be `youtubedlmail` and the body must only contain lines 
that start with `audio ` or `video ` and a link to a youtube video after that.

Example mail:
```
From: you@you.com
To:  your-youtubedlmail@example.com
Subject: youtubedlmail
Body:
video https://www.youtube.com/watch?v=mHsL7ALp7l8
audio https://www.youtube.com/watch?v=0_4WWf9MT9s
video https://www.youtube.com/watch?v=i44L0CR06x4
```

The docker container will get new mails every minute and download each video link that was sent.
After downloading it will be converted to audio if desired.
The result is then sent back as an attachment to the mail address that sent the download request.

When an error occurs, an error mail is sent.

## Configuration

`python/configuration_example.py` must be modified to work with your setup and renamed to `python/configuration.py`.
After that you can run
`docker build -t youtubedlmail .; docker run -d --name ytdlm youtubedlmail`

**!Please take care!** The script wants its own email address. It deletes any mail it fetches.
