import re


def valid_url(url: str):
    pattern = re.compile(
        r"^(https?:\/\/)?"  # Optional http or https
        r"(([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,6}|"  # Domain name
        r"localhost|"  # OR localhost
        r"\d{1,3}(\.\d{1,3}){3})"  # OR IPv4
        r"(:\d+)?"  # Optional port
        r"(\/[^\s]*)?$",  # Optional path
        re.IGNORECASE,
    )
    return bool(pattern.match(url))
