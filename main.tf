provider "aws" {
  region = "ap-southeast-1"
}

variable "project" {
  description = "Project Name"
  type        = string
  default     = "aws-ug-demo"
}

data "aws_caller_identity" "current" {}

resource "aws_cloudtrail" "trail" {
  name                          = var.project
  s3_bucket_name                = aws_s3_bucket.bucket.id
  include_global_service_events = false
  cloud_watch_logs_group_arn    = aws_cloudwatch_log_group.log_group.arn
  cloud_watch_logs_role_arn     = aws_iam_role.role.arn
}

resource "aws_s3_bucket" "bucket" {
  bucket        = "${var.project}-trail"
  force_destroy = true

  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck",
            "Effect": "Allow",
            "Principal": {
              "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::${var.project}-trail"
        },
        {
            "Sid": "AWSCloudTrailWrite",
            "Effect": "Allow",
            "Principal": {
              "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::${var.project}-trail/AWSLogs/${data.aws_caller_identity.current.account_id}/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
}
POLICY
}

resource "aws_cloudwatch_log_group" "log_group" {
  name = var.project
}

resource "aws_iam_role" "role" {
  name = "${var.project}-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "policy" {
  name = "${var.project}-policy"
  role = aws_iam_role.role.id
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream"
            ],
            "Resource": [
                "${aws_cloudwatch_log_group.log_group.arn}"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:PutLogEvents"
            ],
            "Resource": [
                "${aws_cloudwatch_log_group.log_group.arn}"
            ]
        }
    ]
}
EOF
}