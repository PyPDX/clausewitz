def unescape(s: str) -> str:
    return s.strip('"').encode().decode('unicode-escape')
