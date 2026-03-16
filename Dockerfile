
FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN python init_db.py

CMD gunicorn -b 0.0.0.0:10000 app:app
