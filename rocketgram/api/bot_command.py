# Copyright (C) 2015-2022 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BotCommand:
    """\
    Represents BotCommand object:
    https://core.telegram.org/bots/api#botcommand
    """

    command: str
    description: str

    @classmethod
    def parse(cls, data: dict) -> Optional['BotCommand']:
        return None if data is None else cls(data['command'], data['description'])
