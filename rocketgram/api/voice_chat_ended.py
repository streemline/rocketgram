# Copyright (C) 2015-2022 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class VoiceChatEnded:
    """\
    Represents VoiceChatEnded object:
    https://core.telegram.org/bots/api#voicechatended
    """

    duration: int

    @classmethod
    def parse(cls, data: Optional[Dict]) -> Optional['VoiceChatEnded']:
        return None if data is None else cls(data['duration'])
