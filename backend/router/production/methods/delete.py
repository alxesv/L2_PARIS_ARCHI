from authorization import authorization_header
from database import session
from router.production.production import router
from models import Production
from fastapi import status, HTTPException

@router.delete("/{production}", status_code=status.HTTP_200_OK)
def delete_production(production: int, header_authorization=authorization_header):
    """
    Supprime une ligne dans la table Production
    ### Paramètres
    - production : le code de la production
    ### Retour
    - Status code 200 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    productions = session.query(Production).all()
    for production_item in productions:
        if production_item.code_production == production:
            deleted_production_name = production_item.nom_production
            session.delete(production_item)
            session.commit()
            return {"message": "Production supprimée avec succès", "delete": deleted_production_name}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune production trouvée")