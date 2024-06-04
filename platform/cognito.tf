provider "aws" {
  region = "eu-west-1"
}

resource "aws_cognito_user_pool" "user_pool" {
  name = "local-dev-enworth-user-pool "

  # Additional configuration options for the user pool
  auto_verified_attributes = ["email"]

  password_policy {
    minimum_length    = 8
    require_uppercase = true
    require_lowercase = true
    require_numbers   = true
    require_symbols   = false
  }
}

resource "aws_cognito_user_pool_client" "user_pool_client" {
  name         = "local-dev-enworth-user-pool-client"
  user_pool_id   = aws_cognito_user_pool.user_pool.id
  generate_secret = false

  allowed_oauth_flows       = ["code"]
  allowed_oauth_scopes      = ["openid", "email", "profile"]
  callback_urls             = ["http://localhost:3000/"]
  logout_urls               = ["http://localhost:3000/"]
  supported_identity_providers = ["COGNITO"]

  explicit_auth_flows = [
    "ALLOW_USER_SRP_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH"
  ]
}

resource "aws_cognito_user_pool_domain" "user_pool_domain" {
  domain      = "local-dev-enworth-login"
  user_pool_id = aws_cognito_user_pool.user_pool.id
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.user_pool.id
}

output "cognito_user_pool_client_id" {
  value = aws_cognito_user_pool_client.user_pool_client.id
}

output "cognito_domain" {
  value = aws_cognito_user_pool_domain.user_pool_domain
}
