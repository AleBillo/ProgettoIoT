FROM python:3

WORKDIR /app
COPY server/ .

RUN pip install --no-cache-dir -r requirements.txt || true
# RUN apt-get update
# RUN apt-get install -y python3
# RUN apt-get install -y python3-opencv
# RUN apt-get install -y python3-paho-mqtt
# RUN apt-get install -y python3-numpy

CMD ["python3", "server.py"]
