from database import session
from router.compteur.compteur import router
from models import Compteur
from fastapi import HTTPException, status
from authorization import authorization_header
from database import base_url

@router.get("/", status_code=status.HTTP_200_OK)
def read_compteurs(skip: int = 0, limit: int = 10, sort: str = None, methode: str = None, route: str = None, header_authorization=authorization_header):
    """
    Récupère les lignes de la table compteur
    ### Paramètres
    - skip: nombre d'éléments à sauter
    - limit: nombre d'éléments à retourner
    - sort: champs à trier
    ### Retour
    - un tableau d'objets de type Compteur
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """
    url = f"{base_url}/api/compteur?"

    data = session.query(Compteur).all()

    sortable = Compteur.__table__.columns.keys()

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
                sort_criteria.append(getattr(Compteur, s[1:]).desc())
                sort_url += f"-{s[1:]},"
            else:
                sort_criteria.append(getattr(Compteur, s))
                sort_url += f"{s},"
        if url[-1] != "?":
            url += "&"
        url += f"sort={sort_url[:-1]}"
        data = session.query(Compteur).order_by(*sort_criteria).all()

    if methode is not None:
        methode = methode.upper()
        if not any(compteur.methode == methode for compteur in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune méthode trouvée")
        data = [compteur for compteur in data if compteur.methode == methode]

    if route is not None:
        if not any(compteur.route.split("/")[2] == route for compteur in data):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune route trouvée")
        data = [compteur for compteur in data if compteur.route.split("/")[2] == route]

    if len(data) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun engrais trouvé")

    if skip >= len(data):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skip est plus grand que le nombre d'engrais")

    if limit > len(data):
        limit = len(data)

    if url[-1] != "?":
        url += "&"

    response = {"compteur": data[skip:skip + limit]}

    if skip + limit < len(data):
        response["nextPage"] = f"{url}skip={str(skip + limit)}&limit={str(limit)}"
    if skip > 0:
        response["previousPage"] = f"{url}skip={str(skip - limit)}&limit={str(limit)}"
    return response

@router.get("/stats", status_code=status.HTTP_200_OK)
def read_stats(header_authorization=authorization_header):
    """
    Récupère les statistiques de la table Compteur
    ### Retour
    - un objet contenant les statistiques
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """

    methods = session.query(Compteur.methode).distinct().all()
    method_count = {methods[i][0]: session.query(Compteur).filter(Compteur.methode == methods[i][0]).count() for i in
                    range(len(methods))}
    method_count = dict(sorted(method_count.items(), key=lambda x: x[1], reverse=True))

    routes = session.query(Compteur.route).distinct().all()
    route_count = {routes[i][0]: session.query(Compteur).filter(Compteur.route == routes[i][0]).count() for i in
               range(len(routes))}
    route_count = dict(sorted(route_count.items(), key=lambda x: x[1], reverse=True))
    total_route_count = {}
    for key, value in route_count.items():
        if key.split("/")[2] not in total_route_count:
            total_route_count.update({key.split("/")[2]: value})
        else:
            total_route_count[key.split("/")[2]] += value
    total_route_count = dict(sorted(total_route_count.items(), key=lambda x: x[1], reverse=True))

    methods_percentages = {methods[i][0]: session.query(Compteur).filter(Compteur.methode == methods[i][0]).count() / session.query(Compteur).count() * 100 for i in
                    range(len(methods))}
    methods_percentages = dict(sorted(methods_percentages.items(), key=lambda x: x[1], reverse=True))
    for key, value in methods_percentages.items():
        methods_percentages[key] = round(value, 2)

    routes_percentages = {routes[i][0]: session.query(Compteur).filter(Compteur.route == routes[i][0]).count() / session.query(Compteur).count() * 100 for i in
                range(len(routes))}
    routes_percentages = dict(sorted(routes_percentages.items(), key=lambda x: x[1], reverse=True))
    for key, value in routes_percentages.items():
        routes_percentages[key] = round(value, 2)




    reponse = {"methode_count": method_count, "route_count": total_route_count, "percentages": {"methodes": methods_percentages, "routes": routes_percentages}}
    return reponse

@router.get("/stats/{route}", status_code=status.HTTP_200_OK)
def read_stats_by_route(route: str, header_authorization=authorization_header):
    """
    Récupère les statistiques de la table compteur pour une route
    ### Paramètres
    - route: la route
    ### Retour
    - un objet contenant les statistiques
    - un message d'erreur en cas d'erreur
    - un status code correspondant
    """
    routes = session.query(Compteur.route).filter(Compteur.route.like(f"%/api/{route}%")).distinct().all()
    if len(routes) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucune route trouvée")
    route_count = {routes[i][0]: session.query(Compteur).filter(Compteur.route == routes[i][0]).count() for i in
                  range(len(routes))}
    route_count = dict(sorted(route_count.items(), key=lambda x: x[1], reverse=True))

    methods = session.query(Compteur.methode).filter(Compteur.route.like(f"%/api/{route}%")).distinct().all()
    method_count = {methods[i][0]: session.query(Compteur).filter(Compteur.route.like(f"%/api/{route}%")).filter(Compteur.methode == methods[i][0]).count() for i in
                    range(len(methods))}
    method_count = dict(sorted(method_count.items(), key=lambda x: x[1], reverse=True))


    return {"methodes": method_count, "routes": route_count}
