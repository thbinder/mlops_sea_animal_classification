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

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.8/lib /project/pkgs
COPY --from=builder /project/src /project/src
# TODO: Should be retrieved from an artifact registry
COPY ./model /project/model
RUN pip uninstall dataclasses -y
RUN rm -rf /project/pkgs/dataclasses*
WORKDIR /project

# set command/entrypoint, adapt to fit your needs
# to override, run docker run -it --entrypoint=/bin/bash $image 
CMD ["python", "-m", "uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]

## Uncomment to showcase functional API setup
# CMD ["python", "-m", "uvicorn", "src.api.api_functional:app", "--host", "0.0.0.0", "--port", "8081"]