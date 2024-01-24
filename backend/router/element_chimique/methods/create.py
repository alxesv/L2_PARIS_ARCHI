from authorization import authorization_header
from database import session
from router.element_chimique.element_chimique import router
from models import ElementChimique, Unite
from fastapi import HTTPException, status
from pydantic import BaseModel

class ElementChimiqueBase(BaseModel):
    code_element: str
    un: str
    libelle_element: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_element_chimique(new_element_chimique: ElementChimiqueBase, header_authorization=authorization_header):
    """
   Ajoute une ligne dans la table Element_Chimique
    ### Paramètres
    - new_element_chimique : objet de type ElementChimique, avec les champs code_element, un et libelle_element
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    element_chimiques = session.query(ElementChimique).all()
    for elt_chimique in element_chimiques:
        if elt_chimique.code_element == new_element_chimique.code_element:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Élément déjà existant")

    unites = session.query(Unite).all()
    if not any(un.un == new_element_chimique.un for un in unites):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unité trouvée")

    try:
        add_element_chimique = ElementChimique(**new_element_chimique.__dict__)
        session.add(add_element_chimique)
        session.commit()
        return {"message": "Élément chimique créé avec succès", "element": new_element_chimique}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
