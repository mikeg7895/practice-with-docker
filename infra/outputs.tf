output "instance_ip_addr_priv" {
  value = aws_instance.tasks.private_ip
}

output "instance_ip_addr_pub" {
  value = aws_instance.tasks.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.rds_postgres.endpoint
}
