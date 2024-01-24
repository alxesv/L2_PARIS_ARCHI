from authorization import authorization_header
from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique, Unite
from fastapi import HTTPException, status
from pydantic import BaseModel

class ElementChimiqueBase(BaseModel):
    un: str
    libelle_element: str

@router.put("/{code_element}", status_code=status.HTTP_200_OK)
def replace_element_chimique(code_element: str, new_element_chimique: ElementChimiqueBase
                             , header_authorization=authorization_header):
    """
    Remplace une ligne dans la table Element_Chimique
    ### Paramètres
    - code_element: le code de l'élément chimique
    - new_element_chimique: objet de type ElementChimique, avec les champs un et libelle_element
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if new_element_chimique.un is None or new_element_chimique.libelle_element is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque un paramètre")

    all_elements_chimique = session.query(ElementChimique).all()

    if not any(element_chimique.code_element == code_element for element_chimique in all_elements_chimique):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun élément chimique trouvé")

    if new_element_chimique.un is not None:
        all_unites = session.query(Unite).all()
        if not any(unite.un == new_element_chimique.un for unite in all_unites):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unité trouvée")

    if new_element_chimique.libelle_element is not None:
        for element_chimique in all_elements_chimique:
            if element_chimique.libelle_element == new_element_chimique.libelle_element and element_chimique.code_element != code_element:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Élément chimique déjà existant")

    try:
        engrais = session.query(ElementChimique).filter(ElementChimique.code_element == code_element).first()
        for (key, value) in new_element_chimique:
            setattr(engrais, key, value)
        session.commit()
        return {"message": "Élément chimique remplacé avec succès", "new_element_chimique": new_element_chimique.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
