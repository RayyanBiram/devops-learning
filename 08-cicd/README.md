# 08 - CI/CD

Continuous Integration and Continuous Delivery with GitHub Actions - code that is automatically linted, tested, built, and shipped on every push, so a `git push` is all it takes to validate a change and get it running.

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Hub](https://img.shields.io/badge/Docker%20Hub-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Amazon EC2](https://img.shields.io/badge/Amazon%20EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

CI/CD is the practice of automating everything between writing code and running it in production. **Continuous Integration (CI)** runs quality gates, linting, tests, a build, automatically on every change, so problems are caught the moment they land instead of at release time. **Continuous Delivery (CD)** takes it further. Once the gates pass, the change is automatically packaged and deployed to a running environment. The payoff is speed and confidence. Every commit is validated the same way, and a deploy is a push rather than a manual checklist. This folder contains two GitHub Actions builds, from a standalone CI pipeline up to a full CI/CD pipeline that deploys to AWS, each documented in full.

## How CI/CD Works

- **Trigger** - a workflow runs on an event: a push, a pull request, a tag, or a schedule.
- **Runner** - GitHub spins up a fresh virtual machine and checks out the repo onto it. Every run starts from a clean slate.
- **Jobs & steps** - a workflow is made of **jobs** (which can run in parallel or depend on each other), and each job is a sequence of **steps**.
- **CI gates** - lint, test, and build steps run first. A failure fails the job, and the change is blocked.
- **CD deploy** - a deploy job, gated behind CI with `needs`, ships the artifact, pushing an image to a registry, then pulling and restarting it on a server.
- **Secrets** - credentials (registry tokens, SSH keys) are injected from encrypted repository secrets at runtime, never committed to the repo.

## Projects

| Project | What it builds | README |
|---------|----------------|--------|
| **Flask CI Pipeline** | A standalone CI pipeline - GitHub Actions lints with flake8, tests with pytest, and builds a Docker image on every push and PR, publishing to Docker Hub only on pushes via a conditional | [View](projects/flask-ci-pipeline/README.md) |
| **Flask Stack CI/CD to AWS** | A full CI/CD pipeline - lint, test, build, and push, then SCP + SSH deploy of a Flask + Redis + nginx stack to a Terraform-provisioned EC2 instance on a custom domain | [View](projects/flask-stack-cicd-tf-aws/README.md) |

## What This Section Covers

- **Workflow triggers** - running on `push` and `pull_request`, and gating steps by event with `if`
- **Jobs and dependencies** - splitting CI from CD and chaining them with `needs`
- **Reusable actions** - `actions/checkout`, `actions/setup-python`, the Docker actions, and community actions for SCP/SSH
- **Linting and testing** - flake8 and pytest as automated quality gates
- **Building and publishing** - Docker Buildx builds and `build-push-action` publishing to Docker Hub
- **Remote deployment** - copying config with SCP and running deploy commands over SSH
- **Secrets management** - injecting Docker Hub tokens and SSH keys from repository secrets
- **Deploying to real infrastructure** - shipping onto a Terraform-provisioned EC2 instance behind a custom domain

## Core Concepts

| Concept | What it is |
|---------|------------|
| Workflow | A YAML file in `.github/workflows/` that defines when and how automation runs. |
| Trigger | The event that starts a workflow - `push`, `pull_request`, a tag, or a schedule. |
| Runner | The fresh VM GitHub provisions to execute a job which starts empty every time. |
| Job | A group of steps run on one runner. Jobs can depend on others via `needs`. |
| Step | A single unit of work - a shell command (`run`) or a reusable action (`uses`). |
| Action | A packaged, reusable step (e.g. `actions/checkout@v4`). |
| CI | Continuous Integration - automated lint, test, and build on every change. |
| CD | Continuous Delivery - automated packaging and deployment once CI passes. |
| Secret | An encrypted repository value (token, key) injected at runtime. |
| Artifact | The thing CI produces and CD ships - here, a Docker image. |

## Folder Structure

```
08-cicd/
└── projects/
    ├── flask-ci-pipeline/        # CI only: lint, test, build, conditional push to Docker Hub
    └── flask-stack-cicd-tf-aws/  # Full CI/CD: build & push, then SCP + SSH deploy to EC2
```

## Key Commands

```bash
# ─── Trigger a pipeline ───────────────────────────────────────────────
git push origin main                     # push to run the workflow (CI, and CD on the full pipeline)

# ─── Run the CI gates locally, as the pipeline does ───────────────────
flake8 app.py                            # lint the code
pytest                                   # run the test suite

# ─── Build and publish the image locally (mirrors the build stage) ────
docker build -t myapp .                  # build the image
docker push <user>/<image>:latest        # push to Docker Hub

# ─── Deploy target (full pipeline) - provision and inspect ────────────
terraform apply                          # build the EC2 instance the pipeline deploys to
ssh ubuntu@frn.aws.biram.uk              # connect to the instance
docker ps                                # confirm the deployed containers are running
```

## Basic Structure

A workflow is a single YAML file under `.github/workflows/`. It declares a trigger, then one or more jobs of sequential steps:

```yaml
name: ci

# Run on every push and pull request
on: [ push, pull_request ]

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      # Pull the repo onto the fresh runner - nothing works without this
      - name: checkout code
        uses: actions/checkout@v4

      # A reusable action to set up the language runtime
      - name: setup python
        uses: actions/setup-python@v5
        with:
          python-version: 3.12

      # A shell command: the lint gate
      - name: lint
        run: |
          pip install flake8
          flake8 app.py

      # Build and publish, but only on a real push - not on PRs
      - name: build and push
        uses: docker/build-push-action@v7
        if: github.event_name == 'push'
        with:
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/myapp:latest
```

A second job can then deploy, gated behind the first so it only runs if CI passed:

```yaml
  deploy:
    needs: build-and-publish        # only runs if CI succeeded
    runs-on: ubuntu-latest
    steps:
      - name: ssh and deploy
        uses: appleboy/ssh-action@v1
        if: github.event_name == 'push'
        with:
          host: ${{ secrets.HOST }}
          username: ubuntu
          key: ${{ secrets.SSH_KEY }}
          script: |
            docker compose pull && docker compose up -d
```

## Quick Start

```bash
# CI-only project (lint, test, build, conditional push)
cd projects/flask-ci-pipeline
# push a change to trigger the pipeline, or run the gates locally:
flake8 app.py && pytest

# Full CI/CD project (build, push, and deploy to EC2)
cd projects/flask-stack-cicd-tf-aws
# provision the target once, then push to deploy:
cd infra && terraform init && terraform apply
```

## Best Practices

- **Fail fast** - put the cheapest gates (lint) before the expensive ones (build, deploy) so failures surface quickly
- **Gate CD behind CI** - use `needs` so a deploy never runs on a failed lint, test, or build
- **Scope by event** - guard publish and deploy steps with `if: github.event_name == 'push'` so pull requests validate without shipping
- **Never commit secrets** - inject registry tokens and SSH keys from repository secrets, not the workflow file
- **Checkout first** - the runner starts empty, so `actions/checkout` has to run before anything touches the code
- **Pin action versions** - use `@v4`, not a floating tag, so a workflow doesn't change under you
- **Keep jobs single-purpose** - one job validates and publishes, another deploys. Best to not blur the two
- **Build once, deploy the artifact** - publish an image in CI and have the server pull it, rather than rebuilding from source on the box
- **Deploy to a stable address** - target a DNS name over a raw IP, so a replaced server doesn't break the pipeline

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [docker/build-push-action](https://github.com/docker/build-push-action)
- [Encrypted Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)