terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.52.0"
    }
  }
  backend "s3" {
    bucket = "terraform-state-rayyan"
    key    = "terraform.tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
    region = "eu-west-2"
}

