"""Contains basic configurations for the application."""
from os import environ

REDIS_URL = environ.get("REDIS_URL", "redis://localhost:6379/0")
