from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=['authentification'])
from .methods.jwt import *
