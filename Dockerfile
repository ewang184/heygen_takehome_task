FROM python:3.10-slim

WORKDIR /app

COPY . /app

CMD ["python", "generate_new_video.py", "Tanzania-2.mp4"]
