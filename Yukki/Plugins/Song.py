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
- Belirli sorguyu ses veya video formatında indirin.



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
                "𝗕𝘂 𝗦𝗼𝗵𝗯𝗲𝘁 𝗚𝗿𝘂𝗯𝘂𝗻𝗱𝗮 __𝗔𝗻𝗼𝗻𝗶𝗺 𝗯𝗶𝗿 𝗬𝗼̈𝗻𝗲𝘁𝗶𝗰𝗶__ 𝘀𝗶𝘇𝘀𝗶𝗻𝗶𝘇!!\n│\n╰𝐘𝐨̈𝐧𝐞𝐭𝐢𝐜𝐢 𝐇𝐚𝐤𝐥𝐚𝐫𝐢𝐧𝐝𝐚𝐧 𝐊𝐮𝐥𝐥𝐚𝐧𝐢𝐜𝐢 𝐇𝐞𝐬𝐚𝐛𝐢𝐧𝐚 𝐠𝐞𝐫𝐢 𝐝𝐨̈𝐧𝐮̈𝐧."
            )
    try:
        await message.delete()
    except:
        pass
    url = get_url(message)
    if url:
        mystic = await message.reply_text("𝐔𝐑𝐋 𝐢𝐬̧𝐥𝐞𝐧𝐢𝐲𝐨𝐫... 𝐋𝐮̈𝐭𝐟𝐞𝐧 𝐁𝐞𝐤𝐥𝐞𝐲𝐢𝐧𝐢𝐳!")
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
            caption=f"📎𝗜̇𝘀𝗶𝗺: **{title}\n│\n╰⏳𝗦𝘂̈𝗿𝗲:** {duration_min} 𝗗𝗮𝗸𝗶𝗸𝗮\n│\n╰__[Video Hakkında Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            await message.reply_text(
                "**𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗺:**\n│\n╰/bul [Youtube Url'si veya Müzik Adı]\n│\n╰Belirli Sorguyu indirir."
            )
            return
        mystic = await message.reply_text("🔍")
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
            caption=f"📎𝗜̇𝘀𝗶𝗺: **{title}\n│\n╰⏳𝗦𝘂̈𝗿𝗲:** {duration_min} 𝗗𝗮𝗸𝗶𝗸𝗮\n│\n╰__[Video Hakkında Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
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
            "𝗞𝗲𝗻𝗱𝗶 𝗠𝘂̈𝘇𝗶𝗴̆𝗶𝗻𝗶 𝗔𝗿𝗮 𝗗𝗼𝘀𝘁𝘂𝗺. 𝗕𝘂 𝗱𝘂̈𝗴̆𝗺𝗲𝘆𝗶 𝗸𝘂𝗹𝗹𝗮𝗻𝗺𝗮𝗻𝗮 𝗶𝘇𝗶𝗻 𝘃𝗲𝗿𝗺𝗶𝘆𝗼𝗿𝘂𝗺.",
            show_alert=True,
        )
    what = str(what)
    type = int(type)
    if what == "F":
        if type == 9:
            query_type = 0
        else:
            query_type = int(type + 1)
        await CallbackQuery.answer("𝗦𝗼𝗻𝗿𝗮𝗸𝗶 𝗦𝗼𝗻𝘂𝗰̧ 𝗔𝗹𝗶𝗻𝗶𝘆𝗼𝗿", show_alert=True)
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
            caption=f"📎𝗜̇𝘀𝗶𝗺: **{title}\n│\n╰⏳𝗦𝘂̈𝗿𝗲:** {duration_min} 𝗗𝗮𝗸𝗶𝗸𝗮\n│\n╰__[Video Hakkında Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
    if what == "B":
        if type == 0:
            query_type = 9
        else:
            query_type = int(type - 1)
        await CallbackQuery.answer("𝗢̈𝗻𝗰𝗲𝗸𝗶 𝗦𝗼𝗻𝘂𝗰𝘂 𝗔𝗹𝗺𝗮", show_alert=True)
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
            caption=f"📎𝗜̇𝘀𝗶𝗺: **{title}\n│\n╰⏳𝗦𝘂̈𝗿𝗲:** {duration_min} 𝗗𝗮𝗸𝗶𝗸𝗮\n│\n╰__[Video Hakkında Ek Bilgi Alın](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
