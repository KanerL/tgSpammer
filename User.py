from dataclasses import dataclass

import telethon


@dataclass
class User:
    username: str = None
    fullname: str = None
    userid: int = None
    phone: int = None
    user_entity :telethon.types.User = None
