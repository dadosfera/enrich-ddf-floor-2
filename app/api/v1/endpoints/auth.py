"""
Authentication endpoints for login, registration, and token management.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.core.database import get_db
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

# Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Pydantic models
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    # TODO: Get user from database using db session
    # user = await get_user_by_id(db, user_id)
    # if user is None:
    #     raise credentials_exception
    
    return {"id": user_id, "email": "placeholder@example.com", "role": "user"}


@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """User login endpoint."""
    # TODO: Implement database user lookup and password verification
    # user = await get_user_by_email(db, user_credentials.email)
    # if not user or not verify_password(user_credentials.password,
    #                                  user.password_hash):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #     )
    
    # Placeholder implementation
    if (user_credentials.email == "admin@example.com" and
            user_credentials.password == "admin123"):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": "user-uuid-placeholder"},
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={"sub": "user-uuid-placeholder"}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """User registration endpoint."""
    # TODO: Implement user registration with database
    # Check if user already exists
    # existing_user = await get_user_by_email(db, user_data.email)
    # if existing_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email already registered"
    #     )
    
    # Hash password and create user
    # hashed_password = get_password_hash(user_data.password)
    # new_user = await create_user(db, user_data.email, hashed_password,
    #                             user_data.full_name)
    
    # Placeholder implementation
    return {
        "id": "new-user-uuid-placeholder",
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": "user"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Token refresh endpoint."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Create new tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": credentials.credentials,  # Return the same refresh token
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user profile."""
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "full_name": "Current User",
        "role": current_user["role"]
    }