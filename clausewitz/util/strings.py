def unescape(s: str) -> str:
    return s[3:-3].encode().decode('unicode-escape')
