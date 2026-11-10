from pydantic import BaseModel, ConfigDict, Field


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    username: str


class UserCreateSchema(BaseModel):
    username: str
    password: str = Field(min_length=8)


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"