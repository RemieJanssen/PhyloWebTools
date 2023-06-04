# The build-stage image:
FROM continuumio/miniconda3:23.3.1-0 AS build

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Install the package as normal:
COPY ./envs/phylo-web-tools.source.yml environment.yml
RUN conda env create -f environment.yml

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n phylo-web-tools -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack




# Actual container without conda
FROM ubuntu:focal
ARG DEBIAN_FRONTEND=noninteractive

COPY --from=build /venv /venv
COPY ./flask_app /app
WORKDIR /app

SHELL ["/bin/bash", "-c"]