from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int

    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    permissions: List[Permission] = []

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    national_id: str
    password: str
    
    # שדות אופציונליים שיתווספו בטופס הפרופיל האישי
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    building: Optional[str] = None
    entrance: Optional[str] = None
    postal_code: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None
    role_id: Optional[int] = None


class User(UserBase):
    id: int
    first_name: str
    last_name: str
    national_id: str
    is_active: bool
    capsule_status: str
    created_at: datetime
    items: List[Item] = []
    role: Optional[Role] = None
    
    # שדות אופציונליים שיתווספו בטופס הפרופיל האישי
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    building: Optional[str] = None
    entrance: Optional[str] = None
    postal_code: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    permissions: List[str] = [] 