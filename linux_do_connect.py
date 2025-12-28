import re
from typing import Optional, Unpack

from curl_cffi import requests
from curl_cffi.requests import RequestParams

CONNECT_URL = "https://connect.linux.do"
IMPERSONATE = "chrome"
TOKEN_KEY = "_t"
CONNECT_KEY = "auth.session-token"

class LinuxDoConnect:
    def __init__(self, token: str, session: Optional[requests.AsyncSession] = requests.AsyncSession(),
                 connect_url: Optional[str] = CONNECT_URL, connect_token: str = "") -> None:
        self.session = session
        self.connect_url = connect_url

        session.cookies.set(TOKEN_KEY, token, domain="linux.do", secure=True)

    async def login(self, **kwargs: Unpack[RequestParams]) -> "LinuxDoConnect":
        await self.session.get(CONNECT_URL, impersonate=IMPERSONATE, **kwargs)
        return self

    async def get_session(self) -> requests.AsyncSession:
        return self.session

    async def get_connect_token(self) -> tuple[str, str | None]:
        """
        请自行维护 Token 的生命周期。当返回的第二个参数和输入 Token 有变化时，表示 Token 已刷新，请及时更新保存的 Token 值。
        """
        return self.session.cookies.get(CONNECT_KEY), self.session.cookies.get(TOKEN_KEY)

    async def approve_oauth(self, oauth_url: str, **kwargs: Unpack[RequestParams]) -> str:
        """
        :param oauth_url:
        :param kwargs:
        :return: oauth callback url
        """
        options = {
            "impersonate": IMPERSONATE,
            **kwargs,
        }
        r = await self.session.get(oauth_url, **options)

        if match := re.search(r'href\s*=\s*["\'](/oauth2/approve/[^"\']+)["\']', r.text):
            r = await self.session.get(f"{CONNECT_URL}{match.group(1)}", **options, allow_redirects=False)
            return r.headers["Location"]

        raise ValueError("Approve url not found")
