FROM python:3

RUN mkdir -p /github-webhooks

WORKDIR /github-webhooks

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY webhook-github.py ./webhook-github.py
CMD ["python", "webhook-github.py"]

EXPOSE 8000
