variable "ami_id" {
  description = "AMI ID of the EC2 instance"
}

variable "instance_type" {
  description = "Instance type of the EC2 instance"
}

variable "key_pair" {
  description = "Key pair for SSH access to the EC2 instance"
}

variable "my_ip" {
  description = "My public IP"
}