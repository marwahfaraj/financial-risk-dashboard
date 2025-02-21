variable "db_username" {
  description = "MySQL database username"
  type        = string
}

variable "db_password" {
  description = "MySQL database password"
  type        = string
}

variable "groq_api_key" {
  description = "API key for Groq"
  type        = string
  sensitive   = true
}
