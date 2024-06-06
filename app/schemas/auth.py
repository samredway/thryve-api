from pydantic import BaseModel


class LoginPostRequest(BaseModel):
    code: str
