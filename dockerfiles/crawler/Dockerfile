FROM python:3.10.4-alpine
USER root

ENV LC_CTYPE='C.UTF-8'
ENV TZ='Asia/Tokyo'
ENV DEBIAN_FRONTEND=noninteractive

RUN set -x && \
    apk add --no-cache build-base nano git tzdata ncdu libxslt-dev && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN python -m pip install mysql-connector-python
RUN python -m pip install requests
RUN python -m pip install lxml
RUN python -m pip install bs4 feedparser httpx nest_asyncio


CMD ["/opt/start_crawler.sh"]