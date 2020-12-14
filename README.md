# Squidlite
User blocking by proxy and rules db.

- [Introduction](#introduction)
  - [Contributing](#contributing)
  - [Issues](#issues)
- [Getting started](#getting-started)
  - [Installation](#installation)
  - [Quickstart](#quickstart)
  - [Command-line arguments](#command-line-arguments)
  - [Persistence](#persistence)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Logs](#logs)
- [Maintenance](#maintenance)
  - [Upgrading](#upgrading)
  - [Shell Access](#shell-access)

# Introduction

Squid is a caching proxy for the Web supporting HTTP, HTTPS, FTP, and more. It reduces bandwidth and improves response times by caching and reusing frequently-requested web pages. Squid has extensive access controls and makes a great server accelerator.

The rules of each user will be inserted in a configuration file, which is fine for a system administrator, but to extend this to an automated system, a quick and lightweight query database (sqlite) and a redirector for block traffic from specific users to specific websites.

## Contributing

If you find this image useful here's how you can help:

- Send a pull request with your awesome features and bug fixes
- Help users resolve their [issues](../../issues?q=is%3Aopen+is%3Aissue).

## Issues

Before reporting your issue please try updating Docker to the latest version and check if it resolves the issue. Refer to the Docker [installation guide](https://docs.docker.com/installation) for instructions.

SELinux users should try disabling SELinux using the command `setenforce 0` to see if it resolves the issue.

If the above recommendations do not help then [report your issue](../../issues/new) along with the following information:

- Output of the `docker version` and `docker info` commands
- The `docker run` command or `docker-compose.yml` used to start the image. Mask out the sensitive bits.
- Please state if you are using [Boot2Docker](http://www.boot2docker.io), [VirtualBox](https://www.virtualbox.org), etc.

# Getting started

## Installation

Automated builds of the image are available on [Dockerhub](https://hub.docker.com/r/kevinzepeda/squidlite) and is the recommended method of installation.


```bash
docker pull kevinzepeda/squidlite:1.0-beta
```

Alternatively you can build the image yourself.

```bash
docker build -t squidlite github.com/kevinzepeda/squidlite
```

## Quickstart

Start Squid using:

```bash
docker run -itd --name squidlite \
  --publish 3128:3128 \
  --publish 3129:3129 \
  --volume $(pwd)/squid/cache:/var/spool/squid \
  --volume your_cert.pem:/etc/squid/certificate.pem \
  kevinzepeda/squidlite:1.0-beta
```

*Alternatively, you can use the sample [docker-compose.yml](docker-compose.yml) file to start the container using [Docker Compose](https://docs.docker.com/compose/)*

## Command-line arguments

You can customize the launch command of the Squid server by specifying arguments to `squid` on the `docker run` command. For example the following command prints the help menu of `squidlite` command:

```bash
docker run -itd --name squidlite --rm \
  --publish 3128:3128 \
  --publish 3129:3129 \
  --volume $(pwd)/squid/cache:/var/spool/squid \
  --volume your_cert.pem:/etc/squid/certificate.pem \
  kevinzepeda/squidlite:1.0-beta -h
```

## Persistence

For the cache to preserve its state across container shutdown and startup you should mount a volume at `/var/spool/squid`.

> *The [Quickstart](#quickstart) command already mounts a volume for persistence.*

SELinux users should update the security context of the host mountpoint so that it plays nicely with Docker:

```bash
mkdir -p /srv/docker/squid
chcon -Rt svirt_sandbox_file_t /srv/docker/squid
```

## Configuration

Squid is a full featured caching proxy server and a large number of configuration parameters. To configure Squid as per your requirements mount your custom configuration at `/etc/squid/squid.conf`.

```bash
docker run -itd --name squidlite \
  --publish 3128:3128 \
  --publish 3129:3129 \
  --volume $(pwd)/squid/cache:/var/spool/squid \
  --volume $(pwd)/squid/etc/squid.conf:/etc/squid/squid.conf \
  --volume your_cert.pem:/etc/squid/certificate.pem \
  kevinzepeda/squidlite:1.0-beta
```

To reload the Squid configuration on a running instance you can send the `HUP` signal to the container.

```bash
docker kill -s HUP squidlite
```

## Usage

Configure your web browser network/connection settings to use the proxy server which is available at `172.17.0.1:3128`

If you are using Linux then you can also add the following lines to your `.bashrc` file allowing command line applications to use the proxy server for outgoing connections.

```bash
export ftp_proxy=http://172.17.0.1:3128
export http_proxy=http://172.17.0.1:3128
export https_proxy=http://172.17.0.1:3128
```

To use Squid in your Docker containers add the following line to your `Dockerfile`.

```dockerfile
ENV http_proxy=http://172.17.0.1:3128 \
    https_proxy=http://172.17.0.1:3128 \
    ftp_proxy=http://172.17.0.1:3128
```

To use the lock and unlock feature you need to be inside the container, you need to call a function `block.py` | `unblock.py`

```bash
docker exec -it squidlite python block.py
```
```bash
$ Block User BY [user_ip]

        usage:  [user_ip] [domain] | [--get] [user_ip]

        <user_ip>:  IPV4 Network user

        <domaini>:  Word included in the domain to block

         --get:     Option to get blocked sites by user

        ie: block.py 172.17.0.2 .google.com 
```

To block a user from the network
```bash
docker exec -it squidlite python block.py 172.17.0.2 google.com
```

To Unblock a user from the network
```bash
docker exec -it squidlite python unblock.py 172.17.0.2 google.com
```
to get blocked sites by de user_ip
```bash
docker exec -it squidlite python block.py --get 172.17.0.2
```

## Logs

To access the Squid logs, located at `/var/log/squid/`, you can use `docker exec`. For example, if you want to tail the access logs:

```bash
docker exec -it squid tail -f /var/log/squid/access.log
```

You can also mount a volume at `/var/log/squid/` so that the logs are directly accessible on the host.

# Maintenance

## Upgrading

To upgrade to newer releases:

  1. Download the updated Docker image:

  ```bash
  docker pull kevinzepeda/squidlite:1.0-beta
  ```

  2. Stop the currently running image:

  ```bash
  docker stop squidlite
  ```

  3. Remove the stopped container

  ```bash
  docker rm -v squidlite
  ```

  4. Start the updated image

  ```bash
  docker run -name squidlite -d \
    [OPTIONS] \
    kevinzepeda/squidlite:1.0-beta
  ```

## Modify SQL Database

Into `./block` folder exist the file `SQUIDLITE.sql` that file contains SQL sentence to create the db.
You can modify it to adapt it to your needs, it is necessary to reflect the new tables inside `tables.py` 
also to be able to access the data it is necessary to create the sentences in `crud.py`

## Shell Access

For debugging and maintenance purposes you may want access the containers shell. If you are using Docker version `1.3.0` or higher you can access a running containers shell by starting `bash` using `docker exec`:

```bash
docker exec -it squidlite bash
```