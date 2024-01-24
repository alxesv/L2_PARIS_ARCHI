from authorization import authorization_header
from database import session
from router.unite.unite import router
from models import Unite
from pydantic import BaseModel
from fastapi import HTTPException, status

class UniteBase(BaseModel):
    un: str
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_unite(new_unite: UniteBase, header_authorization=authorization_header):
    """
    Ajoute une ligne dans la table Unite
    ### Paramètres
    - new_unite: objet de type Unite, avec le champs un
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    unites = session.query(Unite).all()
    for un in unites:
        if un.un == new_unite.un:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unité déjà existante")

    try:
        add_unite = Unite(**new_unite.__dict__)
        session.add(add_unite)
        session.commit()
        return {"message": "Unite créée avec succès", "new_unite": new_unite.model_dump()}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))