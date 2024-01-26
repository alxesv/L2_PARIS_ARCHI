from authorization import authorization_header
from database import session
from router.date.date import router
from models import Date
from fastapi import HTTPException, status
@router.delete("/{datetime}",status_code=status.HTTP_200_OK)
def delete_date(datetime:str, header_authorization=authorization_header):
    """
    Supprime une ligne dans la table Date
    ### Paramètres
    - date: la string de la date selectionner
    ### Retour
    - Status code 200 si tout s'est bien passé avec message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """

    dates = session.query(Date).all()
    for date in dates:
        if date.date == datetime:
            deleted_date = date
            session.delete(date)
            session.commit()
            return {"message": "Date supprimée avec succès", "deleted_date": deleted_date}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune date trouvée")