from http import HTTPStatus
from typing import Optional
from curl_cffi import requests

class LinuxDoConnect:
    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()

    def login(self, connect_cookie: str, **kwargs) -> requests.Session:
        r = self.session.get(
            "https://connect.linux.do",
            impersonate="chrome",
            allow_redirects=False,
            **kwargs
        )
        
        if r.status_code != HTTPStatus.FOUND:
            raise Exception("Cannot get redirect url from connect.linux.do")

        redirect_url = r.headers.get('Location')
        if not redirect_url:
            raise Exception("No Location header found in response")

        self.session.get(
            redirect_url,
            impersonate="chrome",
            cookies={'_t': connect_cookie},
            **kwargs
        )
        
        return self.session

    def get_token(self, connect_cookie: str, **kwargs) -> Optional[str]:
        self.login(connect_cookie, **kwargs)
        return self.session.cookies.get("auth.session-token")

def get_auth_session(connect_cookie: str, session: Optional[requests.Session] = None, **kwargs) -> requests.Session:
    connector = LinuxDoConnect(session)
    return connector.login(connect_cookie, **kwargs)

__all__ = ["LinuxDoConnect", "get_auth_session"]