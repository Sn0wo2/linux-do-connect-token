import re
from typing import Unpack
from urllib.parse import urlparse

from curl_cffi import requests
from curl_cffi.requests import RequestParams

BASE_URL = "https://linux.do"
CONNECT_URL = "https://connect.linux.do"
IMPERSONATE = "chrome"
TOKEN_KEY = "_t"
CONNECT_KEY = "auth.session-token"

class LinuxDoConnect:
    def __init__(self, session: requests.AsyncSession = requests.AsyncSession(),
                 base_url: str = BASE_URL,
                 connect_url: str = CONNECT_URL,
                 token: str = "") -> None:
        self.session = session
        self.connect_url = connect_url
        self.base_url = base_url
        self.base_domain = urlparse(base_url).hostname
        self.connect_domain = urlparse(connect_url).hostname

        if token:
            session.cookies.set(TOKEN_KEY, token, domain=self.base_domain, secure=True)

    async def login(self, **kwargs: Unpack[RequestParams]) -> "LinuxDoConnect":
        await self.session.get(self.connect_url, impersonate=IMPERSONATE, **kwargs)
        return self

    def set_connect_token(self, connect_token: str) -> "LinuxDoConnect":
        """
        如果你拥有 LINUX_DO_CONNECT_TOKEN，可以使用此方法直接设置 LINUX_DO_CONNECT_TOKEN，跳过login。
        :param connect_token:
        :return:
        """
        self.session.cookies.set(CONNECT_KEY, connect_token, domain=self.connect_domain)
        return self

    async def get_session(self) -> requests.AsyncSession:
        return self.session

    async def get_connect_token(self) -> tuple[str, str | None]:
        """
        请自行维护 Token 的生命周期。当返回的第二个参数和输入 Token 有变化时，表示 Token 已刷新，请及时更新保存的 Token 值。
        """
        return self.session.cookies.get(CONNECT_KEY, domain=self.connect_domain), self.session.cookies.get(TOKEN_KEY)

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
            r = await self.session.get(f"{self.connect_url}{match.group(1)}", **options, allow_redirects=False)
            return r.headers["Location"]

        raise ValueError("Approve url not found")
