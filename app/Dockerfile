FROM python:3.11
RUN apt-get update \
     && mkdir /app
WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["sh", "/app/app.sh"]


