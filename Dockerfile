FROM python:3.7-slim-buster

RUN apt update && \
    apt install -y build-essential pkg-config libsodium-dev libsecp256k1-dev libgmp-dev && \
    rm -rf /var/lib/apt/lists/*
RUN pip install notebook jupyter-client

RUN useradd -ms /bin/bash jupyter
USER jupyter
WORKDIR /home/jupyter

RUN pip install --user pytezos>=2.5.3 michelson-kernel>=0.1.6

EXPOSE 8888
ENTRYPOINT [ "jupyter",  "notebook", "--port=8888", "--ip=0.0.0.0", "--no-browser", "--no-mathjax"]
