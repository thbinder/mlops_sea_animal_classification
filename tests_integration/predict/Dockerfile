FROM python:3.8.10

COPY ./requirements.txt ./requirements.txt
RUN pip install install -r requirements.txt

COPY ./test_api_predict.py ./test_api_predict.py
COPY ./nudibranch.jpg ./nudibranch.jpg
WORKDIR .

CMD ["python", "./test_api_predict.py"]