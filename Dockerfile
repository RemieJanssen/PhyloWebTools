# Container for building the environment
FROM continuumio/miniconda:latest as builder

COPY ./envs/phylo-web-tools.source.yml ./envs/phylo-web-tools.yml

RUN conda env create -f ./envs/phylo-web-tools.yml

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n phylo-web-tool -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack



# Actual container without conda
FROM ubuntu:focal
ARG DEBIAN_FRONTEND=noninteractive

COPY --from=build /venv /opt/venv
COPY ./flask_app /app
WORKDIR /app

SHELL ["/bin/bash", "-c"]

ENTRYPOINT source /opt/venv/bin/activate