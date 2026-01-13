import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

# Football API Configuration
# Assuming usage of an API like football-data.org or similar
FOOTBALL_API_KEY = os.getenv('FOOTBALL_API_KEY')
FOOTBALL_API_URL = os.getenv('FOOTBALL_API_URL', 'https://api.football-data.org/v4')

# Validation
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env")
if not FOOTBALL_API_KEY:
    print("Warning: FOOTBALL_API_KEY not found in .env")
