# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/scipy-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Set when building on Travis so that certain long-running build steps can
# be skipped to shorten build time.
ARG TEST_ONLY_BUILD

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# R pre-requisites
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    gfortran \
    gcc && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /tmp

USER $NB_UID

# R packages including IRKernel which gets installed globally.
RUN conda install --quiet --yes \
    'r-base=3.6.3' \
    'r-caret=6.0*' \
    'r-crayon=1.3*' \
    'r-devtools=2.3*' \
    'r-forecast=8.12*' \
    'r-hexbin=1.28*' \
    'r-htmltools=0.4*' \
    'r-htmlwidgets=1.5*' \
    'r-irkernel=1.1*' \
    'r-nycflights13=1.0*' \
    'r-plyr=1.8*' \
    'r-randomforest=4.6*' \
    'r-rcurl=1.98*' \
    'r-reshape2=1.4*' \
    'r-rmarkdown=2.1*' \
    'r-rsqlite=2.2*' \
    'r-shiny=1.4*' \
    'r-tidyverse=1.3*' \
    'rpy2=3.1*' \
    && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"


WORKDIR $HOME

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        emacs \
        git \
        inkscape \
        jed \
        libsm6 \
        libxext-dev \
        libxrender1 \
        lmodern \
        netcat \
        unzip \
        nano \
        curl \
        wget \
        cmake \
        rsync \
        gnuplot-x11 \
        libopenblas-base \
        python3-dev \
        ttf-dejavu && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN cd $HOME/work;\
    pip install --upgrade pip; \
    pip install plotly \
                dash \
                dash_core_components \
                dash_html_components \
                dash_dangerously_set_inner_html \
                dash-renderer \
                flask \
                ipywidgets \
                nibabel \
                nbconvert; \
    jupyter labextension install --minimize=False jupyterlab-sos; \
    git clone https://github.com/dimitarmileski/Medical-KGs-WBS.git; \
    cd Medical-KGs-WBS;\
    chmod -R 777 $HOME/work/Medical-KGs-WBS
    
WORKDIR $HOME/work/Medical-KGs-WBS

USER $NB_UID
