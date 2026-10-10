variable "aws_region" {
  description = "AWS region for the project."
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "Small Arm instance for this short demo."
  type        = string
  default     = "t4g.nano"
}

variable "bucket_prefix" {
  type    = string
  default = "kartik-session19-"
}
