FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install git+https://github.com/flatlib/flatlib.git@master \
    && pip install fastapi uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
