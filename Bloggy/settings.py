from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")


# This code snippet is used to enable debugging mode in the application.
# By setting DEBUG to True, the application will display detailed error messages and stack traces in case of any errors.
# It is recommended to set DEBUG to False in production environments for security reasons.
DEBUG = True


# The ALLOWED_HOSTS setting in Django is used to define a list of host/domain names that this Django site can serve.
# This is a security measure to prevent HTTP Host header attacks,
# which are possible even under many seemingly-safe web server configurations.
# Using ["*"]: As shown in the provided code, setting ALLOWED_HOSTS to ["*"] allows any domain to host your application.
# This is suitable for development but poses a security risk in production.
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # "jazzmin",
    "django.contrib.admin",  # Django admin app for administration interface
    "django.contrib.auth",  # Django authentication app
    "django.contrib.contenttypes",  # Django content types app
    "django.contrib.sessions",  # Django sessions app
    "django.contrib.messages",  # Django messages app
    "django.contrib.staticfiles",  # Django static files app
    "core",
    "ckeditor",  # Third-party app for rich text editing
    "admin_honeypot",  # Third-party app for detecting and logging unauthorized access attempts to the admin interface
    "allauth",  # Third-party app for authentication and account management
    "allauth.account",  # Third-party app for account management
    "allauth.socialaccount",  # Third-party app for social authentication
    "allauth.socialaccount.providers.github",  # Third-party app for GitHub social authentication
    "allauth.socialaccount.providers.yandex",  # Third-party app for Yandex social authentication
    "allauth.socialaccount.providers.google",  # Third-party app for Google social authentication
    "request",  # Third-party app for capturing HTTP requests
    "django_htmx",  # Third-party app for adding HTMX functionality to Django
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Provides various security enhancements to the project such as preventing clickjacking, adding content security policy headers, etc.
    "django.contrib.sessions.middleware.SessionMiddleware",  # Manages sessions across requests, enabling the use of session variables for storing information specific to a session.
    "django.middleware.common.CommonMiddleware",  # Provides common functionalities like URL trailing slash append or prepend and redirecting non-www to www URLs and vice versa.
    "django.middleware.csrf.CsrfViewMiddleware",  # Adds Cross-Site Request Forgery protection by adding hidden form fields to POST forms and checking requests for the correct tokens.
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Associates users with requests using sessions, enabling the use of request.user.
    "django.contrib.messages.middleware.MessageMiddleware",  # Enables cookie- and session-based message support for one-time notifications to the user.
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Prevents clickjacking by adding the X-Frame-Options header to HTTP responses. This header controls whether a browser should be allowed to render a page in a <frame>, <iframe>, <embed>, or <object>.
    "allauth.account.middleware.AccountMiddleware",  # Specific to the django-allauth package, it provides functionalities related to user accounts, such as handling email confirmation.
    "request.middleware.RequestMiddleware",  # Captures and stores details about each request in the database for debugging and analysis purposes.
    "django_htmx.middleware.HtmxMiddleware",  # Specific to integrating HTMX with Django, it enhances server-side processing by enabling partial page updates and AJAX requests in a more streamlined manner.
]

ROOT_URLCONF = "Bloggy.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.profile_context_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "Bloggy.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# AllAuth Config

LOGIN_REDIRECT_URL = "/blog"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 1800
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_USERNAME_MIN_LENGTH = 2


SITE_ID = 1


SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "VERIFIED_EMAIL": True,
        "APP": {
            "client_id": os.environ.get("GITHUB_CLIENT_ID"),
            "secret": os.environ.get("GITHUB_SECRET_KEY"),
            "key": "",
        },
    },
    "yandex": {
        "VERIFIED_EMAIL": True,
        "APP": {
            "client_id": os.environ.get("YANDEX_CLIENT_ID"),
            "secret": os.environ.get("YANDEX_SECRET_KEY"),
            "key": "",
        },
    },
    "google": {
        "VERIFIED_EMAIL": True,
        "APP": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "secret": os.environ.get("GOOGLE_SECRET_KEY"),
            "key": "",
        },
    },
}
