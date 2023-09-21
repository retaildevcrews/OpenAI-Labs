# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Install dependencies
FROM python:3.10 AS base

# Install FFModel (and unpack secrets into environment first)
RUN --mount=type=secret,id=ffmodel \
    export $(grep -v '^#' /run/secrets/ffmodel | tr -d '\r' | xargs -d '\n') \
    && pip install "git+https://$FFMODEL_REPO_PAT@$FFMODEL_REPO@$FFMODEL_REPO_REF#egg=ffmodel"

# Install from requirements.txt
WORKDIR /setup
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the app
FROM base AS app

WORKDIR /app
COPY . .

WORKDIR /app/examples/nl2python
ENTRYPOINT ["python", "../docker/app.py"]
