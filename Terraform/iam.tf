resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = var.ecs_role
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

locals {
  policy_arn = [
    "arn:aws:iam::aws:policy/AdministratorAccess",
    "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role",
    "arn:aws:iam::669122243705:policy/CustomPolicyECS"
  ]
}
resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  count      = length(local.policy_arn)
  role       = aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = element(local.policy_arn, count.index)
}