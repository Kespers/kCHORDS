FROM mcr.microsoft.com/playwright/python:v1.32.0-focal

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP=server.py

COPY . .

EXPOSE 6000

ENTRYPOINT ["python"]
CMD ["-m", "flask", "run", "--host=0.0.0.0", "--port=6000", "--reload"]
