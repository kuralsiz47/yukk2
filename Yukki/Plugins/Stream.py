import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto,
                            KeyboardButton, Message, ReplyKeyboardMarkup,
                            ReplyKeyboardRemove, Voice)
from youtube_search import YoutubeSearch
from youtubesearchpython import VideosSearch

from Yukki import (BOT_USERNAME, DURATION_LIMIT, DURATION_LIMIT_MIN,
                   MUSIC_BOT_NAME, app, db_mem)
from Yukki.Core.PyTgCalls.Converter import convert
from Yukki.Core.PyTgCalls.Downloader import download
from Yukki.Database import (get_active_video_chats, get_video_limit,
                            is_active_video_chat, is_on_off)
from Yukki.Decorators.assistant import AssistantAdd
from Yukki.Decorators.checker import checker
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (choose_markup, livestream_markup, playlist_markup,
                          search_markup, search_markup2, stream_quality_markup,
                          url_markup, url_markup2)
from Yukki.Utilities.changers import seconds_to_min, time_to_seconds
from Yukki.Utilities.chat import specialfont_to_normal
from Yukki.Utilities.theme import check_theme
from Yukki.Utilities.thumbnails import gen_thumb
from Yukki.Utilities.url import get_url
from Yukki.Utilities.videostream import start_live_stream, start_video_stream
from Yukki.Utilities.youtube import (get_m3u8, get_yt_info_id,
                                     get_yt_info_query,
                                     get_yt_info_query_slider)

loop = asyncio.get_event_loop()

__MODULE__ = "Video Akışı"
__HELP__ = f"""

/oynat [Herhangi bir Videoyu Yanıtla] veya [YT Bağlantısı] veya [Müzik Adı]
- Sesli Sohbette Video Akışı

**Sudo Kullanıcısı İçin:-**

/set_video_limit [Sohbet Sayısı]
- Bir seferde Görüntülü Aramalar için izin verilen maksimum Sohbet Sayısını ayarlayın.


"""


@app.on_callback_query(filters.regex(pattern=r"Yukki"))
async def choose_playmode(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, duration, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Bu senin için değil! Kendi Şarkını Ara.", show_alert=True
        )
    buttons = choose_markup(videoid, duration, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"Choose"))
