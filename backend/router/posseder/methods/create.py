from authorization import authorization_header
from database import session
from router.posseder.posseder import router
from models import Posseder, Engrais, ElementChimique
from fastapi import HTTPException, status
from pydantic import BaseModel

class PossederBase(BaseModel):
    id_engrais: int
    code_element: str
    valeur: int

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_posseder(new_posseder: PossederBase, header_authorization=authorization_header):
    """
    Ajoute une ligne dans la table Posseder
    ### Paramètres
    - new_posseder: objet de type Posseder, avec les champs id_engrais, code_element et valeur
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    engrais = session.query(Engrais).all()
    if not any(engrais_item.id_engrais == new_posseder.id_engrais for engrais_item in engrais):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun engrais trouvé")

    code_elements = session.query(ElementChimique).all()
    if not any(code_element.code_element == new_posseder.code_element for code_element in code_elements):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun code d'élément chimique trouvé")

    posseders = session.query(Posseder).all()
    for posseder_item in posseders:
        if posseder_item.id_engrais == new_posseder.id_engrais and posseder_item.code_element == new_posseder.code_element:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Possession déjà existante")

    try:
        add_posseder = Posseder(**new_posseder.__dict__)
        session.add(add_posseder)
        session.commit()
        return {"message": "Possession créée avec succès", "add_posseder": new_posseder.model_dump()}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))