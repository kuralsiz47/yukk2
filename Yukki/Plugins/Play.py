import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)
from youtube_search import YoutubeSearch

import Yukki
from Yukki import (BOT_USERNAME, DURATION_LIMIT, DURATION_LIMIT_MIN,
                   MUSIC_BOT_NAME, app, db_mem)
from Yukki.Core.PyTgCalls.Converter import convert
from Yukki.Core.PyTgCalls.Downloader import download
from Yukki.Core.PyTgCalls.Tgdownloader import telegram_download
from Yukki.Database import (get_active_video_chats, get_video_limit,
                            is_active_video_chat)
from Yukki.Decorators.assistant import AssistantAdd
from Yukki.Decorators.checker import checker
from Yukki.Decorators.logger import logging
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (livestream_markup, playlist_markup, search_markup,
                          search_markup2, url_markup, url_markup2)
from Yukki.Utilities.changers import seconds_to_min, time_to_seconds
from Yukki.Utilities.chat import specialfont_to_normal
from Yukki.Utilities.stream import start_stream, start_stream_audio
from Yukki.Utilities.theme import check_theme
from Yukki.Utilities.thumbnails import gen_thumb
from Yukki.Utilities.url import get_url
from Yukki.Utilities.videostream import start_stream_video
from Yukki.Utilities.youtube import (get_yt_info_id, get_yt_info_query,
                                     get_yt_info_query_slider)

loop = asyncio.get_event_loop()


