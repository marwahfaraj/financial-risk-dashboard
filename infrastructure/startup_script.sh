#!/bin/bash
# Update and install dependencies
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -aG docker ec2-user

# Install Python and Pip
sudo yum install -y python3
python3 -m ensurepip --default-pip
pip3 install --upgrade pip

# Install project dependencies
pip3 install -r requirements.txt

# Start Streamlit dashboard
nohup streamlit run app.py --server.port 8501 &
