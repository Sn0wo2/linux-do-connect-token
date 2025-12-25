import asyncio
import os

from linux_do_connect import LinuxDoConnect, get_auth_token


async def test_class_usage(connect_cookie, timeout):
    try:
        client = LinuxDoConnect()
        auth_token, _t = await get_auth_token(await client.login(connect_cookie, timeout=timeout))
        feedback = f"Token from class: {auth_token}"
        if _t is not None and connect_cookie != _t:
            feedback += f" (Mismatch in _t cookie:\n Before: {connect_cookie}\nNow: {_t})"

        return feedback
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
        test_class_usage(connect_cookie, timeout)
    )

    print("\n" + "-" * 40 + "\n")

    print("----- Login linux.do connect session -----")
    print(results[0])

    print("\n" + "-" * 40 + "\n")


if __name__ == "__main__":
    asyncio.run(main())