@app.on_message(
    filters.command(["oynat", f"play@{BOT_USERNAME}"]) & filters.group
)
@checker
@logging
@PermissionCheck
@AssistantAdd
async def play(_, message: Message):
    await message.delete()
    if message.chat.id not in db_mem:
        db_mem[message.chat.id] = {}
    if message.sender_chat:
        return await message.reply_text(
            "𝗕𝘂 𝗦𝗼𝗵𝗯𝗲𝘁 𝗚𝗿𝘂𝗯𝘂𝗻𝗱𝗮 __𝗔𝗻𝗼𝗻𝗶𝗺 𝗯𝗶𝗿 𝗬𝗼̈𝗻𝗲𝘁𝗶𝗰𝗶__ 𝘀𝗶𝘇𝘀𝗶𝗻𝗶𝘇!\n│\n╰𝗬𝗼̈𝗻𝗲𝘁𝗶𝗰𝗶 𝗛𝗮𝗸𝗹𝗮𝗿𝗶𝗻𝗱𝗮𝗻 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗰𝗶 𝗛𝗲𝘀𝗮𝗯𝗶𝗻𝗮 𝗴𝗲𝗿𝗶 𝗱𝗼̈𝗻𝘂̈𝗻."
        )
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    if audio:
        mystic = await message.reply_text(
            "🔄 𝗦𝗲𝘀 𝗜̇𝘀̧𝗹𝗲𝗻𝗶𝘆𝗼𝗿... 𝗟𝘂̈𝘁𝗳𝗲𝗻 𝗕𝗲𝗸𝗹𝗲𝘆𝗶𝗻𝗶𝘇"
        )
        try:
            read = db_mem[message.chat.id]["live_check"]
            if read:
                return await mystic.edit(
                    "𝗖𝗮𝗻𝗹𝗶 𝗬𝗮𝘆𝗶𝗻 𝗢𝘆𝗻𝗮𝘁𝗶𝗹𝗶𝘆𝗼𝗿...𝗠𝘂̈𝘇𝗶𝗸 𝗰̧𝗮𝗹𝗺𝗮𝗸 𝗶𝗰̧𝗶𝗻 𝗱𝘂𝗿𝗱𝘂𝗿𝘂𝗻"
                )
            else:
                pass
        except:
            pass
        if audio.file_size > 1073741824:
            return await mystic.edit_text(
                "𝗦𝗲𝘀 𝗗𝗼𝘀𝘆𝗮𝘀𝗶 𝗕𝗼𝘆𝘂𝘁𝘂 𝟭𝟱𝟬 𝗺𝗯'𝗱𝗲𝗻 𝗞𝘂̈𝗰̧𝘂̈𝗸 𝗢𝗹𝗺𝗮𝗹𝗶𝗱𝗶𝗿"
            )
        duration_min = seconds_to_min(audio.duration)
        duration_sec = audio.duration
        if (audio.duration) > DURATION_LIMIT:
            return await mystic.edit_text(
                f"**𝗦𝘂̈𝗿𝗲 𝗦𝗶𝗻𝗶𝗿𝗶 𝗔𝘀̧𝗶𝗹𝗱𝗶**\n│\n╰**𝗜̇𝘇𝗶𝗻 𝗩𝗲𝗿𝗶𝗹𝗲𝗻 𝗦𝘂̈𝗿𝗲: **{DURATION_LIMIT_MIN} 𝗗𝗮𝗸𝗶𝗸𝗮(s)\n│\n╰**𝗔𝗹𝗶𝗻𝗮𝗻 𝗦𝘂̈𝗿𝗲:** {duration_min} 𝗗𝗮𝗸𝗶𝗸𝗮(s)"
            )
        file_name = (
            audio.file_unique_id
            + "."
            + (
                (audio.file_name.split(".")[-1])
                if (not isinstance(audio, Voice))
                else "ogg"
            )
        )
        file_name = path.join(path.realpath("downloads"), file_name)
        file = await convert(
            (await message.reply_to_message.download(file_name))
            if (not path.isfile(file_name))
            else file_name,
        )
        return await start_stream_audio(
            message,
            file,
            "smex1",
            "𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺𝗱𝗮𝗻 𝗩𝗲𝗿𝗶𝗹𝗲𝗻 𝗦𝗲𝘀",
            duration_min,
            duration_sec,
            mystic,
        )
    elif video:
        limit = await get_video_limit(141414)
        if not limit:
            return await message.reply_text(
                "**𝗚𝗼̈𝗿𝘂̈𝗻𝘁𝘂̈𝗹𝘂̈ 𝗔𝗿𝗮𝗺𝗮𝗹𝗮𝗿 𝗶𝗰̧𝗶𝗻 𝗟𝗶𝗺𝗶𝘁 𝗧𝗮𝗻𝗶𝗺𝗹𝗮𝗻𝗺𝗮𝗱𝗶**\n│\n╰ /set_video_limit [𝐘𝐚𝐥𝐧𝐢𝐳𝐜𝐚 𝐁𝐨𝐭 𝐘𝐨̈𝐧𝐞𝐭𝐢𝐜𝐢 𝐊𝐮𝐥𝐥𝐚𝐧𝐢𝐜𝐢𝐥𝐚𝐫𝐢] 𝐭𝐚𝐫𝐚𝐟𝐢𝐧𝐝𝐚𝐧 𝐁𝐨𝐭𝐭𝐚 𝐢𝐳𝐢𝐧 𝐯𝐞𝐫𝐢𝐥𝐞𝐧 𝐌𝐚𝐤𝐬𝐢𝐦𝐮𝐦 𝐆𝐨̈𝐫𝐮̈𝐧𝐭𝐮̈𝐥𝐮̈ 𝐀𝐫𝐚𝐦𝐚 𝐒𝐚𝐲𝐢𝐬𝐢 𝐢𝐜̧𝐢𝐧 𝐛𝐢𝐫 𝐒𝐢𝐧𝐢𝐫 𝐁𝐞𝐥𝐢𝐫𝐥𝐞𝐲𝐢𝐧."
            )
        count = len(await get_active_video_chats())
        if int(count) == int(limit):
            if await is_active_video_chat(message.chat.id):
                pass
            else:
                return await message.reply_text(
                    "𝐎̈𝐳𝐮̈𝐫 𝐝𝐢𝐥𝐞𝐫𝐢𝐦! 𝐁𝐨𝐭, 𝐂𝐏𝐔 𝐚𝐬̧𝐢𝐫𝐢 𝐲𝐮̈𝐤𝐥𝐞𝐧𝐦𝐞 𝐬𝐨𝐫𝐮𝐧𝐥𝐚𝐫𝐢 𝐧𝐞𝐝𝐞𝐧𝐢𝐲𝐥𝐞 𝐲𝐚𝐥𝐧𝐢𝐳𝐜𝐚 𝐬𝐢𝐧𝐢𝐫𝐥𝐢 𝐬𝐚𝐲𝐢𝐝𝐚 𝐠𝐨̈𝐫𝐮̈𝐧𝐭𝐮̈𝐥𝐮̈ 𝐠𝐨̈𝐫𝐮̈𝐬̧𝐦𝐞𝐲𝐞 𝐢𝐳𝐢𝐧 𝐯𝐞𝐫𝐢𝐫. 𝐃𝐢𝐠̆𝐞𝐫 𝐛𝐢𝐫𝐜̧𝐨𝐤 𝐬𝐨𝐡𝐛𝐞𝐭 𝐬̧𝐮 𝐚𝐧𝐝𝐚 𝐠𝐨̈𝐫𝐮̈𝐧𝐭𝐮̈𝐥𝐮̈ 𝐠𝐨̈𝐫𝐮̈𝐬̧𝐦𝐞 𝐤𝐮𝐥𝐥𝐚𝐧𝐢𝐲𝐨𝐫. 𝐒𝐞𝐬𝐞 𝐠𝐞𝐜̧𝐦𝐞𝐲𝐢 𝐝𝐞𝐧𝐞𝐲𝐢𝐧 𝐯𝐞𝐲𝐚 𝐝𝐚𝐡𝐚 𝐬𝐨𝐧𝐫𝐚 𝐭𝐞𝐤𝐫𝐚𝐫 𝐝𝐞𝐧𝐞𝐲𝐢𝐧"
                )
        mystic = await message.reply_text(
            "🔄 𝗩𝗶𝗱𝗲𝗼 𝗜̇𝘀̧𝗹𝗲𝗻𝗶𝘆𝗼𝗿... 𝗟𝘂̈𝘁𝗳𝗲𝗻 𝗕𝗲𝗸𝗹𝗲𝘆𝗶𝗻𝗶𝘇!"
        )
        try:
            read = db_mem[message.chat.id]["live_check"]
            if read:
                return await mystic.edit(
                    "𝗖𝗮𝗻𝗹𝗶 𝗬𝗮𝘆𝗶𝗻 𝗢𝘆𝗻𝗮𝘁𝗶𝗹𝗶𝘆𝗼𝗿...𝗠𝘂̈𝘇𝗶𝗸 𝗰̧𝗮𝗹𝗺𝗮𝗸 𝗶𝗰̧𝗶𝗻 𝗱𝘂𝗿𝗱𝘂𝗿𝘂𝗻"
                )
            else:
                pass
        except:
            pass
        file = await telegram_download(message, mystic)
        return await start_stream_video(
            message,
            file,
            "𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺𝗱𝗮𝗻 𝗩𝗲𝗿𝗶𝗹𝗲𝗻 𝗩𝗶𝗱𝗲𝗼",
            mystic,
        )
    elif url:
        mystic = await message.reply_text("🔄 𝗨𝗥𝗟 𝗶𝘀̧𝗹𝗲𝗻𝗶𝘆𝗼𝗿... 𝗟𝘂̈𝘁𝗳𝗲𝗻 𝗕𝗲𝗸𝗹𝗲𝘆𝗶𝗻𝗶𝘇!")
        if not message.reply_to_message:
            query = message.text.split(None, 1)[1]
        else:
            query = message.reply_to_message.text
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query(query)
        await mystic.delete()
        buttons = url_markup2(videoid, duration_min, message.from_user.id)
        return await message.reply_photo(
            photo=thumb,
            caption=f"📎𝗜̇𝘀𝗶𝗺: **{title}\n│\n╰⏳𝗦𝘂̈𝗿𝗲:** {duration_min} 𝗗𝗮𝗸𝗶𝗸𝗮\n│\n╰__[𝗩𝗶𝗱𝗲𝗼 𝗛𝗮𝗸𝗸𝗶𝗻𝗱𝗮 𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹𝗶𝗻](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            buttons = playlist_markup(
                message.from_user.first_name, message.from_user.id, "abcd"
            )
            await message.reply_photo(
                photo="Utils/Playlist.jpg",
                caption=(
                    "**𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗺:** /oynat [Müzik Adı veya Youtube Bağlantısı veya Sese Cevap Ver]\n│\n╰Çalın! Aşağıdan birini seçin."
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
        mystic = await message.reply_text("🔍 **Senin İçin Arıyorum**")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query(query)
        await mystic.delete()
        buttons = url_markup(
            videoid, duration_min, message.from_user.id, query, 0
        )
        return await message.reply_photo(
            photo=thumb,
            caption=f"📎𝗜̇𝘀𝗶𝗺: **{title}\n│\n╰⏳𝗦𝘂̈𝗿𝗲:** {duration_min} 𝗗𝗮𝗸𝗶𝗸𝗮\n│\n╰__[𝗩𝗶𝗱𝗲𝗼 𝗛𝗮𝗸𝗸𝗶𝗻𝗱𝗮 𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹𝗶𝗻](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(filters.regex(pattern=r"MusicStream"))
async def Music_Stream(_, CallbackQuery):
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
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    videoid, duration, user_id = callback_request.split("|")
    if str(duration) == "None":
        buttons = livestream_markup("720", videoid, duration, user_id)
        return await CallbackQuery.edit_message_text(
            "**𝗖𝗮𝗻𝗹𝗶 𝗬𝗮𝘆𝗶𝗻 𝗔𝗹𝗴𝗶𝗹𝗮𝗻𝗱𝗶**\n│\n╰𝗖𝗮𝗻𝗹𝗶 𝗮𝗸𝗶𝘀̧𝗶 𝗼𝘆𝗻𝗮𝘁𝗺𝗮𝗸 𝗶𝘀𝘁𝗲𝗿 𝗺𝗶𝘀𝗶𝗻𝗶𝘇? 𝗕𝘂, 𝗺𝗲𝘃𝗰𝘂𝘁 𝗺𝘂̈𝘇𝗶𝗸 𝗰̧𝗮𝗹𝗺𝗮𝘆𝗶 𝗱𝘂𝗿𝗱𝘂𝗿𝗮𝗰𝗮𝗸 (𝘃𝗮𝗿𝘀𝗮) 𝘃𝗲 𝗰𝗮𝗻𝗹𝗶 𝘃𝗶𝗱𝗲𝗼 𝗮𝗸𝗶𝘀̧𝗶 𝗯𝗮𝘀̧𝗹𝗮𝘁𝗮𝗰𝗮𝗸𝘁𝗶𝗿.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "𝗕𝘂 𝘀𝗲𝗻𝗶𝗻 𝗶𝗰̧𝗶𝗻 𝗱𝗲𝗴̆𝗶𝗹 𝗗𝗼𝘀𝘁𝘂𝗺 𝘀𝗼𝗹𝗮 𝘁𝗶𝗸𝗹𝗮𝗺𝗮!\n│\n╰𝗞𝗲𝗻𝗱𝗶 𝗦̧𝗮𝗿𝗸𝗶𝗻𝗶 𝗔𝗿𝗮.", show_alert=True
        )
    await CallbackQuery.message.delete()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    if duration_sec > DURATION_LIMIT:
        return await CallbackQuery.message.reply_text(
            f"**𝗦𝘂̈𝗿𝗲 𝗦𝗶𝗻𝗶𝗿𝗶 𝗔𝘀̧𝗶𝗹𝗱𝗶**\n│\n╰**𝗜̇𝘇𝗶𝗻 𝗩𝗲𝗿𝗶𝗹𝗲𝗻 𝗦𝘂̈𝗿𝗲: **{DURATION_LIMIT_MIN} 𝗱𝗮𝗸𝗶𝗸𝗮(s)\n│\n╰**𝗔𝗹𝗶𝗻𝗮𝗻 𝗦𝘂̈𝗿𝗲:** {duration_min} 𝗱𝗮𝗸𝗶𝗸𝗮(s)"
        )
    await CallbackQuery.answer(f"𝗜̇𝘀̧𝗹𝗲𝗺𝗲:- {title[:20]}", show_alert=True)
    mystic = await CallbackQuery.message.reply_text(
        f"**{MUSIC_BOT_NAME} 𝗜̇𝗡𝗗𝗜̇𝗥𝗜̇𝗬𝗢𝗥**\n│\n╰**𝗜̇𝘀𝗶𝗺:** {title[:50]}\n│\n╰0% ▂▃▄▅▆▇▉ 100%"
    )
    downloaded_file = await loop.run_in_executor(
        None, download, videoid, mystic, title
    )
    raw_path = await convert(downloaded_file)
    theme = await check_theme(chat_id)
    chat_title = await specialfont_to_normal(chat_title)
    thumb = await gen_thumb(thumbnail, title, user_id, theme, chat_title)
    if chat_id not in db_mem:
        db_mem[chat_id] = {}
    await start_stream(
        CallbackQuery,
        raw_path,
        videoid,
        thumb,
        title,
        duration_min,
        duration_sec,
        mystic,
    )


@app.on_callback_query(filters.regex(pattern=r"Search"))
async def search_query_more(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "𝗞𝗲𝗻𝗱𝗶 𝗠𝘂̈𝘇𝗶𝗴̆𝗶𝗻𝗶 𝗔𝗿𝗮 𝗗𝗼𝘀𝘁𝘂𝗺. 𝗕𝘂 𝗱𝘂̈𝗴̆𝗺𝗲𝘆𝗶 𝗸𝘂𝗹𝗹𝗮𝗻𝗺𝗮𝗻𝗮 𝗶𝘇𝗶𝗻 𝘃𝗲𝗿𝗺𝗶𝘆𝗼𝗿𝘂𝗺.",
            show_alert=True,
        )
    await CallbackQuery.answer("Daha Fazla Sonuç Aranıyor")
    results = YoutubeSearch(query, max_results=5).to_dict()
    med = InputMediaPhoto(
        media="Utils/Result.JPEG",
        caption=(
            f"1️⃣<b>{results[0]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[0]['id']})__</u>\n\n2️⃣<b>{results[1]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[1]['id']})__</u>\n\n3️⃣<b>{results[2]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[2]['id']})__</u>\n\n4️⃣<b>{results[3]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[3]['id']})__</u>\n\n5️⃣<b>{results[4]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[4]['id']})__</u>"
        ),
    )
    buttons = search_markup(
        results[0]["id"],
        results[1]["id"],
        results[2]["id"],
        results[3]["id"],
        results[4]["id"],
        results[0]["duration"],
        results[1]["duration"],
        results[2]["duration"],
        results[3]["duration"],
        results[4]["duration"],
        user_id,
        query,
    )
    return await CallbackQuery.edit_message_media(
        media=med, reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"popat"))
async def popat(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    i, query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "𝗕𝘂 𝘀𝗲𝗻𝗶𝗻 𝗶𝗰̧𝗶𝗻 𝗱𝗲𝗴̆𝗶𝗹! 𝗞𝗲𝗻𝗱𝗶 𝗦̧𝗮𝗿𝗸𝗶𝗻𝗶𝘇𝗶 𝗔𝗿𝗮𝘆𝗶𝗻", show_alert=True
        )
    results = YoutubeSearch(query, max_results=10).to_dict()
    if int(i) == 1:
        buttons = search_markup2(
            results[5]["id"],
            results[6]["id"],
            results[7]["id"],
            results[8]["id"],
            results[9]["id"],
            results[5]["duration"],
            results[6]["duration"],
            results[7]["duration"],
            results[8]["duration"],
            results[9]["duration"],
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"6️⃣<b>{results[5]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[5]['id']})__</u>\n\n7️⃣<b>{results[6]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[6]['id']})__</u>\n\n8️⃣<b>{results[7]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[7]['id']})__</u>\n\n9️⃣<b>{results[8]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[8]['id']})__</u>\n\n🔟<b>{results[9]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[9]['id']})__</u>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        disable_web_page_preview = True
        return
    if int(i) == 2:
        buttons = search_markup(
            results[0]["id"],
            results[1]["id"],
            results[2]["id"],
            results[3]["id"],
            results[4]["id"],
            results[0]["duration"],
            results[1]["duration"],
            results[2]["duration"],
            results[3]["duration"],
            results[4]["duration"],
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"1️⃣<b>{results[0]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[0]['id']})__</u>\n\n2️⃣<b>{results[1]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[1]['id']})__</u>\n\n3️⃣<b>{results[2]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[2]['id']})__</u>\n\n4️⃣<b>{results[3]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[3]['id']})__</u>\n\n5️⃣<b>{results[4]['title']}</b>\n  ┗  🔗 <u>__[𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹](https://t.me/{BOT_USERNAME}?start=info_{results[4]['id']})__</u>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        disable_web_page_preview = True
        return


@app.on_callback_query(filters.regex(pattern=r"slider"))
async def slider_query_results(_, CallbackQuery):
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
        ) = get_yt_info_query_slider(query, query_type)
        buttons = url_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"📎𝐈̇𝐬𝐢𝐦: **{title}\n│\n╰⏳𝐒𝐮̈𝐫𝐞:** {duration_min} 𝐃𝐚𝐤𝐢𝐤𝐚\n│\n╰__[𝗩𝗶𝗱𝗲𝗼 𝗛𝗮𝗸𝗸𝗶𝗻𝗱𝗮 𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹𝗶𝗻](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
    if what == "B":
        if type == 0:
            query_type = 9
        else:
            query_type = int(type - 1)
        await CallbackQuery.answer("Önceki Sonucu Alınıyor", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query_slider(query, query_type)
        buttons = url_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"📎𝐈̇𝐬𝐢𝐦: **{title}\n│\n╰⏳𝐒𝐮̈𝐫𝐞:** {duration_min} 𝐃𝐚𝐤𝐢𝐤𝐚\n│\n╰__[𝗩𝗶𝗱𝗲𝗼 𝗛𝗮𝗸𝗸𝗶𝗻𝗱𝗮 𝗘𝗸 𝗕𝗶𝗹𝗴𝗶 𝗔𝗹𝗶𝗻](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
