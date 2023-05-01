provider "aws" {
  access_key = "AKIA5Y43MDENAEQWDVU4"
  secret_key = "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"
  region = "us-west-2"
}

# vpc
resource "aws_vpc" "mainvpc" {
  cidr_block       = "172.31.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "firstvpc"
  }
}

# subnets of vpc above
resource "aws_subnet" "mainsub1" {
  vpc_id     = aws_vpc.mainvpc.id
  cidr_block = "172.31.32.0/20"
  availability_zone = "us-west-2b"
  map_public_ip_on_launch = true

}

resource "aws_subnet" "mainsub2" {
  vpc_id     = aws_vpc.mainvpc.id
  cidr_block = "172.31.16.0/20"
  availability_zone = "us-west-2a"
  map_public_ip_on_launch = true

}


resource "aws_instance" "my_instance" {
    ami = "ami-009c5f630e96948cb"
    associate_public_ip_address          = true
    availability_zone                    = "us-west-2a"
    cpu_core_count                       = 1
    cpu_threads_per_core                 = 1
    instance_type = "t2.micro"
    tags = {
      "Name" = "webserver2"
    }
}

# Create a new load balancer
resource "aws_lb" "bar" {
  name               = "newloadbalancer"
}

resource "aws_lb_target_group" "load_target" {
  name     = "finaltargetgroup"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.mainvpc.id
}



