from authorization import authorization_header
from database import session
from router.epandre.epandre import router
from models import Epandre, Engrais, Parcelle, Date
from fastapi import HTTPException, status
from pydantic import BaseModel

class EpandreBase(BaseModel):
    id_engrais: int
    no_parcelle: int
    date: str
    qte_epandue: int

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_epandre(new_epandre: EpandreBase, header_authorization=authorization_header):
    """
    Ajoute une ligne dans la table Epandre
    ### Paramètres
    - epandre: objet de type Epandre, avec les champs id_engrais, no_parcelle, date et qte_epandue
    ### Retour
    - Status code 201 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    dates = session.query(Date).all()
    if not any(date.date == new_epandre.date for date in dates):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune date trouvée")

    engrais = session.query(Engrais).all()
    if not any(engrais_item.id_engrais == new_epandre.id_engrais for engrais_item in engrais):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun engrais trouvé")

    parcelles = session.query(Parcelle).all()
    if not any(parcelle.no_parcelle == new_epandre.no_parcelle for parcelle in parcelles):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune parcelle trouvée")

    date_object = session.query(Date).filter(Date.date == new_epandre.date).first()

    epandres = session.query(Epandre).all()
    for epandre_item in epandres:
        if epandre_item.id_engrais == new_epandre.id_engrais and epandre_item.no_parcelle == new_epandre.no_parcelle and epandre_item.date == date_object:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Épandage déjà existant")

    try:
        add_epandre = Epandre(id_engrais=new_epandre.id_engrais, no_parcelle=new_epandre.no_parcelle, date=date_object, qte_epandue=new_epandre.qte_epandue)
        session.add(add_epandre)
        session.commit()
        return {"message": "Épandage créé avec succès", "new_epandre": new_epandre.model_dump()}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
