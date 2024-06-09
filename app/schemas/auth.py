from pydantic import BaseModel

from app.schemas.user import User


class LoginPostRequest(BaseModel):
    code: str


class LoginPostResponse(BaseModel):
    user: User
