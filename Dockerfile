FROM nikolaik/python-nodejs:python3.8-nodejs14

# Create the environment
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-leaflet

COPY helpers.py /code/helpers.py
COPY nasa-spaceapps2020-cogs.ipynb /code/nasa-spaceapps2020-cogs.ipynb
ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''"]
