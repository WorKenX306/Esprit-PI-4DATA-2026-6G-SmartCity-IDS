from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
APP_WEB_DIR = BASE_DIR.parent
PROJECT_ROOT = APP_WEB_DIR.parent


def _first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


MLOPS_DIR = _first_existing(PROJECT_ROOT / "mlops", PROJECT_ROOT / "MLOPS")
DATA_DIR = _first_existing(
    MLOPS_DIR / "data",
    APP_WEB_DIR / "public" / "data",
    PROJECT_ROOT / "Data5G",
)
MLRUNS_DIR = _first_existing(MLOPS_DIR / "mlruns", PROJECT_ROOT / "mlruns")
DEFAULT_DB_PATH = BASE_DIR / "iotinel.db"

JWT_SECRET = os.getenv("JWT_SECRET", "hexamind-dev-secret")
JWT_ALGORITHM = "HS256"
TOKEN_COOKIE_NAME = "iotinel_access_token"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", MLRUNS_DIR.as_posix())
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN", "hexamind-internal-token")
MLOPS_API_BASE = os.getenv("MLOPS_API_BASE", "http://mlops-api:8000")
MLOPS_API_LOCAL = os.getenv("MLOPS_API_LOCAL", "http://localhost:8088")
ELASTICSEARCH_URL = os.getenv(
    "ELASTICSEARCH_URL",
    os.getenv("ES_HOST", "http://mlops-elasticsearch:9200"),
)
ELASTICSEARCH_TIMEOUT = float(os.getenv("ELASTICSEARCH_TIMEOUT", "5"))

SERVICE_PORTS = {
    "gateway": 8000,
    "auth": 8001,
    "detection": 8002,
    "training": 8003,
    "monitoring": 8004,
    "dashboard": 8005,
    "admin": 8006,
}

def _service_url(env_key: str, default: str) -> str:
    """Normalise a service URL from an env var.

    Render injects the *host* (e.g. ``iotinel-auth.onrender.com``) via the
    ``fromService … property: host`` blueprint directive.  We need a full URL,
    so we prepend ``https://`` when the value has no scheme.
    """
    raw = os.getenv(env_key, "").strip()
    if not raw:
        return default
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    return f"https://{raw}"


SERVICE_URLS = {
    "auth": _service_url("AUTH_SERVICE_URL", "http://auth_service:8001"),
    "detection": _service_url("DETECTION_SERVICE_URL", "http://detection_service:8002"),
    "training": _service_url("TRAINING_SERVICE_URL", "http://ml_training_service:8003"),
    "monitoring": _service_url("MONITORING_SERVICE_URL", "http://monitoring_service:8004"),
    "dashboard": _service_url("DASHBOARD_SERVICE_URL", "http://dashboard_service:8005"),
    "admin": _service_url("ADMIN_SERVICE_URL", "http://admin_service:8006"),
    "analyst_ui": _service_url("ANALYST_UI_URL", "http://analyst-ui:80"),
    "scientist_ui": _service_url("SCIENTIST_UI_URL", "http://scientist-ui:80"),
    "admin_ui": _service_url("ADMIN_UI_URL", "http://admin-ui:80"),
}

_extra_origins = os.getenv("ALLOWED_ORIGINS", "")
_extra_list = [o.strip() for o in _extra_origins.split(",") if o.strip()]

ALLOWED_ORIGINS = [
    "http://localhost:8010",
    "http://127.0.0.1:8010",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3002",
    "http://127.0.0.1:3003",
    *_extra_list,
]
