import asyncio
import os

from linux_do_connect import get_auth_session, get_token, LinuxDoConnect


async def test_get_auth_session(connect_cookie, timeout):
    try:
        session = await get_auth_session(connect_cookie, timeout=timeout)
        return f"Token from session: {session.cookies.get('auth.session-token')}"
    except Exception as e:
        return f"Login failed: {e}"


async def test_get_token(connect_cookie, timeout):
    try:
        token = await get_token(connect_cookie, timeout=timeout)
        return f"Token: {token}"
    except Exception as e:
        return f"Get token failed: {e}"


async def test_class_usage(connect_cookie, timeout):
    try:
        client = LinuxDoConnect()
        token = await client.get_token(connect_cookie, timeout=timeout)
        return f"Token from class: {token}"
    except Exception as e:
        return f"Class usage failed: {e}"


async def main():
    connect_cookie = os.getenv("_t")
    if not connect_cookie:
        print("Please set '_t' environment variable")
        exit(1)

    timeout = 30

    print("Running tests concurrently...")

    results = await asyncio.gather(
        test_get_auth_session(connect_cookie, timeout),
        test_get_token(connect_cookie, timeout),
        test_class_usage(connect_cookie, timeout)
    )

    print("\n" + "-" * 40 + "\n")

    print("----- Login linux.do connect session -----")
    print(results[0])

    print("\n" + "-" * 40 + "\n")

    print("----- Get linux.do connect token -----")
    print(results[1])

    print("\n" + "-" * 40 + "\n")

    print("----- Use LinuxDoConnect class directly -----")
    print(results[2])

    print("\n" + "-" * 40 + "\n")


if __name__ == "__main__":
    asyncio.run(main())