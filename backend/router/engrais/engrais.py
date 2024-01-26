from fastapi import APIRouter

router = APIRouter(prefix="/engrais", tags=['engrais'])
from .methods.create import *
from .methods.read import *
from .methods.delete import *
from .methods.update import *
from .methods.replace import *