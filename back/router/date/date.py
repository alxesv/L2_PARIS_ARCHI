from fastapi import APIRouter

router = APIRouter(prefix="/dates", tags=['date'])
from .methods.create import *
from .methods.delete import *
from .methods.read import *
