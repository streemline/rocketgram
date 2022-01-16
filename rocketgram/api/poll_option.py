# Copyright (C) 2015-2022 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PollOption:
    """\
    Represents PollOption object:
    https://core.telegram.org/bots/api#polloption
    """

    text: str
    voter_count: int

    @classmethod
    def parse(cls, data: dict) -> Optional['PollOption']:
        return None if data is None else cls(data['text'], data['voter_count'])
