from dataclasses import dataclass


@dataclass
class AuthTokens:
    access_token: str
    refresh_token: str
    id_token: str
