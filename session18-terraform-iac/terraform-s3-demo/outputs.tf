output "bucket_name" {
  description = "Unique S3 bucket name."
  value       = aws_s3_bucket.demo.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.demo.arn
}

output "bucket_region" {
  value = var.aws_region
}
