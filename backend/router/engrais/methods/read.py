from authorization import authorization_header
from database import session
from router.engrais.engrais import router
from models import Engrais
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload
from database import base_url
@router.get("/", status_code=status.HTTP_200_OK)
def read_engrais(skip: int = 0, limit: int = 10, sort: str = None, un: str = None, populate: bool = False
                 , nom_engrais: str = None, header_authorization=authorization_header):
    """
    Récupère les lignes de la table engrais
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    - sort: le ou les champs sur lequel trier les résultats
    - un: le nom de l'unite à filtrer
    ### Retour
    - un objet JSON contenant les lignes de la table Engrais, filtrées et/ou triées
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    - url de navigation pour la pagination
    """
    url = f"{base_url}/api/engrais?"

    sortable = Engrais.__table__.columns.keys()

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
                sort_criteria.append(getattr(Engrais, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Engrais, s))
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
        if populate is not False:
            data = (session.query(Engrais).order_by(*sort_criteria)
                    .options(joinedload(Engrais.epandres), joinedload(Engrais.posseder), joinedload(Engrais.unite)).all())
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = (session.query(Engrais).order_by(*sort_criteria).all())
    else:
        if populate is not False:
            data = (session.query(Engrais)
                    .options(joinedload(Engrais.epandres), joinedload(Engrais.posseder), joinedload(Engrais.unite)).all())
            if url[-1] != "?":
                url += "&"
            url += f"populate=true"
        else:
            data = (session.query(Engrais).all())


    if un is not None:
        if not any(engrais.un == un for engrais in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune unité trouvée")
        data = [engrais for engrais in data if engrais.un == un]

    if nom_engrais is not None:
        if not any(engrais.nom_engrais == nom_engrais for engrais in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun nom d'engrais trouvé")
        data = [engrais for engrais in data if engrais.nom_engrais == nom_engrais]

    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun engrais trouvé")

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skip est plus grand que le nombre d'engrais")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"engrais": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"

    return response
  
@router.get("/{id_engrais}", status_code=status.HTTP_200_OK)
def read_engrais_by_id_engrais(id_engrais: int, populate: bool = False, header_authorization=authorization_header):
    """
    Récupère une ligne dans la table Engrais
    ### Paramètres
    - id_engrais: l'identifiant de l'engrais
    ### Retour
    - un object de type Engrais
    - un message de confirmation ou d'erreur
    - un status code correspondant
    """

    if populate is not False:
        data = (session.query(Engrais).filter(Engrais.id_engrais == id_engrais)
                .options(joinedload(Engrais.epandres), joinedload(Engrais.posseder), joinedload(Engrais.unite)).first())
    else:
        data = (session.query(Engrais).filter(Engrais.id_engrais == id_engrais).first())

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Engrais introuvable")

    return {"engrais": data}
