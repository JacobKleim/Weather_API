FROM python:3.12-slim

ARG BASE_DIR=/opt/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install pipx && \
    pipx install poetry

WORKDIR ${BASE_DIR}

COPY pyproject.toml poetry.lock ${BASE_DIR}/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

WORKDIR ${BASE_DIR}/src

COPY src/ .