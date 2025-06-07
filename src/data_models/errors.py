from pydantic import BaseModel


class BasicErrorModel(BaseModel):
    err: str
    ECODE: str
