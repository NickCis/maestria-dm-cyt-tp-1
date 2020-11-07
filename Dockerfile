FROM python:3

WORKDIR /opt/dm-cyt/

RUN pip install numpy pandas sklearn
COPY processing.py clustering.py ./

CMD ["/bin/bash"]