async def quality_markup(_, CallbackQuery):
    limit = await get_video_limit(141414)
    if not limit:
        await CallbackQuery.message.delete()
        return await CallbackQuery.message.reply_text(
            "**𝗩𝗶𝗱𝗲𝗼 𝗮𝗸𝗶𝘀̧𝗶 𝗶𝗰̧𝗶𝗻 𝗟𝗶𝗺𝗶𝘁 𝗧𝗮𝗻𝗶𝗺𝗹𝗮𝗻𝗺𝗮𝗱𝗶**\n│\n╰ /set_video_limit [𝗬𝗮𝗹𝗻𝗶𝘇𝗰𝗮 𝗕𝗼𝘁 𝗬𝗼̈𝗻𝗲𝘁𝗶𝗰𝗶 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗰𝗶𝗹𝗮𝗿𝗶] 𝗜̇𝘇𝗶𝗻 𝘃𝗲𝗿𝗶𝗹𝗲𝗻 𝗠𝗮𝗸𝘀𝗶𝗺𝘂𝗺 𝗩𝗶𝗱𝗲𝗼𝗹𝘂 𝘀𝗲𝘀𝗹𝗶 𝗦𝗮𝘆𝗶𝘀𝗶 𝗶𝗰̧𝗶𝗻 𝗯𝗶𝗿 𝗦𝗶𝗻𝗶𝗿 𝗕𝗲𝗹𝗶𝗿𝘁𝗶𝗿.. 𝗦𝗮𝗵𝗶𝗯𝗶𝗺 𝗶𝗹𝗲 𝗶𝗹𝗲𝘁𝗶𝘀̧𝗶𝗺𝗲 𝗚𝗲𝗰̧𝗶𝗻𝗶𝘇."
        )
    count = len(await get_active_video_chats())
    if int(count) == int(limit):
        if await is_active_video_chat(CallbackQuery.message.chat.id):
            pass
        else:
            return await CallbackQuery.answer(
                "𝐎̈𝐳𝐮̈𝐫 𝐝𝐢𝐥𝐞𝐫𝐢𝐦! 𝐁𝐨𝐭, 𝐂𝐏𝐔 𝐚𝐬̧𝐢𝐫𝐢 𝐲𝐮̈𝐤𝐥𝐞𝐧𝐦𝐞 𝐬𝐨𝐫𝐮𝐧𝐥𝐚𝐫𝐢 𝐧𝐞𝐝𝐞𝐧𝐢𝐲𝐥𝐞 𝐲𝐚𝐥𝐧𝐢𝐳𝐜𝐚 𝐬𝐢𝐧𝐢𝐫𝐥𝐢 𝐬𝐚𝐲𝐢𝐝𝐚 𝐠𝐨̈𝐫𝐮̈𝐧𝐭𝐮̈𝐥𝐮̈ 𝐠𝐨̈𝐫𝐮̈𝐬̧𝐦𝐞𝐲𝐞 𝐢𝐳𝐢𝐧 𝐯𝐞𝐫𝐢𝐫. 𝐃𝐢𝐠̆𝐞𝐫 𝐬𝐨𝐡𝐛𝐞𝐭𝐥𝐞𝐫 𝐬̧𝐮 𝐚𝐧𝐝𝐚 𝐠𝐨̈𝐫𝐮̈𝐧𝐭𝐮̈𝐥𝐮̈ 𝐠𝐨̈𝐫𝐮̈𝐬̧𝐦𝐞 𝐤𝐮𝐥𝐥𝐚𝐧𝐢𝐲𝐨𝐫. 𝐒𝐞𝐬𝐞 𝐠𝐞𝐜̧𝐦𝐞𝐲𝐢 𝐝𝐞𝐧𝐞𝐲𝐢𝐧 𝐯𝐞𝐲𝐚 𝐝𝐚𝐡𝐚 𝐬𝐨𝐧𝐫𝐚 𝐭𝐞𝐤𝐫𝐚𝐫 𝐝𝐞𝐧𝐞𝐲𝐢𝐧",
                show_alert=True,
            )
    if CallbackQuery.message.chat.id not in db_mem:
        db_mem[CallbackQuery.message.chat.id] = {}
    try:
        read1 = db_mem[CallbackQuery.message.chat.id]["live_check"]
        if read1:
            return await CallbackQuery.answer(
                "𝗖𝗮𝗻𝗹𝗶 𝗬𝗮𝘆𝗶𝗻 𝗢𝘆𝗻𝗮𝘁𝗶𝗹𝗶𝘆𝗼𝗿...𝗠𝘂̈𝘇𝗶𝗸 𝗰̧𝗮𝗹𝗺𝗮𝗸 𝗶𝗰̧𝗶𝗻 𝗱𝘂𝗿𝗱𝘂𝗿𝘂𝗻",
                show_alert=True,
            )
        else:
            pass
    except:
        pass
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, duration, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Bu senin için değil! Kendi Şarkını Ara.", show_alert=True
        )
    buttons = stream_quality_markup(videoid, duration, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"LiveStream"))
