from authorization import authorization_header
from database import session
from router.date.date import router
from models import Date
from pydantic import BaseModel
from fastapi import HTTPException, status
from datetime import datetime as dt

class DateBase(BaseModel):
    date: str

@router.patch("/{date}", status_code=status.HTTP_200_OK)
def update_date(date: str, updated_date: DateBase, header_authorization=authorization_header):
    """
    Modifie une ligne dans la table Date
    ### Paramètres
    - date: le nom de la date à modifier
    - updated_date: objet de type DateBase, avec le champ date
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """
    try:
        # Vérifiez si date est une chaîne de caractères au format YYYY-MM-DD
        datetime_obj = dt.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le format de la date invalide. Veuillez respecter ce format -> %Y-%m-%d")

    existing_date = session.query(Date).filter(Date.date == date).first()
    if existing_date:
        try:
            # Mettez à jour la date existante dans la base de données
            existing_date.date = updated_date.date
            session.commit()
            return {"message": "Date modifiée avec succès"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune date trouvée")
