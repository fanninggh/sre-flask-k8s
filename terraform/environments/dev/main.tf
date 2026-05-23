terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket       = "sre-flask-k8s-tfstate"
    key          = "environments/dev/terraform.tfstate"
    region       = "eu-west-1"
    use_lockfile = true
    encrypt      = true
  }
}

provider "aws" {
  region = var.aws_region
}

module "networking" {
  source      = "../../modules/networking"
  project     = var.project
  environment = var.environment
}

module "ecr" {
  source      = "../../modules/ecr"
  project     = var.project
  environment = var.environment
  services    = ["flask-app"]
}

module "eks" {
  source      = "../../modules/eks"
  project     = var.project
  environment = var.environment

  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.public_subnet_ids

  cluster_version    = "1.31"
  node_instance_type = "t3.small"
  node_min_size      = 1
  node_max_size      = 2
  node_desired_size  = 1

  ecr_repository_arns = values(module.ecr.repository_arns)
}
