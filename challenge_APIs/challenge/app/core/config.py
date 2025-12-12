import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Variables que voy a usar en el Cohere
API_KEY = os.getenv("COHERE_API_KEY") # Variable para relacionarnos con cohere