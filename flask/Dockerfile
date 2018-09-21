FROM python:3.6
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY hello.py hello.py

CMD ["FLASK_APP=hello.py", "flask", "run"]