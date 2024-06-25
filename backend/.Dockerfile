FROM python:3.12-slim-bookworm

RUN python --version

RUN echo 'Installing Poetry packaging and dependency management...'
RUN pip install poetry
RUN poetry config virtualenvs.in-project true

RUN mkdir -p /backend
COPY . /backend/

WORKDIR /backend/
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root

WORKDIR /backend/src
EXPOSE 5000
