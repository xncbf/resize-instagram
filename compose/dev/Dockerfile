FROM python:3.9-alpine

WORKDIR /usr/src/app

COPY Pipfile* ./

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

RUN pip install pipenv 
RUN pipenv install --system --deploy --ignore-pipfile

ADD src ./
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/src"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

