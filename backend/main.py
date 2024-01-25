from datetime import datetime
from typing import Union
from database import session
from models import Compteur
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse

from router.compteur.compteur import router as compteur_router
from router.epandre.epandre import router as epandre_router
from router.unite.unite import router as unite_router


from router.parcelle.parcelle import router as parcelle_router

from router.date.date import router as date_router


from router.production.production import router as production_router
from router.engrais.engrais import router as engrais_router
from router.element_chimique.element_chimique import router as element_chimique_router
from router.posseder.posseder import router as posseder_router

from router.authentification.authentification import router as authentification_router
from router.culture.culture import router as culture_router

from jose import jwt

from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
@app.middleware("http")
async def verify_token(request: Request, call_next):
    """
    used to verify authorization from an http request
    request param = details on the request
    call_next     = call the function next the middleware
    """
        # Debug mode, no token verification
    if True :
        return await call_next(request)
    if request.url.path.startswith("/api"):
        # don't verify on route /jwt/
        if request.url.path == "/api/auth/jwt":
            return await call_next(request)
        # try to decode the token if there's one
        if request.headers.get('authorization') is not None:
            try:
                jwt.decode(request.headers.get('authorization'), os.getenv('JWT_SECRET'), algorithms=['HS256'])
            except Exception as e:
                return_message = {
                    "message": "Token de connection invalide",
                    "reason": str(e)
                }
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=return_message)
        else:
            return_message = {
                "message": "Aucun token de connexion envoyé",
            }
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=return_message)
        response = await call_next(request)
        return response
    else:
        return await call_next(request)

@app.middleware("http")
async def add_compteur(request: Request, call_next):
    """
    Ajoute une ligne dans la table compteur
    request param = details on the request
    call_next     = call the function next the middleware
    """
    routes = [
    "engrais",
    "unites",
    "elements_chimiques",
    "productions",
    "epandre",
    "compteur",
    "cultures",
    "dates",
    "parcelles",
    "posseder"
    ]
    if request.url.path.startswith("/api") and request.headers.get('referer') is None and request.url.path.split("/")[2] in routes:
        try:
            compteur = Compteur(
                horodatage=datetime.now(),
                route=request.url.path,
                methode=request.method
            )
            session.add(compteur)
            session.commit()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    response = await call_next(request)
    return response

app.include_router(epandre_router, prefix="/api")
app.include_router(unite_router, prefix="/api")

app.include_router(parcelle_router, prefix="/api")

app.include_router(engrais_router, prefix="/api")
app.include_router(element_chimique_router, prefix="/api")

app.include_router(authentification_router, prefix="/api")

app.include_router(date_router, prefix="/api")

app.include_router(production_router, prefix="/api")
app.include_router(compteur_router, prefix="/api")
app.include_router(posseder_router, prefix="/api")
app.include_router(culture_router, prefix="/api")



@app.get("/")
def read_root():
    return {"Hello": "World"}
