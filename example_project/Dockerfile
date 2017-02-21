# run me like this:
# docker run -d -p 443:443 fredhutch/openidconnect_server

FROM ubuntu:16.04

RUN apt-get -yy update

RUN apt-get install -y apache2 python3 python3-pip git

RUN pip3 install --upgrade pip # (be sure and run pip3 though, not pip)

RUN pip3 install virtualenvwrapper

RUN mkdir /envs

RUN export WORKON_HOME=/envs

RUN export VIRTUALENVWRAPPER_PYTHON=$(which python3)

# does export work? or do you need env? TODO which works and
# which can be removed?

ENV WORKON_HOME=/envs
ENV VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3

RUN . /usr/local/bin/virtualenvwrapper.sh




# TODO remove stuff below

FROM python:2-onbuild

RUN [ "python", "manage.py", "migrate" ]
RUN [ "python", "manage.py", "creatersakey" ]
EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
