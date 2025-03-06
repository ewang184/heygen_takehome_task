FROM python:3.10

WORKDIR /app

# Install essential packages
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    gnupg \
    ca-certificates \
    lsb-release \
    ffmpeg \
    && apt-get clean

# Copy your application files
COPY . /app

