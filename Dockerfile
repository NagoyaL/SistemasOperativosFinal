
        FROM ubuntu:latest
        RUN apt-get update && apt-get install -y procps
        CMD echo ejemplo2
        