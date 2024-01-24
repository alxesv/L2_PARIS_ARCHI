from fastapi import APIRouter

router = APIRouter(prefix="/compteur", tags=['compteur'])
from .methods.read import *
