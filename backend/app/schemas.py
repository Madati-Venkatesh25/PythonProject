from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
from datetime import datetime
from app.models import TaskStatus, TaskPriority, MoodType


# ─────────────────────────────────────────
# AUTH SCHEMAS
# ─────────────────────────────────────────

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator('username')
    @classmethod
    def username_valid(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        if not v.isalnum():
            raise ValueError('Username must contain only letters and numbers')
        return v

    @field_validator('password')
    @classmethod
    def password_valid(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = {'from_attributes': True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserResponse


# ─────────────────────────────────────────
# LOG SCHEMAS
# ─────────────────────────────────────────

class LogCreate(BaseModel):
    title: str
    content: str
    mood: Optional[MoodType] = MoodType.neutral
    tags: Optional[str] = ''

    @field_validator('title')
    @classmethod
    def title_valid(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters')
        return v.strip()

    @field_validator('content')
    @classmethod
    def content_valid(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Content must be at least 10 characters')
        return v.strip()


class LogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[MoodType] = None
    tags: Optional[str] = None


class LogResponse(BaseModel):
    id: int
    title: str
    content: str
    mood: MoodType
    tags: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    model_config = {'from_attributes': True}


# ─────────────────────────────────────────
# TASK SCHEMAS
# ─────────────────────────────────────────

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ''
    status: Optional[TaskStatus] = TaskStatus.todo
    priority: Optional[TaskPriority] = TaskPriority.medium
    due_date: Optional[datetime] = None

    @field_validator('title')
    @classmethod
    def title_valid(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters')
        return v.strip()


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    user_id: int

    model_config = {'from_attributes': True}


# ─────────────────────────────────────────
# STATS SCHEMA
# ─────────────────────────────────────────

class StatsResponse(BaseModel):
    total_logs: int
    total_tasks: int
    tasks_todo: int
    tasks_in_progress: int
    tasks_done: int