async def Live_Videos_Stream(_, CallbackQuery):
    limit = await get_video_limit(141414)
    if not limit:
        await CallbackQuery.message.delete()
        return await CallbackQuery.message.reply_text(
            "**𝗩𝗶𝗱𝗲𝗼 𝗮𝗸𝗶𝘀̧𝗶 𝗶𝗰̧𝗶𝗻 𝗟𝗶𝗺𝗶𝘁 𝗧𝗮𝗻𝗶𝗺𝗹𝗮𝗻𝗺𝗮𝗱𝗶**\n│\n╰ /set_video_limit [𝗬𝗮𝗹𝗻𝗶𝘇𝗰𝗮 𝗕𝗼𝘁 𝗬𝗼̈𝗻𝗲𝘁𝗶𝗰𝗶 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗰𝗶𝗹𝗮𝗿𝗶] 𝗜̇𝘇𝗶𝗻 𝘃𝗲𝗿𝗶𝗹𝗲𝗻 𝗠𝗮𝗸𝘀𝗶𝗺𝘂𝗺 𝗩𝗶𝗱𝗲𝗼𝗹𝘂 𝘀𝗲𝘀𝗹𝗶 𝗦𝗮𝘆𝗶𝘀𝗶 𝗶𝗰̧𝗶𝗻 𝗯𝗶𝗿 𝗦𝗶𝗻𝗶𝗿 𝗕𝗲𝗹𝗶𝗿𝘁𝗶𝗿.. 𝗦𝗮𝗵𝗶𝗯𝗶𝗺 𝗶𝗹𝗲 𝗶𝗹𝗲𝘁𝗶𝘀̧𝗶𝗺𝗲 𝗚𝗲𝗰̧𝗶𝗻𝗶𝘇."
        )
    count = len(await get_active_video_chats())
    if int(count) == int(limit):
        if await is_active_video_chat(CallbackQuery.message.chat.id):
            pass
        else:
            return await CallbackQuery.answer(
                "𝐎̈𝐳𝐮̈𝐫 𝐝𝐢𝐥𝐞𝐫𝐢𝐦! 𝐁𝐨𝐭, 𝐂𝐏𝐔 𝐚𝐬̧𝐢𝐫𝐢 𝐲𝐮̈𝐤𝐥𝐞𝐧𝐦𝐞 𝐬𝐨𝐫𝐮𝐧𝐥𝐚𝐫𝐢 𝐧𝐞𝐝𝐞𝐧𝐢𝐲𝐥𝐞 𝐲𝐚𝐥𝐧𝐢𝐳𝐜𝐚 𝐬𝐢𝐧𝐢𝐫𝐥𝐢 𝐬𝐚𝐲𝐢𝐝𝐚 𝐠𝐨̈𝐫𝐮̈𝐧𝐭𝐮̈𝐥𝐮̈ 𝐠𝐨̈𝐫𝐮̈𝐬̧𝐦𝐞𝐲𝐞 𝐢𝐳𝐢𝐧 𝐯𝐞𝐫𝐢𝐫. 𝐃𝐢𝐠̆𝐞𝐫 𝐬𝐨𝐡𝐛𝐞𝐭𝐥𝐞𝐫 𝐬̧𝐮 𝐚𝐧𝐝𝐚 𝐠𝐨̈𝐫𝐮̈𝐧𝐭𝐮̈𝐥𝐮̈ 𝐠𝐨̈𝐫𝐮̈𝐬̧𝐦𝐞 𝐤𝐮𝐥𝐥𝐚𝐧𝐢𝐲𝐨𝐫. 𝐒𝐞𝐬𝐞 𝐠𝐞𝐜̧𝐦𝐞𝐲𝐢 𝐝𝐞𝐧𝐞𝐲𝐢𝐧 𝐯𝐞𝐲𝐚 𝐝𝐚𝐡𝐚 𝐬𝐨𝐧𝐫𝐚 𝐭𝐞𝐤𝐫𝐚𝐫 𝐝𝐞𝐧𝐞𝐲𝐢𝐧",
                show_alert=True,
            )
    if CallbackQuery.message.chat.id not in db_mem:
        db_mem[CallbackQuery.message.chat.id] = {}
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    quality, videoid, duration, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Bu senin için değil! Kendi Şarkını Ara.", show_alert=True
        )
    await CallbackQuery.message.delete()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    await CallbackQuery.answer(f"𝗜̇𝘀̧𝗹𝗲𝗻𝗶𝘆𝗼𝗿:- {title[:20]}", show_alert=True)
    theme = await check_theme(chat_id)
    chat_title = await specialfont_to_normal(chat_title)
    thumb = await gen_thumb(thumbnail, title, user_id, theme, chat_title)
    nrs, ytlink = await get_m3u8(videoid)
    if nrs == 0:
        return await CallbackQuery.message.reply_text(
            "𝗩𝗶𝗱𝗲𝗼 𝗙𝗼𝗿𝗺𝗮𝘁𝗹𝗮𝗿𝗶 𝗕𝘂𝗹𝘂𝗻𝗮𝗺𝗮𝗱𝗶.."
        )
    await start_live_stream(
        CallbackQuery,
        quality,
        ytlink,
        thumb,
        title,
        duration_min,
        duration_sec,
        videoid,
    )


