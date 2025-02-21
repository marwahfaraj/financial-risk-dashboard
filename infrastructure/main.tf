provider "aws" {
  region = "us-west-2"  # Change to your preferred region
}

# 🔹 Create VPC
resource "aws_vpc" "finengine_vpc" {
  cidr_block = "10.0.0.0/16"
}

# 🔹 Create Security Group for EC2 & RDS
resource "aws_security_group" "finengine_sg" {
  vpc_id = aws_vpc.finengine_vpc.id

  # Allow inbound traffic to EC2 for Streamlit app
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow SSH access (Optional - for debugging)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 🔹 Create RDS MySQL Database
resource "aws_db_instance" "finengine_db" {
  allocated_storage    = 20
  engine              = "mysql"
  engine_version      = "8.0"
  instance_class      = "db.t3.micro"
  db_name             = "finengine_db"
  username           = var.db_username
  password           = var.db_password
  parameter_group_name = "default.mysql8.0"
  publicly_accessible = false
  vpc_security_group_ids = [aws_security_group.finengine_sg.id]
}

# 🔹 Create S3 Bucket for Financial Data Storage
resource "aws_s3_bucket" "finengine_bucket" {
  bucket = "finengine-financial-data"
  acl    = "private"
}

# 🔹 Create IAM Role for EC2
resource "aws_iam_role" "ec2_role" {
  name = "ec2_finengine_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# 🔹 Attach IAM Policy for S3 access
resource "aws_iam_policy" "s3_policy" {
  name        = "S3AccessPolicy"
  description = "Allows EC2 to access S3 bucket"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": ["arn:aws:s3:::finengine-financial-data", "arn:aws:s3:::finengine-financial-data/*"]
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "s3_attach" {
  policy_arn = aws_iam_policy.s3_policy.arn
  role       = aws_iam_role.ec2_role.name
}

# 🔹 Create EC2 Instance for Streamlit App
resource "aws_instance" "finengine_ec2" {
  ami                    = "ami-12345678"  # Use latest Ubuntu AMI
  instance_type          = "t3.micro"
  subnet_id              = aws_vpc.finengine_vpc.id
  vpc_security_group_ids = [aws_security_group.finengine_sg.id]

  iam_instance_profile = aws_iam_role.ec2_role.name

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install python3-pip -y
              pip3 install streamlit dotenv phi yfinance
              echo "GROQ_API_KEY=${var.groq_api_key}" > ~/.env
              echo "export GROQ_API_KEY=${var.groq_api_key}" >> ~/.bashrc
              source ~/.bashrc
              cd /home/ubuntu
              echo "Running Streamlit..."
              nohup streamlit run app.py &
              EOF

  tags = {
    Name = "FinEngine-Streamlit-Server"
  }
}
