#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Terraform/terraform.tfvars of ALB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

TG_conf = {
  enabled           = true
  healthy_threshold = "2"
  interval          = "30"
  name              = "ChatbotTG"
  port              = "8501"
  protocol          = "HTTP"
  target_type       = "ip"
  path              = "/"
}

ALB_conf = {
  internal           = false
  ip_address_type    = "ipv4"
  load_balancer_type = "application"
  name               = "ALB-Chatbot"
}

Listener_conf = {
  "1" = {
    port     = "80"
    priority = 100
    protocol = "HTTP"
    type     = "forward"
  }
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Terraform/terraform.tfvars of ECS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

ecs_details = {
  Name                           = "Chatbot"
  logging                        = "OVERRIDE"
  cloud_watch_encryption_enabled = true
}

ecs_task_def = {
  family                   = "custom-task-definition-chatbot"
  cont_name                = "streamlit-chatbot"
  cpu                      = 1024
  cpu_allocations          = 800
  memory                   = 3072
  mem_allocations          = 2000
  essential                = true
  logdriver                = "awslogs"
  containerport            = 8501
  networkmode              = "awsvpc"
  requires_compatibilities = ["FARGATE", ]
}


cw_log_grp = "cloudwatch-log-group-ecs-cluster-chatbot"

kms_key = {
  description             = "log group encryption"
  deletion_window_in_days = 7
}