# Simple Serverless Security Notification Service

## Introduction

Security is important. Using [CloudTrail](https://aws.amazon.com/cloudtrail/), [CloudWatch](https://aws.amazon.com/cloudwatch/) and [Lambda](https://aws.amazon.com/lambda/), we are going to create a simple security notification service when security issue is detected.

This is what we are going to build

![](/diagrams-stage-1.png)

[Link to presentation](https://docs.google.com/presentation/d/1W0JBZd3thWOEKqUAZUWeg2kQC-5evfy-LnnLZQ3ReTs/edit?usp=sharing)

[Link to recording](https://www.youtube.com/watch?v=Vq7n4s5vlxk)

## Rules

When these rules below is detected, we will receive slack notification within several minutes, approximately within 15 minutes.

- A port 22 is open to 0.0.0.0/0 in any EC2 instance
- A new port is open beside port 80 and 443
- New IAM user is created and joined the Administrator Group
- A user login as Root

The rules is created using [Jmespath](https://jmespath.org/). Take a look at `src/example-events` directory to try the example events from Cloudtrail with the rule.

## Installation

```
export AWS_PROFILE=YOUR_PROFILE AWS_DEFAULT_REGION="ap-southeast-1"
terraform init
./deploy.sh
```

## Goat

The name is coming from Jurassic Park scene where the goat is feed to T-Rex. This means, goat is a vulnerable things. The terraform script will create an EC2 instance with several dangerous port is open to world.

```
cd goat
terraform init
terraform plan
terraform apply -auto-approve
```
