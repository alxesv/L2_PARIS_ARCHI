from authorization import authorization_header
from database import session
from router.date.date import router
from models import Date
from pydantic import BaseModel
from fastapi import HTTPException, status
from datetime import datetime as dt


class DateBase(BaseModel):
    date: str

@router.put("/{date}", status_code=status.HTTP_200_OK)
def replace_date(new_date: DateBase, header_authorization=authorization_header):
    """
    Remplace une ligne dans la table Date
    ### Paramètres
    - date: la date
    - new_date: objet de type Date, avec le champs date
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    try:
        # Vérifiez si datetime.date est une chaîne de caractères au format YYYY-MM-DD
        datetime_obj = dt.strptime(new_date.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le format de la date est invalide. Utilisez le format 'YYYY-MM-DD'.")

    dates = session.query(Date).all()
    for date in dates:
        if date.date == new_date.date:
            new_date = new_date.model_dump()
            session.commit()
            return {"message": "Date remplacée avec succès", "new_date": new_date}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune date trouvée")
