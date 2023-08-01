
# Чистый макет модуля

# Licensed under the *license* # Лицензия 
# meta developer: @example # Будет указываться автор при установке модуля
# scope: hikka_min 1.6.2 # Минимальная версия хикки для работы модуля

from hikkatl.types import Message

from .. import loader, utils  # type: ignore


@loader.tds # Название модуля
class ModuleName(loader.Module): # используемые библиотеки
    """description of module""" # Описание модуля

    strings = {"name": "ModuleName", "example": "example"} # name - Название модуля, которое будет видеть пользователь при устновке и help
                                                           # example: - переменная, седержащая текст "example"
    strings_ru = {"example": "пример"} # Тоже самое, но на русском языке, будет показываться, если у пользователя выбран русский язык для hikka

    @loader.command(alias="cmd", ru_doc="Пример команды") # Алиас - возможный вариант написания команды / ru_doc - описание команды, если у пользователя выбран русский язык для hikka
    async def command(self, m: Message): # используемые библиотеки и как выглядит команда
        """description of command""" # Описание команды, если у пользователя выбран любой язык, кроме русского
        await utils.answer(m, self.strings("example"))  # type: ignore
                        # сам скрипт команды