from authorization import authorization_header
from database import session
from router.epandre.epandre import router
from models import Epandre
from fastapi import HTTPException, status
from pydantic import BaseModel

class EpandreBase(BaseModel):
    id_engrais: int
    no_parcelle: int
    date: str
    qte_epandue: int

@router.patch('/', status_code=status.HTTP_200_OK)
def update_epandre(id_epandre: EpandreBase, header_authorization=authorization_header):
    """
    Modifie une ligne dans la table epandre
    ### Paramètres
    - id_epandre: objet de type Epandre, avec les champs id_engrais, no_parcelle et date
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    pass