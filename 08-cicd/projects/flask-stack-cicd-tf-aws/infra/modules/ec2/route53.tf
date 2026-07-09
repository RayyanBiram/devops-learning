# Read from existing hosted zone
data "aws_route53_zone" "frn-app_dns" {
  name = "aws.biram.uk"
}

# Create new A record in Route 53
resource "aws_route53_record" "frn-app_dns" {
  zone_id = data.aws_route53_zone.frn-app_dns.zone_id
  name    = "frn.aws.biram.uk"
  type    = "A"
  ttl     = 300
  records = [aws_instance.frn-app.public_ip]
}