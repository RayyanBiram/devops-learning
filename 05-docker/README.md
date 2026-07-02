# 05 - Docker

Containerisation with Docker - packaging applications and their dependencies into portable, reproducible containers that run the same everywhere.

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)

Docker is a platform for building, shipping, and running applications in **containers** - lightweight, isolated packages that bundle an app with everything it needs to run. Unlike a virtual machine, a container shares the host's operating system kernel instead of booting its own, so it starts in seconds and stays small. The payoff is consistency: the same image runs identically on your laptop, a teammate's machine, or a production server, no more "works on my machine." This folder contains two hands-on Docker builds, from a single containerised Flask app up to a scaled, load-balanced multi-container stack, each documented in full.

## How Docker Works

- **Dockerfile** - you declare, step by step, how to assemble an image: a base, your code, its dependencies, and a start command.
- **`build`** - Docker runs the Dockerfile top to bottom and produces an **image**, caching each step as a layer so rebuilds are fast.
- **`run`** - starts a **container** from that image. The same image can spawn many identical containers.
- **Compose** - one YAML file brings up several containers together, on a shared network, with their volumes and settings wired up.
- **Volumes & networks** - volumes persist data beyond a container's life. The network lets containers find each other by service name.
- **Registry** - images are pushed to and pulled from a registry like Docker Hub, so builds are shareable and reproducible.

## Projects

| Project | What it builds | README |
|---------|----------------|--------|
| **Hello Flask** | A single-container Flask web app - the first Docker build: writing a Dockerfile, building an image, and running a containerised app on a mapped port | [View](projects/hello-flask/README.md) |
| **Flask + Redis + nginx** | A multi-container visit-counter - a Flask app backed by Redis, orchestrated with Docker Compose, scaled to multiple instances and load-balanced by nginx, with persistent storage, environment-based config, and a personalised styled frontend | [View](projects/flask-redis-nginx/README.md) |

## What This Section Covers

- **Images & the Dockerfile** - building images, choosing base images, layer caching, and single vs multi-stage builds
- **Containers** - running, listing, inspecting, and shelling into containers
- **Docker Compose** - orchestrating multi-container apps from a single file
- **Service networking** - containers reaching each other by service name over a private network
- **Persistence** - named volumes that outlive containers
- **Configuration** - passing settings in with environment variables
- **Scaling & load balancing** - running multiple app instances behind an nginx reverse proxy
- **Production hardening** - the gap between a dev setup and a production-ready one (WSGI server, pinned versions, non-root user, healthchecks)

## Core Concepts

| Concept | What it is |
|---------|------------|
| Image | A read-only, ready-to-run package - OS, code, and dependencies baked in. Built once, from a Dockerfile. |
| Container | A running instance of an image. Many can run from one image. |
| Dockerfile | The recipe for building an image - one instruction per line. |
| Docker Compose | A tool for defining and running multi-container apps from one YAML file. |
| Volume | Docker-managed storage that lives outside a container, so data survives restarts. |
| Network | A private network Compose puts services on, letting them reach each other by name. |
| Port mapping | Exposing a container's internal port to the host (e.g. `5000:80`). |
| Registry | A store for images (e.g. Docker Hub) you push to and pull from. |

## Folder Structure

```
05-docker/
└── projects/
    ├── hello-flask/         # First container: a single Flask app (Dockerfile + image + run)
    └── flask-redis-nginx/   # Multi-container app: Flask + Redis + nginx (Compose, scaling, volumes)
```

## Key Commands

```bash
docker build -t myapp .                  # build an image from the Dockerfile in this folder
docker run -d -p 5000:5000 myapp         # run a container, mapping host:container ports
docker ps                                # list running containers
docker ps -a                             # list all containers (including stopped)
docker images                            # list local images
docker logs <container>                  # view a container's logs
docker exec -it <container> sh           # open a shell inside a running container
docker stop <container>                  # stop a running container

docker compose up --build                # build images and start the whole stack
docker compose up --build --scale web=3  # start with 3 instances of the web service
docker compose ps                        # list the stack's containers and their state
docker compose logs -f                   # follow logs from all services
docker compose down                      # stop and remove containers + network
docker compose down -v                   # also remove named volumes (wipes persisted data)
```

## Basic Structure

A Dockerfile defines a single image:

```dockerfile
# Start from a small, specific base image (avoid :latest)
FROM python:3.12-slim

# Set the working directory inside the image
WORKDIR /app

# Copy the dependency list first so this layer caches when only code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Document the port the app listens on
EXPOSE 5000

# The command that runs when a container starts
CMD ["python", "app.py"]
```

Docker Compose wires several images together into a running stack:

```yaml
services:
  web:
    build: .                 # build the Dockerfile in this folder
    ports:
      - "5000:5000"          # host:container
    depends_on:
      - redis
    environment:
      REDIS_HOST: redis      # reachable by service name on the shared network

  redis:
    image: redis:7-alpine    # pull a pre-built, pinned image
    volumes:
      - redis-data:/data     # persist data in a named volume

volumes:
  redis-data:
```

## Quick Start

```bash
# Multi-container project (Flask + Redis + nginx)
cd projects/flask-redis-nginx
docker compose up --build
# then open http://localhost:5000

# Single-container project (Hello Flask)
cd projects/hello-flask
docker build -t hello-flask .
docker run -d -p 5000:5000 hello-flask
```

## Best Practices

- **Pin image tags** - use `python:3.12-slim`, not `:latest`, so builds stay reproducible
- **Keep images small** - prefer `slim`/`alpine` bases and multi-stage builds to drop build-only tooling
- **Order layers for caching** - copy dependency files and install *before* copying the rest of the code
- **Use a `.dockerignore`** - keep `.git`, local virtual environments, and secrets out of the build context
- **Run as a non-root user** - add a user and a `USER` instruction rather than running as root
- **One concern per container** - app, database, and proxy each get their own service
- **Persist state in named volumes** - never rely on a container's own filesystem for data you care about
- **Never bake in secrets** - pass them via environment variables or a secrets manager, not the image
- **Use Compose for multi-container** - define the whole stack in one file and bring it up together
- **Don't ship the dev server** - swap Flask's built-in server for a production WSGI server (e.g. Gunicorn)

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Hub](https://hub.docker.com/)
- [Best Practices for Building Images](https://docs.docker.com/build/building/best-practices/)