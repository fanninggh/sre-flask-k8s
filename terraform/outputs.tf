output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.flask.repository_url
}

output "apprunner_role_arn" {
  description = "App Runner ECR role ARN"
  value       = aws_iam_role.apprunner_ecr.arn
}

output "github_actions_role_arn" {
  description = "GitHub Actions deploy role ARN"
  value       = aws_iam_role.github_actions.arn
}
