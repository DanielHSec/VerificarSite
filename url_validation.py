"""Normalização defensiva de URLs enviadas ao serviço externo de consulta."""

import ipaddress
from urllib.parse import urlsplit, urlunsplit

MAX_URL_LENGTH = 2048
RESTRICTED_SUFFIXES = (".local", ".internal", ".localhost", ".test", ".invalid")


def normalize_public_url(raw: str) -> str:
    """Aceita URLs públicas HTTP(S), sem credenciais ou endereços internos."""
    value = (raw or "").strip()
    if not value:
        raise ValueError("Informe um endereço para consultar.")
    if len(value) > MAX_URL_LENGTH or any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError("O endereço contém caracteres inválidos ou é longo demais.")
    if "://" not in value and ":" not in value.split("/", 1)[0]:
        value = "https://" + value

    try:
        parts = urlsplit(value)
        hostname = parts.hostname
        port = parts.port
    except ValueError as exc:
        raise ValueError("Informe uma URL válida.") from exc

    if parts.scheme.lower() not in {"http", "https"} or not hostname:
        raise ValueError("Use um endereço HTTP ou HTTPS válido.")
    if parts.username is not None or parts.password is not None:
        raise ValueError("Endereços com credenciais não são aceitos.")
    if port is not None and not 1 <= port <= 65535:
        raise ValueError("A porta da URL é inválida.")
    hostname = hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith(RESTRICTED_SUFFIXES):
        raise ValueError("Use um endereço público; endereços internos não são aceitos.")

    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        if "." not in hostname or any(not part for part in hostname.split(".")):
            raise ValueError("Informe um domínio público válido.")
    else:
        if not ip.is_global:
            raise ValueError("Endereços de rede local ou reservados não são aceitos.")

    if len(value) > MAX_URL_LENGTH:
        raise ValueError("O endereço é longo demais.")
    return urlunsplit((parts.scheme.lower(), parts.netloc, parts.path, parts.query, ""))
