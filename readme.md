# Sending security event to slack

## Introduction

Security is important. Using cloudtrail, cloudwatch and lambda, we are going to create a simple security notification system when some security problem is arise.

This is what we are going to build

![](/diagrams-stage-1.png)

## Scenario

When these scenario below is happened, we will receive slack notification.

- A port 22 is open to 0.0.0.0/0 in any EC2 instance
- A new port is open beside port 80 and 443
- New IAM user is created and joined the Administrator Group
- New S3 bucket is public
- Root login detection

## Installation

Execute the `build.sh` and `deploy.sh`

## Demo

1. Execute terraform script under goat directory to create a new EC2 instance with bad Security Group
2. Login a new Root login account in other incognito tab
3. Add a new User using IAM and assign it to Administrator group
4. Show EC2 and Security Group Page
5. Show CloudTrail event page
6. Show Cloudwatch logs page
7. Show Lambda page