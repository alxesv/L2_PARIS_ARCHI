from fastapi import APIRouter

router = APIRouter(prefix="/elements_chimiques", tags=['element_chimique'])
from .methods.create import *
from .methods.read import *
from .methods.delete import *
from .methods.replace import *
from .methods.update import *