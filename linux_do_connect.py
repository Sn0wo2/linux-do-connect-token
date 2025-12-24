from http import HTTPStatus
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

        r = await self.session.get(
            CONNECT_URL,
            impersonate=IMPERSONATE,
            allow_redirects=False,
            **kwargs
        )

        if r.status_code != HTTPStatus.FOUND:
            raise Exception(f"Cannot get redirect url from {CONNECT_URL}")

        redirect_url = r.headers.get('Location')
        if not redirect_url:
            raise Exception("No Location header found in response")

        await self.session.get(
            redirect_url,
            impersonate=IMPERSONATE,
            cookies={AUTH_COOKIE_KEY: connect_cookie},
            **kwargs
        )

        return self.session

    async def get_token(self, connect_cookie: str, **kwargs) -> Optional[str]:
        await self.login(connect_cookie, **kwargs)
        return self.session.cookies.get(SESSION_TOKEN_KEY)


async def get_auth_session(connect_cookie: str, session: Optional[requests.AsyncSession] = None,
                           **kwargs) -> requests.AsyncSession:
    connector = LinuxDoConnect(session)
    return await connector.login(connect_cookie, **kwargs)
