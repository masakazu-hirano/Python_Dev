FROM python:3.11.4-bookworm

RUN apt-get update \
	&& apt-get install --yes --show-progress --verbose-versions git

RUN git config --global user.name masakazu-hirano \
	&& git config --global user.email @users.noreply.github.com \
	&& git config --global init.defaultBranch master

COPY . /usr/local/src
WORKDIR /usr/local/src

RUN pip install --upgrade pip \
	&& pip install --requirement requirements.txt
