FROM alpine:edge

ENV LANG C.UTF-8

ENV PY_DEPS \
      curl \
      pkgconfig \
      freetype-dev \
      py-numpy-dev@community \
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
      libgfortran \
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
      mariadb-dev \
      postgresql-dev
RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && apk update \
    && apk add --update --no-cache --virtual .build-deps \
       $PY_DEPS \
    && update-ca-certificates \
    && curl -fSL https://s3.amazonaws.com/redshift-downloads/redshift-ssl-ca-cert.pem > /redshift-ssl-ca-cert.pem \
    && curl -fSL 'https://bootstrap.pypa.io/get-pip.py' | python \
    && pip install --no-cache-dir setuptools cffi psycopg2 cryptography numpy matplotlib pandas python-dateutil pytz six wsgiref scipy sqlalchemy mysql-connector boto awscli \
    && find /usr/local -depth \
        \( \
            \( -type d -a -name test -o -name tests \) \
            -o \
            \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        \) -exec rm -rf '{}' + \
    && apk add --update --virtual .python-deps \
        postgresql-client \
        mariadb-client \
        mariadb-client-libs \
        python \
        curl \
        less \
        groff \
        jq \
        py-numpy \
        freetype \
        libpng \
    && mkdir /root/.aws \
    && rm -rf /usr/src/python ~/.cache \
    && rm -Rf /tmp/* \
    && apk del .build-deps

CMD ["python2"]
