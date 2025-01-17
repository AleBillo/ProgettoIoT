FROM python:3

WORKDIR /app
COPY client/ .

RUN pip install --no-cache-dir -r requirements.txt || true
# RUN apt-get update
# RUN apt-get install -y python3
# RUN apt-get install -y python3-flask
# RUN apt-get install -y python3-paho-mqtt

CMD ["python3", "app.py"]
