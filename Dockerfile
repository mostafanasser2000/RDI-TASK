FROM python:3.10.4-slim-bullseye

# ENV variables
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1


WORKDIR /app

RUN apt-get update && apt-get install -y poppler-utils libmagic1
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .

RUN python3 manage.py migrate
EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]