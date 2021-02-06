import os
from os.path import join, dirname
from dotenv import load_dotenv
load_dotenv(join(dirname(__file__), ".env"))

class Config:
    """Contains program config constants."""
    TOKEN = os.environ.get("mathbot-token")
    GUILD = "Fermicide's server"
