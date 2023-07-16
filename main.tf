provider "aws" {
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

//resource "aws_ecs_task_definition" "example_task" {
//  family                   = "example-task"
//  network_mode             = "awsvpc"
//  cpu                      = 1024
//  memory                   = 2048
//  requires_compatibilities = ["FARGATE"]
//
//  container_definitions = jsonencode([
//    {
//      name  = "container1"
//      image = "your-image-1:latest"
//      portMappings = [
//        {
//          containerPort = 80
//          hostPort      = 80
//        }
//      ]
//    },
//    {
//      name  = "container2"
//      image = "your-image-2:latest"
//      portMappings = [
//        {
//          containerPort = 8080
//          hostPort      = 8080
//        }
//      ]
//    }
//  ])
//}
//

