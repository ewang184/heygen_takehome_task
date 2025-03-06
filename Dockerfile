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

# Set executable permissions for your setup script
RUN chmod +x /app/setup.sh

# Only the last CMD will be executed
CMD ["/bin/bash", "/app/setup.sh"]
CMD ["python", "/app/generate_new_video.py", "Tanzania-2.mp4"]
