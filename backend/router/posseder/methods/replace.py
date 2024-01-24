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

@router.put('/', status_code=status.HTTP_201_CREATED)
def replace_posseder(new_posseder: PossederBase, header_authorization=authorization_header):
    """
    Remplace une ligne dans la table Posseder
    ### Paramètres
    - new_posseder: objet de type Posseder, avec les champs id_engrais, code_element et valeur
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if new_posseder.id_engrais is None or new_posseder.code_element is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque au moins un paramètre")

    if new_posseder.id_engrais is not None:
        all_engrais = session.query(Engrais).all()
        if not any(engrais.id_engrais == new_posseder.id_engrais for engrais in all_engrais):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun engrais trouvé")

    if new_posseder.code_element is not None:
        all_code_elements = session.query(ElementChimique).all()
        if not any(code_element.code_element == new_posseder.code_element for code_element in all_code_elements):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun code d'élément chimique trouvé")

    posseders = session.query(Posseder).all()
    for posseder in posseders:
        if posseder.id_engrais == new_posseder.id_engrais and posseder.code_element == new_posseder.code_element:
            new_posseder = new_posseder.model_dump()
            session.commit()
            return {"message": "Possession remplacée avec succès", "new_posseder": new_posseder}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune possession trouvée")