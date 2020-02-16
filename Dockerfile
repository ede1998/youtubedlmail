FROM python:3-alpine

WORKDIR /usr/bin/youtubedlmail

COPY requirements.txt ./
COPY python/* ./

RUN pip install --no-cache-dir -r requirements.txt
RUN apk add ffmpeg

ADD run-youtubedlmail.sh ./run-youtubedlmail.sh
RUN chmod 755 ./run-youtubedlmail.sh

ADD youtubedlmail-cron /etc/crontabs/youtubedlmail-cron
RUN /usr/bin/crontab /etc/crontabs/youtubedlmail-cron

COPY startup.sh /startup.sh
RUN chmod 755 /startup.sh

CMD ["/startup.sh"]

