variable "aws_region" {
  description = "AWS region for the demo."
  type        = string
  default     = "ap-south-1"
}

variable "bucket_prefix" {
  description = "Terraform adds a unique suffix to this bucket prefix."
  type        = string
  default     = "kartik-session18-"
}
