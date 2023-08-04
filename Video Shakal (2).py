# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the CC BY-NC-ND 4.0.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: VideoShakal
# Description: No description
# Author: D4n13l3k00
# Commands:
# .vsh
# ---------------------------------------------------------------------------------


# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2022 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00


import os
import random
import string

from .. import loader, utils
from telethon.tl.types import Document

@loader.tds
class VSHAKALMod(loader.Module):
    strings = {"name": "Video Shakal"}

    @loader.owner
    async def vshcmd(self, m):
        ".vsh <уровень от 1 до 5 (по умолчанию 3)>\nСшакалить видео"
        reply = await m.get_reply_message()
        if not reply or not reply.file or "video" not in reply.file.mime_type:
            return await utils.answer(m, "Пожалуйста, пришлите реплай на видео!")

        args = utils.get_args_raw(m)
        lvls = {
            "1": ("0.35M", "35k"),
            "2": ("0.2M", "24k"),
            "3": ("0.06M", "16k"),
            "4": ("0.03M", "8k"),
            "5": ("0.01M", "4k"),
        }
        if args:
            if args in lvls:
                lvl, audio_bitrate = lvls[args]
            else:
                return await utils.answer(m, "Не знаю такого уровня сжатия")
        else:
            lvl, audio_bitrate = lvls["3"]

        m = await utils.answer(m, "[Шакал] Качаю...")
        vid = await reply.download_media(
            "".join(random.choice(string.ascii_letters) for _ in range(25)) + ".mp4"
        )

        out = "".join(random.choice(string.ascii_letters) for _ in range(25)) + ".mp4"

        m = await utils.answer(m, "[Шакал] Шакалю...")
        os.system(
            f'ffmpeg -y -i "{vid}" -b:v {lvl} -maxrate:v {lvl} -b:a {audio_bitrate} -maxrate:a'
            f' {audio_bitrate} "{out}"'
        )
        
        sent_message = await m.client.send_file(reply.to_id, out, caption="[Шакал] Обработанное видео", video_note=True, reply_to=reply)
        
        os.remove(vid)
        os.remove(out)

        await sent_message.delete()
