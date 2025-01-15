FROM python:3.13 as base
WORKDIR /home
COPY ./app/requirements.txt /home
RUN pip install -r requirements.txt

FROM base as staging
ADD ./app /home