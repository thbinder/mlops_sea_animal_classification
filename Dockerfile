# build stage
FROM python:3.8.10 AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock README.md /project/
# install dependencies and project
WORKDIR /project
RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable
COPY src/ /project/src

# run stage, you can start from a more lightweighted base image
FROM python:3.8.10-slim-buster

# Adding necessary packages for mysql connection
RUN apt-get -y update
RUN apt-get -y install gcc
RUN apt-get -y install python-mysqldb
RUN apt-get -y install default-libmysqlclient-dev
RUN pip install mysqlclient

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.8/lib /project/pkgs
COPY --from=builder /project/src /project/src
# Remove some unnecessary packages
RUN pip uninstall dataclasses -y
RUN rm -rf /project/pkgs/dataclasses*
WORKDIR /project

# set command/entrypoint, adapt to fit your needs
# to override, run docker run -it --entrypoint=/bin/bash $image 
CMD ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8081"]