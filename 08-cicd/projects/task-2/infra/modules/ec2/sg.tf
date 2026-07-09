data "aws_vpc" "default" { 
  default = true 
  }

resource "aws_security_group" "sg_frn-app" {
  vpc_id = data.aws_vpc.default.id

    ingress {
      description = "Open Docker + HTTP for frn-app"
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
      Name = "sg_frn-app"
    }
}