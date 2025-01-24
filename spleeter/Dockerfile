FROM python:3.8-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y ffmpeg

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=server.py
ENV TF_FORCE_CPU="true"
ENV SPLITTER_PATH="/pretrained_models"

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["-m", "flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]

