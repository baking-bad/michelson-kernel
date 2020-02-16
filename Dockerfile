FROM python:3.7-slim-buster

RUN pip install notebook michelson-kernel

RUN useradd -ms /bin/bash jupyter
USER jupyter
WORKDIR /home/jupyter

EXPOSE 8888
ENTRYPOINT [ "jupyter",  "notebook", "--port=8888", "--ip=0.0.0.0", "--no-browser", "--no-mathjax"]