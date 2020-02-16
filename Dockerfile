FROM python:3.8
EXPOSE 8080
WORKDIR /bitelio
COPY requirements/main.txt /bitelio/
RUN pip install --upgrade pip && pip install -r main.txt
COPY api /bitelio/api
ENTRYPOINT ["python3.8", "-OO", "-m", "api"]
