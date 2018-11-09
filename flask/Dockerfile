FROM python:3.6
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY binger-api.py binger-api.py

ENV FLASK_APP binger-api.py
CMD ["python","binger-api.py"]
