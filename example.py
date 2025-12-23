import os

from linux_do_connect import get_auth_session

connect_cookie = os.getenv("_t")
if not connect_cookie:
    print("Please set '_t' environment variable")
    exit(1)

timeout = 30

print("--- Login with helper ---")
try:
    session = get_auth_session(connect_cookie, timeout=timeout)
    print(f"Token: {session.cookies.get('auth.session-token')}")
except Exception as e:
    print(f"Helper login failed: {e}")

print("\n" + "-" * 30 + "\n")
