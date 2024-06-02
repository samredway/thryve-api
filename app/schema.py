from pydantic import BaseModel


class GetPlaidLinkTokenResponse(BaseModel):
    plaid_link_token: str
