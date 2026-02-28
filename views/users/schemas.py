from pydantic import BaseModel, EmailStr

class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    motto: str | None = None


class UserSchemaIn(UserBaseSchema):
    pass

class UserSchemaUpdate(UserBaseSchema):
    username: str | None = None
    email: EmailStr | None = None
    motto: str | None = None

class UserSchema(UserBaseSchema):
    id: int



