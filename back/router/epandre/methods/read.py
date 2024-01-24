from authorization import authorization_header
from database import session
from router.epandre.epandre import router
from models import Epandre, Date
from fastapi import HTTPException, status
from models import Date
from sqlalchemy.orm import joinedload
from database import base_url
@router.get("/", status_code=status.HTTP_200_OK)
def read_epandres(skip: int = 0, limit: int = 10, sort: str = None, id_engrais: int = None
                  , no_parcelle: int = None, date: str = None, qte_epandue: int = None, populate: bool = False
                  , header_authorization=authorization_header):
    """
    Récupère  les lignes de la table Epandre
    ### Paramètres
    - skip: nombre de lignes à sauter
    - limit: nombre de lignes à récupérer
    - sort: le ou les champs sur lequel trier les résultats
    - id_engrais: le nom de l'engrais à filtrer
    - no_parcelle: le numéro de la parcelle à filtrer
    - date: la date de l'épandage à filtrer
    - qte_epandue: la quantité épandue à filtrer, minimum
    ### Retour
    - un objet JSON contenant  les lignes de la table Epandre, filtrées et/ou triées
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    - url de navigation pour la pagination
    """
    url = f"{base_url}/api/epandre?"

    sortable = Epandre.__table__.columns.keys()

    if sort is not None:
        sort_criteria = []
        sort_url = ""
        sort = sort.split(",")
        for s in sort:
            if s[0] == "-":
                check_sort = s[1:]
            else:
                check_sort = s
            if check_sort == "date":
                check_sort = "date_fk"
                s = s.replace("date", "date_fk")
            if check_sort not in sortable:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Le champ de tri {check_sort} n'existe pas")
            if s[0] == "-":
                sort_criteria.append(getattr(Epandre, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Epandre, s))
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
        if populate is not False:
            data = (session.query(Epandre).order_by(*sort_criteria)
                    .options(joinedload(Epandre.parcelle), joinedload(Epandre.engrais), joinedload(Epandre.date)).all())
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = (session.query(Epandre).order_by(*sort_criteria).all())
    else:
        if populate is not False:
            data = (session.query(Epandre)
                    .options(joinedload(Epandre.parcelle), joinedload(Epandre.engrais), joinedload(Epandre.date)).all())
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = (session.query(Epandre).all())

    if qte_epandue is not None and qte_epandue > 0:
        if not any(epandre.qte_epandue >= qte_epandue for epandre in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune quantité épandue trouvée")
        data = [epandre for epandre in data if epandre.qte_epandue >= qte_epandue]

    if id_engrais is not None:
        if not any(epandre.id_engrais == id_engrais for epandre in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun engrais trouvé")
        data = [epandre for epandre in data if epandre.id_engrais == id_engrais]

    if no_parcelle is not None:
        if not any(epandre.no_parcelle == no_parcelle for epandre in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune parcelle trouvée")
        data = [epandre for epandre in data if epandre.no_parcelle == no_parcelle]

    if date is not None:
        try:
            date_object = (session.query(Date).filter(Date.date == date).first())
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Date non existante")
        if not any(epandre.date == date_object for epandre in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune date trouvée")
        data = [epandre for epandre in data if epandre.date == date_object]


    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun épandage trouvé")

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skip est plus grand que le nombre d'épandage")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"epandres": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response
