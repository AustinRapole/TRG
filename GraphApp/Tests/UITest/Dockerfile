FROM ubuntu

# Gets python in the docker container
FROM python:3.11-slim

RUN apt-get update

# Installs selenium in the container
RUN pip install selenium
RUN pip install helium # idk if this needs selenium isntalled or not
RUN pip install pytest
RUN pip install webdriver-manager

RUN apt install wget -y
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz 
RUN tar -xvzf geckodriver-v0.34.0-linux64.tar.gz 
RUN chmod +x geckodriver 
RUN mv geckodriver /usr/local/bin/

RUN apt install firefox-esr -y
RUN export MOZ_HEADLESS=1

# Sets working dir
WORKDIR /app

# Copies test file into the container
COPY ui_test.py .

# Defines the command to run
CMD ["pytest", "ui_test.py"]
