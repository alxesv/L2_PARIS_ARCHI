from fastapi import Security
from fastapi.security import APIKeyHeader

authorization_header = Security(APIKeyHeader(name='Authorization', scheme_name='jwt'))