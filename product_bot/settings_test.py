from .settings import INSTALLED_APPS, MIDDLEWARE, TEMPLATES

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_product_db",
        "USER": "test_user",
        "PASSWORD": "test_password",
        "HOST": "test_db",
        "PORT": "5432",
    },
}

DEBUG = False

MIDDLEWARE = MIDDLEWARE
TEMPLATES = TEMPLATES
INSTALLED_APPS = INSTALLED_APPS
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
