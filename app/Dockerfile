FROM python:3.11
RUN apt-get update \
     && mkdir /app
WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR ..
#CMD ["sh", "./app.sh"]
CMD ["python","app/main.py"]

#CMD ["uvicorn","main:app", "--host", "0.0.0.0"]

