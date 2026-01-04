# vpc details :

data "aws_vpc" "this_vpc" {
  state = "available"
  filter {
    name   = "tag:Name"
    values = ["custom-vpc"]
  }
}
# subnets details :

data "aws_subnet" "web_subnet_1a" {
  vpc_id = data.aws_vpc.this_vpc.id
  filter {
    name   = "tag:Name"
    values = ["weblayer-pub1-1a"]
  }
}

data "aws_subnet" "web_subnet_1b" {
  vpc_id = data.aws_vpc.this_vpc.id
  filter {
    name   = "tag:Name"
    values = ["weblayer-pub2-1b"]
  }
}

# ALB security group details :
data "aws_security_group" "ext_alb" {
  filter {
    name   = "tag:Name"
    values = ["ALBSG"]
  }
}

data "aws_security_group" "streamlit_app" {
  filter {
    name   = "tag:Name"
    values = ["StreamlitAppSG"]
  }
}