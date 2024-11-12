from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str
    phone: str


class UserVerifyTotp(BaseModel):
    email: EmailStr
    otp: str


class CountryAdd(BaseModel):
    name: str
    short_code: str


class WorkerResponse(BaseModel):
    id: int
    item_name: str
    hosting_cost: str
    profit: str
    dohod: str
    rashod: str
    status: str
