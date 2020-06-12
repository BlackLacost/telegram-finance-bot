from typing import Union

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):
    """
    Аутентификация — пропускаем сообщения только
    от одного Telegram аккаунта
    """

    def __init__(self, access_id: int):
        self.access_id = access_id
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if int(message.from_user.id) != self.access_id:
            await message.answer("Access Denied")
            raise CancelHandler()
