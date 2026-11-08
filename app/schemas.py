from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(min_length=1, max_length=32)


class UserResponse(BaseModel):
    username: str
    identity: str


class MessageCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(min_length=1, max_length=32)
    body: str = Field(min_length=1, max_length=2000)


class MessageResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    sender: str = Field(alias="from")
    origin: str
    lamport: int
    sent_at: str
    body: str


class FederatedMessage(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    id: str = Field(min_length=1, max_length=128)
    sender: str = Field(alias="from", min_length=1, max_length=128)
    origin: str = Field(min_length=1, max_length=32)
    lamport: int = Field(ge=0)
    sent_at: str = Field(min_length=1, max_length=64)
    body: str = Field(max_length=2000)
