from authorization import authorization_header
from database import session
from router.production.production import router
from models import Production
from fastapi import status, HTTPException
from sqlalchemy.orm import joinedload
from database import base_url

@router.get("/", status_code=status.HTTP_200_OK)
def read_productions(skip: int = 0, limit: int = 10, sort: str = None, un: str = None
                     , nom_production: str = None, populate: bool = False, header_authorization=authorization_header):
    """
    Récupère les lignes de la table Production
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    - sort: le ou les champs sur lequel trier les résultats
    - un: le nom de l'unité à filtrer
    ### Retour
    - un objet JSON contenant les lignes de la table Production, filtrées et/ou triées
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    - url de navigation pour la pagination
    """
    url = f"{base_url}/api/productions?"

    sortable = Production.__table__.columns.keys()

    if sort is not None:
        sort_criteria = []
        sort_url = ""
        sort = sort.split(",")
        for s in sort:
            if s[0] == "-":
                check_sort = s[1:]
            else:
                check_sort = s
            if check_sort not in sortable:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Le champ de tri {check_sort} n'existe pas")
            if s[0] == "-":
                sort_criteria.append(getattr(Production, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Production, s))
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
        if populate is not False:
            data = (session.query(Production).order_by(*sort_criteria)
                    .options(joinedload(Production.cultures), joinedload(Production.unite)).all())
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = (session.query(Production).order_by(*sort_criteria).all())
    else:
        if populate is not False:
            data = (
                session.query(Production).options(joinedload(Production.cultures), joinedload(Production.unite)).all())
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = (session.query(Production).all())

    if un is not None:
        if not any(production.un == un for production in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unité trouvée")
        data = [production for production in data if production.un == un]

    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aucune production trouvée")

    if nom_production is not None:
        if not any(production.nom_production == nom_production for production in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun nom de production trouvé")
        data = [production for production in data if production.nom_production == nom_production]

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skip est plus grand que le nombre de production")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"productions": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{code_production}", status_code=status.HTTP_200_OK)
def read_production_by_code_production(code_production: int, populate: bool = False, header_authorization=authorization_header):
    """
    Récupère une ligne de la table Production
    ### Paramètres
    - code_production: le code de la production
    ### Retour
    - un objet de type Production
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    if populate is not False:
        data = (session.query(Production).filter(Production.code_production == code_production)
                .options(joinedload(Production.cultures), joinedload(Production.unite)).first())
    else:
        data = (session.query(Production).filter(Production.code_production == code_production).first())

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production introuvable")

    return {"production": data}