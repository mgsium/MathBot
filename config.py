from dotenv import load_dotenv
load_dotenv()

import os

class Config:
    TOKEN = os.environ.get("mathbot-token")
    GUILD = "Fermicide's server"