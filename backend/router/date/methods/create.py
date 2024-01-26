from fastapi.security import APIKeyHeader

from database import session
from router.date.date import router
from models import Date
from pydantic import BaseModel
from fastapi import HTTPException, status, Security
from datetime import datetime as dt
from authorization import authorization_header

class DateBase(BaseModel):
    date: str


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_date(new_date: DateBase, header_authorization=authorization_header):
    """
    Ajoute une ligne dans la table Date
    ### Paramètres
    - date: objet de type Date, avec le champ date
    ### Retour
    - Status code 201 si tout s'est bien passé avec un message de confirmation
    - Message d'erreur avec le status code correspondant sinon
    """
    try:
        # Vérifiez si datetime.date est une chaîne de caractères au format YYYY-MM-DD
        datetime_obj = dt.strptime(new_date.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le format de la date est invalide. Utilisez le format 'YYYY-MM-DD'.")

    dates = session.query(Date).all()
    for date in dates:
        if date.date == new_date.date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Date déjà existante")

    try:
        # Ajoutez la date à la base de données
        new_date = Date(date=new_date.date)
        session.add(new_date)
        session.commit()
        return {"message": "Date créée avec succès", "new_date": new_date.date}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
