from pydantic import BaseModel, ConfigDict


class CreatedTaskModel(BaseModel):
    model_config = ConfigDict(extra='allow')

    id: str
    name: str


class CreationTaskModel(BaseModel):
    name: str
