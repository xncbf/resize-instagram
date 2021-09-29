FROM public.ecr.aws/lambda/python:3.9

COPY Pipfile* ./

RUN yum -y update \
    && yum install -y libjpeg-devel libpng-devel

RUN pip install pipenv 
RUN pipenv install --system --deploy --ignore-pipfile
COPY src ${LAMBDA_TASK_ROOT}

CMD ["main.handler"]

