from fastapi import APIRouter

router = APIRouter(prefix="/parcelles", tags=['parcelle'])

from .methods.create import *
from .methods.read import *
from .methods.delete import *
from .methods.update import *
from .methods.replace import *