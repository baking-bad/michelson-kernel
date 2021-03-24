FROM python:3.7-slim-buster

RUN apt update && \
    apt install -y build-essential pkg-config libsodium-dev libsecp256k1-dev libgmp-dev make curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN useradd -ms /bin/bash jupyter

RUN mkdir /home/jupyter/michelson-kernel
RUN mkdir /home/jupyter/notebooks
COPY . /home/jupyter/michelson-kernel/
RUN chown -R jupyter /home/jupyter/

USER jupyter
WORKDIR /home/jupyter/michelson-kernel
RUN poetry config virtualenvs.in-project true
RUN make install
RUN make post-install

WORKDIR /home/jupyter/notebooks

EXPOSE 8888
ENTRYPOINT [ "/home/jupyter/michelson-kernel/.venv/bin/jupyter",  "notebook", "--port=8888", "--ip=0.0.0.0", "--no-browser", "--no-mathjax"]
