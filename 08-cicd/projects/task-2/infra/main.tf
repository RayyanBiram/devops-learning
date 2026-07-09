module "ec2" {
  source        = "./modules/ec2"
  ami_id        = var.ami_id
  instance_type = var.instance_type
  my_ip         = var.my_ip
  key_pair      = var.key_pair
}