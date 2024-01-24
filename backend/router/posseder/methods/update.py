from authorization import authorization_header
from database import session
from router.posseder.posseder import router
from models import Posseder
from fastapi import HTTPException, status
from pydantic import BaseModel

class PossederBase(BaseModel):
    id_engrais: int
    code_element: str
    valeur: int

@router.patch('/', status_code=status.HTTP_200_OK)
def update_posseder(id_posseder: PossederBase, header_authorization=authorization_header):
    """
    Modifie une ligne dans la table Posseder
    ### Paramètres
    - id_posseder: objet de type Posseder, avec les champs id_engrais, code_element et valeur
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    pass