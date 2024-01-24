from fastapi import APIRouter

router = APIRouter(prefix="/posseder", tags=['posseder'])
from .methods.create import *
from .methods.delete import *
from .methods.read import *
from .methods.replace import *