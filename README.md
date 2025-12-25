# Linux Do Connect Token

A helper library to authenticate with connect.linux.do and retrieve auth.session-token

---

## Usage

### Get Sessions

```python
import os
from linux_do_connect import get_auth_session

connect_cookie = os.getenv("_t")
session = get_auth_session(
    connect_cookie,
    timeout=30,
    proxies={"https": "http://127.0.0.1:7890"}
)
print(session.cookies.get("auth.session-token"))
```

---

### Custom Session

```python
import os
from curl_cffi import requests
from linux_do_connect import LinuxDoConnect

connect_cookie = os.getenv("_t")
session = requests.Session()

client = LinuxDoConnect(session)
token = client.get_token(
    connect_cookie,
    timeout=30,
    proxies={"https": "http://127.0.0.1:7890"}
)
print(token)
```

---

## Get the `_t` Cookie

1. Open InPrivate page(Because token refresh)
2. Log in to [linux.do](https://linux.do)
3. Open DevTools by pressing F12
4. Go to the Application tab
5. Expand Cookies in the left sidebar and select linux.do
6. Find the `_t` cookie in the list
7. Copy its value for later use
8. Close InPrivate page(Dont logout linux.do)
