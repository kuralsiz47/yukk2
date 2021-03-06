import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)
from youtube_search import YoutubeSearch

from Yukki import (BOT_USERNAME, DURATION_LIMIT, DURATION_LIMIT_MIN,
                   MUSIC_BOT_NAME, app, db_mem)
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import song_download_markup, song_markup
from Yukki.Utilities.url import get_url
from Yukki.Utilities.youtube import get_yt_info_query, get_yt_info_query_slider

loop = asyncio.get_event_loop()

__MODULE__ = "Bul"
__HELP__ = """


/bul [Youtube URL'si veya Arama Sorgusu] 
- Belirli sorguyu ses veya video formatฤฑnda indirin.



"""


@app.on_message(
    filters.command(["bul", f"song@{BOT_USERNAME}"])
)
@PermissionCheck
async def play(_, message: Message):
    if message.chat.type == "private":
        pass
    else:
        if message.sender_chat:
            return await message.reply_text(
                "๐๐ ๐ฆ๐ผ๐ต๐ฏ๐ฒ๐ ๐๐ฟ๐๐ฏ๐๐ป๐ฑ๐ฎ __๐๐ป๐ผ๐ป๐ถ๐บ ๐ฏ๐ถ๐ฟ ๐ฌ๐ผฬ๐ป๐ฒ๐๐ถ๐ฐ๐ถ__ ๐๐ถ๐๐๐ถ๐ป๐ถ๐!!\nโ\nโฐ๐๐จฬ๐ง๐๐ญ๐ข๐๐ข ๐๐๐ค๐ฅ๐๐ซ๐ข๐ง๐๐๐ง ๐๐ฎ๐ฅ๐ฅ๐๐ง๐ข๐๐ข ๐๐๐ฌ๐๐๐ข๐ง๐ ๐ ๐๐ซ๐ข ๐๐จฬ๐ง๐ฎฬ๐ง."
            )
    try:
        await message.delete()
    except:
        pass
    url = get_url(message)
    if url:
        mystic = await message.reply_text("๐๐๐ ๐ข๐ฌฬง๐ฅ๐๐ง๐ข๐ฒ๐จ๐ซ... ๐๐ฎฬ๐ญ๐๐๐ง ๐๐๐ค๐ฅ๐๐ฒ๐ข๐ง๐ข๐ณ!")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(None, get_yt_info_query, query)
        if str(duration_min) == "None":
            return await mystic.edit("Sorry! Its a Live Video")
        await mystic.delete()
        buttons = song_download_markup(videoid, message.from_user.id)
        return await message.reply_photo(
            photo=thumb,
            caption=f"๐๐ฬ๐๐ถ๐บ: **{title}\nโ\nโฐโณ๐ฆ๐ฬ๐ฟ๐ฒ:** {duration_min} ๐๐ฎ๐ธ๐ถ๐ธ๐ฎ\nโ\nโฐ__[Video Hakkฤฑnda Ek Bilgi Alฤฑn](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            await message.reply_text(
                "**๐๐๐น๐น๐ฎ๐ป๐ถ๐บ:**\nโ\nโฐ/bul [Youtube Url'si veya Mรผzik Adฤฑ]\nโ\nโฐBelirli Sorguyu indirir."
            )
            return
        mystic = await message.reply_text("๐")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(None, get_yt_info_query, query)
        if str(duration_min) == "None":
            return await mystic.edit("Sorry! Its a Live Video")
        await mystic.delete()
        buttons = song_markup(
            videoid, duration_min, message.from_user.id, query, 0
        )
        return await message.reply_photo(
            photo=thumb,
            caption=f"๐๐ฬ๐๐ถ๐บ: **{title}\nโ\nโฐโณ๐ฆ๐ฬ๐ฟ๐ฒ:** {duration_min} ๐๐ฎ๐ธ๐ถ๐ธ๐ฎ\nโ\nโฐ__[Video Hakkฤฑnda Ek Bilgi Alฤฑn](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(filters.regex("qwertyuiopasdfghjkl"))
async def qwertyuiopasdfghjkl(_, CallbackQuery):
    print("234")
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = song_download_markup(videoid, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"song_right"))
async def song_right(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, type, query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "๐๐ฒ๐ป๐ฑ๐ถ ๐ ๐ฬ๐๐ถ๐ดฬ๐ถ๐ป๐ถ ๐๐ฟ๐ฎ ๐๐ผ๐๐๐๐บ. ๐๐ ๐ฑ๐ฬ๐ดฬ๐บ๐ฒ๐๐ถ ๐ธ๐๐น๐น๐ฎ๐ป๐บ๐ฎ๐ป๐ฎ ๐ถ๐๐ถ๐ป ๐๐ฒ๐ฟ๐บ๐ถ๐๐ผ๐ฟ๐๐บ.",
            show_alert=True,
        )
    what = str(what)
    type = int(type)
    if what == "F":
        if type == 9:
            query_type = 0
        else:
            query_type = int(type + 1)
        await CallbackQuery.answer("๐ฆ๐ผ๐ป๐ฟ๐ฎ๐ธ๐ถ ๐ฆ๐ผ๐ป๐๐ฐฬง ๐๐น๐ถ๐ป๐ถ๐๐ผ๐ฟ", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(
            None, get_yt_info_query_slider, query, query_type
        )
        buttons = song_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"๐๐ฬ๐๐ถ๐บ: **{title}\nโ\nโฐโณ๐ฆ๐ฬ๐ฟ๐ฒ:** {duration_min} ๐๐ฎ๐ธ๐ถ๐ธ๐ฎ\nโ\nโฐ__[Video Hakkฤฑnda Ek Bilgi Alฤฑn](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
    if what == "B":
        if type == 0:
            query_type = 9
        else:
            query_type = int(type - 1)
        await CallbackQuery.answer("๐ขฬ๐ป๐ฐ๐ฒ๐ธ๐ถ ๐ฆ๐ผ๐ป๐๐ฐ๐ ๐๐น๐บ๐ฎ", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(
            None, get_yt_info_query_slider, query, query_type
        )
        buttons = song_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"๐๐ฬ๐๐ถ๐บ: **{title}\nโ\nโฐโณ๐ฆ๐ฬ๐ฟ๐ฒ:** {duration_min} ๐๐ฎ๐ธ๐ถ๐ธ๐ฎ\nโ\nโฐ__[Video Hakkฤฑnda Ek Bilgi Alฤฑn](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
