FROM python:3.8-buster

ENV MONOREPO_ROOT "/opt/codebase"
ENV VENV_NAME ".venv-docker"

# Setup system environment variables neded for python to run smoothly
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# Install system requirements
RUN apt-get update && apt-get install -y \
    # Needed for typed-ast dependency
    build-essential \
    # python requirements
    python3-dev python3-pip python3-venv jq && \
    # cleanup apt caches to keep image small
    rm -rf /var/lib/apt/lists/*

WORKDIR "$MONOREPO_ROOT"
RUN pip install virtualenv && \
    virtualenv "$VENV_NAME"
ENV PATH="$MONOREPO_ROOT/$VENV_NAME/bin:${MONOREPO_ROOT}/monorepo/cicd/tools:${PATH}"

# Install the python dependencies from requirements.txt into /opt/oddslingers.poker/.venv-docker.
COPY ./cicd/tools/requirements.txt "$MONOREPO_ROOT/requirements.txt"
RUN pip install --no-cache-dir -r requirements.txt
