FROM python:3.11-bullseye

COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "uvicorn", "src.main:app", "--host=0.0.0.0" ]
