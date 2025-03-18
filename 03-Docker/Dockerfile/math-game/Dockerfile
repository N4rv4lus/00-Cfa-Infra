# syntax=docker/dockerfile:1

FROM rockylinux:9.3

# install app
RUN dnf upgrade -y && dnf install python3 python3-pip -y

# Copy script

COPY math-game.py /