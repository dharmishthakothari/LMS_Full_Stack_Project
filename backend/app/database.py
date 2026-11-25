import ssl
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings


def get_sqlalchemy_url_and_connect_args(raw_url: str) -> tuple[str, dict]:
    """Normalize mysql:// to mysql+pymysql:// and translate ssl-mode=REQUIRED for PyMySQL."""
    url = raw_url.strip()
    if url.startswith("mysql://"):
        url = "mysql+pymysql://" + url[len("mysql://"):]

    connect_args = {}
    parsed = urlparse(url)
    query = parse_qs(parsed.query, keep_blank_values=True)
    ssl_mode = query.pop("ssl-mode", query.pop("ssl_mode", [None]))[0]
    if ssl_mode and ssl_mode.upper() in ("REQUIRED", "VERIFY_CA", "VERIFY_IDENTITY"):
        ctx = ssl.create_default_context()
        if ssl_mode.upper() == "REQUIRED":
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        connect_args["ssl"] = ctx

    new_query = urlencode(query, doseq=True)
    clean_url = urlunparse(parsed._replace(query=new_query))
    return clean_url, connect_args


_db_url, _connect_args = get_sqlalchemy_url_and_connect_args(settings.DATABASE_URL)

# Engine configuration with strict connection testing
# Silent SQLite fallback has been removed to ensure errors are surfaced immediately.
engine = create_engine(
    _db_url,
    connect_args=_connect_args,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
