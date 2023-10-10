FROM alpine:3.17
LABEL maintainer="Michael Trip <m.trip@atcomputing.nl>"
RUN apk add --no-cache stress-ng \
    iperf3 \
    python3

RUN mkdir -p /app

COPY load_testing.py /app
COPY load_testing_v2.py /app

WORKDIR /app

RUN adduser -H -D app
RUN chown -R app /app

USER app


ENTRYPOINT [ "python3", "/app/load_testing_v3.py"]
