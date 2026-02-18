import re
from typing import Unpack, cast, Optional
from urllib.parse import urlparse

from curl_cffi import requests
from curl_cffi.requests.session import RequestParams, BrowserTypeLiteral

BASE_URL = "https://linux.do"
CONNECT_URL = "https://connect.linux.do"
IMPERSONATE: BrowserTypeLiteral = "chrome"
TOKEN_KEY = "_t"
CONNECT_KEY = "auth.session-token"

class LinuxDoConnect:
    def __init__(self, token: str = "",
                 session: Optional[requests.AsyncSession] = None,
                 base_url: str = BASE_URL,
                 connect_url: str = CONNECT_URL) -> None:
        self.session = session or requests.AsyncSession()
        self.connect_url = connect_url
        self.base_url = base_url
        self.base_domain = urlparse(base_url).hostname or "linux.do"
        self.connect_domain = urlparse(connect_url).hostname or "connect.linux.do"

        if token:
            self.session.cookies.set(TOKEN_KEY, token, domain=self.base_domain, secure=True)

    async def login(self, **kwargs: Unpack[RequestParams]) -> "LinuxDoConnect":
        if "impersonate" not in kwargs:
            kwargs["impersonate"] = IMPERSONATE
        await self.session.get(self.connect_url, **kwargs)
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
        return self.session.cookies.get(CONNECT_KEY, domain=self.connect_domain) or "", self.session.cookies.get(
            TOKEN_KEY)

    async def approve_oauth(self, oauth_url: str, **kwargs: Unpack[RequestParams]) -> str:
        """
        :param oauth_url:
        :param kwargs:
        :return: oauth callback url
        """
        if "impersonate" not in kwargs:
            kwargs["impersonate"] = IMPERSONATE
        
        r = await self.session.get(oauth_url, **kwargs)

        if match := re.search(r'href\s*=\s*["\'](/oauth2/approve/[^"\']+)["\']', r.text):
            approve_kwargs = kwargs.copy()
            approve_kwargs["allow_redirects"] = False
            r = await self.session.get(f"{self.connect_url}{match.group(1)}", **approve_kwargs)
            return cast(str, r.headers.get("Location", ""))

        raise ValueError("Approve url not found")
