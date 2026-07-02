# 04 - Networking

The fundamentals that connect everything - IP addressing, DNS, ports, protocols, and firewalls - applied to hosting a real website on AWS.

![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Amazon EC2](https://img.shields.io/badge/Amazon%20EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Cloudflare DNS](https://img.shields.io/badge/Cloudflare%20DNS-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)
![SSH](https://img.shields.io/badge/SSH-000000?style=for-the-badge&logo=openssh&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

Networking is the layer that lets machines find and talk to each other. Every request, like loading a web page, SSHing into a server, calling an API, travels the same path. A name is resolved to an IP address, a connection is opened to a specific port, a firewall decides whether to allow it, and a server responds. Understanding that path is foundational to everything else in DevOps, because when something breaks, it's usually one layer of it. This folder puts the theory into practice by hosting a live website end to end. A domain, a cloud server, a firewall, and a web server, all wired together and verified layer by layer.

## How Networking Works

- **IP addressing** - every device on a network has an **IP address**. Public IPs are reachable from the internet, and private IPs live inside a local network (like a VPC).
- **DNS** - the **Domain Name System** translates human-readable names (`nginx.biram.uk`) into IP addresses. An **A record** maps a name straight to an IPv4.
- **Ports** - a single server runs many services, each listening on a numbered **port** (80 for HTTP, 443 for HTTPS, 22 for SSH). The IP finds the machine and the port finds the service.
- **Protocols** - the rules for how data is exchanged. **TCP** gives ordered, reliable delivery (used by HTTP and SSH); **UDP** is faster but best-effort.
- **Firewalls** - a firewall (on AWS, a **security group**) decides which traffic is allowed in or out, by protocol, port, and source. It's deny-by-default, you open only what you need.

## Projects

| Project | What it builds | README |
|---------|----------------|--------|
| **Domain + EC2 + nginx** | An end-to-end web host - an Amazon Linux EC2 instance running nginx, locked down by a security group, and served over a custom subdomain via Cloudflare DNS - built and verified layer by layer | [View](projects/README.md) |

## What This Section Covers

- **IP addressing** - public vs private IPv4, and how an instance gets both
- **DNS** - A records, resolution, TTL, and DNS-only vs proxied (Cloudflare grey cloud vs orange cloud)
- **Ports & protocols** - TCP/UDP and the well-known ports (22 / 80 / 443)
- **Firewalls** - AWS security groups as a stateful, deny-by-default firewall scoped by CIDR
- **Web hosting** - installing and running nginx, and serving a page over both a raw IP and a domain
- **Remote access** - SSH key pairs and connecting to a cloud instance
- **Verification** - proving each layer works with `dig`, `nslookup`, and the browser

## Core Concepts

| Concept | What it is |
|---------|------------|
| IP address | The numeric address of a device on a network (e.g. `13.42.27.129`). Public IPs are internet-reachable; private IPs are internal. |
| DNS | The system that resolves human-readable names to IP addresses. |
| A record | A DNS record mapping a hostname directly to an IPv4 address. |
| CIDR | A notation for an IP range - `/32` is a single IP, `0.0.0.0/0` is everything. |
| Port | A numbered endpoint for a specific service on a host (80 = HTTP). |
| Protocol | The rules governing a connection - TCP (reliable) or UDP (fast, best-effort). |
| Security group | A stateful, deny-by-default firewall controlling inbound/outbound traffic on AWS. |
| TTL | How long a DNS record may be cached before resolvers re-check it. |

## Common Ports

| Port | Service |
|------|---------|
| 22 | SSH - encrypted remote shell |
| 53 | DNS - name resolution |
| 80 | HTTP - unencrypted web |
| 443 | HTTPS - encrypted web |

## Folder Structure

```
04-networking/
└── projects/
    ├── README.md       # Domain + EC2 + nginx (the full build walkthrough)
    └── screenshots/    # Step-by-step screenshots
```

## Key Commands

```bash
# ─── DNS resolution ───────────────────────────────────
dig nginx.biram.uk +short        # quick lookup - just the IP
dig nginx.biram.uk               # full answer (record, TTL, resolver)
nslookup nginx.biram.uk          # alternative DNS lookup

# ─── Connectivity & requests ──────────────────────────
ping <host>                      # check a host is reachable (ICMP)
curl -I http://nginx.biram.uk    # fetch just the HTTP response headers
curl http://<ip>                 # request a page by raw IP

# ─── Remote access ────────────────────────────────────
chmod 400 key.pem                # lock down the private key (required by ssh)
ssh -i key.pem ec2-user@<host>   # connect to the instance
```

## Core Building Block - Security Group Rules

On AWS, network access is controlled by a **security group** - a stateful, deny-by-default firewall. Each rule is a small, concrete unit: a protocol, a port, and a source. The rules from this folder's project:

| Type | Protocol | Port | Source | Why |
|------|----------|------|--------|-----|
| SSH | TCP | 22 | My IP (`/32`) | remote admin, locked to me only |
| HTTP | TCP | 80 | `0.0.0.0/0` | public web traffic |
| HTTPS | TCP | 443 | `0.0.0.0/0` | public web traffic (encrypted) |

Every rule needs a **protocol** (TCP/UDP), a **port**, and a **source CIDR** (`/32` = one IP, `0.0.0.0/0` = anywhere). Nothing is allowed until a rule explicitly permits it, so you expose the minimum. SSH to yourself, web ports to the world.

## Best Practices

- **Restrict SSH** - never open port 22 to `0.0.0.0/0`; limit it to your own IP (`/32`)
- **Expose the minimum** - open only the ports a service actually needs
- **Read the AWS warning correctly** - a `0.0.0.0/0` rule on web ports is expected; on SSH it's a red flag
- **Use DNS-only to verify origins** - Cloudflare's grey cloud resolves straight to your server, so you can confirm the record points where you think it does
- **Prefer HTTPS** - serve encrypted (443) for anything real; plain HTTP is for local testing
- **Protect keys and personal data** - `chmod 400` your `.pem`, never commit it, and redact your home IP from screenshots
- **Mind the TTL** - DNS changes propagate only as fast as the record's TTL allows
- **Tear down** - terminate EC2 instances and remove DNS records when you're done

## Resources

- [Cloudflare Learning - What is DNS?](https://www.cloudflare.com/learning/dns/what-is-dns/)
- [Cloudflare DNS Documentation](https://developers.cloudflare.com/dns/)
- [AWS - Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [MDN - An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- [nginx Documentation](https://nginx.org/en/docs/)