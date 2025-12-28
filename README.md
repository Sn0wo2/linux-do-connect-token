# Linux Do Connect Token

A helper library to authenticate with connect.linux.do and retrieve auth.session-token

---

[![GitHub release](https://img.shields.io/github/v/release/Sn0wo2/linux-do-connect-token?color=blue)](https://github.com/Sn0wo2/linux-do-connect-token/releases)

[![Python CI](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/py.yml/badge.svg)](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/py.yml)
[![Release](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/release.yml/badge.svg)](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/release.yml)
[![CodeQL Advanced](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/codeql.yml/badge.svg)](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/codeql.yml)

---

> [!] 项目当前正在开发, **不保证`v0`的向后兼容性**, 如果要在生产环境使用请等待`v1`发布

---

## Usage

> See example

---

## Get `LINUX_DO_TOKEN(_t)`

1. Open InPrivate page(Because token refresh)
2. Log in to [linux.do](https://linux.do)
3. Open DevTools by pressing F12
4. Go to the Application tab
5. Expand Cookies in the left sidebar and select linux.do
6. Find the `_t` cookie in the list
7. Copy its value for later use
8. Close InPrivate page(Dont logout linux.do)
