# Copyright (C) 2015-2022 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class MessageAutoDeleteTimerChanged:
    """\
    Represents MessageAutoDeleteTimerChanged object:
    https://core.telegram.org/bots/api#messageautodeletetimerchanged
    """

    message_auto_delete_time: int

    @classmethod
    def parse(cls, data: Optional[Dict]) -> Optional['MessageAutoDeleteTimerChanged']:
        return None if data is None else cls(data['message_auto_delete_time'])
