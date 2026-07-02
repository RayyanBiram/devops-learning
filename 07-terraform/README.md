# 07 - Terraform

Infrastructure as Code (IaC) on AWS - infrastructure defined in code, version-controlled, and deployed with a single command.

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Amazon EC2](https://img.shields.io/badge/Amazon%20EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)
![cloud-init](https://img.shields.io/badge/cloud--init-F5C211?style=for-the-badge&logo=cloudinit&logoColor=black)
![Amazon Linux 2023](https://img.shields.io/badge/Amazon%20Linux%202023-232F3E?style=for-the-badge&logo=amazonlinux&logoColor=white)
![Amazon Route 53](https://img.shields.io/badge/Amazon%20Route%2053-8C4FFF?style=for-the-badge&logo=amazonroute53&logoColor=white)
![WordPress](https://img.shields.io/badge/WordPress-21759B?style=for-the-badge&logo=wordpress&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GNU Bash](https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)

Terraform is HashiCorp's Infrastructure as Code tool. Instead of clicking through a cloud console, you declare the infrastructure you want in configuration files (HCL), and Terraform works out how to create, change, or destroy resources to match. Due to the config being just code, it's version-controlled, reviewable, and reproducible, the same files build the same infrastructure every time. This is why we call Terraform idempotent. This folder contains two AWS builds, each provisioned end-to-end with Terraform and documented in full.

## How Terraform Works

- **Declare** the desired state in `.tf` files - providers, resources, variables, outputs.
- **`init`** downloads the providers and wires up the backend where state is stored.
- **`plan`** compares your config against reality and previews exactly what will change.
- **`apply`** makes it happen, then records what it built in the **state** file - Terraform's memory of the real infrastructure.
- **`destroy`** reads that state to tear everything back down cleanly.

## Projects

| Project | What it deploys | README |
|---------|-----------------|--------|
| **WordPress on AWS** | A full WordPress stack on an Ubuntu EC2 instance - security group, user data install, Route 53 DNS, remote S3 state | [View](projects/wordpress-terraform-deployment/README.md) |
| **EC2 with cloud-init (NGINX)** | An Amazon Linux 2023 instance running NGINX, configured entirely by cloud-init and passed via `user_data_base64` | [View](projects/ec2-cloud-init-terraform-deployment/README.md) |

## What This Section Covers

- **Providers and resources** - the AWS (and cloudinit) providers, and resources like EC2 instances, security groups, and DNS records
- **Variables and outputs** - inputs that keep configs reusable, and outputs that surface live values like the public URL
- **Data sources** - reading existing infrastructure (an existing Route 53 zone) instead of recreating it
- **Remote state** - storing `terraform.tfstate` in an S3 backend rather than on the local machine
- **User data and cloud-init** - bootstrapping instances on first boot, both via a plain `user_data` script and via a `cloudinit_config` payload on `user_data_base64`
- **DNS with Route 53** - mapping clean subdomains to instances with A records

## Folder Structure

```
07-terraform/
└── projects/
    ├── wordpress-terraform-deployment/        # WordPress on AWS (EC2 + security group + Route 53)
    └── ec2-cloud-init-terraform-deployment/    # NGINX via cloud-init (user_data_base64)
```

## Key Commands

```bash
terraform init       # initialise the working directory (providers + backend)
terraform plan       # preview changes before applying
terraform apply      # create or update infrastructure
terraform destroy    # tear infrastructure back down
terraform fmt        # format the code to canonical style
terraform validate   # check the configuration is valid
terraform state list # list the resources Terraform is tracking
```

## Basic Structure

```hcl
# provider.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# variables.tf
variable "region" {
  type    = string
  default = "eu-west-2"
}

# main.tf
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = "web-server"
  }
}

# outputs.tf
output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

## Quick Start

```bash
cd projects/wordpress...      # or projects/ec2-cloud-init...
terraform init
terraform plan
terraform apply
```

Each project supplies its own values through a `terraform.tfvars` file (ignored by Git), so you provide the AMI and instance type at run time.

## Best Practices

- Store state remotely (S3), and add **DynamoDB for state locking** so only one `apply` runs at a time
- Never commit `.tfstate` or `.tfvars` files - they hold live state and secrets
- Use variables for anything environment-specific
- Reference existing infrastructure with **data sources** rather than recreating it
- Break reusable pieces into **modules**
- Run `terraform fmt` and `terraform validate` before committing
- **Pin provider versions** so builds stay reproducible

## Resources

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)