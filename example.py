import asyncio
import os

from curl_cffi import requests

from linux_do_connect import LinuxDoConnect, IMPERSONATE


async def test_connect_token(token, timeout):
    try:
        client = LinuxDoConnect(token)
        await client.login(timeout=timeout)
        connect_token, new_token = await client.get_connect_token()

        feedback = f"Token: {connect_token}"
        if new_token is not None and token != new_token:
            feedback += f" (Mismatch in _t cookie:\n Before: {token}\nNow: {new_token})"

        return client, feedback
    except Exception as e:
        return None, f"Failed : {e}"


async def test_oauth_callback(client, timeout):
    if not client:
        return "Skipping OAuth test due to login failure."

    try:
        async with requests.AsyncSession() as session:
            # 薄荷的恩情还不完 ✋😭✋
            r = await session.get("https://qd.x666.me/api/auth/login", impersonate=IMPERSONATE)
            oauth_url = r.json()["authUrl"]

        call_back_url = await client.approve_oauth(oauth_url, timeout=timeout)

        return f"Callback URL: {call_back_url}"
    except Exception as e:
        return f"OAuth usage failed: {e}"


async def main():
    connect_token = os.getenv("LINUX_DO_TOKEN")
    if not connect_token:
        print("Please set 'LINUX_DO_TOKEN' environment variable")
        exit(1)

    timeout = 30

    print("\n" + "=" * 50)
    print(" LinuxDoConnect Test Suite ")
    print("=" * 50 + "\n")

    print("[*] Testing Authentication...")
    client, auth_feedback = await test_connect_token(connect_token, timeout)
    print(auth_feedback)
    print("-" * 50)

    print("\n[*] Testing OAuth Callback...")
    oauth_feedback = await test_oauth_callback(client, timeout)
    print(oauth_feedback)

    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())