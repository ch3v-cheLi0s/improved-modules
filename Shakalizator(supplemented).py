# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the CC BY-NC-ND 4.0.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: VideoShakal
# Description: No description
# Author: D4n13l3k00 and fixed by @three_six_mafia
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

# meta developer: @D4n13l3k00 and fixed by @three_six_mafia


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
            return await utils.answer(m, "<u>[Шакализатор]</u> <b>А видео где!?</b>\nПример команды: <code>vsh <реплай на видео> <уровень сжатия></code>")

        args = utils.get_args_raw(m)
        lvls = {
            "1": ("0.2M", "23k"),
            "2": ("0.150M", "19k"),
            "3": ("0.06M", "15k"),
            "4": ("0.03M", "8k"),
            "5": ("0.01M", "4k"),
        }
        if args:
            if args in lvls:
                lvl, audio_bitrate = lvls[args]
            else:
                return await utils.answer(m, "<u>[Шакализатор]</u> <b>Не знаю такого уровня сжатия.\nИспользуй только от 1 до 5. Пример команды:\n<code>vsh <реплай на видео> <уровень сжатия></code>")
        else:
            lvl, audio_bitrate = lvls["3"]

        m = await utils.answer(m, "<u>[Шакализатор]</u> <b>Качаю...</b>")
        vid = await reply.download_media(
            "".join(random.choice(string.ascii_letters) for _ in range(25)) + ".mp4"
        )

        out = "".join(random.choice(string.ascii_letters) for _ in range(25)) + ".mp4"

        m = await utils.answer(m, "<u>[Шакализатор]</u> <b>Шакалю...</b>")
        os.system(
            f'ffmpeg -y -i "{vid}" -b:v {lvl} -maxrate:v {lvl} -b:a {audio_bitrate} -maxrate:a'
            f' {audio_bitrate} "{out}"'
        )
        sent_message = await utils.answer(m, "<u>[Шакализатор]</u> <b>Отправляю...</b>")
        await sent_message.delete()
        
        sent_message = await m.client.send_file(reply.to_id, out, caption="<u>[Шакализатор]</u> <b>Обработанное видео</b>", video_note=True, reply_to=reply)
        
        os.remove(vid)
        os.remove(out)