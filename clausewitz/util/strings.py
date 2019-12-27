def unescape(s: str) -> str:
    return s.encode().decode('unicode-escape')
