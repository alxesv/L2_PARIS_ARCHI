from authorization import authorization_header
from database import session
from router.epandre.epandre import router
from models import Epandre, Date, Parcelle, Engrais
from fastapi import HTTPException, status
from pydantic import BaseModel

class EpandreBase(BaseModel):
    id_engrais: int
    no_parcelle: int
    date: str
    qte_epandue: int

@router.put('/', status_code=status.HTTP_200_OK)
def replace_epandre(new_epandre: EpandreBase, header_authorization=authorization_header):
    """
    Remplace une ligne dans la table epandre
    ### Paramètres
    - new_epandre: objet de type Epandre, avec les champs id_engrais, no_parcelle, date et qte_epandue
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    if new_epandre.id_engrais is None or new_epandre.no_parcelle is None or new_epandre.date is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque au moins un paramètre")

    dates = session.query(Date).all()
    if not any(date.date == new_epandre.date for date in dates):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune date trouvée")
    else:
        date_object = session.query(Date).filter(Date.date == new_epandre.date).first()

    if new_epandre.id_engrais is not None:
        all_engrais = session.query(Engrais).all()
        if not any(engrais.id_engrais == new_epandre.id_engrais for engrais in all_engrais):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun engrais trouvé")

    if new_epandre.no_parcelle is not None:
        all_parcelles = session.query(Parcelle).all()
        if not any(parcelle.no_parcelle == new_epandre.no_parcelle for parcelle in all_parcelles):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune parcelle trouvée")

    epandres = session.query(Epandre).all()
    for epandre in epandres:
        if epandre.id_engrais == new_epandre.id_engrais and epandre.no_parcelle == new_epandre.no_parcelle and epandre.date == date_object:
            epandre.qte_epandue = new_epandre.qte_epandue
            new_epandre = new_epandre.model_dump()
            session.commit()
            return {"message": "Épandage remplacé avec succès", "new_epandre": new_epandre}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aucun épandage trouvé")
