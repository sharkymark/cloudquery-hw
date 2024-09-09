# Define the argument before its first use
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# get utilities in the container
RUN apt-get update && apt-get install -y procps ssh git net-tools htop curl postgresql-client

# Install pip dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install psycopg2-binary

RUN /bin/bash -c 'ARCH=$(uname -m) && \
    URL="https://github.com/cloudquery/cloudquery/releases/download/cli-v6.6.2/cloudquery_linux_${ARCH//aarch64/arm64}" && \
    curl -L "$URL" -o cloudquery && \
    chmod a+x cloudquery && \
    mv cloudquery /usr/local/bin/'