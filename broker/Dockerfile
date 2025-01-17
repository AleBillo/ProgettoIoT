FROM debian

WORKDIR /app
COPY broker/ .

RUN apt-get update
RUN apt-get install -y mosquitto

CMD ["mosquitto"]
