from .base import * 
import dj_database_url
import os
from .base import BASE_DIR, env

env_path = BASE_DIR / ".env"
if env_path.exists():
    env.read_env(str(env_path))

DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")

# Hosts (Render expone RENDER_EXTERNAL_HOSTNAME)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# HTTPS detrás de proxy (Render)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

# CSRF para el dominio de Render (para POST de forms como login/logout)
CSRF_TRUSTED_ORIGINS = []
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# DB desde DATABASE_URL (Render te lo da)
# DATABASES = {
#     "default": dj_database_url.config(conn_max_age=60, ssl_require=True)
# }
# SSL requerido en Render, pero NO en local
DB_SSL_REQUIRE = env.bool("DJANGO_DB_SSL_REQUIRE", default=True)

DATABASES = {
    "default": dj_database_url.config(conn_max_age=60, ssl_require=DB_SSL_REQUIRE)
}

# Static con WhiteNoise (sin S3)
STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}
MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware", *MIDDLEWARE]  # noqa: F405

# Cache simple (sin Redis)
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# Email simple
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Allauth (tu Opción A)
ACCOUNT_LOGOUT_ON_GET = False
LOGIN_REDIRECT_URL = "users:panel"
LOGOUT_REDIRECT_URL = "account_login"

# Admin URL (si el proyecto lo usa)
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")