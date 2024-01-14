# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: screenshot
# Description: Screenshot module
# Author: GeekTG
# Commands:
# .webshot | .fileshot
# ---------------------------------------------------------------------------------


# -*- coding: utf-8 -*-

# Module author: @GovnoCodules

# requires: pygments

import io
import logging
import os

import pygments
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer
from requests import get

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class screenshotMod(loader.Module):
    """Screenshot module"""

    strings = {"name": "screenshot"}

    async def client_ready(self, client, db):
        self.client = client

    def __init__(self):
        self.name = self.strings["name"]

    @loader.sudo
    async def webshotcmd(self, message):
        """.webshot <link>"""
        reply = None
        link = utils.get_args_raw(message)
        if not link:
            reply = await message.get_reply_message()
            if not reply:
                await message.delete()
                return
            link = reply.raw_text
        await message.edit("<b>📸Фоткаю сайт...</b>")
        url = "https://mini.s-shot.ru/1024x768/JPEG/1024/Z100/?{}"
        file = get(url.format(link))
        file = io.BytesIO(file.content)
        file.name = "webshot.png"
        file.seek(0)
        await message.client.send_file(message.to_id, file, reply_to=reply)
        await message.delete()

    async def fileshotcmd(self, message):
        """Reply to file"""
        await message.edit("<b>📸Фоткаю файл...</b>")
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b>reply to file.py</b>")
            return
        media = reply.media
        if not media:
            await message.edit("<b>reply to file.py</b>")
            return
        file = await message.client.download_file(media)
        text = file.decode("utf-8")
        pygments.highlight(
            text,
            Python3Lexer(),
            ImageFormatter(font_name="DejaVu Sans Mono", line_numbers=True),
            "fileScreenshot.png",
        )
        await message.client.send_file(
            message.to_id, "fileScreenshot.png", force_document=True
        )
        os.remove("fileScreenshot.png")
        await message.delete()
