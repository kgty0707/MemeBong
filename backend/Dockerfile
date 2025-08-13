FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/backend/requirements.txt
RUN grep -v "pywin32" /code/backend/requirements.txt > /code/backend/requirements.linux.txt
RUN pip install --no-cache-dir --upgrade -r /code/backend/requirements.linux.txt

COPY . /code/backend/

CMD ["uvicorn", "backend.manage:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--reload"]