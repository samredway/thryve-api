provider "aws" {
  region = "eu-west-1"  # Adjust the region as needed
}

resource "aws_cognito_user_pool" "user_pool" {
  name = "local-dev-enworth-user-pool"

  # Password policy
  password_policy {
    minimum_length    = 8
    require_uppercase = true
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    temporary_password_validity_days = 7
  }

  deletion_protection = "ACTIVE"

  # Auto-verified attributes
  auto_verified_attributes = ["email"]

  # Username attributes
  username_attributes = ["email"]

  # Verification message template
  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
  }

  # User attribute update settings
  user_attribute_update_settings {
    attributes_require_verification_before_update = ["email"]
  }

  mfa_configuration = "OFF"

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  admin_create_user_config {
    allow_admin_create_user_only     = false
  }

  username_configuration {
    case_sensitive = false
  }

  account_recovery_setting {
    recovery_mechanism {
      priority = 1
      name     = "verified_email"
    }
  }

  schema {
    name                  = "email"
    attribute_data_type   = "String"
    developer_only_attribute = false
    mutable               = true
    required              = true
    string_attribute_constraints {
      min_length = "0"
      max_length = "2048"
    }
  }

  schema {
    name                  = "email_verified"
    attribute_data_type   = "Boolean"
    developer_only_attribute = false
    mutable               = true
    required              = false
  }

  # Add more properties and schema as needed based on your user pool configuration

  tags = {
    Environment = "development"
  }
}

resource "aws_cognito_user_pool_client" "user_pool_client" {
  name                                 = "local-dev-enworth-user-pool-client"
  user_pool_id                         = aws_cognito_user_pool.user_pool.id
  callback_urls                        = ["http://localhost:3000/auth-callback"]
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code", "implicit"]
  allowed_oauth_scopes                 = ["email", "openid"]
  supported_identity_providers         = ["COGNITO"]
}

output "user_pool_id" {
  value = aws_cognito_user_pool.user_pool.id
}

output "user_pool_client_id" {
  value = aws_cognito_user_pool_client.user_pool_client.id
}
