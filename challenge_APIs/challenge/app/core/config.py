import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)

# Variables que voy a usar en el Cohere
API_KEY = os.getenv("COHERE_API_KEY") # Variable para relacionarnos con cohere