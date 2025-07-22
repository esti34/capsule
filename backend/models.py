from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# Association table for role-permission many-to-many relationship
role_permission = Table(
    'role_permission',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # Relationships
    users = relationship("User", back_populates="role")
    permissions = relationship("Permission", secondary=role_permission, back_populates="roles")

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    
    # Relationships
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    national_id = Column(String(20), unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String)
    
    # Address fields - כל השדות הפכו לאופציונליים
    city = Column(String(100), nullable=True)
    neighborhood = Column(String(100), nullable=True)
    street = Column(String(100), nullable=True)
    building = Column(String(20), nullable=True)
    entrance = Column(String(20), nullable=True)
    postal_code = Column(String(20), nullable=True)
    
    # Personal information - שדות אופציונליים
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    phone_number = Column(String(20), nullable=True)
    
    # Status and role
    is_active = Column(Boolean, default=True)
    capsule_status = Column(String(20), default="not_ready")
    created_at = Column(DateTime, server_default=func.now())
    
    # Foreign keys
    role_id = Column(Integer, ForeignKey("roles.id"))
    
    # Relationships
    role = relationship("Role", back_populates="users")
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    is_active = Column(Boolean, default=True)

    # Example of a relationship
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items") 