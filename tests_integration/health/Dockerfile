FROM python:3.8.10

COPY ./requirements.txt ./requirements.txt
RUN pip install install -r requirements.txt

COPY ./test_api_health.py ./test_api_health.py
WORKDIR .

CMD ["python", "./test_api_health.py"]