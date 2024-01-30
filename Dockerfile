FROM continuumio/miniconda3:latest
WORKDIR /app
COPY environment.yml .
COPY . /app
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "nom_de_votre_env", "/bin/bash", "-c"]
CMD [ "python3", "app.py" ]