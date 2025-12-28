# Linux Do Connect Token

A helper library to authenticate with connect.linux.do and retrieve auth.session-token

---

[![GitHub release](https://img.shields.io/github/v/release/Sn0wo2/linux-do-connect-token?color=blue)](https://github.com/Sn0wo2/linux-do-connect-token/releases)

[![Python CI](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/py.yml/badge.svg)](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/py.yml)
[![Release](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/release.yml/badge.svg)](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/release.yml)
[![CodeQL Advanced](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/codeql.yml/badge.svg)](https://github.com/Sn0wo2/linux-do-connect-token/actions/workflows/codeql.yml)

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

---

请自行维护 Token 的生命周期。当 `get_connect_token` 返回的第二个参数不等于输入 Token 时，表示 **Token 已刷新**，请及时更新保存的
Token 值。
