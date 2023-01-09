# redis-rest-api, the project :

TLDR; This is a Python **very simple** REST API to access Redis data

This project started as I wanted to have a lightweight container with a Flask API to access Redis DB easily.  

### Variables

To work properly, the API will require informations and credentials.  
We assume they are passed to the container in ENV variables.

Gunicorn variables :
Most of these variables have default values, and are not Mandatory
- `GUNICORN_CHDIR`: Change directory to specified directory before loading apps. (Defaults: `/code`)
- `GUNICORN_HOST`:  Run the server using this specific host (Defaults: `0.0.0.0`)
- `GUNICORN_PORT`:  Run the server using this specific host (Defaults: `5000`)
- `GUNICORN_WORKERS`: The number of worker processes for handling requests. (Defaults: `1`)
- `GUNICORN_THREADS`: The number of worker threads for handling requests. (Defaults: `2`)
- `GUNICORN_RELOAD`: Restart workers when code changes. (Defaults: `True`)

API variables :
- `ACCESS_TOKEN`: JWT Token used to restrict access to the API (Default: `None`)

ENV global variables :
- `LOGURU_LEVEL`: Minimal level for log output (Default: `DEBUG`)

WARNING:
`ACCESS_TOKEN` is here to protect you and avoid the API to be publicly accessible.  
Set this variable, and/or put other protection mesures in front of the API (ie: restrict access with nginx)
Don't blame the project if you fail with this.

### Output on server start

```
2023-01-09 16:53:33 | level=DEBUG    | utils.redis:<module>:24 - Redis Connection OK (r)
2023-01-09 16:53:33 | level=SUCCESS  | __main__:<module>:107 - ENV var ACCESS_TOKEN set. API protected
2023-01-09 16:53:33 | level=INFO     | gunicorn.glogging:info:264 - Starting gunicorn 20.1.0
2023-01-09 16:53:33 | level=INFO     | gunicorn.glogging:info:264 - Listening at: http://0.0.0.0:5000 (609)
2023-01-09 16:53:33 | level=INFO     | gunicorn.glogging:info:264 - Using worker: gthread
2023-01-09 16:53:33 | level=INFO     | gunicorn.glogging:info:264 - Booting worker with pid: 610
```

### Tech

I mainly used :

* [pallets/flask][flask] as it's the best/fastest way to have a simple API in Python
* [docker/docker-ce][docker] to make it easy to maintain
* [kubernetes/kubernetes][kubernetes] to make everything smooth
* [Alpine][alpine] - probably the best/lighter base container to work with
* [Python] - as usual
* [Delgan/loguru][loguru] - an amazingly easy logger

And of course GitHub to store all these shenanigans.

### Installation

You can build the container yourself :
```
$ git clone https://github.com/lordslair/redis-rest-api
$ cd redis-rest-api
$ docker build .
```

Or the latest build is available on [Docker hub][hub]: `lordslair/redis-rest-api`:
```
$ docker pull lordslair/redis-rest-api:latest
latest: Pulling from lordslair/redis-rest-api
Digest: sha256:34729944fd2f1eaebb50983081c76c2162488165f76d400f82b69c1db97b88ff
Status: Downloaded newer image for lordslair/redis-rest-api:latest
docker.io/lordslair/redis-rest-api:latest
```

#### Tests

PyTests have been wrote and the builds are tested to pass them.  
Tests are accessible in the folder `tests`.  

#### Disclaimer/Reminder

> Always store somewhere safe your ACCESS_TOKEN.  
> I won't take any blame if you mess up somewhere in the process =)  

### Resources / Performance

The container is quite light, as [Alpine][alpine] is used as base.  

```
$ docker images
REPOSITORY                 TAG       SIZE
lordslair/redis-rest-api   latest    82.5MB
```

On the performance topic, the container consumes about :
 - 0,1% of a CPU
 - 64MB of RAM

### Todos

They will be added as PR here: https://github.com/lordslair/redis-rest-api/pulls  
I'm open to requests/comments/ideas/issues in PR section.  

---
   [alpine]: <https://github.com/alpinelinux>
   [docker]: <https://github.com/docker/docker-ce>
   [kubernetes]: <https://github.com/kubernetes/kubernetes>
   [flask]: <https://github.com/pallets/flask>
   [loguru]: <https://github.com/Delgan/loguru>
   [hub]: <https://hub.docker.com/repository/docker/lordslair/redis-rest-api>
