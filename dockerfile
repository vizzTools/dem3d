# DOCKERFILE for building blender as a python module!
FROM python:3.10

ENV DEBIAN_FRONTEND noninteractive

ARG PYTHON_VER_MAJ 3.10

RUN apt-get update && apt-get -y install \
    build-essential \
    cmake \
    curl \
    git \
    subversion \
    sudo \
    ncdu \
    zlib1g zlib1g-dev \
    libx11-dev \
    libxxf86vm-dev \
    libxcursor-dev \
    libxi-dev \
    libxrandr-dev \
    libxinerama-dev \
    libglew-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/tmp/lib
RUN svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_centos7_x86_64

WORKDIR /home/tmp
RUN git clone https://git.blender.org/blender.git # -b v3.1.2 \
    && cd blender \
    && make update \
    && make bpy \
    && cd buil_linux_bpy \
    && make install

WORKDIR /home
CMD bash
