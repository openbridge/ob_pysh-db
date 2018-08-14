FROM alpine:3.7
MAINTAINER Thomas Spicer <thomas@openbridge.com>

ENV LANG C.UTF-8

ENV PY_DEPS \
      curl \
      pkgconfig \
      freetype-dev \
      openblas-dev \
      ca-certificates \
      bzip2-dev \
      build-base \
      gcc \
      gdbm-dev \
      libc-dev \
      linux-headers \
      musl-dev \
      python-dev \
      cmake \
      g++ \
      gfortran \
      make \
      ncurses-dev \
      libressl-dev \
      libstdc++ \
      tcl-dev \
      libffi-dev \
      tk-dev \
      zlib-dev \
      mariadb-common \
      py-numpy-dev \
      mariadb-dev \
      postgresql-dev
RUN apk update \
    && apk add --update --no-cache --virtual .build-deps \
       $PY_DEPS \
    && update-ca-certificates \
    && curl -fSL https://s3.amazonaws.com/redshift-downloads/redshift-ssl-ca-cert.pem > /redshift-ssl-ca-cert.pem \
    && apk add --update --virtual .python-deps \
        postgresql-client \
        mariadb-client \
        mariadb-client-libs \
        mariadb-common \
        py-pip \
        libgfortran \
        python \
        bash \
        curl \
        less \
        groff \
        jq \
        py-numpy-f2py \
        py-numpy \
        freetype \
        libpng \
    && pip install --no-cache-dir awscli setuptools cffi psycopg2 cryptography matplotlib pandas python-dateutil pytz six wsgiref scipy \
    && mkdir /root/.aws \
    && rm -rf /usr/src/python ~/.cache \
    && rm -Rf /tmp/* \
    && apk del .build-deps

CMD ["python2"]
