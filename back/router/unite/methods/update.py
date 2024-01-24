from authorization import authorization_header
from database import session
from router.unite.unite import router
from models import Unite
from pydantic import BaseModel
from fastapi import HTTPException, status
class UniteBase(BaseModel):
    un: str

@router.patch("/{unite}")
def update_unite(unite: str, updated_unite: UniteBase, header_authorization=authorization_header):
    """
    Modifie une ligne dans la table Unite
    ### Paramètres
    - unite: le nom de l'unite
    - new_unite: objet de type Unite, avec le champs un
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    unites = session.query(Unite).all()

    if len(updated_unite.un) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unité vide")

    if updated_unite.un in [un.un for un in unites]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unité déjà existante")

    for un in unites:
        if un.un == unite:
            un.un = updated_unite.un
            session.commit()
            return {"message": "Unite modifiée avec succès"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unité trouvée")