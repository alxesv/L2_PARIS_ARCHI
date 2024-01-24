from authorization import authorization_header
from database import session
from router.unite.unite import router
from models import Unite
from pydantic import BaseModel
from fastapi import HTTPException, status

class UniteBase(BaseModel):
    un: str

@router.put("/{unite}", status_code=status.HTTP_200_OK)
def replace_unite(unite: str, new_unite: UniteBase, header_authorization=authorization_header):
    """
    Remplace une ligne dans la table Unite
    ### Paramètres
    - unite: le nom de l'unite
    - new_unite: objet de type Unite, avec le champs un
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    unites = session.query(Unite).all()

    if len(new_unite.un) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unité vide")

    if new_unite.un in [un.un for un in unites]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unité déjà existante")

    try:
        unite_item = session.query(Unite).filter(Unite.un == unite).first()
        for (key, value) in new_unite:
            setattr(unite_item, key, value)
        session.commit()
        return {"message": "Unite modifiée avec succès", "new_unite": new_unite.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))