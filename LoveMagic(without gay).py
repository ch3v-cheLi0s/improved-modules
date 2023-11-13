# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: lovemagic
# Description: Famous TikTok hearts animation implemented in Hikka w/o logspam
# Author: hikariatama
# Commands:
# .ilyi | .ilygayi | .ily | .ilygay
# ---------------------------------------------------------------------------------


#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://static.hikari.gay/lovemagic_icon.png
# meta banner: https://mods.hikariatama.ru/badges/lovemagic.jpg
# meta developer: @hikarimods
# scope: inline
# scope: hikka_only
# scope: hikka_min 1.3.0

import json
import logging
import random
from asyncio import sleep
from typing import Union

import requests
from telethon.tl.types import Message

from .. import loader, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


@loader.tds
class ILYMod(loader.Module):
    """Famous TikTok hearts animation implemented in Hikka w/o logspam"""

    strings = {
        "name": "LoveMagic",
        "message": "<b>❤️‍🔥 I want to tell you something...</b>\n<i>{}</i>",
    }

    strings_ru = {
        "message": "<b>❤️‍🔥 Я хочу тебе сказать кое-что...</b>\n<i>{}</i>",
        "_cls_doc": "Известная TikTok анимация сердечек без спама в логи и флудвейтов",
    }

    async def client_ready(self):
        self.classic_frames = (
            await utils.run_sync(
                requests.get,
                "https://gist.github.com/hikariatama/89d0246c72e5882e12af43be63f5bca5/raw/08a5df7255d5e925ab2ede1efc892d9dc93af8e1/ily_classic.json",
            )
        ).json()

    async def ily_handler(
        self,
        obj: Union[InlineCall, Message],
        text: str,
        inline: bool = False,
    ):
        frames = self.classic_frames + [
            f'<b>{" ".join(text.split()[: i + 1])}</b>'
            for i in range(len(text.split()))
        ]

        obj = await self.animate(obj, frames, interval=0.5, inline=inline)

        await sleep(10)
        if not isinstance(obj, Message):
            await obj.edit(
                f"<b>{text}</b>",
                reply_markup={
                    "text": "💔 Хочу также!",
                    "url": "https://t.me/hikka_talks",
                },
            )

            await obj.unload()

    async def ily_handler_gay(
        self,
        obj: Union[InlineCall, Message],
        text: str,
        inline: bool = False,
    ):
        obj = await self.animate(
            obj,
            self.gay_frames
            + [
                f'<b>{" ".join(text.split()[: i + 1])}</b>'
                for i in range(len(text.split()))
            ],
            interval=0.5,
            inline=inline,
        )

            await obj.unload()

    @loader.command(ru_doc="Отправить анимацию сердец в инлайне")
    async def ilyicmd(self, message: Message):
        """Send inline message with animated hearts"""
        args = utils.get_args_raw(message)
        await self.inline.form(
            self.strings("message").format("*" * (len(args) or 9)),
            reply_markup={
                "text": "🧸 Open",
                "callback": self.ily_handler,
                "args": (args or "I ❤️ you!",),
                "kwargs": {"inline": True},
            },
            message=message,
            disable_security=True,
        )

    @loader.command(ru_doc="Отправить анимацию сердец")
    async def ily(self, message: Message):
        """Send message with animated hearts"""
        await self.ily_handler(
            message,
            utils.get_args_raw(message) or "I ❤️ you!",
            inline=False,
        )