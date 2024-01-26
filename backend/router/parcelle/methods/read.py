from fastapi import HTTPException, status

from authorization import authorization_header
from database import session
from router.parcelle.parcelle import router
from models import Parcelle
from sqlalchemy.orm import joinedload
from database import base_url
@router.get("/", status_code=status.HTTP_201_CREATED)
def read_parcelles(skip: int = 0, limit: int = 10, sort: str = None
                   , surface:int=None, nom_parcelle:str=None, coordonnees:str=None, populate: bool = False
                   , header_authorization=authorization_header):
    """
    Récupère les lignes de la table parcelle
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    ### Retour
    - un tableau d'objets de type Parcelle
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """
    url = f"{base_url}/api/parcelles?"

    sortable = Parcelle.__table__.columns.keys()

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
                sort_criteria.append(getattr(Parcelle, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Parcelle, s))
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
        if populate is not False:
            data = (session.query(Parcelle).order_by(*sort_criteria)
                    .options(joinedload(Parcelle.cultures), joinedload(Parcelle.epandres)).all())
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = (session.query(Parcelle).order_by(*sort_criteria).all())
    else:
        if populate is not False:
            data = session.query(Parcelle).options(joinedload(Parcelle.cultures), joinedload(Parcelle.epandres)).all()
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = session.query(Parcelle).all()


    if surface is not None and surface > 0:
        if not any(parcelle.surface >= surface for parcelle in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune parcelle trouvée avec surface")
        data = [parcelle for parcelle in data if parcelle.surface >= surface]

    if coordonnees is not None:
        if not any(parcelle.coordonnees == coordonnees for parcelle in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune parcelle trouvée avec coordonnees")
        data = [parcelle for parcelle in data if parcelle.coordonnees == coordonnees]
    if nom_parcelle is not None:
        if not any(parcelle.nom_parcelle == nom_parcelle for parcelle in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune parcelle trouvée avec nom_parcelle")
        data = [parcelle for parcelle in data if parcelle.nom_parcelle == nom_parcelle]

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skip est plus grand que le nombre de parcelle")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"parcelles": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response

@router.get("/{parcelle}", status_code=status.HTTP_201_CREATED)
def read_parcelle(parcelle: int, populate: bool = False, header_authorization=authorization_header):
    """
    Récupère une ligne de la table parcelle
    ### Paramètres
    - no_parcelle: l'id de parcelle'
    ### Retour
    - un objet de type Parcelle
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    if populate is not False:
        data = (session.query(Parcelle).filter(Parcelle.no_parcelle == parcelle)
                .options(joinedload(Parcelle.cultures), joinedload(Parcelle.epandres)).first())
    else:
        data = (session.query(Parcelle).filter(Parcelle.no_parcelle == parcelle).first())

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcelle introuvable")

    return {"parcelle": data}