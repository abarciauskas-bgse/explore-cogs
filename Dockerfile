FROM continuumio/miniconda3

# Create the environment
COPY environment.yml .
RUN conda env create -f environment.yml

WORKDIR /code
COPY helpers.py /code/helpers.py
COPY nasa-spaceapps2020-cogs.ipynb /code/nasa-spaceapps2020-cogs.ipynb
ENTRYPOINT ["conda", "run", "-n", "eo_cog", "jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''"]
