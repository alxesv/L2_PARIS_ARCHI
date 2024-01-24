from authorization import authorization_header
from database import session
from router.culture.culture import router
from models import Culture
from fastapi import status, HTTPException

@router.delete("/{identifiant_culture}", status_code=status.HTTP_200_OK)
def delete_culture(identifiant_culture: int, header_authorization=authorization_header):
    """
    Supprime une ligne dans la table Culture
    ### Paramètres
    - identifiant_culture : L'identifiant de la culture à supprimer
    ### Retour
    - Status code 200 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    cultures = session.query(Culture).all()
    for culture in cultures:
        if culture.identifiant_culture == identifiant_culture:
            deleted_culture = culture
            session.delete(culture)
            session.commit()
            return {"message": "Culture supprimée avec succès", "deleted_culture": deleted_culture}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune culture trouvée")