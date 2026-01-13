import discord
from discord.ext import commands, tasks
import logging
from src.config import DISCORD_CHANNEL_ID
from src.services.football_api import FootballAPI

logger = logging.getLogger(__name__)

class FootballBot(commands.Bot):
    def __init__(self):
        # Intents are required for modern Discord bots
        intents = discord.Intents.default()
        intents.message_content = True 
        
        super().__init__(command_prefix='!', intents=intents, help_command=None)
        
        self.football_api = FootballAPI()
        self.notification_channel_id = int(DISCORD_CHANNEL_ID) if DISCORD_CHANNEL_ID else None
        self.known_match_ids = set() # Track matches to avoid duplicate alerts
        self.match_states = {} # Store score/status

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        if self.notification_channel_id:
            logger.info("Starting live score task...")
            self.live_score_task.start()
        else:
            logger.warning("DISCORD_CHANNEL_ID not set. Notification task will not start.")

    async def setup_hook(self):
        # Load extensions (cogs) here
        try:
            await self.load_extension('src.bot.cogs.football_commands')
            logger.info("Loaded extension: src.bot.cogs.football_commands")
            
            # Sync commands to Discord (required for Slash Commands / Suggestions)
            # Note: This syncs globally, which might take time to propagate. 
            # For development, syncing to a specific guild is faster.
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} commands globally.")
            
        except Exception as e:
            logger.error(f"Failed to load extension or sync commands: {e}")

    @tasks.loop(minutes=1)
    async def live_score_task(self):
        """Background task to check for live scores and notify on changes."""
        try:
            matches = await self.football_api.get_live_matches()
        except Exception as e:
            logger.error(f"Failed to fetch matches: {e}")
            return

        channel = self.get_channel(self.notification_channel_id)
        if not channel:
            return

        current_match_ids = set()

        for match in matches:
            match_id = match.get('id')
            current_match_ids.add(match_id)
            
            home_team = match.get('homeTeam', {}).get('name', 'Home')
            away_team = match.get('awayTeam', {}).get('name', 'Away')
            score_home = match.get('score', {}).get('fullTime', {}).get('home', 0)
            score_away = match.get('score', {}).get('fullTime', {}).get('away', 0)
            status = match.get('status', 'LIVE')
            
            match_state = {
                'score_home': score_home,
                'score_away': score_away,
                'status': status
            }

            # Check previous state
            if match_id not in self.known_match_ids:
                # New match found
                self.known_match_ids.add(match_id)
                self.match_states[match_id] = match_state
                await self.send_notification(channel, "⚽ Match Started / Tracking", home_team, away_team, score_home, score_away, status, discord.Color.blue())
            
            else:
                prev_state = self.match_states.get(match_id)
                if prev_state != match_state:
                    # Something changed (Score or Status)
                    self.match_states[match_id] = match_state
                    title = "⚽ Update"
                    color = discord.Color.green()
                    
                    if (score_home != prev_state['score_home']) or (score_away != prev_state['score_away']):
                        title = "🥅 GOAL!"
                        color = discord.Color.gold()
                    
                    await self.send_notification(channel, title, home_team, away_team, score_home, score_away, status, color)

        # Cleanup finished matches (optional logic: check if id disappeared from live list)
        # Note: In some APIs, finished matches stay in 'live' endpoint for a bit or move to 'finished'.
        # For simplicity, if it's no longer in the list returned by 'live' endpoint, we assume it's done or no longer live.
        # We can implement a cleanup:
        for old_id in list(self.known_match_ids):
            if old_id not in current_match_ids:
                self.known_match_ids.remove(old_id)
                if old_id in self.match_states:
                    del self.match_states[old_id]
                # Optional: Send "Tracking Ended" message

    async def send_notification(self, channel, title, home, away, score_h, score_a, status, color):
        embed = discord.Embed(title=title, description=f"{home} vs {away}", color=color)
        embed.add_field(name="Score", value=f"{score_h} - {score_a}", inline=False)
        embed.add_field(name="Status", value=status, inline=True)
        await channel.send(embed=embed)

    @live_score_task.before_loop
    async def before_live_score_task(self):
        await self.wait_until_ready()

    async def on_command_error(self, context, exception):
        logger.error(f"Command error: {exception}")
