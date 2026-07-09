output "instance_public_ip" {
  description = "Public IPv4 of the EC2 instance"
  value       = module.ec2.instance_public_ip
}

output "instance_public_url_dns" {
    description = "Public URL of the EC2 instance"
    value       = module.ec2.instance_public_url_dns
}