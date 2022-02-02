import os
import re

import lyricsgenius
from pyrogram import Client, filters
from pyrogram.types import Message
from youtubesearchpython import VideosSearch

from Yukki import MUSIC_BOT_NAME, app

__MODULE__ = "Şarkı Sözleri"
__HELP__ = """

/Lyrics [Müzik Adı]
- Web'de belirli bir Müzik için Şarkı Sözlerini Arar.

**Not**:
Şarkı Sözleri'nin Satır içi düğmesinde bazı hatalar vardır. Yalnızca %50 sonuç arar. Herhangi bir müzik çalmak için şarkı sözleri istiyorsanız bunun yerine komutu kullanabilirsiniz.

"""


@app.on_callback_query(filters.regex(pattern=r"lyrics"))
async def lyricssex(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    try:
        id, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(
            f"Hata Oluştu\n**Olası neden**:{e}"
        )
    url = f"https://www.youtube.com/watch?v={id}"
    print(url)
    try:
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = result["title"]
    except Exception as e:
        return await CallbackQuery.answer(
            "Ses bulunamadı. Youtube sorunları.", show_alert=True
        )
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    t = re.sub(r"[^\w]", " ", title)
    y.verbose = False
    S = y.search_song(t, get_full_info=False)
    if S is None:
        return await CallbackQuery.answer(
            "𝗦̧𝗮𝗿𝗸𝗶 𝘀𝗼̈𝘇𝗹𝗲𝗿𝗶 𝗯𝘂𝗹𝘂𝗻𝗮𝗺𝗮𝗱𝗶 :p", show_alert=True
        )
    await CallbackQuery.message.delete()
    userid = CallbackQuery.from_user.id
    usr = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
    xxx = f"""
**𝗦̧𝗮𝗿𝗸𝗶 𝗦𝗼̈𝘇𝗹𝗲𝗿𝗶 𝗔𝗿𝗮𝗺𝗮 𝗗𝗲𝘀𝘁𝗲𝗸𝗰̧𝗶 {MUSIC_BOT_NAME}**
│
↦**𝗔𝗿𝗮𝗺𝗮 𝗬𝗲𝗿𝗶:-** {usr}
│
↦**𝗔𝗿𝗮𝗻𝗮𝗻 𝗦̧𝗮𝗿𝗸𝗶:-** __{title}__
│
↦**𝗦̧𝗮𝗿𝗸𝗶 𝗦𝗼̈𝘇𝗹𝗲𝗿𝗶 𝗕𝘂𝗹𝘂𝗻𝗱𝘂:-** __{S.title}__
│
↦**𝗦𝗮𝗻𝗮𝘁𝗰̧𝗶:-** {S.artist}
│
↳**__𝗦𝗼̈𝘇𝗹𝗲𝗿:__**

{S.lyrics}"""
    if len(xxx) > 4096:
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await CallbackQuery.message.reply_document(
            document=filename,
            caption=f"**ÇIKTI:**\n\n`Lyrics`",
            quote=False,
        )
        os.remove(filename)
    else:
        await CallbackQuery.message.reply_text(xxx)


@app.on_message(filters.command("söz"))
async def lrsearch(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗺:**\n│\n╰/söz [ Müzik adı]")
    m = await message.reply_text("𝗦̧𝗮𝗿𝗸𝗶 𝗦𝗼̈𝘇𝗹𝗲𝗿𝗶 𝗔𝗿𝗮𝗻𝗶𝘆𝗼𝗿")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("𝗦̧𝗮𝗿𝗸𝗶 𝘀𝗼̈𝘇𝗹𝗲𝗿𝗶 𝗯𝘂𝗹𝘂𝗻𝗮𝗺𝗮𝗱𝗶 :p")
    xxx = f"""
**𝗦̧𝗮𝗿𝗸𝗶 𝗦𝗼̈𝘇𝗹𝗲𝗿𝗶 𝗔𝗿𝗮𝗺𝗮 𝗗𝗲𝘀𝘁𝗲𝗸𝗰̧𝗶 {MUSIC_BOT_NAME}**
│
↦**𝗔𝗿𝗮𝗻𝗮𝗻 𝗦̧𝗮𝗿𝗸𝗶:-** __{query}__
│
↦**𝗦̧𝗮𝗿𝗸𝗶 𝗦𝗼̈𝘇𝗹𝗲𝗿𝗶 𝗕𝘂𝗹𝘂𝗻𝗱𝘂:-** __{S.title}__
│
↦**𝗦𝗮𝗻𝗮𝘁𝗰̧𝗶:-** {S.artist}
│
↳**__𝗦𝗼̈𝘇𝗹𝗲𝗿:__**

{S.lyrics}"""
    if len(xxx) > 4096:
        await m.delete()
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**ÇIKTI:**\n\n`Lyrics`",
            quote=False,
        )
        os.remove(filename)
    else:
        await m.edit(xxx)
