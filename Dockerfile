FROM       python
COPY       /app /app
COPY       requirements.txt requirements.txt
RUN        pip install -r requirements.txt
WORKDIR    /app
RUN        chmod a+x main.py
ENTRYPOINT ["python", "main.py"]
