"""Linux Do Connect Token - A helper library to authenticate with connect.linux.do and retrieve auth.session-token."""

__version__ = "0.0.0"

from .linux_do_connect import LinuxDoConnect, get_auth_session

__all__ = ["LinuxDoConnect", "get_auth_session"]
