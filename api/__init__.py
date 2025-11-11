import os
from dotenv import load_dotenv

if os.path.isfile(".env"):
    # Is running in local testing environment
    # Load environment variables from .env file
    load_dotenv()

else:
    # Is running in deploy
    pass
