# build stage
FROM python:3.8 AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
RUN ls -l
COPY pyproject.toml pdm.lock README.md /project/
COPY src/ /project/src

# install dependencies and project
WORKDIR /project
RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable


# run stage
FROM python:3.8

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.8/lib /project/pkgs

# set command/entrypoint, adapt to fit your needs
# to override, run docker run -it --entrypoint=/bin/bash $image 
CMD ["python", "-m", "uvicorn", "project.pkgs.application.app:app", "--host", "0.0.0.0", "--port", "8080"]