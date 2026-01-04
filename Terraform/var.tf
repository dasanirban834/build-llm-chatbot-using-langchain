#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Variables of ALB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

variable "TG_conf" {
  type = object({
    name              = string
    port              = string
    protocol          = string
    target_type       = string
    enabled           = bool
    healthy_threshold = string
    interval          = string
    path              = string
  })
}

variable "ALB_conf" {
  type = object({
    name               = string
    internal           = bool
    load_balancer_type = string
    ip_address_type    = string
  })
}

variable "Listener_conf" {
  type = map(object({
    port     = string
    protocol = string
    type     = string
    priority = number
  }))
}

variable "alb_tags" {
  description = "provides the tags for ALB"
  type = object({
    Environment = string
    Email       = string
    Type        = string
    Owner       = string
  })
  default = {
    Email       = "dasanirban9019@gmail.com"
    Environment = "Dev"
    Owner       = "Anirban Das"
    Type        = "External"
  }
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Variables of ECR~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

variable "ecr_repo" {
  description = "Name of repository"
  default     = "streamlit-chatbot"
}

variable "ecr_tags" {
  type = map(any)
  default = {
    "AppName" = "StreamlitApp"
    "Env"     = "Dev"
  }
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Variables of ECS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "ecs_role" {
  description = "ecs roles"
  default     = "ecsTaskExecutionRole"
}

variable "ecs_details" {
  description = "details of ECS cluster"
  type = object({
    Name                           = string
    logging                        = string
    cloud_watch_encryption_enabled = bool
  })
}

variable "ecs_task_def" {
  description = "defines the configurations of task definition"
  type = object({
    family                   = string
    cont_name                = string
    cpu                      = number
    cpu_allocations          = number
    mem_allocations          = number
    memory                   = number
    essential                = bool
    logdriver                = string
    containerport            = number
    networkmode              = string
    requires_compatibilities = list(string)

  })
}


variable "cw_log_grp" {
  description = "defines the log group in cloudwatch"
  type        = string
  default     = ""
}

variable "kms_key" {
  description = "defines the kms key"
  type = object({
    description             = string
    deletion_window_in_days = number
  })
}

variable "custom_tags" {
  description = "defines common tags"
  type        = object({})
  default = {
    AppName = "StreamlitApp"
    Env     = "Dev"
  }
}

variable "ecs_task_count" {
  description = "ecs task count"
  type = number
  default = 2
}