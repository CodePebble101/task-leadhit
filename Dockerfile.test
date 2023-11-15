FROM python:3.11-slim-buster
RUN apt-get update \
     && mkdir /app
WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir -r app/requirements.txt

CMD ["pytest"]