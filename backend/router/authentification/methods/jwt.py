from router.authentification.authentification import router
from jose import jwt
import uuid
from datetime import datetime, timedelta
from fastapi import status

import os


@router.get("/jwt", status_code=status.HTTP_201_CREATED)
def create_jwt(expire_in: int = 3600):
    """
    Renvoie un jwt valide
    ### Paramètres
    - expire_in: temps (en seconde) de validité du token (par défaut 1 heure : 3600)
    ### Retour
    - Status code 201 avec le token
    """
    secret = os.getenv('JWT_SECRET')
    token = jwt.encode(claims={"id": str(uuid.uuid4()), "exp": datetime.utcnow() + timedelta(seconds=expire_in)},
                       key=secret, algorithm='HS256')

    return {"message": "JWT created", "access_token": token, "expire_in": expire_in}
