from pydantic import BaseModel

class LoginRequest(BaseModel):
	username: str
	password: str

class CreateAccountRequest(BaseModel):
	name: str
	username: str
	password: str