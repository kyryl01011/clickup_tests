from pydantic import BaseModel


class AuthErrorModel(BaseModel):
    err: str
    ECODE: str
