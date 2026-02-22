#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~AWS ECS Cluster~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

resource "aws_ecs_cluster" "aws-ecs-cluster" {
  name = var.ecs_details["Name"]
  configuration {
    execute_command_configuration {
      kms_key_id = aws_kms_key.kms.arn
      logging    = var.ecs_details["logging"]
      log_configuration {
        cloud_watch_encryption_enabled = true
        cloud_watch_log_group_name     = aws_cloudwatch_log_group.log-group.name
      }
    }
  }
  tags = var.custom_tags
}

resource "aws_ecs_task_definition" "taskdef" {
  family = var.ecs_task_def["family"]
  container_definitions = jsonencode([
    {
      "name" : "${var.ecs_task_def["cont_name"]}",
      "image" : "${aws_ecr_repository.aws-ecr.repository_url}:v3",
      "entrypoint" : [],
      "essential" : "${var.ecs_task_def["essential"]}",
      "logConfiguration" : {
        "logDriver" : "${var.ecs_task_def["logdriver"]}",
        "options" : {
          "awslogs-group" : "${aws_cloudwatch_log_group.log-group.id}",
          "awslogs-region" : "${var.region}",
          "awslogs-stream-prefix" : "app-dev"
        }
      },
      "portMappings" : [
        {
          "containerPort" : "${var.ecs_task_def["containerport"]}",
        }
      ],
      "cpu" : "${var.ecs_task_def["cpu_allocations"]}",
      "memory" : "${var.ecs_task_def["mem_allocations"]}",
      "networkMode" : "${var.ecs_task_def["networkmode"]}"
    }
  ])

  requires_compatibilities = var.ecs_task_def["requires_compatibilities"]
  network_mode             = var.ecs_task_def["networkmode"]
  memory                   = var.ecs_task_def["memory"]
  cpu                      = var.ecs_task_def["cpu"]
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole.arn
  task_role_arn            = aws_iam_role.ecsTaskExecutionRole.arn
  tags = var.custom_tags
}



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~AWS CloudWatch Log Group~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

resource "aws_cloudwatch_log_group" "log-group" {
  name = var.cw_log_grp
  tags = var.custom_tags
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~AWS KMS Key~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

resource "aws_kms_key" "kms" {
  description             = var.kms_key["description"]
  deletion_window_in_days = var.kms_key["deletion_window_in_days"]
  tags                    = var.custom_tags
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ECS Service~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

resource "aws_ecs_service" "streamlit" {
  name            = "service-chatbot"
  cluster         = aws_ecs_cluster.aws-ecs-cluster.id
  task_definition = aws_ecs_task_definition.taskdef.arn
  desired_count   = var.ecs_task_count
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.this_tg.arn
    container_name = "${var.ecs_task_def["cont_name"]}"
    container_port = "${var.ecs_task_def["containerport"]}"
  }

  network_configuration {
    assign_public_ip = true
    subnets = [data.aws_subnet.web_subnet_1a.id, data.aws_subnet.web_subnet_1b.id]
    security_groups = [data.aws_security_group.streamlit_app.id]
  }

}

