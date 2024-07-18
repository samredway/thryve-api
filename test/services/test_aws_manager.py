from app.services.aws.aws_manager import get_db_credentials


def test_get_db_credentials() -> None:
    secret = get_db_credentials()
    assert secret.username == "postgres"
    assert secret.password
