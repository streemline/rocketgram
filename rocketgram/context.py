# Copyright (C) 2015-2019 by Vd.
# This file is part of RocketGram, the modern Telegram bot framework.
# RocketGram is released under the MIT License (see LICENSE).


import logging
import typing

from .types import Default
from .update import Update
from .update import UpdateType

if typing.TYPE_CHECKING:
    from .bot import Bot
    from .request import Request

logger = logging.getLogger('rocketgram.context')


class Context:
    def __init__(self, bot: 'Bot', update: 'Update', context_data):
        self.__bot = bot
        self.__update = update
        self.__webhook_requests = list()
        self.__data = context_data

    @property
    def globals(self):
        return self.bot.globals

    @property
    def data(self):
        return self.__data

    @property
    def bot(self):
        return self.__bot

    @property
    def update(self):
        return self.__update

    def webhook_request(self, request: 'Request'):
        self.__webhook_requests.append(request)

    def get_webhook_requests(self):
        return self.__webhook_requests

    def send_message(self, text, parse_mode=Default, disable_web_page_preview=Default, disable_notification=Default,
                     reply_to_message_id=None, reply_markup=None):
        """https://core.telegram.org/bots/api#sendmessage"""

        if self.__update.update_type is UpdateType.message:
            chat_id = self.__update.message.chat.chat_id
        elif self.__update.update_type is UpdateType.edited_message:
            chat_id = self.__update.edited_message.chat.chat_id
        elif self.__update.update_type is UpdateType.channel_post:
            chat_id = self.__update.channel_post.chat.chat_id
        elif self.__update.update_type is UpdateType.edited_channel_post:
            chat_id = self.__update.edited_channel_post.chat.chat_id
        elif self.__update.update_type is UpdateType.callback_query and self.__update.callback_query.message:
            chat_id = self.__update.callback_query.message.chat.chat_id
        elif self.__update.update_type is UpdateType.shipping_query:
            chat_id = self.__update.shipping_query.user.user_id
        elif self.__update.update_type is UpdateType.pre_checkout_query:
            chat_id = self.__update.pre_checkout_query.user.user_id
        else:
            raise TypeError('Wrong update type')  # TODO!

        return self.__bot.send_message(chat_id, text, parse_mode=parse_mode,
                                       disable_web_page_preview=disable_web_page_preview,
                                       disable_notification=disable_notification,
                                       reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)

    def reply_message(self, text, parse_mode=Default, disable_web_page_preview=Default, disable_notification=Default,
                      reply_markup=None):
        """https://core.telegram.org/bots/api#sendmessage"""

        if self.__update.update_type is UpdateType.message:
            chat_id = self.__update.message.chat.chat_id
            reply_to_message_id = self.__update.message.message_id
        elif self.__update.update_type is UpdateType.edited_message:
            chat_id = self.__update.edited_message.chat.chat_id
            reply_to_message_id = self.__update.edited_message.message_id
        elif self.__update.update_type is UpdateType.channel_post:
            chat_id = self.__update.channel_post.chat.chat_id
            reply_to_message_id = self.__update.channel_post.message_id
        elif self.__update.update_type is UpdateType.edited_channel_post:
            chat_id = self.__update.edited_channel_post.chat.chat_id
            reply_to_message_id = self.__update.edited_channel_post.message_id
        elif self.__update.update_type is UpdateType.callback_query and self.__update.callback_query.message:
            chat_id = self.__update.callback_query.message.chat.chat_id
            reply_to_message_id = self.__update.callback_query.message.message_id
        else:
            raise TypeError('Wrong update type')  # TODO!

        return self.__bot.send_message(chat_id, text, parse_mode=parse_mode,
                                       disable_web_page_preview=disable_web_page_preview,
                                       disable_notification=disable_notification,
                                       reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)

    def answer_callback_query(self, text=None, show_alert=None, url=None, cache_time=None):
        """https://core.telegram.org/bots/api#answercallbackquery"""

        if not self.__update.update_type is UpdateType.callback_query:
            raise TypeError('Wrong update type')  # TODO!

        return self.__bot.answer_callback_query(self.__update.callback_query.query_id, text=text, show_alert=show_alert,
                                                url=url,
                                                cache_time=cache_time)

    def send_or_answer(self, text, parse_mode=Default, disable_web_page_preview=Default, disable_notification=Default,
                       reply_to_message_id=None, reply_markup=None, show_alert=None, url=None, cache_time=None):
        """https://core.telegram.org/bots/api#sendmessage
        https://core.telegram.org/bots/api#answercallbackquery"""

        if self.__update.update_type is UpdateType.callback_query and self.__update.callback_query.message:
            return self.__bot.answer_callback_query(self.__update.callback_query.query_id, text=text,
                                                    show_alert=show_alert, url=url,
                                                    cache_time=cache_time)

        if self.__update.update_type is UpdateType.message:
            chat_id = self.__update.message.chat.chat_id
        elif self.__update.update_type is UpdateType.edited_message:
            chat_id = self.__update.edited_message.chat.chat_id
        elif self.__update.update_type is UpdateType.channel_post:
            chat_id = self.__update.channel_post.chat.chat_id
        elif self.__update.update_type is UpdateType.edited_channel_post:
            chat_id = self.__update.edited_channel_post.chat.chat_id
        elif self.__update.update_type is UpdateType.shipping_query:
            chat_id = self.__update.shipping_query.user.user_id
        elif self.__update.update_type is UpdateType.pre_checkout_query:
            chat_id = self.__update.pre_checkout_query.user.user_id
        else:
            raise TypeError('Wrong update type')  # TODO!

        return self.__bot.send_message(chat_id, text, parse_mode=parse_mode,
                                       disable_web_page_preview=disable_web_page_preview,
                                       disable_notification=disable_notification,
                                       reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)

    def send_or_edit(self, text, parse_mode=Default, disable_web_page_preview=Default, disable_notification=Default,
                     reply_to_message_id=None, reply_markup=None):
        """https://core.telegram.org/bots/api#sendmessage
        https://core.telegram.org/bots/api#editmessagetext"""

        if self.__update.update_type == UpdateType.message:
            return self.__bot.send_message(self.update.message.chat.chat_id, text, parse_mode=parse_mode,
                                           disable_web_page_preview=disable_web_page_preview,
                                           disable_notification=disable_notification,
                                           reply_to_message_id=reply_to_message_id, reply_markup=reply_markup)
        else:
            return self.__bot.edit_message_text(chat_id=self.__update.callback_query.message.chat.chat_id,
                                                message_id=self.__update.callback_query.message.message_id, text=text,
                                                parse_mode=parse_mode,
                                                disable_web_page_preview=disable_web_page_preview,
                                                reply_markup=reply_markup)

    def edit_message_text(self, text, parse_mode=Default, disable_web_page_preview=Default, reply_markup=None):
        """https://core.telegram.org/bots/api#editmessagetext"""

        if not self.__update.update_type is UpdateType.callback_query:
            raise TypeError('Wrong update type')  # TODO!

        if self.__update.callback_query.message:
            return self.__bot.edit_message_text(chat_id=self.__update.callback_query.message.chat.chat_id,
                                                message_id=self.__update.callback_query.message.message_id, text=text,
                                                parse_mode=parse_mode,
                                                disable_web_page_preview=disable_web_page_preview,
                                                reply_markup=reply_markup)
        else:
            return self.__bot.edit_message_text(inline_message_id=self.__update.callback_query.inline_message_id,
                                                text=text,
                                                parse_mode=parse_mode,
                                                disable_web_page_preview=disable_web_page_preview,
                                                reply_markup=reply_markup)
