import asyncio
import logging
import os
import sys

# Add the project root to python path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import DISCORD_TOKEN
from src.bot.discord_bot import FootballBot

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    if not DISCORD_TOKEN:
        logger.error("No valid DISCORD_TOKEN found. Exiting.")
        return

    bot = FootballBot()
    
    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.exception("An error occurred running the bot.")
