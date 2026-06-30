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