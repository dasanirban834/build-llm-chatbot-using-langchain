terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.17.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.7.1"
    }
  }
}

terraform {
  backend "s3" {
    bucket = "terraform0806"
    key    = "TerraformStateFiles1"
    region = "us-east-1"
  }
}


provider "aws" {
  # Configuration options
  region = "us-east-1"
}