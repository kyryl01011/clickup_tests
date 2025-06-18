from typing import ClassVar, Any

import allure
from pydantic import BaseModel, ConfigDict, Field


class CreatorModel(BaseModel):
    id: int
    username: str
    color: str
    profile_picture: str | None = Field(None, alias='profilePicture')


class StatusModel(BaseModel):
    status: str
    color: str
    order_index: int = Field(alias='orderindex')
    type: str


class CreatedTaskModel(BaseModel):
    model_config = ConfigDict(extra='allow')

    # Set of created tasks IDs to clean after tests
    created_tasks_set: ClassVar[set[str]] = set()

    id: str
    name: str
    status: StatusModel
    creator: CreatorModel

    def model_post_init(self, context: Any, /) -> None:
        allure.attach(str(self.model_dump()), name='Created task data', attachment_type=allure.attachment_type.JSON)
        self.created_tasks_set.add(self.id)


class CreationTaskModel(BaseModel):
    name: str
    parent: str | None = None
    links_to: str | None = None
