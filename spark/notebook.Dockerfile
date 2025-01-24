FROM quay.io/jupyter/pyspark-notebook:spark-3.5.3

USER root
RUN apt-get update && apt-get install -y libpq-dev
RUN apt-get install -y ffmpeg

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

USER $NB_UID