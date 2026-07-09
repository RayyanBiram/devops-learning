output "instance_public_ip" {
  description = "Public IPv4 of the EC2 instance"
  value = "http://${aws_instance.frn-app.public_ip}"
}

output "instance_public_url_dns" {
    description = "Public URL of the EC2 instance"
    value       = "http://${aws_route53_record.frn-app_dns.name}"
}