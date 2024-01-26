from authorization import authorization_header
from database import session
from router.parcelle.parcelle import router
from models import Parcelle
from pydantic import BaseModel
from fastapi import HTTPException, status


class ParcelleBase(BaseModel):
    no_parcelle: int
    surface: int
    nom_parcelle: str
    coordonnees: str
@router.post("/",status_code=status.HTTP_201_CREATED)
def create_parcelle(parcelle: ParcelleBase, header_authorization=authorization_header):
    """
   Ajoute une ligne dans la table parcelle
    ### Paramètres
    - parcelle: objet de type Parcelle, avec les champs no_parcelle,surface,nom_parcelle,coordonnees
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    parcelles = session.query(Parcelle).all()
    for no_parcelle in parcelles:
        if no_parcelle.no_parcelle == parcelle.no_parcelle:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parcelle déjà existant")

    try:
        parcelle = Parcelle(no_parcelle=parcelle.no_parcelle,surface=parcelle.surface,nom_parcelle=parcelle.nom_parcelle,coordonnees=parcelle.coordonnees)
        session.add(parcelle)
        session.commit()
        return {"message": "Parcelle créée avec succès", "parcelle": parcelle.no_parcelle}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
