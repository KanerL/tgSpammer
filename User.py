from dataclasses import dataclass


@dataclass
class User:
    username: str = None
    fullname: str = None
    userid: int = None
    phone: int = None
