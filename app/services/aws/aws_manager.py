# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

from dataclasses import dataclass
import json

import boto3
from botocore.exceptions import ClientError

from app.exceptions import ConfigurationError


@dataclass
class DbCredentials:
    password: str
    username: str


def get_db_credentials() -> DbCredentials:
    secret_name = "rds!cluster-f05f507d-bfad-4d2f-8126-b2dea68c1aa9"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret_string: str = get_secret_value_response["SecretString"]
    if not secret_string:
        raise ConfigurationError("No secret for DB credentials")

    secret: dict[str, str] = json.loads(secret_string)

    db_creds = DbCredentials(
        username=secret["username"],
        password=secret["password"],
    )
    return db_creds
