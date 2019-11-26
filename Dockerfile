FROM python:3.7

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /soccer_data
COPY . /soccer_data

RUN mkdir /etc/scrapyd

COPY scrapyd.conf /etc/scrapyd

ENTRYPOINT [ "scrapyd" ]
