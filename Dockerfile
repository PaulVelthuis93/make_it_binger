FROM       python

RUN        pip install beautifulsoup4
RUN        pip install requests
COPY       main.py /app/
WORKDIR    /app
RUN        chmod a+x main.py
ENTRYPOINT ["python", "main.py"]
CMD        ["http://www.mkyong.com/author/marilena/"]
