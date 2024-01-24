from fastapi import APIRouter

router = APIRouter(prefix="/epandre", tags=['epandre'])
from .methods.create import *
from .methods.read import *
from .methods.delete import *
from .methods.replace import *