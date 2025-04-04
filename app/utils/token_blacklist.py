# Sementara menggunakan in-memory set. Bisa diganti ke Redis nanti
blacklisted_tokens = set()

def is_token_blacklisted(token: str) -> bool:
    return token in blacklisted_tokens

def add_to_blacklist(token: str):
    blacklisted_tokens.add(token)
