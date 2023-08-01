from .. import loader

@loader.tds
class ЭхоMod(loader.Module):
    """Мы где-то в пещере..?"""
    strings = {'name': 'Эхо...'}

    async def client_ready(self, client, db):
        self.db = db

    async def эхоcmd(self, message):
        """Включить/выключить эхо."""
        echos = self.db.get("Echo", "chats", []) 
        chatid = str(message.chat_id)

        if chatid not in echos:
            echos.append(chatid)
            self.db.set("Echo", "chats", echos)
            return await message.edit("Теперь тут слышно <b>Эхо</b>...")

        echos.remove(chatid)
        self.db.set("Echo", "chats", echos)
        return await message.edit("<b>Эхо</b> пропало...")


    async def watcher(self, message):
        echos = self.db.get("Echo", "chats", [])
        chatid = str(message.chat_id)

        if chatid not in str(echos): return
        if message.sender_id == (await message.client.get_me()).id: return

        await message.client.send_message(int(chatid), message, reply_to=await message.get_reply_message() or message)