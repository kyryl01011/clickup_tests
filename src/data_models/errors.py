from pydantic import BaseModel


class BasicErrorModel(BaseModel):
    err: str | tuple
    ECODE: str | tuple
