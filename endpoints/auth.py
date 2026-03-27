from datetime import timedelta
import time
import os
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from database import MySQLDatabase, RedisDatabase
import logs as log
from utils.models import SignUpResult, SignUpResults, UserCreate
# from utils.utils import UserBase, UserCreate, UserWithRole, SignUpResult, SignUpResults, Token, LoginInfo, create_jwt, get_current_active_user, UserWithRole, oauth2_scheme


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        404: {"description": "Not found"}
    }
)


@router.post("/signup", response_model=SignUpResult)
def signup(user: UserCreate):
    """
    Register a new user
    
    Args:
        user (UserCreate): User registration data
    
    Returns:
        SignUpResult: Registration result model
    """
    if any(field is None for field in user.model_dump().values()):
        return SignUpResult(result=SignUpResults.fail)
    
    try:
        MySQLDatabase().register_user(
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name
        )
        return SignUpResult(result=SignUpResults.success)
    
    except Exception as ex:
        log.actions.error(f'Signup error: {ex}')
        return SignUpResult(result=SignUpResults.fail)