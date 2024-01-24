from authorization import authorization_header
from database import session
from router.parcelle.parcelle import router
from models import Parcelle
from fastapi import HTTPException, status

@router.delete("/{parcelle}",status_code=status.HTTP_201_CREATED)
def delete_parcelle(parcelle: int, header_authorization=authorization_header):
    """
    Supprime une ligne dans la table parcelle
    ### Paramètres
    - parcelle: l'id de la table Parcelle utilisé pour trouver l'élément cherché à supprimer
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    parcelles = session.query(Parcelle).all()
    for parcelle_item in parcelles:
        if parcelle_item.no_parcelle == parcelle:
            deleted_parcelle = parcelle_item
            session.delete(parcelle_item)
            session.commit()
            return {"message": "Parcelle supprimée avec succès", "deleted_parcelle": parcelle}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Parcelle non trouvée")
