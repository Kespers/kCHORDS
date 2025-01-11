FROM jupyter/pyspark-notebook:5ae537728c69

USER root
RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt .


RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

USER $NB_UID