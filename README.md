# Puffin
[![Build Status](https://travis-ci.org/puffinrocks/puffin.svg?branch=master)](https://travis-ci.org/puffinrocks/puffin)

## Introduction

The goal of the project is to allow average, tech-oriented user to run web applications with ease. 
The idea is to create an easy to host, technology agnostic private cloud.
The ultimate aim is to achieve greater decentralization of web services, such as social networks, 
file sharing, blog or email.

While many other tools are looking at containers as a way to run massive 
applications, Puffin concentrates on lightweight ones, each serving just a handful of people.

You can chose to host the applications on Puffin managed platform or on your own server.

## Demo

Live demo platform is available at [puffin.rocks](http://puffin.rocks)

[![Puffin Front Page](/doc/screenshot.png?raw=true)](http://puffin.rocks)

## Architecture
 
Puffin consists of two main components - application catalog and interface that provides 
means to run the applications. Any of them can be used independently - you 
can run the applications from the catalog directly, and you can use the 
interface to run your own applications that are not present in the catalog.

## Technology

Puffin is based on [Docker](https://www.docker.com/) containers and 
for orchestration is uses [Docker Compose](https://docs.docker.com/compose/).

Software is written in [Python 3](https://www.python.org/), 
using [Flask](http://flask.pocoo.org/) web microframework. 
[PosttgreSQL](http://www.postgresql.org/) database is used to store the data.
[Nginx](http://nginx.org/) is used as a reverse proxy.

## Deployment

### Demo deployment

The easiest way to deploy Puffin and start playing with it to use 
[Docker Compose](https://docs.docker.com/compose/):

    docker-compose up

Go to [http://localhost:8080](http://localhost:8080) to acces Puffin. 
Log In as user "puffin", password "puffin". 

To rebuild the code:

    docker-compose build

Before accessing the apps you also need to [set-up DNS](#set-up-dns)
on your computer.

### Production deployment

To deploy Puffin for private needs, for a single user or a limited number of users, 
use docker-compose-example.yml file as a basis:

    cp docker-compose-example.yml docker-compose-production.yml
    docker-compose -f docker-compose-production.yml up -d

You need to change SERVER_NAME and VIRTUAL_HOST variables to point to your domain. 
You also need to set SECRET_KEY variable to a random value. 

To send emails or to disable them completely take a look at [email configuration](#email).

Initially only "puffin" user with "puffin" password will be created - make sure to change it. 
Later you can either allow other users to register themselves on your platform 
(SECURITY_REGISTERABLE = True) or create them manually:

    docker exec -it puffin_main_1 bash
    ./puffin.py user create <login>

(The password will be the same as login, so it should be changed 
by the account owner.)

You may also decide to run apps on a separate machine than Puffin itself.
To achieve that take a look on MACHINE\_\* options. You also won't need network sections in
Compose file, since they will be created automatically on the remote machine.

### Development deployment directly on host system

During development it's more convenient to run Puffin in virtualenv. 
You can still run all dependencies via Docker, but execute Puffin 
directly on the host system.

#### Dependencies:

Make sure that you have Python 3 installed on your system. For example on Debian run:

    apt-get install python3

#### Virtual environment

First of all you need to install it:

    apt-get install python3-venv

then create it:

    pyvenv env

and activate it:
    
    . env/bin/activate

Next you can install runtime and development dependencies:
    
    pip install -r requirements-dev.txt

You might have some problems in the last step, most likely due to missing libraries on your system. 
Read the message carefully and install the development versions of offending library 
(usually lib&lt;name&gt;-dev on Debian).

#### Run dependencies

Run dependencies, such as database server, mail server, DNS, and configure them:

    docker-compose up -d
    docker stop puffin_main_1

#### Run Puffin

Finally run Puffin:

    ./puffin.py server

If you want to automatically reload the server on any code change, 
I recommend using [reload](https://github.com/loomchild/reload):

    reload ./puffin.py server

### Set-up DNS

To access applications from localhost you need to set-up DNS. 
On public server you need to configure wildacard DNS record to point to your domain.
On localhost there are many alternative solutions to this problem. 

The easiest is to update your /etc/resolv.conf file to include the following line at the top:

    nameserver 127.0.0.1
    options ndots:0

Make sure that you disable your local DNS server, such as dnsmasq, before running Puffin.

### Email

During testing you can use embedded test mail server which is accessible via 
[http://localhost:8025](http://localhost:8025).

To really send emails from Puffin and the applications you need to configure few environment variables 
before starting Puffin. It's probably easiest to register to an external email service to avoid 
being classified as spammer. The variables are (not all are obligatory, see [Configuration](#configuration) for details):

    MAIL_SERVER
    MAIL_PORT
    MAIL_USE_TLS
    MAIL_USE_SSL
    MAIL_USERNAME
    MAIL_PASSWORD
    MAIL_DEFAULT_SENDER
    MAIL_SUPPRESS_SEND

### Docker Machine

If you can't use docker directly on your system or would like to deploy 
Puffin on a remote server, [Docker Machine](https://docs.docker.com/machine/) comes in handy.

You can easily install Docker [in the cloud](https://docs.docker.com/machine/get-started-cloud/) 
or on [your own server](http://loomchild.net/2015/09/20/your-own-docker-machine/).

To create and activate a local Docker virtual machine, run:

    docker-machine create -d virtualbox dev
    eval "$(docker-machine env dev)"

After that all subsequent Docker commands will be executed in a virtual machine. 
Keep in mind that you'll need to use IP address or hostname of the machine 
to access Puffin, instead of locahost.

## Configuration

Puffin is configured via environment variables. 

Either set them directly before starting it:

    export SECRET_KEY=mysupersecretkey

or cofigure them in Docker Compose file.

For a full list of configuration options see [puffin/core/config.py](puffin/core/config.py).

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

# Changelog

See [CHANGELOG.md](CHANGELOG.md).

# License

AGPL, see [LICENSE.txt](LICENSE.txt) for details.
