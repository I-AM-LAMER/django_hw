FROM python:3.10.13

WORKDIR /

COPY . .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py collectstatic && y && python3 manage.py runserver ${WEB_HOST}:${WEB_PORT}"]