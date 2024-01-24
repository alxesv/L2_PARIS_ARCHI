from authorization import authorization_header
from database import session
from router.production.production import router
from models import Production, Unite
from pydantic import BaseModel
from fastapi import status, HTTPException

class ProductionBase(BaseModel):
    code_production: int
    un: str
    nom_production: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_production(new_production: ProductionBase, header_authorization=authorization_header):
    """
    Ajoute une ligne dans la table Production
    ### Paramètres
    - new_production : objet de type Production, avec les champs code_production, un et nom_production
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    productions = session.query(Production).all()
    for code_production in productions:
        if code_production.code_production == new_production.code_production:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Production déjà existante")

        if new_production.un is not None:
            all_unites = session.query(Unite).all()
            if not any(unite.un == new_production.un for unite in all_unites):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unite non trouvée")
    try:
        add_production = Production(**new_production.__dict__)
        session.add(add_production)
        session.commit()
        return {"message": "Production créée avec succès", "add_production": new_production.model_dump()}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))