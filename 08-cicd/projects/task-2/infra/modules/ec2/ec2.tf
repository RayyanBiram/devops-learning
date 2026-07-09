resource "aws_instance" "frn-app" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_pair
  user_data              = file("${path.module}/userdata.sh")
  vpc_security_group_ids = [aws_security_group.sg_frn-app.id]

  tags = {
    Name = "frn-app instance"
  }
}
