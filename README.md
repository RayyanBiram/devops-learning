# DevOps Learning Journey

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)

A hands-on portfolio working through the DevOps toolchain from the ground up - Linux and Bash, through Docker, AWS, and Terraform, to full CI/CD pipelines. Each module is documented in full, and most contain production-shaped projects: real infrastructure built as code, deployed, and written up with architecture, screenshots, and the problems solved along the way.

**Start with the projects** - each module README below links straight to them.

## Modules

| # | Module | What's inside | Explore |
|---|--------|---------------|---------|
| 01 | **Linux** | Command-line fundamentals, filesystem, permissions, processes | [View](01-linux/README.md) |
| 02 | **Bash** | Scripting, automation, and shell challenges | [View](02-bash/README.md) |
| 03 | **Git** | Version control workflows and branching | [View](03-git/README.md) |
| 04 | **Networking** | How the internet works - DNS, HTTP, the OSI model | [View](04-networking/README.md) |
| 05 | **Docker** | Containers, Compose, and a scaled multi-container app | [View](05-docker/README.md) |
| 06 | **AWS** | Four cloud builds - from a custom VPC to a serverless API | [View](06-aws/README.md) |
| 07 | **Terraform** | Infrastructure as Code - EC2, DNS, and remote state | [View](07-terraform/README.md) |
| 08 | **CI/CD** | GitHub Actions pipelines - lint, test, build, and deploy | [View](08-cicd/README.md) |
| 09 | **Kubernetes** | Container orchestration | *In progress* |

## Highlights

A few projects worth a look first:

- **Serverless REST API** *(06 - AWS)* - API Gateway → Lambda → DynamoDB, secured with least-privilege IAM, API keys, WAF, and a custom HTTPS domain.
- **Global Static Site + CI/CD** *(06 - AWS)* - S3 behind CloudFront over HTTPS, auto-deployed by GitHub Actions via OIDC.
- **WordPress on AWS with Terraform** *(07)* - a full LAMP + WordPress stack provisioned end-to-end as code, on a custom subdomain.
- **Flask Stack CI/CD to AWS** *(08)* - a Flask + Redis + nginx app built, pushed, and deployed to a Terraform-provisioned EC2 instance on every push.

## Repository Structure

```
devops-learning/
├── 01-linux/         # Linux fundamentals
├── 02-bash/          # Bash scripting
├── 03-git/           # Version control
├── 04-networking/    # How the internet works
├── 05-docker/        # Containers
├── 06-aws/           # Cloud (AWS)
├── 07-terraform/     # Infrastructure as Code
├── 08-cicd/          # CI/CD pipelines
├── 09-kubernetes/    # Container orchestration
└── challenges/       # Extra challenges
```

Each module contains a documented `README.md`, with `notes/`, `labs/`, and `projects/` where applicable.

## Progress

| Module | Status |
|--------|--------|
| 01 - Linux | ✅ Complete |
| 02 - Bash | ✅ Complete |
| 03 - Git | ✅ Complete |
| 04 - Networking | ✅ Complete |
| 05 - Docker | ✅ Complete |
| 06 - AWS | ✅ Complete |
| 07 - Terraform | ✅ Complete |
| 08 - CI/CD | ✅ Complete |
| 09 - Kubernetes | 🚧 In progress |
