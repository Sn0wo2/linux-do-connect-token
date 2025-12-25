from typing import Optional

from curl_cffi import requests

CONNECT_URL = "https://connect.linux.do"
IMPERSONATE = "chrome"
AUTH_COOKIE_KEY = "_t"
SESSION_TOKEN_KEY = "auth.session-token"

class LinuxDoConnect:
    def __init__(self, session: Optional[requests.AsyncSession] = None):
        self.session = session or requests.AsyncSession()

    async def login(self, connect_cookie: str, **kwargs) -> requests.AsyncSession:
        options = {"impersonate": IMPERSONATE, "allow_redirects": False, **kwargs}
        r = await self.session.get(CONNECT_URL, **options)
        r = await self.session.get(
            r.headers["Location"],
            cookies={AUTH_COOKIE_KEY: connect_cookie},
            **options,
        )
        await self.session.get(r.headers["Location"], **options)

        return self.session


async def get_auth_token(session: requests.AsyncSession) -> tuple[str, str]:
    return session.cookies.get(SESSION_TOKEN_KEY), session.cookies.get(AUTH_COOKIE_KEY)
