FROM python:slim-buster

ENV DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:99

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get install -yq --no-install-recommends wget gnupg2 curl && wget -qO - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get -y update && apt-get install -yq --no-install-recommends unzip google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*


RUN curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE \
    | xargs -I {} wget -q https://chromedriver.storage.googleapis.com/{}/chromedriver_linux64.zip -O /tmp/chromedriver.zip \
    && unzip -q /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

RUN cd /usr/src/app && pip install --no-cache-dir -U -r requirements.txt && rm -f requirements.txt


EXPOSE 6969

CMD ["supervisord", "-c", "supervisord.conf"]


