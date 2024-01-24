from authorization import authorization_header
from database import session
from router.posseder.posseder import router
from models import Posseder
from fastapi import HTTPException, status

@router.delete("/", status_code=status.HTTP_200_OK)
def delete_posseder(id_engrais: int, code_element: str, header_authorization=authorization_header):
    """
    Supprime une ligne dans la table Posseder
    ### Paramètres
    - id_engrais: l'identifiant de l'engraise
    - code_element: le code de l'élément chimique
    ### Retour
    - Status code 200 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    if id_engrais is None or code_element is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque au moins un paramètre")

    posseders = session.query(Posseder).all()
    for posseder in posseders:
        if posseder.id_engrais == id_engrais and posseder.code_element == code_element:
            deleted_posseder = posseder
            session.delete(posseder)
            session.commit()
            return {"message": "Possession supprimée avec succès", "deleted_posseder ": deleted_posseder}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune possession trouvée")