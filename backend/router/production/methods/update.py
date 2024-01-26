from authorization import authorization_header
from database import session
from router.production.production import router
from models import Production, Unite
from pydantic import BaseModel
from fastapi import HTTPException, status

class ProductionBase(BaseModel):
    un: str = None
    nom_production: str = None
@router.patch("/{code_production}", status_code=status.HTTP_200_OK)
def update_production(code_production: int, updated_production: ProductionBase, header_authorization=authorization_header):
    """
    Modifie une ligne dans la table Production
    ### Paramètres
    - code_production: le code de la production
    - updated_production: objet de type Production, avec les champs un et nom_production
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """

    if updated_production.nom_production is None and updated_production.un is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque un paramètre")

    all_productions = session.query(Production).all()

    if not any(production.code_production == code_production for production in all_productions):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune production trouvée")

    if updated_production.un is not None:
        all_unites = session.query(Unite).all()
        if not any(unite.un == updated_production.un for unite in all_unites):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unité trouvée")

    if updated_production.nom_production is not None:
        for production in all_productions:
            if production.nom_production == updated_production.nom_production and production.code_production != code_production:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Production déjà existante")

    try:
        production = session.query(Production).filter(Production.code_production == code_production).first()
        if updated_production.nom_production is not None:
            production.nom_production = updated_production.nom_production
        else:
            updated_production.nom_production = production.nom_production
        if updated_production.un is not None:
            production.un = updated_production.un
        else:
            updated_production.un = production.un
        session.commit()
        return {"message": "Production modifiée avec succès", "updated_production": updated_production.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))