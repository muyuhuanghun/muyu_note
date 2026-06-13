"""安全校验：验证 URL 是否合法、防止 SSRF。"""
from __future__ import annotations

import ipaddress
from urllib.parse import urlparse

from app.errors import AppError


def validate_target_url(url: str) -> str:
    """校验 URL 合法性，拒绝内网地址。"""
    try:
        parsed = urlparse(url)
    except ValueError as exc:
        raise AppError(1002, "url parse failed") from exc

    if parsed.scheme not in ("http", "https"):
        raise AppError(1002, "only http/https urls are allowed")
    if not parsed.netloc:
        raise AppError(1002, "url host is required")

    hostname = parsed.hostname
    if not hostname:
        raise AppError(1002, "url host is required")
    if hostname.lower() == "localhost":
        raise AppError(1002, "localhost is not allowed")

    try:
        ip = ipaddress.ip_address(hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            raise AppError(1002, "private or unsafe network targets are forbidden")
    except ValueError:
        pass

    return url
