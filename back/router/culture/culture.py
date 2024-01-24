from fastapi import APIRouter

router = APIRouter(prefix="/cultures", tags=['culture'])
from .methods.create import *
from .methods.read import *
from .methods.update import *
from .methods.replace import *
from .methods.delete import *