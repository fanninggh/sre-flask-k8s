terraform {
  backend "s3" {
    bucket         = "sre-flask-k8s-tfstate"
    key            = "environments/dev/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "sre-flask-k8s-tflock"
    encrypt        = true
  }
}
