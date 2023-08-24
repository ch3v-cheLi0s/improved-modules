# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: SquareBlur
# Description: Make image 1:1 ratio
# Author: KeyZenD, ch3v.cheLi0s
# Commands:
# .squareblur
# ---------------------------------------------------------------------------------

import io
import os
from PIL import Image, ImageFilter
from moviepy.editor import VideoFileClip
from .. import loader, utils

@loader.tds
class SquareBlurMod(loader.Module):
    """Make image or video 1:1 ratio with blur. Responsible for video @three_six_mafia 😎"""

    strings = {"name": "SquareBlur"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def squareblurcmd(self, message):
        """make image or video 1:1 ratio with blur"""
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            await message.edit("<b>Reply to an image or video!</b>")
            return

        mime_type = reply.file.mime_type.split("/")[0].lower()
        if mime_type not in ["image", "video"]:
            await message.edit("<b>Unsupported file type!</b>")
            return

        media = io.BytesIO()
        await reply.download_media(media)

        if mime_type == "image":
            im = Image.open(media)
            w, h = im.size
            if w == h:
                await message.edit("<b>Image is already square!</b>")
                return
            _min, _max = min(w, h), max(w, h)
            bg = im.crop(
                ((w - _min) // 2, (h - _min) // 2, (w + _min) // 2, (h + _min) // 2)
            )
            bg = bg.filter(ImageFilter.GaussianBlur(5))
            bg = bg.resize((_max, _max))
            bg.paste(im, ((_max - w) // 2, (_max - h) // 2))
            img = io.BytesIO()
            img.name = "im.png"
            bg.save(img)
            img.seek(0)
            await reply.reply(file=img)
            await message.delete()

        elif mime_type == 'video':
            video_path = "video.mp4"
            with open(video_path, 'wb') as f:
                f.write(media.getvalue())

            clip = VideoFileClip(video_path)
            w, h = clip.size
            _min, _max = min(w, h), max(w, h)
            bg_clip = clip.crop(x1=(w - _min) // 2, y1=(h - _min) // 2, x2=(w + _min) // 2, y2=(h + _min) // 2)
            bg_clip = bg_clip.fx(vfx.blur, 5)
            bg_clip = bg_clip.resize((_max, _max))
            final_clip = bg_clip.set_position(('center', 'center')).resize((w, h))

            output_path = 'SquareBlured_video.mp4'
            final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

            await reply.reply(file=output_path)
            await message.delete()

            os.remove(video_path)
            os.remove(output_path)
