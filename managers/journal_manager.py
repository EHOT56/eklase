from models.journal_models import WeeklyJournalModel
from datetime import datetime, timedelta


class JournalManager:
    def __init__(self, eklase_client):
        self.eklase_client = eklase_client
    
    async def get_weekly_journal(self, date: datetime):
        async with self.eklase_client.aiohttp_session.get(f"https://my.e-klase.lv/Family/Diary?Date={datetime.strftime(date, '%d.%m.%Y.')}") as response:
            if response.status != 200:
                raise ConnectionError(f"Get weekly journal unexpected statuscode ({response.status})")

            if response.history:
                raise RuntimeError("Session expired: login required")
            
            return WeeklyJournalModel(await response.text())