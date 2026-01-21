import os

debug_mode: bool = os.getenv("DJANGO_DEBUG", "True") == "True"
host_email: str = os.getenv("EMAIL_HOST_USER", "")
host_password: str = os.getenv("EMAIL_HOST_PASSWORD", "")
