FROM plexinc/pms-docker:latest


RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    libpq-dev \
    make \
    python-pip \
    python2.7 \
    && apt-get autoremove \
    && apt-get clean

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY root/ /

WORKDIR /
