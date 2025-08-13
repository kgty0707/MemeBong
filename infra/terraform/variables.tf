variable "minio_endpoint" {
  type        = string
  description = "MinIO 서버 주소"
}

variable "minio_access_key" {
  type      = string
  sensitive = true
}

variable "minio_secret_key" {
  type      = string
  sensitive = true
}