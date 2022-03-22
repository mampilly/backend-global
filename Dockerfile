# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# set environment variables
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# set working directory
WORKDIR /global-api

# copy dependencies
COPY requirements.txt /global-api/

# install dependencies
RUN pip3 install -r requirements.txt

# copy project
COPY . /global-api/

# expose port
EXPOSE 8000

# run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]