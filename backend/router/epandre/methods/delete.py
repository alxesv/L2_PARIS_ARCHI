from authorization import authorization_header
from database import session
from router.epandre.epandre import router
from models import Epandre, Date
from fastapi import HTTPException, status

@router.delete("/", status_code=status.HTTP_200_OK)
def delete_epandre(id_engrais: int, no_parcelle: int, date: str, header_authorization=authorization_header):
    """
    Supprime une ligne dans la table Epandre
    ### Paramètres
    - id_engrais: l'identifiant de l'engrais
    - no_parcelle: le numéro de la parcelle
    - date: la date de l'épandage
    ### Retour
    - Status code 200 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    if id_engrais is None or no_parcelle is None or date is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque au moins un paramètre")

    dates = session.query(Date).all()
    if not any(orm_date.date == date for orm_date in dates):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune date trouvée")
    else:
        date_object = session.query(Date).filter(Date.date == date).first()

    epandres = session.query(Epandre).all()
    for epandre in epandres:
        if epandre.id_engrais == id_engrais and epandre.no_parcelle == no_parcelle and epandre.date == date_object:
            deleted_epandre = epandre
            session.delete(epandre)
            session.commit()
            return {"message": "Epandre supprimé avec succès", "deleted_epandre": deleted_epandre}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun épandage trouvé")
