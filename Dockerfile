FROM python:3.9-alpine
EXPOSE 8085
WORKDIR /django_ci
COPY ./ /django_ci
RUN apk update && pip install -r /django_ci/requirements.txt --no-cache-dir
CMD ["python", "manage.py", "runserver", "0.0.0.0:8085"]
