from authorization import authorization_header
from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique, Unite
from fastapi import HTTPException, status
from pydantic import BaseModel


class ElementChimiqueBase(BaseModel):
    un: str = None
    libelle_element: str = None

@router.patch("/{code_element}", status_code=status.HTTP_200_OK)
def update_element_chimique(code_element: str, updated_element_chimique: ElementChimiqueBase
                            , header_authorization=authorization_header):
    """
    Modifie une ligne dans la table Element_Chimique
    ### Paramètres
    - code_element: le code de l'élément chimique
    - updated_element_chimique: objet de type ElementChimique, avec les champs un et libelle_element
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if updated_element_chimique.un is None and updated_element_chimique.libelle_element is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque un paramètre")

    all_elements = session.query(ElementChimique).all()

    if not any(element_chimique.code_element == code_element for element_chimique in all_elements):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun élément chimique trouvé")

    if updated_element_chimique.un is not None:
        all_unites = session.query(Unite).all()
        if not any(unite.un == updated_element_chimique.un for unite in all_unites):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unité trouvée")

    if updated_element_chimique.libelle_element is not None:
        for element_chimique in all_elements:
            if element_chimique.libelle_element == updated_element_chimique.libelle_element and element_chimique.code_element != code_element:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Élément chimique déjà existant")

    try:
        element_chimique = session.query(ElementChimique).filter(ElementChimique.code_element == code_element).first()
        if updated_element_chimique.un is not None:
            element_chimique.un = updated_element_chimique.un
        else:
            updated_element_chimique.un = element_chimique.un
        if updated_element_chimique.libelle_element is not None:
            element_chimique.libelle_element = updated_element_chimique.libelle_element
        else:
            updated_element_chimique.libelle_element = element_chimique.libelle_element
        session.commit()
        return {"message": "Élément chimique modifié avec succès", "updated_element_chimique": updated_element_chimique.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
