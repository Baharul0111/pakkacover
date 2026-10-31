"""All person-data reads are scoped to the authenticated journey owner."""
import hashlib
from datetime import timedelta
from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy import select
from apps.api.app.db import Session,AuthToken,Journey,now
bearer=HTTPBearer(auto_error=False)
async def principal(credentials:HTTPAuthorizationCredentials|None=Depends(bearer)):
 if not credentials:raise HTTPException(401,'Start a session first')
 digest=hashlib.sha256(credentials.credentials.encode()).hexdigest()
 async with Session() as s:
  token=await s.scalar(select(AuthToken).where(AuthToken.token_hash==digest,AuthToken.expires_at>now()))
  if not token:raise HTTPException(401,'Session expired; start again')
  return token.journey_id
async def owned(s,model,object_id,owner,lock=False):
 field=model.id
 condition=(Journey.id==owner) if model is Journey else (model.journey_id==owner)
 query=select(model).where(field==object_id,condition)
 if lock:query=query.with_for_update()
 row=await s.scalar(query)
 if row is None:raise HTTPException(404,'Not found')
 return row
