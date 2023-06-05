# The build-stage image:
FROM condaforge/mambaforge:23.1.0-1 AS build

# Install conda-pack:
RUN mamba install -c conda-forge conda-pack

# Install the package as normal:
COPY ./envs/phylo-web-tools.source.yml environment.yml
RUN mamba env create -f environment.yml

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

# system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
	locales \
	build-essential \
	python3-dev \
	python3-pip \
	python3-venv \
	python3-wheel \
	gettext \
	git \
    libmagic-dev \
&& apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8
RUN pip3 install --upgrade setuptools pip wheel

COPY --from=build /venv /venv
COPY ./flask_app /app
WORKDIR /app
