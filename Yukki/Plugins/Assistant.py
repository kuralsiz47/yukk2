import random

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            Message)

from Yukki import ASSISTANT_PREFIX, SUDOERS, app, random_assistant
from Yukki.Database import get_assistant, save_assistant
from Yukki.Utilities.assistant import get_assistant_details

__MODULE__ = "Asistan"
__HELP__ = f"""


/checkassistant
- Sohbetinizin tahsis edilen asistanını kontrol edin


**Not:**
- Sadece Bot Yönetici Kullanıcıları İçin

{ASSISTANT_PREFIX[0]}block [ Kullanıcı İletisini Yanıtlama] 
- Kullanıcıyı Asistan Hesabından Engeller.

{ASSISTANT_PREFIX[0]}unblock [ Kullanıcı İletisini Yanıtlama] 
- Kullanıcının Asistan Hesabıyla Olan Engelini Kaldırır.

{ASSISTANT_PREFIX[0]}approve [ Kullanıcı İletisini Yanıtlama] 
- Kullanıcıyı DM için Onaylar.

{ASSISTANT_PREFIX[0]}disapprove [ Kullanıcı İletisini Yanıtlama] 
- Kullanıcıyı DM için onaylar.

{ASSISTANT_PREFIX[0]}pfp [ Fotoğrafı Yanıtlama] 
- Yardımcı hesap PFP'sini değiştirir.

{ASSISTANT_PREFIX[0]}bio [Bio text] 
- Asistan Hesabının Biyografisini Değiştirir.

/changeassistant [ASS NUMARASI]
- Önceden tahsis edilmiş asistanı yenisine değiştirme.

/setassistant [ASS NUMARASI veya Rastgele]
- Sohbet için asistan hesabı ayarlama. 
"""


ass_num_list = ["1", "2", "3", "4", "5"]


@app.on_message(filters.command("changeassistant") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"**Kullanım:**\n/changeassistant [ASS_NO]\n│\n╰Onlardan seç\n{' | '.join(ass_num_list)}"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    num = message.text.split(None, 1)[1].strip()
    if num not in ass_num_list:
        return await message.reply_text(usage)
    ass_num = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "Önceden Kaydedilmiş Yardımcı Bulunamadı.\n│\n╰Asistan'ı /setassistant"
        )
    else:
        ass = _assistant["saveassistant"]
    assis = {
        "saveassistant": ass_num,
    }
    await save_assistant(message.chat.id, "assistant", assis)
    await message.reply_text(
        f"**Değiştirilen Yardımcı**\n│\n╰Değiştirilen Yardımcı Hesabı **{ass}** Yardımcı Numarasına **{ass_num}**"
    )


ass_num_list2 = ["1", "2", "3", "4", "5", "Random"]


@app.on_message(filters.command("setassistant") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"**Kullanım:**\n/setassistant [ASS_NO or Random]\n│\n╰Onlardan seç\n{' | '.join(ass_num_list2)}\n│\n╰Use 'Random' rasgele Yardımcı ayarlamak için"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    query = message.text.split(None, 1)[1].strip()
    if query not in ass_num_list2:
        return await message.reply_text(usage)
    if str(query) == "Random":
        ran_ass = random.choice(random_assistant)
    else:
        ran_ass = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        await message.reply_text(
            f"**__Talia Winamp Müzik Bot Asistanı Tahsis__**\n│\n╰Asistan No. **{ran_ass}**"
        )
        assis = {
            "saveassistant": ran_ass,
        }
        await save_assistant(message.chat.id, "assistant", assis)
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"Önceden Kaydedilmiş Asistan Numarası {ass} Kurmak.\n│\n╰Asistan'ı /changeassistant"
        )


@app.on_message(filters.command("checkassistant") & filters.group)
async def check_ass(_, message: Message):
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "Önceden Kaydedilmiş Yardımcı Bulunamadı.\n│\n╰Asistan'ı /play /oynat"
        )
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"Önceden Kaydedilmiş Yardımcı Bulundu\n│\n╰Yardımcı Numarası {ass} "
        )
