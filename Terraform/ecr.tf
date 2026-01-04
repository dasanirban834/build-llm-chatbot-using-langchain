#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~AWS ECR Repository~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

resource "aws_ecr_repository" "aws-ecr" {
  name = var.ecr_repo
  tags = var.ecr_tags
}
