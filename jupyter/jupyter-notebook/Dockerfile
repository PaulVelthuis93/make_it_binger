FROM jupyter/minimal-notebook:latest

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


CMD start-notebook.sh --NotebookApp.password="$(echo "import IPython,os; print(IPython.lib.passwd(os.environ['JUPYTER_PASSWORD']))" | python)"
USER $NB_UID