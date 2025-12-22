# Linux Do Connect Token

A helper library to authenticate with connect.linux.do and retrieve auth.session-token

## Usage

### High-level helper

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

### Custom Session

```python
import os
from curl_cffi import requests
from linux_do_connect import LinuxDoConnect

connect_cookie = os.getenv("_t")
session = requests.Session()
# Configure session...

client = LinuxDoConnect(session)
token = client.get_token(
    connect_cookie,
    timeout=30,
    proxies={"https": "http://127.0.0.1:7890"}
)
print(token)
```