FROM python:3.8
EXPOSE 80
WORKDIR /bitelio
COPY entrypoint.sh requirements/main.txt /bitelio/
RUN pip install --upgrade pip && \
    pip install -r main.txt && \
    chmod +x entrypoint.sh
COPY api /bitelio/api
CMD ["/bitelio/entrypoint.sh"]
