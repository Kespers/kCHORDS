FROM apache/spark:3.5.3

USER 0

COPY requirements.txt ./

RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.9 -y

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

RUN apt-get install -y libpq-dev
RUN apt-get install -y ffmpeg

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/spark/work-dir