FROM python:3.8.1-slim
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./src /app/src
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt
RUN spacy download en
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "src.main:app"]

