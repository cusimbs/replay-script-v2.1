FROM gcr.io/google.com/cloudsdktool/cloud-sdk

COPY replay-data.py /
COPY entrypoint.sh /

RUN mkdir /logfiles && \
    chmod +x /entrypoint.sh

VOLUME /logfiles

WORKDIR /logfiles
