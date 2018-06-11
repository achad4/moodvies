FROM joyzoursky/python-chromedriver:3.6-xvfb-selenium
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
