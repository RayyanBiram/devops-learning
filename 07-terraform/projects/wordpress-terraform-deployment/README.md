# WordPress on AWS with Terraform: EC2, Security Groups, User Data & Route 53 DNS - All as Code

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Amazon EC2](https://img.shields.io/badge/Amazon%20EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)
![Amazon Route 53](https://img.shields.io/badge/Amazon%20Route%2053-8C4FFF?style=for-the-badge&logo=amazonroute53&logoColor=white)
![WordPress](https://img.shields.io/badge/WordPress-21759B?style=for-the-badge&logo=wordpress&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GNU Bash](https://img.shields.io/badge/GNU%20Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)

A full WordPress stack on AWS, provisioned end-to-end with Terraform - no console clicking. Terraform creates an Ubuntu EC2 instance, a security group, a Route 53 DNS record, a user data script that installs the WordPress on first boot, and the site comes up on a custom subdomain over HTTP. State lives remotely in S3, so the whole thing is reproducible: one `apply` builds it, one `destroy` tears it down.

## What I Built

A single-instance WordPress deployment in the **eu-west-2** region, defined entirely as code. **Terraform** provisions every resource. An **EC2** instance runs the site, a **security group** controls traffic, a **user data** script installs and configures WordPress unattended on first boot, and **Route 53** maps a clean subdomain (`wordpress.aws.biram.uk`) to the instance. Terraform **state** is stored in an **S3 backend** rather than locally, so the configuration is reproducible and safe to collaborate on.

**Stack:**
- **Terraform** - provisions and manages every resource. One `apply` builds the whole stack, one `destroy` removes it
- **Amazon EC2** - a `t2.micro` Ubuntu instance that runs the WordPress site
- **Security Group** - a virtual firewall which allows inbound HTTP (port 80) and SSH (port 22) from anywhere and all outbound traffic
- **User data (cloud-init)** - a Bash script that runs once on first boot to install the LAMP stack and WordPress
- **Amazon Route 53** - DNS - an A record points `wordpress.aws.biram.uk` at the instance's public IP, referencing the existing hosted zone via a `data` source
- **Amazon S3** - remote backend storing `terraform.tfstate`, keeping state off the local machine
- **LAMP stack** - Linux + Apache + MySQL + PHP, the runtime WordPress needs


**How it actually works:**
- **Terraform applies the config.** Reading `provider.tf`, `variables.tf`, `main.tf`, and `outputs.tf`, Terraform creates the EC2 instance, the security group, and the DNS record in a single pass, tracking everything in remote S3 state.
- **The instance boots and self-installs.** On first boot the user data script runs as root: it updates packages, installs Apache, MySQL, and PHP, downloads WordPress, wires up the database, and writes `wp-config.php` - no SSH, no manual setup.
- **The site URL is locked in at provision time.** Before Apache restarts, the script injects `WP_HOME` and `WP_SITEURL` into `wp-config.php`, so WordPress answers on the domain name from the very first request instead of pinning itself to the raw IP.
- **DNS resolves the domain.** Route 53 answers `wordpress.aws.biram.uk` with the instance's public IP, so the site is reachable by name as well as by IP.
- **The security group lets traffic through.** Inbound port 80 is open so a browser anywhere can reach Apache; all outbound is allowed so the instance can pull packages and WordPress during install.

### Resources created

| Resource | Name | Detail |
|----------|------|--------|
| EC2 instance | `aws_instance.wordpress` | Ubuntu - `t2.micro` - eu-west-2 - runs the LAMP + WordPress stack |
| Security group | `aws_security_group.sg_wordpress` | Inbound `80/tcp` from `0.0.0.0/0` - all outbound allowed |
| Route 53 record | `aws_route53_record.wordpress_dns` | `A` record - `wordpress.aws.biram.uk` → instance public IP - TTL 300 |
| Route 53 zone *(data)* | `data.aws_route53_zone.primary` | Existing `aws.biram.uk` zone - referenced, **not** created |
| Remote state | S3 backend | bucket `terraform-state-rayyan` - key `terraform.tfstate` - eu-west-2 |

## Screenshots - quick reference

| # | Step | Screenshot |
|---|------|-----------|
| 1 | `terraform apply` complete, both output URLs printed | [View](screenshots/terminal_outputs.png) |
| 2 | WordPress live via **both** the IP and the domain | [GIF](screenshots/wordpress-ip-dns.gif) |

## Build Walkthrough

The stack file by file, in the order it comes together: the provider and remote state, the inputs, the install script, the compute and firewall, DNS, the outputs, and finally the deploy.

### 1. Provider and remote state - `provider.tf`

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.52.0"
    }
  }
  backend "s3" {
    bucket = "terraform-state-rayyan"
    key    = "terraform.tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
  region = "eu-west-2"
}
```

`required_providers` pins the **AWS provider** so the build is reproducible. The **S3 backend** keeps state remote - durable, shareable, and never accidentally committed to Git, unlike a local state file.

### 2. Input variables - `variables.tf`

```hcl
variable "instance_type" {
    type        = string
    description = "EC2 instance type"
}

variable "ami_id" {
    type        = string
    description = "AMI ID for the wordpress EC2 instances"
}
```

Variables hold the values most likely to change - instance type, ami id - so the config stays reusable without editing `main.tf`.

### 3. The user data script - `userdata.sh`

This is the script the instance runs on first boot. It installs the full **LAMP stack**, pulls down WordPress, configures the database, and writes `wp-config.php`:

```bash
#!/bin/bash
# ============================================================
# WordPress User Data Script – Ubuntu EC2
# LAMP Stack: Linux + Apache + MySQL + PHP
# ============================================================

# --- 1. Update the system ---
apt-get update -y
apt-get upgrade -y

# --- 2. Install Apache web server ---
apt-get install -y apache2
systemctl start apache2
systemctl enable apache2

# --- 3. Install MySQL server ---
apt-get install -y mysql-server
systemctl start mysql
systemctl enable mysql

# --- 4. Install PHP and required extensions for WordPress ---
apt-get install -y \
  php \
  php-mysql \
  php-curl \
  php-gd \
  php-xml \
  php-mbstring \
  php-xmlrpc \
  php-zip \
  libapache2-mod-php

# --- 5. Create the WordPress database and user ---
# These credentials are referenced again in wp-config.php below
DB_NAME="wordpress"
DB_USER="wp_user"
DB_PASSWORD="StrongPass123!"

mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

# --- 6. Download and extract WordPress ---
cd /tmp
wget -q https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz

# --- 7. Move WordPress files to Apache web root ---
cp -r wordpress/* /var/www/html/
# Remove the default Apache placeholder page
rm -f /var/www/html/index.html

# --- 8. Set correct file permissions ---
chown -R www-data:www-data /var/www/html/
chmod -R 755 /var/www/html/

# --- 9. Configure wp-config.php from the sample file ---
cp /var/www/html/wp-config-sample.php /var/www/html/wp-config.php

# Replace placeholder values with the actual DB credentials
sed -i "s/database_name_here/${DB_NAME}/"   /var/www/html/wp-config.php
sed -i "s/username_here/${DB_USER}/"        /var/www/html/wp-config.php
sed -i "s/password_here/${DB_PASSWORD}/"    /var/www/html/wp-config.php

# --- 10. Hardcoding the domain directly into the script so it works on startup  ---
sed -i "s|<?php|<?php\ndefine('WP_HOME','http://wordpress.aws.biram.uk');\ndefine('WP_SITEURL','http://wordpress.aws.biram.uk');|" /var/www/html/wp-config.php

# --- 11. Enable Apache mod_rewrite (needed for WordPress permalinks) ---
a2enmod rewrite

# Allow .htaccess overrides in the web root
sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf

# --- 12. Restart Apache to apply all changes ---
systemctl restart apache2
```

The part that matters most is **step 10**. WordPress pins its own site URL on first run, reached by raw IP first, it locks that IP in and then rejects requests by domain name. Injecting `WP_HOME` and `WP_SITEURL` at provision time fixes the URL up front, so the site works on `wordpress.aws.biram.uk` from the first request (full story in Challenges). Steps 1-5 stand up the runtime and create a dedicated DB user rather than running as MySQL root.

> **Note on credentials:** the DB password is hard-coded to keep the build self-contained. In production it would come from a `sensitive` variable or Secrets Manager, not the script.

### 4. EC2 instance and security group - `main.tf`

```hcl
# Create EC2 instance with user data installing wordpress 
resource "aws_instance" "wordpress" {
    ami           = var.ami_id
    instance_type = var.instance_type
    user_data = file("userdata.sh")
    vpc_security_group_ids = [aws_security_group.sg_wordpress.id]

    tags = {
        Name = "wordpress instance"
    }
}

# Create security group for wordpress with all inbound traffic through
# port 80 (HTTP) and port 22 (SSH) for troubleshooting.
# All outbound traffic allowed through on all ports
resource "aws_security_group" "sg_wordpress" {

    ingress {
        description = "HTTP for WordPress"
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"] 
    }

    ingress {
        description = "SSH for troubleshooting"
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"] 
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

  tags = {
    Name = "sg_wordpress"
  }
}
```

`file("userdata.sh")` passes the script to the instance as user data. `vpc_security_group_ids` is what actually **attaches** the security group - without it the group exists but does nothing. `protocol = "tcp"` is correct because security groups work at the transport layer. The port (80) is what makes it HTTP. Port 22 for SSH is also open for any troubleshooting. Egress `-1` (all protocols) lets the instance download packages and WordPress.

> **Note on SSH:** Port 22 is only open for troubleshooting purposes. In a real production environment, the EC2 instance would be configured behind a private subnet, accessed by external users only through an ALB. The only way to access would be via a bastion host with security groups set up for SSH access only from the  bastion host IP.

### 5. DNS with Route 53 - `main.tf`

```hcl
# Read from existing hosted zone
data "aws_route53_zone" "primary" {
  name = "aws.biram.uk"
}

# Create new A record in Route 53
resource "aws_route53_record" "wordpress_dns" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = "wordpress.aws.biram.uk"
  type    = "A"
  ttl     = 300
  records = [aws_instance.wordpress.public_ip]
}
```

The key choice is `data` vs `resource`. The `aws.biram.uk` zone already exists (delegated from Cloudflare), so a `data` source **references** it. A `resource` block would have created a second, orphaned zone with different nameservers - invisible to the internet and billed twice. The A record maps the subdomain to the instance IP with a short 300s TTL.

### 6. Outputs - `outputs.tf`

```hcl
output "instance_public_url_dns" {
  description = "WordPress URL via the Route 53 domain"
  value       = "http://${aws_route53_record.wordpress_dns.name}"
}

output "instance_public_url_ip" {
  description = "WordPress URL via the instance public IP"
  value       = "http://${aws_instance.wordpress.public_ip}"
}
```

Both outputs are formatted as full URLs, so the moment `apply` finishes the terminal prints two clickable links - domain and raw IP - with no console digging.

### 7. Deploy and verify

```bash
terraform init      # download the AWS provider and wire up the S3 backend
terraform plan      # preview what will be created
terraform apply     # build it
```

After `apply`, both URLs print in the outputs:

![terraform apply complete with output URLs](screenshots/terminal%20outputs.png)

And the site is live on **both** the public IP and the custom domain:

![WordPress live via IP and DNS](screenshots/wordpress-ip-dns.gif)

## Commands Used

```bash
# ─── Initialise: download the provider, wire up the S3 backend ────────
terraform init

# ─── Preview, then build the stack ────────────────────────────────────
terraform plan
terraform apply

# ─── Confirm the domain resolves to the instance's public IP ──────────
nslookup wordpress.aws.biram.uk

# ─── Tear everything down when finished ───────────────────────────────
terraform destroy
```

## What I Learnt

- **Resource vs data source** - a `resource` creates infrastructure, a `data` source only reads what already exists. Referencing the existing zone with `data` avoided creating a second one, with no ns records pointing to Cloudflare.
- **Remote state** - an S3 backend keeps `terraform.tfstate` durable, shareable, and out of Git, perfect for realtime production. Will have to implement DynamoDB in the future, which can help with state locking, so only one person at a time can `terraform apply`.
- **Security groups** - the `protocol` is transport-layer (`tcp` / `udp` / `-1`), and a group does nothing until it's attached via `vpc_security_group_ids`.
- **EC2 public IPs** - a default-VPC instance gets one automatically, but it changes on stop/start. An Elastic IP pins it.
- **WordPress URL lock-in** - WordPress fixes its site URL on first run, so `WP_HOME` / `WP_SITEURL` have to be set at provision time to serve on the domain.
- **DNS vs browser cache** - `nslookup` and the browser cache DNS separately, so a record can resolve correctly while a browser still hits a stale IP.

## Challenges & How I Solved Them

### 1. Invalid security group protocol
The first `apply` failed because the ingress rule used `protocol = "HTTP"`. Security groups don't understand application-layer names, they work at the transport layer.

**Solution:** changed the protocol to `tcp` and let the port number (80) define the traffic as HTTP. The rule then validated and applied cleanly.

### 2. Security group created but not attached
With the protocol fixed and applied, the site still wasn't reachable on port 80. Terraform had created the security group, but the EC2 instance wasn't actually using it.

**Solution:** added `vpc_security_group_ids = [aws_security_group.sg_wordpress.id]` to the instance. A security group only takes effect once it's explicitly attached. Defining it alongside the instance isn't the same as wiring it in.

### 3. Route 53 would have created a duplicate zone
The first DNS attempt used `resource "aws_route53_zone"` for `aws.biram.uk`, but that zone already exists, it's delegated to Route 53 from Cloudflare. A `resource` block would have created a **second** zone with its own nameservers, which the delegation doesn't point to, so the record would have been invisible to the internet (and billed as a duplicate).

**Solution:** switched to a `data "aws_route53_zone"` source to *reference* the existing zone, and added the A record into it. The record then landed in the live, delegated zone.

### 4. WordPress ignored the domain and only worked on the IP
DNS resolved correctly (`nslookup` returned the instance IP), but the site wouldn't load on `wordpress.aws.biram.uk`. WordPress had locked the raw IP into its config as the canonical site URL on first visit, and was redirecting away from the domain.

**Solution:** rather than patch a live box by hand, I baked the fix into the user data script. A `sed` line injecting `WP_HOME` and `WP_SITEURL` into `wp-config.php` before Apache starts. On a clean `destroy` + `apply`, the site came up correctly on the domain from first boot, with no manual step.

### 5. The browser kept serving a dead IP
After a rebuild the domain still failed in the normal browser even though `nslookup` was correct - but it worked perfectly in incognito. The browser and OS had cached the old DNS resolution from before the rebuild, pointing at a now-terminated instance.

**Solution:** flushed the DNS cache (`ipconfig /flushdns`, plus Chrome's `chrome://net-internals/#dns`) and did a hard refresh, which picked up the new IP. A clean reminder that "DNS is correct" and "my browser sees it" are two different things.

## Cleanup

Everything here is Terraform-managed, so teardown is a single command:

```bash
terraform destroy
```

This removes the EC2 instance, the security group, and the Route 53 A record in one pass. Two things deliberately survive:
- The **`aws.biram.uk` hosted zone** stays - it's referenced via a `data` source, not created here, so `destroy` leaves it untouched.
- The **S3 state bucket** (`terraform-state-rayyan`) isn't part of this configuration either, so it persists for future runs.

What actually costs money: effectively nothing once destroyed. While running, the `t2.micro` (free-tier eligible) and the shared Route 53 hosted zone (~$0.50/month) are the only charges.

## Files

- [`README.md`](README.md) - this file
- [`provider.tf`](provider.tf) - AWS provider and S3 remote-state backend
- [`variables.tf`](variables.tf) - input variables (instance type, AMI, region)
- [`main.tf`](main.tf) - EC2 instance, security group, and Route 53 record
- [`outputs.tf`](outputs.tf) - the IP and domain URLs printed after `apply`
- [`userdata.sh`](userdata.sh) - first-boot script installing the LAMP stack and WordPress
- [`.gitignore`](.gitignore) - excludes state, `.tfvars`, and the `.terraform` directory
- [`screenshots/`](screenshots/) - screenshots and the demo GIF referenced above