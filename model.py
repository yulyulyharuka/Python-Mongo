from pydantic import BaseModel

class CreateUserRequestBodyModel(BaseModel):
    username: str
    password: str
    name: str
    age: int

class LoginUserRequestBodyModel(BaseModel) :
    username: str
    password: str