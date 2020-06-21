provider "aws" {
  region = "ap-southeast-1"
}

variable "project" {
  description = "Project Name"
  type        = string
  default     = "demo-aws-ug"
}

variable "webhook_url" {
  description = "Slack Webhook URL"
  type        = string
  default     = "https://hooks.slack.com/services/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"
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

resource "aws_cloudtrail" "trail" {
  name                          = var.project
  s3_bucket_name                = aws_s3_bucket.bucket.id
  cloud_watch_logs_group_arn    = aws_cloudwatch_log_group.log_group_trail.arn
  cloud_watch_logs_role_arn     = aws_iam_role.role_trail.arn
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

resource "aws_cloudwatch_log_group" "log_group_trail" {
  name = "${var.project}-trail"
}


resource "aws_iam_role" "role_trail" {
  name = "${var.project}-trail-role"

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
  role = aws_iam_role.role_trail.id
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {

      "Sid": "AWSCloudTrailCreateLogStream2014110",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream"
      ],
      "Resource": [
        "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:${aws_cloudwatch_log_group.log_group_trail.name}:log-stream:${data.aws_caller_identity.current.account_id}_CloudTrail_${data.aws_region.current.name}*"
      ]

    },
    {
      "Sid": "AWSCloudTrailPutLogEvents20141101",
      "Effect": "Allow",
      "Action": [
        "logs:PutLogEvents"
      ],
      "Resource": [
        "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:${aws_cloudwatch_log_group.log_group_trail.name}:log-stream:${data.aws_caller_identity.current.account_id}_CloudTrail_${data.aws_region.current.name}*"
      ]
    }
  ]
}
EOF
}

resource "aws_lambda_function" "lambda" {
  filename         = "lambda_package.zip"
  function_name    = "${var.project}-lambda"
  role             = aws_iam_role.role_lambda.arn
  handler          = "main.lambda_handler"
  source_code_hash = filebase64sha256("lambda_package.zip")
  runtime          = "python3.8"
  timeout          = 1
  memory_size      = 128
  layers           = ["${aws_lambda_layer_version.layer.arn}"]

  environment {
    variables = {
      WEBHOOK_URL = var.webhook_url
    }
  }
}

resource "aws_lambda_layer_version" "layer" {
  filename            = "layer.zip"
  layer_name          = "${var.project}-layer"
  source_code_hash    = filebase64sha256("layer.zip")
  compatible_runtimes = ["python3.6", "python3.7", "python3.8"]
}

resource "aws_cloudwatch_log_subscription_filter" "lambda_cloudwatch" {
  name            = "${var.project}-lambda"
  log_group_name  = aws_cloudwatch_log_group.log_group_trail.name
  filter_pattern  = ""
  destination_arn = aws_lambda_function.lambda.arn
}

resource "aws_lambda_permission" "test-app-allow-cloudwatch" {
  statement_id  = "test-app-allow-cloudwatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.arn
  principal     = "logs.amazonaws.com"
  source_arn    = aws_cloudwatch_log_group.log_group_trail.arn
}

resource "aws_cloudwatch_log_group" "log_group_lambda" {
  name = "/aws/lambda/${var.project}-lambda"
}

resource "aws_iam_role" "role_lambda" {
  name = "${var.project}-lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "policy_lambda" {
  name = "${var.project}-lambda-policy"
  role = aws_iam_role.role_lambda.id
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "${aws_cloudwatch_log_group.log_group_lambda.arn}"
            ]
        }
    ]
}
EOF
}