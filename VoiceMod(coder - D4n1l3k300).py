#      Coded by D4n1l3k300       #
#   supplemented by Yahikor0     #
#   been modificated by ch3vy    #

import io
import os
import re
import logging
import ffmpeg
import pytgcalls
from ShazamAPI import Shazam
from youtube_dl import YoutubeDL
from pytgcalls import GroupCallFactory
from pytgcalls.implementation.group_call_file import GroupCallFile
from telethon import types
from typing import *
from .. import loader, utils

@loader.unrestricted
@loader.ratelimit
@loader.tds
class VoiceMod(loader.Module):
    """Модуль для работы с голосовым чатом 📢"""

    strings = {
        "name": "VoiceMod",
        "downloading": "<b>[VoiceMod]</b> Загружаю...",
        "converting": "<b>[VoiceMod]</b> Конвертирую...",
        "playing": "<b>[VoiceMod]</b> Воспроизвожу...",
        "plsjoin": "<b>[VoiceMod]</b> Вы ещё не в голосовом чате (напишите .vjoin)",
        "stop": "<b>[VoiceMod]</b> Остановлено воспроизведение!",
        "join": "<b>[VoiceMod]</b> Присоединён!",
        "leave": "<b>[VoiceMod]</b> Вышел!",
        "pause": "<b>[VoiceMod]</b> Пауза!",
        "resume": "<b>[VoiceMod]</b> Возобновлено!",
        "mute": "<b>[VoiceMod]</b> Заглушено!",
        "unmute": "<b>[VoiceMod]</b> Звук включён!",
        "replay": "<b>[VoiceMod]</b> Повтор...",
        "error": "<b>[VoiceMod]</b> Ошибка: <code>{}</code>",
    }
    ytdlopts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
        "outtmpl": "ytdl_out.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    group_calls: Dict[int, GroupCallFile] = {}
    tag = "<u><b>[Shazam]</u></b> "

    async def get_chat(self, m: types.Message):
        args = utils.get_args_raw(m)
        if not args:
            chat = m.chat.id
        else:
            try:
                chat = int(args)
            except:
                chat = args
            try:
                chat = (await m.client.get_entity(chat)).id
            except Exception as e:
                await utils.answer(m, self.strings("error").format(str(e)))
                return None
        return chat

    def _call(self, m: types.Message, chat: int):
        if str(chat) not in self.group_calls:
            self.group_calls[str(chat)] = GroupCallFactory(
                m.client, pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON
            ).get_file_group_call()

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def vplaycmd(self, m: types.Message):
        """— [чат (не обязательно)] <ссылка/ответом на аудио> - Воспроизвести аудио в ГЧ ▶"""
        args = utils.get_args_raw(m)
        r = await m.get_reply_message()
        chat = from_file = link = None
        if args:
            _ = re.match(r"(-?\d+|@[A-Za-z0-9_]{5,})\s+(.*)", args)
            __ = re.match(r"(-?\d+|@[A-Za-z0-9_]{5,})", args)
            if _:
                chat = _.group(1)
                link = _.group(2)
            elif __:
                chat = __.group(1)
            else:
                chat = m.chat.id
                link = args or None
            try:
                chat = int(chat)
            except:
                chat = chat
            try:
                chat = (await m.client.get_entity(chat)).id
            except Exception as e:
                return await utils.answer(m, self.strings("error").format(str(e)))
        else:
            chat = m.chat.id
        if r and r.audio and not link:
            from_file = True
        if not link and (not r or not r.audio):
            return utils.answer(m, "no audio/link")
        if str(chat) not in self.group_calls:
            return await utils.answer(m, self.strings("plsjoin"))
        self._call(m, chat)
        input_file = f"{chat}.raw"
        m = await utils.answer(m, self.strings("downloading"))
        if from_file:
            audio_original = await r.download_media()
        else:
            try:
                with YoutubeDL(self.ytdlopts) as rip:
                    rip.extract_info(link)
            except Exception as e:
                return await utils.answer(m, self.strings("error").format(str(e)))
            audio_original = "ytdl_out.mp3"
        m = await utils.answer(m, self.strings("converting"))
        ffmpeg.input(audio_original).output(
            input_file, format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
        ).overwrite_output().run()
        os.remove(audio_original)
        await utils.answer(m, self.strings("playing"))
        self.group_calls[str(chat)].input_filename = input_file

    async def vjoincmd(self, m: types.Message):
        """— Присоединить своего юзербота к ГЧ 🏄"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        await self.group_calls[str(chat)].start(chat)
        await utils.answer(m, self.strings("join"))

    async def vleavecmd(self, m: types.Message):
        """— Выгнать своего юзербота из ГЧ 🤕"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        await self.group_calls[str(chat)].stop()
        del self.group_calls[str(chat)]
        try:
            os.remove(f"{chat}.raw")
        except:
            pass
        await utils.answer(m, self.strings("leave"))

    async def vreplaycmd(self, m: types.Message):
        """— Повторить медиа в ГЧ 🔁"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].restart_playout()
        await utils.answer(m, self.strings("replay"))

    async def vstopcmd(self, m: types.Message):
        """— Прекратить проигрывание медиа в ГЧ ⏹"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].stop_playout()
        await utils.answer(m, self.strings("stop"))

    async def vmutecmd(self, m: types.Message):
        """— Заглушить проигрываемое медиа в ГЧ 🔇"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].set_is_mute(True)
        await utils.answer(m, self.strings("unmute"))

    async def vunmutecmd(self, m: types.Message):
        """— Сделать медиа вновь слышимым в ГЧ 🔊"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].set_is_mute(False)
        await utils.answer(m, self.strings("mute"))

    async def vpausecmd(self, m: types.Message):
        """— Остановить медиа в ГЧ"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].pause_playout()
        await utils.answer(m, self.strings("pause"))

    async def vresumecmd(self, m: types.Message):
        """— Resume player in VC"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].resume_playout()
        await utils.answer(m, self.strings("resume"))

    async def vdebugcmd(self, m: types.Message):
        """— Команда для DEBUG режима 🐞"""
        await utils.answer(m, f"DEBUG : {self.group_calls}")

    @loader.unrestricted
    async def smcmd(self, message):                                                                                     
        """— «название» - Найти музыку по названию 🔎"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply:
            args = reply.raw_text
        if not args:
            return await message.edit("<b>Нету аргументов.</b>")
        try:
            await message.edit("<b>Загрузка...</b>")
            music = await message.client.inline_query("lybot", args)
            await message.delete()
            await message.client.send_file(
                message.to_id,
                music[0].result.document,
                reply_to=reply.id if reply else None,
            )
        except:
            return await message.client.send_message(
                message.chat_id,
                f"<b>Музыка с названием <code>{args}</code> не найдена.</b>",
            )

    async def shazamcmd(self, message):
        """— «ответ на аудио» - Распознать и получить информацию о треке 📡"""
        s = await get_media_shazam(message)
        if not s:
            return
        try:
            shazam = Shazam(s.media.read())
            recog = shazam.recognizeSong()
            track = next(recog)[1]["track"]
            await message.client.send_file(
                message.to_id,
                file=track["images"]["background"],
                caption=self.tag + "Распознанный трек: " + track["share"]["subject"],
                reply_to=s.reply.id,
            )
            await message.delete()
        except:
            await message.edit(self.tag + "Не удалось распознать...")

async def get_audio_shazam(message):
    class rct:
        media = io.BytesIO()
        reply = None
    reply = await message.get_reply_message()
    if reply and reply.file and reply.file.mime_type.split("/")[0] in ("audio", "video"):
        ae = rct()
        await utils.answer(message, self.tag + "<b>Скачиваю...</b>")
        ae.media = io.BytesIO(await reply.download_media(bytes))
        ae.reply = reply
        await message.edit(self.tag +"<b>Распознаю...</b>")
        return ae
    else:
        await utils.answer(message, self.tag + "<b>Вы не ответили на медиа для распознавания...</b>")
        return None