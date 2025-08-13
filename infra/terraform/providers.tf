terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    minio = {
      source  = "aminueza/minio"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = "ap-northeast-2"
}

provider "minio" {
  minio_server           = var.minio_endpoint
  minio_user             = var.minio_access_key
  minio_password         = var.minio_secret_key
  minio_api_version      = "v4"
  minio_ssl              = false
}