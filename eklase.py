from managers.journal_manager import JournalManager
from typing import NamedTuple
import aiohttp


class LoginData(NamedTuple):
    username: str
    password: str


class EklaseClientSession:
    def __init__(self, login_data: LoginData):
        self.aiohttp_session = aiohttp.ClientSession()
        self.login_data = login_data

        self.journal_manager = JournalManager(self)

    async def login(self) -> None:
        payload = {
            "username": self.login_data.username,
            "password": self.login_data.password
        }
        async with self.aiohttp_session.post("https://my.e-klase.lv/?v=15", data=payload) as response:
            if response.status != 200:
                raise ConnectionError(f"Unexpected login statuscode ({response.status}).")
            
            if not response.history:
                raise ValueError("Invalid login credentials.")

    async def __aenter__(self):
        await self.login()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aiohttp_session.close()