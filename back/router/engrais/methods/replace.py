from authorization import authorization_header
from database import session
from router.engrais.engrais import router
from models import Engrais, Unite
from pydantic import BaseModel
from fastapi import HTTPException, status

class EngraisBase(BaseModel):
    un: str
    nom_engrais: str
@router.put("/{id_engrais}", status_code=status.HTTP_200_OK)
def replace_engrais(id_engrais: int, new_engrais: EngraisBase, header_authorization=authorization_header):
    """
    Remplace une ligne dans la table Engrais
    ### Paramètres
    - id_engrais: l'identifiant de l'engrais
    - new_engrais: objet de type Engrais, avec les champs un et nom_engrais
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if new_engrais.nom_engrais is None or new_engrais.un is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque un paramètre")

    all_engrais = session.query(Engrais).all()

    if not any(engrais.id_engrais == id_engrais for engrais in all_engrais):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun engrais trouvé")

    if new_engrais.un is not None:
        all_unites = session.query(Unite).all()
        if not any(unite.un == new_engrais.un for unite in all_unites):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unité trouvée")
    if new_engrais.nom_engrais is not None:
        for engrais in all_engrais:
            if engrais.nom_engrais == new_engrais.nom_engrais and engrais.id_engrais != id_engrais:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Engrais déjà existant")

    try:
        engrais = session.query(Engrais).filter(Engrais.id_engrais == id_engrais).first()
        for (key, value) in new_engrais:
            setattr(engrais, key, value)
        session.commit()
        return {"message": "Engrais modifié avec succès", "new_engrais": new_engrais.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
