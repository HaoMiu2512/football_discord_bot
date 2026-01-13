import aiohttp
import logging
from src.config import FOOTBALL_API_URL, FOOTBALL_API_KEY

logger = logging.getLogger(__name__)

class FootballAPI:
    def __init__(self):
        self.base_url = FOOTBALL_API_URL
        self.headers = {
            'X-Auth-Token': FOOTBALL_API_KEY
        } if FOOTBALL_API_KEY else {}

    async def get_match_by_id(self, match_id):
        """Fetch details of a specific match."""
        url = f"{self.base_url}/matches/{match_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error fetching match {match_id}: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Exception in get_match_by_id: {e}")
                return None

    async def get_team_matches(self, team_id, status=None, limit=None):
        """Fetch matches for a specific team."""
        url = f"{self.base_url}/teams/{team_id}/matches"
        params = {}
        if status:
            params['status'] = status
        if limit:
            params['limit'] = limit
            
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('matches', [])
                    else:
                        logger.error(f"Error fetching team matches {team_id}: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"Exception in get_team_matches: {e}")
                return []

    async def get_matches(self, status=None, **kwargs):
        """
        Fetches matches. Status is optional.
        """
        url = f"{self.base_url}/matches"
        params = {}
        if status:
            params['status'] = status
        params.update(kwargs)
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('matches', [])
                    else:
                        logger.error(f"Error fetching matches: {response.status} - {await response.text()}")
                        return []
            except Exception as e:
                logger.error(f"Exception in get_matches: {e}")
                return []

    async def get_live_matches(self):
        return await self.get_matches(status='LIVE')
        
    async def get_scheduled_matches(self):
        return await self.get_matches(status='SCHEDULED')

    async def get_finished_matches(self):
        # Limit to recent finished matches (e.g. today or default filtering)
        # We can pass dateFrom/dateTo if needed, but here we rely on standard behavior (usually today's matches)
        return await self.get_matches(status='FINISHED')

    async def get_competitions(self):
        """Fetch list of available competitions."""
        url = f"{self.base_url}/competitions"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('competitions', [])
                    else:
                        logger.error(f"Error fetching competitions: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"Exception in get_competitions: {e}")
                return []

    async def get_standings(self, competition_code):
        """Fetch standings for a specific competition (e.g., PL, PD, SA)."""
        url = f"{self.base_url}/competitions/{competition_code}/standings"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('standings', [])
                    else:
                        logger.error(f"Error fetching standings: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Exception in get_standings: {e}")
                return None

    async def get_top_scorers(self, competition_code):
        """Fetch top scorers for a competition."""
        url = f"{self.base_url}/competitions/{competition_code}/scorers"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('scorers', [])
                    else:
                        logger.error(f"Error fetching scorers: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Exception in get_top_scorers: {e}")
                return None

    async def get_areas(self):
        """Fetch all available areas."""
        url = f"{self.base_url}/areas"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('areas', [])
                    else:
                        logger.error(f"Error fetching areas: {response.status}")
                        return []
            except Exception as e:
                logger.error(f"Exception in get_areas: {e}")
                return []

    async def get_teams_in_competition(self, competition_code):
        """Fetch all teams in a specific competition."""
        url = f"{self.base_url}/competitions/{competition_code}/teams"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('teams', [])
                    else:
                        logger.error(f"Error fetching teams for {competition_code}: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Exception in get_teams_in_competition: {e}")
                return None

    async def get_team(self, team_id):
        """Fetch specific team details."""
        url = f"{self.base_url}/teams/{team_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error fetching team {team_id}: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Exception in get_team: {e}")
                return None

    async def get_person(self, person_id):
        """Fetch specific person (player/coach) details."""
        url = f"{self.base_url}/persons/{person_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Error fetching person {person_id}: {response.status}")
                        return None
            except Exception as e:
                logger.error(f"Exception in get_person: {e}")
                return None
