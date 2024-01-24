from authorization import authorization_header
from database import session
from router.date.date import router
from models import Date
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload
from database import base_url
@router.get("/", status_code=status.HTTP_200_OK)
def read_dates(skip: int = 0, limit: int = 10, sort: str = None, populate: bool = False
               , header_authorization=authorization_header):
    """
    Récupère les lignes de la table Date
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    - sort: le ou les champs sur lequel trier les résultats
    ### Retour
    - un objet JSON contenant  les lignes de la table Date, filtrées et/ou triées
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    - url de navigation pour la pagination
    """
    url = f"{base_url}/api/dates?"

    sortable = Date.__table__.columns.keys()

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
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Le champ de tri {check_sort} n'existe pas")
            if s[0] == "-":
                sort_criteria.append(getattr(Date, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Date, s))
                sort_url += f"{s},"
        if populate is not False:
            data = session.query(Date).order_by(*sort_criteria).options(joinedload(Date.epandres)).all()
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = session.query(Date).order_by(*sort_criteria).all()
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
    else:
        if populate is not False:
            data = session.query(Date).options(joinedload(Date.epandres)).all()
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = session.query(Date).all()

    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune date trouvée")

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skip est plus grand que le nombre de date")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"dates": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{date}",status_code=status.HTTP_200_OK)
def read_date_by_datetime(date: str, populate: bool = False, header_authorization=authorization_header):
    """
    Récupère une ligne de la table Date
    ### Paramètres
    - date: le nom de la date
    ### Retour
    - un objet de type Date
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    if populate is not False:
        data = session.query(Date).filter(Date.date == date).options(joinedload(Date.epandres)).first()
    else:
        data = session.query(Date).filter(Date.date == date).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Date introuvable")

    return {"date": data}