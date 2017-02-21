# build me like this:
# docker build -t fredhutch/openidconnect_server .
# run me like this:
# docker run -d -p 443:443 --name openid fredhutch/openidconnect_server

FROM ubuntu:16.04

RUN apt-get -yy update

RUN apt-get install -y apache2 python3 python3-pip git curl unzip libapache2-mod-wsgi-py3

RUN pip3 install --upgrade pip

# RUN pip3 install virtualenvwrapper

# RUN mkdir /envs

# RUN export WORKON_HOME=/envs

# RUN export VIRTUALENVWRAPPER_PYTHON=$(which python3)

# does export work? or do you need env? TODO which works and
# which can be removed?

# ENV WORKON_HOME=/envs
# ENV VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3

# RUN . /usr/local/bin/virtualenvwrapper.sh

# RUN mkvirtualenv django-oidc-provider

RUN git clone https://github.com/dtenenba/hutch-oidc-provider.git

RUN cd hutch-oidc-provider/example_project

WORKDIR /hutch-oidc-provider/example_project


RUN pip3 install -r requirements.txt

RUN python3 manage.py migrate

RUN python3 manage.py creatersakey

RUN python3 manage.py collectstatic --noinput

# set up db perms:

RUN chmod 664 DATABASE.sqlite3

RUN chown :www-data DATABASE.sqlite3

RUN chown :www-data /hutch-oidc-provider/example_project/

RUN chown www-data /hutch-oidc-provider/example_project/

RUN a2enmod ssl

RUN service apache2 restart

RUN cd /etc/apache2/sites-enabled

WORKDIR /etc/apache2/sites-enabled

RUN ln -s ../sites-available/default-ssl.conf .

RUN cd /tmp

WORKDIR /tmp

RUN curl -O http://dist.fhcrc.org/wildcard2014/fhcrc-wildcard-apache.zip

RUN unzip fhcrc-wildcard-apache.zip

RUN curl -O http://dist.fhcrc.org/wildcard2014/fhcrc.org.key

RUN cp 2b497ffb67edc8.crt /etc/ssl/certs/

RUN cp gd_bundle-g2-g1.crt /etc/ssl/certs

RUN cp fhcrc.org.key /etc/ssl/private

RUN chmod 0400 /etc/ssl/private/fhcrc.org.key

RUN cd /etc/apache2/sites-available

WORKDIR /etc/apache2/sites-available

RUN sed -i.bak -r "s#/etc/ssl/certs/ssl-cert-snakeoil.pem#/etc/ssl/certs/2b497ffb67edc8.crt#" default-ssl.conf

RUN sed -i.bak -r "s#/etc/ssl/private/ssl-cert-snakeoil.key#/etc/ssl/private/fhcrc.org.key#" default-ssl.conf

RUN sed -i.bak -r "s@#SSLCertificateChainFile /etc/apache2/ssl.crt/server-ca.crt@SSLCertificateChainFile /etc/ssl/certs/2b497ffb67edc8.crt@" default-ssl.conf

# now we have apache + ssl running but no wsgi yet

# TODO - set up wsgi here
ADD wsgi_conf_fragment.txt /tmp/

RUN sed -i.bak -r "s#</VirtualHost>##" default-ssl.conf
RUN sed -i.bak -r "s#</IfModule>##" default-ssl.conf

RUN cat /tmp/wsgi_conf_fragment.txt >> default-ssl.conf



# make sure the apache2 daemon is off before we turn it on in the foreground:
RUN service apache2 stop

WORKDIR /

# this needs to be the last line in the Dockerfile:
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
