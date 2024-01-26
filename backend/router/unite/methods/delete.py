from authorization import authorization_header
from database import session
from router.unite.unite import router
from models import Unite
from fastapi import HTTPException, status

@router.delete("/{unite}", status_code=status.HTTP_200_OK)
def delete_unite(unite: str, header_authorization=authorization_header):
    """
    Supprime une ligne dans la table Unite
    ### Paramètres
    - unite: le nom de l'unité
    ### Retour
    - Status code 200 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    unites = session.query(Unite).all()
    for un in unites:
        if un.un == unite:
            deleted_un = un
            session.delete(un)
            session.commit()
            return {"message": "Unité supprimée avec succès", "deleted_un": deleted_un}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unité trouvée")