from authorization import authorization_header
from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique
from fastapi import HTTPException, status

@router.delete("/{code_element}", status_code=status.HTTP_200_OK)
def delete_element_chimique(code_element: str, header_authorization=authorization_header):
    """
    Supprime une ligne dans la table Element_Chimique
    ### Paramètres
    - code_element: le code de l'élément chimique
    ### Retour
    - Status code 200 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    element_chimiques = session.query(ElementChimique).all()
    for element_chimique in element_chimiques:
        if element_chimique.code_element == code_element:
            deleted_element_chimique = element_chimique.code_element
            session.delete(element_chimique)
            session.commit()
            return {"message": "Élément chimique supprimé avec succès", "deleted_element_chimique": deleted_element_chimique}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun élément chimique trouvé")
