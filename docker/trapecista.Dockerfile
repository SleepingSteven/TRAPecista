FROM python:3.11-slim

WORKDIR /usr/src/app

USER root

# Update and setup the system
RUN apt update -y && apt upgrade -y
RUN apt-get install -y wget libaio1 unzip build-essential

# Set Oracle Instant Client environment variables
ENV ORACLE_HOME=/opt/oracle/instantclient
ENV LD_LIBRARY_PATH=$ORACLE_HOME
ENV PATH=$PATH:$ORACLE_HOME

# Install Oracle Instant Client
RUN mkdir -p $ORACLE_HOME
RUN cd $ORACLE_HOME && \
    wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linuxx64.zip
    RUN cd $ORACLE_HOME && \
    unzip instantclient-basic-linuxx64.zip && \
    rm instantclient-basic-linuxx64.zip && \
    mv instantclient_*/* ./ && \
    rmdir instantclient_*

# Install modules
RUN mkdir /.local && chmod -R 777 /.local
RUN mkdir /.cache && chmod -R 777 /.cache
COPY services/trapecista/requirements.txt requirements.txt
USER 1001
RUN python3 -m pip install --no-cache-dir pip --upgrade
RUN pip install -U --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir requests redis==5.0.4 datetime itsdangerous chromadb
COPY ./trap /.local/lib/python3.10/site-packages/trap

# Copy sources
USER root
COPY services/trapecista/ .
RUN mkdir shared
COPY services/shared/ ./shared

RUN chmod -R 775 .
USER 1001

ENV ENVIRONMENT=TEST
ENV KUBE_NAMESPACE=trap-test

CMD ["bash", "-c", "python -m uvicorn app:app --host 0.0.0.0 --port 8081"]