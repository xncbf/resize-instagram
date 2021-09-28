FROM public.ecr.aws/lambda/python:3.9

COPY Pipfile* ./

RUN pip install pipenv 
RUN pipenv install --system --deploy --ignore-pipfile
ADD src ${LAMBDA_TASK_ROOT}

CMD ["main.handler"]