@app.on_callback_query(filters.regex(pattern=r"VideoStream"))
async def Videos_Stream(_, CallbackQuery):
    if CallbackQuery.message.chat.id not in db_mem:
        db_mem[CallbackQuery.message.chat.id] = {}
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    quality, videoid, duration, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "Bu senin için değil! Kendi Şarkını Ara.", show_alert=True
        )
    if str(duration) == "None":
        buttons = livestream_markup(quality, videoid, duration, user_id)
        return await CallbackQuery.edit_message_text(
            "**𝗖𝗮𝗻𝗹𝗶 𝗬𝗮𝘆𝗶𝗻 𝗔𝗹𝗴𝗶𝗹𝗮𝗻𝗱𝗶**\n│\n╰𝗖𝗮𝗻𝗹𝗶 𝗮𝗸𝗶𝘀̧𝗶 𝗼𝘆𝗻𝗮𝘁𝗺𝗮𝗸 𝗶𝘀𝘁𝗲𝗿 𝗺𝗶𝘀𝗶𝗻𝗶𝘇? 𝗕𝘂, 𝗺𝗲𝘃𝗰𝘂𝘁 𝗺𝘂̈𝘇𝗶𝗸 𝗰̧𝗮𝗹𝗺𝗮𝘆𝗶 𝗱𝘂𝗿𝗱𝘂𝗿𝗮𝗰𝗮𝗸 (𝘃𝗮𝗿𝘀𝗮) 𝘃𝗲 𝗰𝗮𝗻𝗹𝗶 𝘃𝗶𝗱𝗲𝗼 𝗮𝗸𝗶𝘀̧𝗶 𝗯𝗮𝘀̧𝗹𝗮𝘁𝗮𝗰𝗮𝗸𝘁𝗶𝗿.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    await CallbackQuery.message.delete()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    if duration_sec > DURATION_LIMIT:
        return await CallbackQuery.message.reply_text(
            f"**𝐒𝐮̈𝐫𝐞 𝐒𝐢𝐧𝐢𝐫𝐢 𝐀𝐬̧𝐢𝐥𝐝𝐢**\n│\n╰**𝐈̇𝐳𝐢𝐧 𝐕𝐞𝐫𝐢𝐥𝐞𝐧 𝐒𝐮̈𝐫𝐞: **{DURATION_LIMIT_MIN} 𝐃𝐚𝐤𝐢𝐤𝐚(s)\n│\n╰**𝐀𝐥𝐢𝐧𝐚𝐧 𝐒𝐮̈𝐫𝐞:** {duration_min} 𝐃𝐚𝐤𝐢𝐤𝐚(s)"
        )
    await CallbackQuery.answer(f"𝗜̇𝘀̧𝗹𝗲𝗻𝗶𝘆𝗼𝗿:- {title[:20]}", show_alert=True)
    theme = await check_theme(chat_id)
    chat_title = await specialfont_to_normal(chat_title)
    thumb = await gen_thumb(thumbnail, title, user_id, theme, chat_title)
    nrs, ytlink = await get_m3u8(videoid)
    if nrs == 0:
        return await CallbackQuery.message.reply_text(
            "𝗩𝗶𝗱𝗲𝗼 𝗙𝗼𝗿𝗺𝗮𝘁𝗹𝗮𝗿𝗶 𝗕𝘂𝗹𝘂𝗻𝗮𝗺𝗮𝗱𝗶.."
        )
    await start_video_stream(
        CallbackQuery,
        quality,
        ytlink,
        thumb,
        title,
        duration_min,
        duration_sec,
        videoid,
    )
