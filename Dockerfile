FROM python:3.10

WORKDIR /app

COPY . /app

RUN chmod +x /app/setup.sh

# Set the shell script to be executed when the container starts
CMD ["/bin/bash", "/app/setup.sh"]

CMD ["python", "/app/generate_new_video.py", "Tanzania-2.mp4"]
