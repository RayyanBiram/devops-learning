# Networking Module - Learning Notes
 
Notes covering the core concepts behind this module: IP addressing, DNS, ports, routing, hosting, and the AWS-specific pieces that come together in the project.
 
## IP addresses
 
An IP address is a numerical label that identifies a device on a network.
 
**IPv4** - the original format, 32-bit, written as four dotted decimals (e.g. `13.42.27.129`). About 4.3 billion total addresses, which the world has now exhausted.
 
**IPv6** — 128-bit, written as eight groups of four hex digits separated by colons. Effectively infinite address space. Adoption is partial - most internet traffic still rides on IPv4.
 
### Public vs private
 
- **Public IP** - globally routable, unique on the public internet. An EC2 instance's public IPv4 is in this category.
- **Private IP** - only valid inside a private network (a home LAN, an AWS VPC). RFC 1918 reserves three ranges for private use:
  - `10.0.0.0/8`
  - `172.16.0.0/12` - AWS default VPCs use this range (`172.31.0.0/16`)
  - `192.168.0.0/16`
The same private IP can exist in millions of separate networks at the same time; **NAT** (Network Address Translation) is what lets devices on private IPs share a single public IP to reach the internet.
 
### CIDR notation
 
`/24`, `/16`, `/32` describe how many bits of the address are "network" vs "host".
 
| CIDR | Means |
|------|-------|
| `13.42.27.129/32` | Exactly that one address |
| `192.168.1.0/24` | 256 addresses (`192.168.1.0` – `192.168.1.255`) |
| `10.0.0.0/8` | ~16.7 million addresses |
| `0.0.0.0/0` | The entire IPv4 internet — "anywhere" |
 
Security group rules use CIDR to specify allowed sources.
 
## DNS
 
DNS (Domain Name System) is the phone book of the internet - it maps domain names like `nginx.biram.uk` to IP addresses like `13.42.27.129`.
 
### Common record types
 
| Type | Purpose |
|------|---------|
| `A` | Maps a hostname to an IPv4 address |
| `AAAA` | Maps a hostname to an IPv6 address |
| `CNAME` | Alias from one hostname to another (e.g. `www.example.com` → `example.com`) |
| `MX` | Mail server for the domain |
| `TXT` | Arbitrary text — used for verification, SPF, DKIM, DMARC |
| `NS` | Which nameservers are authoritative for the domain |
 
### Resolution flow
 
When a browser visits `nginx.biram.uk`:
 
1. Browser checks its own cache.
2. OS checks its cache, then asks the configured resolver (often the ISP, or `1.1.1.1`, or `8.8.8.8`).
3. Resolver walks the chain:
   - Root nameservers ("who handles `.uk`?")
   - TLD nameservers ("who handles `biram.uk`?")
   - Authoritative nameservers for `biram.uk` (Cloudflare)
4. Cloudflare returns the A record value: `13.42.27.129`.
5. Browser opens a TCP connection to that IP on port 80.
### TTL and propagation
 
**TTL** (Time To Live) is how long a record can be cached, in seconds. Lower TTL = faster propagation of changes, higher load on DNS infrastructure. Cloudflare's "Auto" picks a sensible default.
 
When a record changes, every cache holding the old value has to expire it before clients see the new one. Cloudflare itself is near-instant; downstream caches depend on the TTL.
 
## Ports & protocols
 
A port is a number (0–65535) that distinguishes services running on the same IP.
 
### Well-known ports
 
| Port | Service |
|------|---------|
| 22 | SSH |
| 25 | SMTP (email sending) |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 6379 | Redis |
 
### TCP vs UDP
 
- **TCP** - reliable, ordered, connection-oriented. Used by HTTP, HTTPS, SSH, most database protocols.
- **UDP** - fire-and-forget, lower latency, no guaranteed delivery. Used by DNS queries, DHCP, video streaming, VoIP.
A connection is identified by the 4-tuple `(source IP, source port, destination IP, destination port)`. That's how a server can serve thousands of simultaneous clients from a single port - every connection's tuple is unique.
 
