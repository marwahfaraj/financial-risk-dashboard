output "ec2_public_ip" {
  description = "Public IP of the EC2 instance running Streamlit"
  value       = aws_instance.finengine_ec2.public_ip
}

output "rds_endpoint" {
  description = "RDS MySQL endpoint"
  value       = aws_db_instance.finengine_db.endpoint
}
