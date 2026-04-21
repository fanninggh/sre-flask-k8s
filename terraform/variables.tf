variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "account_id" {
  description = "AWS account ID"
  type        = string
  default     = "779846820095"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "flask-devops"
}

variable "github_repo" {
  description = "GitHub repository"
  type        = string
  default     = "fanninggh/sre-flask-k8s"
}
