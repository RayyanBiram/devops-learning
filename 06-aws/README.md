# 06 - AWS

Cloud infrastructure on Amazon Web Services - the most widely used cloud platform, covered from a custom network up to a serverless API.

![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Amazon EC2](https://img.shields.io/badge/Amazon%20EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)
![Amazon CloudFront](https://img.shields.io/badge/Amazon%20CloudFront-8C4FFF?style=for-the-badge&logo=amazoncloudfront&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white)
![Amazon API Gateway](https://img.shields.io/badge/API%20Gateway-FF4F8B?style=for-the-badge&logo=amazonapigateway&logoColor=white)
![Amazon DynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=amazondynamodb&logoColor=white)
![Amazon Route 53](https://img.shields.io/badge/Amazon%20Route%2053-8C4FFF?style=for-the-badge&logo=amazonroute53&logoColor=white)
![AWS IAM](https://img.shields.io/badge/AWS%20IAM-DD344C?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Amazon CloudWatch](https://img.shields.io/badge/Amazon%20CloudWatch-FF4F8B?style=for-the-badge&logo=amazoncloudwatch&logoColor=white)

Amazon Web Services (AWS) is the world's most widely used cloud platform, on-demand access to compute, storage, networking, databases, and hundreds of other services, rented by the second rather than bought as hardware. Instead of racking your own servers, you provision exactly what you need through a web console, a command-line tool, or Infrastructure as Code, and you pay only for what you run. This repo contains four production-shaped AWS builds, each designed, deployed, and documented in full, from a custom network at the bottom to a serverless API at the top.

## How AWS Works

- **Regions & Availability Zones** - AWS runs in geographic **regions** (e.g. `eu-west-2` London, `us-east-1` N. Virginia), each split into isolated data centres called **Availability Zones (AZs)**. Spreading across AZs is how you build for high availability.
- **Services on demand** - every capability (a server, a bucket, a database) is a **service** you create in minutes and delete when done. Nothing is pre-owned.
- **IAM governs everything** - every action is allowed or denied by **Identity and Access Management**. The golden rule is **least-privilege**: grant only what's needed, nothing more.
- **Pay-as-you-go** - you're billed for what you run, so idle resources still cost money until you tear them down.
- **Many front doors** - interact through the web **Console**, the **AWS CLI**, or **Infrastructure as Code** (Terraform, CloudFormation).

## Projects

| Project | What it deploys | README |
|---------|-----------------|--------|
| **Custom VPC Networking** | A network built from scratch - public and private subnets, an internet gateway and NAT gateway, route tables, and security-group chaining, with a bastion host reaching a locked-down private instance | [View](projects/assignment-1-vpc-networking/README.md) |
| **Highly Available Web Tier** | An Application Load Balancer spreading traffic across two AZs to an Auto Scaling Group of EC2 web servers - instances reachable only through the ALB, with HTTPS via ACM and a Route 53 domain | [View](projects/assignment-2-application-load-balancer/README.md) |
| **Global Static Site + CI/CD** | An S3-hosted site behind the CloudFront CDN over HTTPS, auto-deployed by GitHub Actions (OIDC), with security headers via CloudFront Functions and URL rewrites via Lambda@Edge | [View](projects/assignment-3-s3-cloudfront-cdn-route53/README.md) |
| **Serverless REST API** | API Gateway → Lambda (Python) → DynamoDB, secured with least-privilege IAM, API keys + usage plans, a WAF rate-limit rule, and a custom HTTPS domain | [View](projects/assignment-4-lambda-iam-api-gateway/README.md) |

## What This Section Covers

- **Compute** - EC2 virtual machines and serverless AWS Lambda functions
- **Networking** - custom VPCs, public/private subnets, internet and NAT gateways, security groups, Application Load Balancers, and Route 53 DNS
- **Storage & databases** - S3 object storage and DynamoDB (NoSQL)
- **Content delivery & edge** - the CloudFront CDN, CloudFront Functions, and Lambda@Edge
- **Security** - IAM least-privilege roles and policies, security-group isolation, AWS WAF, and HTTPS with ACM certificates
- **Automation** - CI/CD with GitHub Actions authenticating via OIDC (no stored credentials)
- **Observability** - CloudWatch logs and metrics for debugging and monitoring

## Key Services

| Service | Purpose |
|---------|---------|
| EC2 | Virtual machines (servers) |
| VPC | Isolated virtual network |
| S3 | Object storage |
| CloudFront | Global content delivery network (CDN) |
| Lambda | Serverless functions |
| API Gateway | Managed REST / HTTP APIs |
| DynamoDB | Managed NoSQL database |
| Route 53 | DNS and domain routing |
| IAM | Identity and access management |
| CloudWatch | Monitoring, logs, and metrics |
| ACM | TLS/SSL certificates for HTTPS |
| WAF | Web application firewall |

## Folder Structure

```
06-aws/       
└── projects/
    ├── .github/workflows                        # GitHub Actions deploy.yml file
    ├── assignment-1-vpc-networking/             # Custom VPC (subnets, IGW, NAT, security groups)
    ├── assignment-2-application-load-balancer/  # ALB + Auto Scaling web tier
    ├── assignment-3-s3-cloudfront-cdn-route53/  # Static site + CloudFront + CI/CD
    └── assignment-4-lambda-iam-api-gateway/     # Serverless REST API (API Gateway + Lambda + DynamoDB)
```

## Key Commands

```bash
aws configure                                   # set up credentials, default region, and output format
aws sts get-caller-identity                     # check which identity you're using
aws ec2 describe-instances                      # list EC2 instances
aws s3 ls                                       # list S3 buckets
aws s3 sync ./site s3://my-bucket               # sync a local folder to a bucket
aws dynamodb scan --table-name students         # read every item in a DynamoDB table
aws logs tail /aws/lambda/<function> --follow   # tail a Lambda's CloudWatch logs
```

## Core Building Block - IAM Policies

Across every project in this folder, access is governed by **IAM policies**. They all share the same JSON shape:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

Every statement answers three questions: **Effect** (Allow or Deny), **Action** (which API calls, e.g. `s3:GetObject`), and **Resource** (which ARN it applies to). Scoping these tightly - one action, one resource - is least-privilege in practice, and it's how permissions are controlled in each build here.

## Quick Start

```bash
# 1. Install and configure the AWS CLI
aws configure                 # access key, secret key, region (e.g. eu-west-2), output format

# 2. Confirm you're authenticated
aws sts get-caller-identity

# 3. Open a project and follow its README
cd projects/assignment-1-vpc-networking     # or any project in the table above
```

Each project is built through the AWS Console and documented step by step in its own README, with architecture diagrams and screenshots. (Most were built in `us-east-1` or `eu-west-2`.)

## Cost Warning

AWS bills for what you run, and some resources cost money even while idle. Always:

- Prefer **Free Tier**-eligible resources while learning
- Set up **billing alerts** with AWS Budgets
- **Tear down** resources when finished - NAT gateways, load balancers, and Route 53 hosted zones bill hourly or monthly even with no traffic
- Check the **Pricing Calculator** before creating anything large

## Best Practices

- **Least-privilege IAM** - grant only the actions a role needs; never use `*:*`
- **No long-lived credentials** - use IAM roles and OIDC instead of access keys in code
- **Enable MFA** and avoid using the root account for day-to-day work
- **Spread across Availability Zones** for high availability
- **Tag resources** so they're easy to find, track, and clean up
- **Encrypt** in transit (HTTPS via ACM) and at rest
- **Automate** with Infrastructure as Code and CI/CD over manual console clicks
- **Watch billing** and destroy what you're not using

## Resources

- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)