## Routing
 
Routing is how packets find their way from one network to another. A router looks at the destination IP, consults its routing table, and forwards the packet toward the next hop.
 
In AWS terms:
- A **VPC** is your own private network in the cloud.
- A **subnet** is a slice of that VPC, tied to one Availability Zone.
- A **route table** decides where traffic goes - including the default route (`0.0.0.0/0`) which points at an **internet gateway** for public subnets.
- An EC2 instance with a public IP in a public subnet can talk to the internet because that route exists. Without it, the instance is fully internal.
## Hosting basics
 
A web server is a process listening on a TCP port (usually 80 or 443) that speaks HTTP. nginx and Apache are the two best-known.
 
### Full request flow for `http://nginx.biram.uk`
 
1. Browser performs DNS lookup → gets `13.42.27.129`.
2. Browser opens a TCP connection to `13.42.27.129:80`.
3. Packet leaves the laptop, goes through the ISP, transits the internet, arrives at AWS's network.
4. AWS routes the packet into the VPC and to the instance's network interface (ENI).
5. The security group checks inbound rules - port 80 from `0.0.0.0/0` is allowed → permit.
6. nginx accepts the connection, parses the HTTP request, reads `/usr/share/nginx/html/index.html`, and sends it back.
7. Browser receives the bytes and renders them.
Every step is a layer that can break independently. That's why the right debugging approach is to test the raw IP first, *then* test the domain - splitting DNS problems from server problems.
 
### HTTP vs HTTPS
 
- **HTTP** sends everything in plaintext. Anyone on the network path can read it.
- **HTTPS** wraps HTTP in TLS, which encrypts the connection. Requires a certificate (free from Let's Encrypt) and listens on port 443.
- This project used HTTP only because TLS setup wasn't part of the brief. Port 443 was opened in the security group for future use.
## AWS-specific concepts
 
- **Region** - geographic area (`eu-west-2` = London). Latency, cost, and data-residency law all vary by region.
- **Availability Zone** - isolated datacenter within a region. AZs in the same region have low-latency links between them but are independently powered/networked for failure isolation.
- **VPC** - your virtual network in AWS. Every AWS account gets a default VPC per region; for projects beyond this level you'd build your own.
- **Subnet** - a slice of the VPC tied to one AZ. Subnets are either *public* (have a route to an internet gateway) or *private* (no direct internet route).
- **Security group** - stateful firewall attached to the instance's network interface. Deny-by-default inbound.
- **Key pair** - RSA public/private keypair for SSH. The `.pem` file is the private half. AWS never stores it; if you lose it, you lose access.
- **Public IPv4** - assigned at launch when `Auto-assign public IP = Enable`. Released when the instance is stopped or terminated. For a stable address use an **Elastic IP**.
- **AMI** (Amazon Machine Image) - the OS template the instance boots from. Amazon Linux, Ubuntu, Debian, Red Hat, Windows, etc.
## Useful commands learnt
 
```bash
# Service management (systemd)
sudo systemctl start <service>     # start now
sudo systemctl stop <service>      # stop now
sudo systemctl enable <service>    # start on boot
sudo systemctl disable <service>   # don't start on boot
sudo systemctl status <service>    # is it running?
sudo systemctl restart <service>   # stop + start
 
# Package management on Amazon Linux 2023
sudo dnf update                    # refresh metadata
sudo dnf install <pkg>             # install
sudo dnf remove <pkg>              # uninstall
sudo dnf search <term>             # find a package
 
# DNS troubleshooting
dig <hostname>                     # full DNS query
dig <hostname> +short              # just the answer
dig <hostname> @1.1.1.1            # query a specific resolver
nslookup <hostname>                # alternative tool, similar output
host <hostname>                    # even more concise output
 
# Connectivity testing
ping <host>                        # ICMP echo
curl -I http://<host>              # HTTP HEAD request, see status + headers
curl http://<host>                 # full response body
```