FROM python:3.6
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY hello.py hello.py

ENV FLASK_APP hello.py
CMD ["python","hello.py"]