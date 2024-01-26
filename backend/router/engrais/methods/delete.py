from authorization import authorization_header
from database import session
from router.engrais.engrais import router
from models import Engrais
from fastapi import HTTPException, status
@router.delete("/{id_engrais}", status_code=status.HTTP_200_OK)
def delete_engrais(id_engrais: int, header_authorization=authorization_header):
    """
    Supprime une ligne dans la table Engrais
    ### Paramètres
    - id_engrais: l'identifiant de l'engrais
    ### Retour
    - Status code 200 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    engrais = session.query(Engrais).all()
    for engrais_item in engrais:
        if engrais_item.id_engrais == id_engrais:
            deleted_engrais_name = engrais_item.nom_engrais
            session.delete(engrais_item)
            session.commit()
            return {"message": "Engrais supprimé avec succès", "deleted_engrais": deleted_engrais_name}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun engrais trouvé")
