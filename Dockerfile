FROM python:3.8
ARG requirements=main
EXPOSE 8080
WORKDIR /bitelio
COPY requirements/${requirements}.txt /bitelio/
RUN pip install --upgrade pip && pip install -r ${requirements}.txt
COPY api /bitelio/api
CMD ["python3.8", "-OO", "-m", "api"]
