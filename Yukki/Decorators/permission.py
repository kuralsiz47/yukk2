from typing import Dict, List, Union

from Yukki import BOT_ID, app


def PermissionCheck(mystic):
    async def wrapper(_, message):
        if message.chat.type == "private":
            return await mystic(_, message)
        a = await app.get_chat_member(message.chat.id, BOT_ID)
        if a.status != "administrator":
            return await message.reply_text(
                "Bazı izinlere sahip yönetici olmam gerekiyor:\n"
                + "\n- **SESLİ SOHBETLERİ YÖNET:** Sesli sohbetleri yönetmek için"
                + "\n- **MESAJLARI SİL:** Botun Aranan Atıklarını silmek için"
                + "\n- **BAĞLANTI YOLUYLA DAVET ET**: Asistanı sohbete davet etmek için."
            )
        if not a.can_manage_voice_chats:
            await message.reply_text(
                "Bu eylemi gerçekleştirmek için gerekli izne sahip değilim."
                + "\n**İzin:** __SESLİ SOHBETLERİ YÖNET__"
            )
            return
        if not a.can_delete_messages:
            await message.reply_text(
                "Bu eylemi gerçekleştirmek için gerekli izne sahip değilim."
                + "\n**İzin:** __MESAJLARI SİL__"
            )
            return
        if not a.can_invite_users:
            await message.reply_text(
                "Bu eylemi gerçekleştirmek için gerekli izne sahip değilim."
                + "\n**İzin:** __KULLANICILARI BAĞLANTI YOLUYLA DAVET ET__"
            )
            return
        return await mystic(_, message)

    return wrapper
