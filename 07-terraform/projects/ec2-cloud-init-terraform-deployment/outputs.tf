output "instance_public_url_ip" {
    description = "Public IPv4 of the EC2 instance"
    value       = "http://${aws_instance.nginx.public_ip}"
}

output "instance_public_url_dns" {
    description = "Public URL of the EC2 instance"
    value       = "http://${aws_route53_record.nginx_dns.name}"
}