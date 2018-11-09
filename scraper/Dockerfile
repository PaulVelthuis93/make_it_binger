FROM       python
COPY       requirements.txt requirements.txt
RUN        pip install -r requirements.txt
COPY       main.py main.py
ENTRYPOINT ["python", "main.py"]
