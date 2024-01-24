from datetime import datetime

from authorization import authorization_header
from database import session
from router.culture.culture import router
from models import Culture, Parcelle, Production
from pydantic import BaseModel
from fastapi import HTTPException, status

class CultureBase(BaseModel):
    no_parcelle: int = None
    code_production: int = None
    date_debut: str = None
    date_fin: str = None
    qte_recoltee: int = None

def compare_date(date_debut, date_fin):
    debut = datetime.strptime(date_debut, "%Y-%m-%d")
    fin = datetime.strptime(date_fin, "%Y-%m-%d")
    if debut > fin:
        return True
    return False

@router.patch("/{identifiant_culture}", status_code=status.HTTP_200_OK)
def update_culture(identifiant_culture: int, updated_culture: CultureBase, header_authorization=authorization_header):
    """
    Modifie une ligne dans la table Culture
    ### Paramètres
    - identifiant_culture: Identifiant de la culture à modifié
    - updated_culture: objet de type Culture, avec les champs no_parcelle, code_production, date_debut, date_fin, qte_recoltee
    ### Retour
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """

    if updated_culture.no_parcelle is None and updated_culture.code_production is None and updated_culture.date_debut is None and updated_culture.date_fin is None and updated_culture.qte_recoltee is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Il manque un paramètre")

    all_culture = session.query(Culture).all()

    if not any(culture.identifiant_culture == identifiant_culture for culture in all_culture):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune culture trouvée")

    if updated_culture.no_parcelle is not None:
        all_parcelles = session.query(Parcelle).all()
        if not any(parcelle.no_parcelle == updated_culture.no_parcelle for parcelle in all_parcelles):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune parcelle trouvée")

    if updated_culture.code_production is not None:
        all_productions = session.query(Production).all()
        if not any(production.code_production == updated_culture.code_production for production in all_productions):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune production trouvée")

    culture = session.query(Culture).filter(Culture.identifiant_culture == identifiant_culture).first()
    if updated_culture.date_debut is not None or updated_culture.date_fin is not None:
        if updated_culture.date_debut is None:
            debut = culture.date_debut
        else:
            debut = updated_culture.date_debut
        if updated_culture.date_fin is None:
            fin = culture.date_fin
        else:
            fin = updated_culture.date_fin
        debut_after_end = compare_date(debut, fin)
        if debut_after_end:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="La date de début doit se trouver avant la date de fin")

    try:
        if updated_culture.no_parcelle is not None:
            culture.no_parcelle = updated_culture.no_parcelle
        else:
            updated_culture.no_parcelle = culture.no_parcelle

        if updated_culture.code_production is not None:
            culture.code_production = updated_culture.code_production
        else:
            updated_culture.code_production = culture.code_production

        if updated_culture.date_debut is not None:
            culture.date_debut = updated_culture.date_debut
        else:
            updated_culture.date_debut = culture.date_debut

        if updated_culture.date_fin is not None:
            culture.date_fin = updated_culture.date_fin
        else:
            updated_culture.date_fin = culture.date_fin

        if updated_culture.qte_recoltee is not None:
            culture.qte_recoltee = updated_culture.qte_recoltee
        else:
            updated_culture.qte_recoltee = culture.qte_recoltee
        session.commit()
        return {"message": "Culture modifiée avec succès", "updated_production": updated_culture.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
