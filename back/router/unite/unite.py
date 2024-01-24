from fastapi import APIRouter

router = APIRouter(prefix="/unites", tags=['unite'])
from .methods.create import *
from .methods.read import *
from .methods.delete import *