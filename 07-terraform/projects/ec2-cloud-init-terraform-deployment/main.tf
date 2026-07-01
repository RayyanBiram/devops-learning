# NOTE ON user_data vs user_data_base64:
# A single plain-text script could be passed with:
#   user_data = file("userdata.sh")
# Terraform base64-encodes plain user_data automatically before sending it to AWS.
#
# This build instead uses the cloudinit_config data source, which supports
# multi-part MIME configs and renders its output as base64 directly - so it's wired to
# user_data_base64, not user_data, to avoid double-encoding an already-encoded string.


resource "aws_instance" "nginx" {
    ami                    = var.ami_id
    instance_type          = var.instance_type
    vpc_security_group_ids = [aws_security_group.sg_nginx.id]
    user_data_base64       = data.cloudinit_config.ec2_userdata.rendered

    tags = {
      Name = "nginx instance"
    }
}

data "cloudinit_config" "ec2_userdata" {
    gzip          = true
    base64_encode = true
    part {
      content_type = "text/cloud-config"
      content = templatefile("${path.module}/cloud-config.yaml", {
      header: aws_security_group.sg_nginx.id
    })
    }
}

# Create security group for nginx with all inbound traffic through
# port 80 (HTTP). All outbound traffic allowed through on all ports
resource "aws_security_group" "sg_nginx" {

    ingress {
        description = "HTTP for nginx"
        from_port   = 80
        to_port     = 80
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
    Name = "sg_nginx"
  }
}

# Read from existing hosted zone
data "aws_route53_zone" "primary" {
  name = "aws.biram.uk"
}

# Create new A record in Route 53
resource "aws_route53_record" "nginx_dns" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = "nginx.aws.biram.uk"
  type    = "A"
  ttl     = 300
  records = [aws_instance.nginx.public_ip]
}