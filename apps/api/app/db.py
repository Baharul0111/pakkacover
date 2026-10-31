import json,hashlib,secrets
from datetime import datetime,timedelta,timezone
from sqlalchemy import String,DateTime,Boolean,ForeignKey,Float,select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy.types import TypeDecorator,LargeBinary
from ulid import ULID
from apps.api.app.config import get,fernet,SERVERLESS

def uid():return str(ULID())
def now():return datetime.now(timezone.utc)
class EncryptedJSON(TypeDecorator):
 impl=LargeBinary
 cache_ok=True
 def process_bind_param(self,value,dialect):return None if value is None else fernet().encrypt(json.dumps(value,ensure_ascii=False,default=str).encode())
 def process_result_value(self,value,dialect):return None if value is None else json.loads(fernet().decrypt(value))
class Base(DeclarativeBase):pass
class Journey(Base):
 __tablename__='journeys';__table_args__={'schema':'app'}
 id:Mapped[str]=mapped_column(String(26),primary_key=True,default=uid)
 payload:Mapped[dict]=mapped_column('payload_E',EncryptedJSON,default=dict,comment='health: encrypted journey, family, interview state and dates')
 lang:Mapped[str]=mapped_column(String(5),default='hi')
 saved:Mapped[bool]=mapped_column(Boolean,default=False)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class AuthToken(Base):
 __tablename__='auth_tokens';__table_args__={'schema':'app'}
 token_hash:Mapped[str]=mapped_column(String(64),primary_key=True)
 journey_id:Mapped[str]=mapped_column(String(26),index=True) # deliberately no FK: credentials cannot delete data
 expires_at:Mapped[datetime]=mapped_column(DateTime(timezone=True))
class Consent(Base):
 __tablename__='consent_events';__table_args__={'schema':'app'}
 id:Mapped[str]=mapped_column(String(26),primary_key=True,default=uid)
 journey_id:Mapped[str]=mapped_column(ForeignKey('app.journeys.id',ondelete='CASCADE'),index=True)
 purpose:Mapped[str]=mapped_column(String(32))
 granted:Mapped[bool]=mapped_column(Boolean)
 notice_version:Mapped[str]=mapped_column(String(32),default='demo-2026-10-31')
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Line(Base):
 __tablename__='disclosure_lines';__table_args__={'schema':'app'}
 id:Mapped[str]=mapped_column(String(26),primary_key=True,default=uid)
 journey_id:Mapped[str]=mapped_column(ForeignKey('app.journeys.id',ondelete='CASCADE'),index=True)
 slot:Mapped[str]=mapped_column(String(64))
 payload:Mapped[dict]=mapped_column('payload_E',EncryptedJSON,comment='health: encrypted values and proposal text')
 confirmed:Mapped[bool]=mapped_column(Boolean,default=False)
 version:Mapped[int]=mapped_column(default=1)
class AuditRun(Base):
 __tablename__='audit_runs';__table_args__={'schema':'app'}
 id:Mapped[str]=mapped_column(String(26),primary_key=True,default=uid)
 journey_id:Mapped[str]=mapped_column(ForeignKey('app.journeys.id',ondelete='CASCADE'),index=True)
 pdf_sha:Mapped[str]=mapped_column(String(64))
 payload:Mapped[dict]=mapped_column('payload_E',EncryptedJSON,comment='health: extracted fields and comparison')
class Payment(Base):
 __tablename__='payments';__table_args__={'schema':'app'}
 id:Mapped[str]=mapped_column(String(26),primary_key=True,default=uid)
 journey_id:Mapped[str]=mapped_column(ForeignKey('app.journeys.id',ondelete='CASCADE'),index=True)
 order_id:Mapped[str]=mapped_column(String(50),unique=True)
 mode:Mapped[str]=mapped_column(String(16))
 status:Mapped[str]=mapped_column(String(32),default='PENDING')
 verified:Mapped[bool]=mapped_column(Boolean,default=False)
 paid_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
class Notification(Base):
 __tablename__='notifications';__table_args__={'schema':'app'}
 id:Mapped[str]=mapped_column(String(26),primary_key=True,default=uid)
 journey_id:Mapped[str]=mapped_column(ForeignKey('app.journeys.id',ondelete='CASCADE'),index=True)
 order_id:Mapped[str]=mapped_column(String(50),unique=True)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
 read:Mapped[bool]=mapped_column(Boolean,default=False)
class AdvisorRequest(Base):
 __tablename__='advisor_requests';__table_args__={'schema':'app'}
 id:Mapped[str]=mapped_column(String(26),primary_key=True,default=uid)
 journey_id:Mapped[str]=mapped_column(ForeignKey('app.journeys.id',ondelete='CASCADE'),index=True)
 payload:Mapped[dict]=mapped_column('payload_E',EncryptedJSON,comment='health: encrypted callback brief')
 status:Mapped[str]=mapped_column(String(16),default='requested')
class ConfigFlag(Base):
 __tablename__='config_flags';__table_args__={'schema':'app'}
 key:Mapped[str]=mapped_column(String(64),primary_key=True)
 value:Mapped[dict]=mapped_column(JSONB)
class Usage(Base):
 __tablename__='usage';__table_args__={'schema':'app'}
 id:Mapped[str]=mapped_column(String(26),primary_key=True,default=uid)
 day:Mapped[str]=mapped_column(String(10),index=True)
 provider:Mapped[str]=mapped_column(String(16))
 amount:Mapped[float]=mapped_column(Float)
 model:Mapped[str]=mapped_column(String(96))
 step:Mapped[str]=mapped_column(String(40))
 outcome:Mapped[str]=mapped_column(String(32),default='ok')
class Idempotency(Base):
 __tablename__='idempotency_keys';__table_args__={'schema':'app'}
 key:Mapped[str]=mapped_column(String(96),primary_key=True)
 journey_id:Mapped[str]=mapped_column(ForeignKey('app.journeys.id',ondelete='CASCADE'),index=True)
 payload:Mapped[dict]=mapped_column('payload_E',EncryptedJSON,comment='health: encrypted response cache')

url=get('DATABASE_URL')
if not url:raise RuntimeError('DATABASE_URL is empty; run scripts/bootstrap_local_db before starting')
url=url.replace('postgres://','postgresql://',1).replace('postgresql://','postgresql+asyncpg://',1)
# Supabase URLs can include SSL query fields consumed by asyncpg as connect arguments.
from sqlalchemy.engine import make_url
u=make_url(url); q=dict(u.query);q.pop('sslmode',None);q.pop('ssl',None)
ssl_value='require' if u.host not in ('localhost','127.0.0.1','::1') else False
from sqlalchemy.pool import NullPool
if SERVERLESS:
 if u.host in ('localhost','127.0.0.1','::1'):raise RuntimeError('Hosted database must be remote')
 u=u.set(port=6543)
 pool_options={'poolclass':NullPool}
else:pool_options={'pool_size':5,'max_overflow':2,'pool_pre_ping':True,'pool_recycle':300}
engine=create_async_engine(u.set(query=q),**pool_options,connect_args={'statement_cache_size':0,'ssl':ssl_value,'timeout':10})
Session=async_sessionmaker(engine,expire_on_commit=False)
async def session():
 async with Session() as s:yield s
