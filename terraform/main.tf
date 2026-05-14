provider "aws" {
  region = "eu-central-1"
}

# 1. Căutăm automat ultima versiune de Ubuntu 22.04 LTS
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # ID-ul oficial al contului Canonical (creatorii Ubuntu)

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# 2. Creăm Firewall-ul (Security Group)
resource "aws_security_group" "iot_sg" {
  name        = "iot_licenta_sg"
  description = "Permite trafic pentru SSH, Web Flask si MQTT"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 1883
    to_port     = 1883
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. Creăm Mașina Virtuală (EC2 Instance)
resource "aws_instance" "iot_server" {
  ami           = data.aws_ami.ubuntu.id  # Aici folosim ID-ul găsit automat mai sus!
  instance_type = "t3.micro"
  
  key_name      = "cheie_licenta"

  vpc_security_group_ids = [aws_security_group.iot_sg.id]

  tags = {
    Name = "Server_IoT_Licenta"
  }
}

# 4. Afișăm IP-ul public
output "server_ip" {
  value       = aws_instance.iot_server.public_ip
  description = "Adresa IP publica a serverului din AWS"
}