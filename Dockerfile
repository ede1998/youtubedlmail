FROM python:3-alpine

WORKDIR /usr/bin/youtubedlmail

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt


# Add crontab file in the cron directory
ADD crontab /etc/cron.d/youtubedlmail-cron
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/youtubedlmail-cron

CMD cron
