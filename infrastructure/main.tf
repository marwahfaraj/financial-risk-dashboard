# Define AWS provider
provider "aws" {
  region = "us-west-2"  # Change based on your region
}

# Create an S3 bucket for storing ML models
resource "aws_s3_bucket" "mlflow_bucket" {
  bucket = "finengine-mlflow-storage"
  acl    = "private"
}

# Create an EC2 instance for running ML models
resource "aws_instance" "ml_instance" {
  ami           = "ami-0c55b159cbfafe1f0" # Update with latest AWS AMI
  instance_type = "t3.medium"

  tags = {
    Name = "FinEngine-ML-Instance"
  }

  provisioner "file" {
    source      = "startup_script.sh"
    destination = "/home/ec2-user/startup_script.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /home/ec2-user/startup_script.sh",
      "bash /home/ec2-user/startup_script.sh"
    ]
  }
}

# Output the EC2 instance public IP
output "instance_ip" {
  value = aws_instance.ml_instance.public_ip
}
