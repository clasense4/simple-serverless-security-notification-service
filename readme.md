# Sending security event to slack

## Introduction

Security is important. Using cloudtrail, cloudwatch and lambda, we are going to create a simple notification system when some security problem is arise.

This is what we are going to build

![](/diagrams-stage-1.png)

## Scenario

When these scenario below is happened, we will receive slack notification.

- A port 22 is open to 0.0.0.0/0 in any EC2 instance
- A new port is open beside port 80 and 443
- New IAM user is created and joined the Administrator Group
- New S3 bucket is public
- Root login detection