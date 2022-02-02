import asyncio
import os
import random
from asyncio import QueueEmpty

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup

from config import get_queue
from Yukki import BOT_USERNAME, MUSIC_BOT_NAME, app, db_mem
from Yukki.Core.PyTgCalls import Queues
from Yukki.Core.PyTgCalls.Converter import convert
from Yukki.Core.PyTgCalls.Downloader import download
from Yukki.Core.PyTgCalls.Yukki import (join_stream, pause_stream,
                                        resume_stream, skip_stream,
                                        skip_video_stream, stop_stream)
from Yukki.Database import (_get_playlists, delete_playlist, get_playlist,
                            get_playlist_names, is_active_chat,
                            remove_active_video_chat, save_playlist)
from Yukki.Database.queue import (add_active_chat, is_active_chat,
                                  is_music_playing, music_off, music_on,
                                  remove_active_chat)
from Yukki.Decorators.admins import AdminRightsCheckCB
from Yukki.Decorators.checker import checkerCB
from Yukki.Inline import (audio_markup, audio_markup2, download_markup,
                          fetch_playlist, paste_queue_markup, primary_markup,
                          secondary_markup2)
from Yukki.Utilities.changers import time_to_seconds
from Yukki.Utilities.chat import specialfont_to_normal
from Yukki.Utilities.paste import isPreviewUp, paste_queue
from Yukki.Utilities.theme import check_theme
from Yukki.Utilities.thumbnails import gen_thumb
from Yukki.Utilities.timer import start_timer
from Yukki.Utilities.youtube import get_m3u8, get_yt_info_id

loop = asyncio.get_event_loop()


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "𝗕𝘂𝗻𝘂 𝗞𝗮𝗽𝗮𝘁𝗺𝗮𝗻𝗮 𝗶𝘇𝗶𝗻 𝗬𝗼𝗸 𝗗𝗼𝘀𝘁𝘂𝗺 𝗗𝗼𝗸𝘂𝗻𝗺𝗮. 𝗦𝗮𝗱𝗲𝗰𝗲 𝗬𝗼̈𝗻𝗲𝘁𝗶𝗹𝗲𝗿 𝗞𝗮𝗽𝗮𝘁𝗶𝗿..", show_alert=True
        )
    await CallbackQuery.message.delete()
    await CallbackQuery.answer()


@app.on_callback_query(
    filters.regex(pattern=r"^(pausecb|skipcb|stopcb|resumecb)$")
)
@AdminRightsCheckCB
@checkerCB
async def admin_risghts(_, CallbackQuery):
    global get_queue
    command = CallbackQuery.matches[0].group(1)
    if not await is_active_chat(CallbackQuery.message.chat.id):
        return await CallbackQuery.answer(
            "𝗦𝗲𝘀𝗹𝗶 𝘀𝗼𝗵𝗯𝗲𝘁𝘁𝗲 𝗵𝗶𝗰̧𝗯𝗶𝗿 𝘀̧𝗲𝘆 𝗰̧𝗮𝗹𝗺𝗶𝘆𝗼𝗿.", show_alert=True
        )
    chat_id = CallbackQuery.message.chat.id
    if command == "pausecb":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(
                "𝗠𝘂̈𝘇𝗶𝗸 𝘇𝗮𝘁𝗲𝗻 𝗗𝘂𝗿𝗮𝗸𝗹𝗮𝘁𝗶𝗹𝗱𝗶", show_alert=True
            )
        await music_off(chat_id)
        await pause_stream(chat_id)
        await CallbackQuery.message.reply_text(
            f"🎧 𝗦𝗲𝘀𝗹𝗶 𝘀𝗼𝗵𝗯𝗲𝘁 𝗗𝘂𝗿𝗮𝗸𝗹𝗮𝘁𝗶𝗹𝗱𝗶.. 𝗦𝗔𝗕𝗜𝗥 𝗬𝘂̈𝗸𝗹𝗲𝗻𝗶𝘆𝗼𝗿. \n│\n╰{CallbackQuery.from_user.mention}!",
            reply_markup=audio_markup2,
        )
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("𝗗𝘂𝗿𝗮𝗸𝗹𝗮𝘁𝗶𝗹𝗱𝗶", show_alert=True)
    if command == "resumecb":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(
                "𝗠𝘂̈𝘇𝗶𝗸 𝘇𝗮𝘁𝗲𝗻 𝗗𝗲𝘃𝗮𝗺 𝗘𝗱𝗶𝘆𝗼𝗿.", show_alert=True
            )
        await music_on(chat_id)
        await resume_stream(chat_id)
        await CallbackQuery.message.reply_text(
            f"🎧 𝗦𝗲𝘀𝗹𝗶 𝘀𝗼𝗵𝗯𝗲𝘁 𝗗𝗲𝘃𝗮𝗺 𝐞𝐝𝐢𝐲𝐨𝐫 \n│\n╰{CallbackQuery.from_user.mention}!",
            reply_markup=audio_markup2,
        )
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("Devam", show_alert=True)
    if command == "stopcb":
        if CallbackQuery.message.chat.id not in db_mem:
            db_mem[CallbackQuery.message.chat.id] = {}
        wtfbro = db_mem[CallbackQuery.message.chat.id]
        wtfbro["live_check"] = False
        try:
            Queues.clear(chat_id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await remove_active_video_chat(chat_id)
        await stop_stream(chat_id)
        await CallbackQuery.message.reply_text(
            f"🎧 𝐒𝐞𝐬𝐥𝐢 𝐬𝐨𝐡𝐛𝐞𝐭 𝐁𝐢𝐭𝐭𝐢 :( \n│\n╰ {CallbackQuery.from_user.mention}!",
            reply_markup=audio_markup2,
        )
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("Kapatıldı", show_alert=True)
    if command == "skipcb":
        if CallbackQuery.message.chat.id not in db_mem:
            db_mem[CallbackQuery.message.chat.id] = {}
        wtfbro = db_mem[CallbackQuery.message.chat.id]
        wtfbro["live_check"] = False
        Queues.task_done(chat_id)
        if Queues.is_empty(chat_id):
            await remove_active_chat(chat_id)
            await remove_active_video_chat(chat_id)
            await CallbackQuery.message.reply_text(
                f"𝗔𝗿𝘁𝗶𝗸 𝗦𝗶𝗿𝗮𝗱𝗮 𝗠𝘂̈𝘇𝗶𝗸 __𝗬𝗼𝗸__ \n│\n╰𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁'𝘁𝗲𝗻 𝗮𝘆𝗿𝗶𝗹𝗶𝘆𝗼𝗿𝘂𝗺.\n│\n╰𝐁𝐢𝐫𝐝𝐚𝐡𝐚 𝐃𝐨𝐤𝐚𝐧𝐦𝐚 𝐁𝐚𝐧𝐚 :- {CallbackQuery.from_user.mention}"
            )
            await stop_stream(chat_id)
            await CallbackQuery.message.delete()
            await CallbackQuery.answer(
                "𝗔𝘁𝗹𝗮𝘁𝗶𝗹𝗱𝗶. 𝗞𝘂𝘆𝗿𝘂𝗸𝘁𝗮 𝗱𝗮𝗵𝗮 𝗳𝗮𝘇𝗹𝗮 𝗺𝘂̈𝘇𝗶𝗸 𝘆𝗼𝗸", show_alert=True
            )
            return
        else:
            videoid = Queues.get(chat_id)["file"]
            got_queue = get_queue.get(CallbackQuery.message.chat.id)
            if got_queue:
                got_queue.pop(0)
            finxx = f"{videoid[0]}{videoid[1]}{videoid[2]}"
            aud = 0
            if str(finxx) == "raw":
                await CallbackQuery.message.delete()
                await CallbackQuery.answer("Skipped!", show_alert=True)
                await skip_stream(chat_id, videoid)
                afk = videoid
                title = db_mem[videoid]["title"]
                duration_min = db_mem[videoid]["duration"]
                duration_sec = int(time_to_seconds(duration_min))
                mention = db_mem[videoid]["username"]
                videoid = db_mem[videoid]["videoid"]
                if str(videoid) == "smex1":
                    buttons = buttons = audio_markup(
                        videoid,
                        CallbackQuery.from_user.id,
                        duration_min,
                        duration_min,
                    )
                    thumb = "Utils/Telegram.JPEG"
                    aud = 1
                else:
                    _path_ = _path_ = (
                        (str(afk))
                        .replace("_", "", 1)
                        .replace("/", "", 1)
                        .replace(".", "", 1)
                    )
                    thumb = f"cache/{_path_}final.png"
                    buttons = primary_markup(
                        videoid,
                        CallbackQuery.from_user.id,
                        duration_min,
                        duration_min,
                    )
                final_output = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"<b>__𝗔𝘁𝗹𝗮𝗻𝗮𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁__</b>\n│\n╰🎥<b>__𝗢𝘆𝗮𝗻𝘁𝗺𝗮𝘆𝗮 𝗕𝗮𝘀̧𝗹𝗮𝗱𝗶:__</b> {title} \n│\n╰⏳<b>__𝗦𝘂̈𝗿𝗲:__</b> {duration_min} \n│\n╰☑️<b>__𝗧𝗮𝗹𝗲𝗽 𝗲𝗱𝗲𝗻:__ </b> {mention}",
                )
                await start_timer(
                    videoid,
                    duration_min,
                    duration_sec,
                    final_output,
                    CallbackQuery.message.chat.id,
                    CallbackQuery.message.from_user.id,
                    aud,
                )
            if str(finxx) == "s1s":
                afk = videoid
                await CallbackQuery.answer()
                mystic = await CallbackQuery.message.reply_text(
                    "𝗔𝘁𝗹𝗮𝗻𝗱𝗶! 𝗟𝘂̈𝘁𝗳𝗲𝗻 𝗩𝗶𝗱𝗲𝗼 𝗔𝗸𝗶𝘀̧𝗶𝗻𝗶 𝗗𝗲𝗴̆𝗶𝘀̧𝘁𝗶𝗿𝗺𝗲𝘆𝗶 𝗕𝗲𝗸𝗹𝗲𝘆𝗶𝗻...."
                )
                read = (str(videoid)).replace("s1s_", "", 1)
                s = read.split("_+_")
                quality = s[0]
                videoid = s[1]
                if int(quality) == 1080:
                    try:
                        await skip_video_stream(chat_id, videoid, 720, mystic)
                    except Exception as e:
                        return await mystic.edit(
                            f"𝗩𝗶𝗱𝗲𝗼 𝗮𝗸𝗶𝘀̧𝗶𝗻𝗶 𝗱𝗲𝗴̆𝗶𝘀̧𝘁𝗶𝗿𝗶𝗿𝗸𝗲𝗻 𝗵𝗮𝘁𝗮 𝗼𝗹𝘂𝘀̧𝘁𝘂.\n│\n╰𝗢𝗹𝗮𝘀𝗶 𝗦𝗲𝗯𝗲𝗽:- {e}"
                        )
                    buttons = secondary_markup2(
                        "Smex1", CallbackQuery.from_user.id
                    )
                    mention = db_mem[afk]["username"]
                    await mystic.delete()
                    final_output = await CallbackQuery.message.reply_photo(
                        photo="Utils/Telegram.JPEG",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=(
                            f"<b>__𝗔𝘁𝗹𝗮𝗻𝗮𝗻 𝗚𝗼̈𝗿𝘂̈𝗻𝘁𝘂̈𝗹𝘂̈ 𝗦𝗼𝗵𝗯𝗲𝘁__</b>\n│\n╰☑️**𝗧𝗮𝗹𝗲𝗽 𝗲𝗱𝗲𝗻:** {mention}"
                        ),
                    )
                    await mystic.delete()
                else:
                    (
                        title,
                        duration_min,
                        duration_sec,
                        thumbnail,
                    ) = get_yt_info_id(videoid)
                    nrs, ytlink = await get_m3u8(videoid)
                    if nrs == 0:
                        return await mystic.edit(
                            "𝗩𝗶𝗱𝗲𝗼 𝗕𝗶𝗰̧𝗶𝗺𝗹𝗲𝗿𝗶 𝗴𝗲𝘁𝗶𝗿𝗶𝗹𝗲𝗺𝗲𝗱𝗶.",
                        )
                    try:
                        await skip_video_stream(
                            chat_id, ytlink, quality, mystic
                        )
                    except Exception as e:
                        return await mystic.edit(
                            f"𝗩𝗶𝗱𝗲𝗼 𝗮𝗸𝗶𝘀̧𝗶𝗻𝗶 𝗱𝗲𝗴̆𝗶𝘀̧𝘁𝗶𝗿𝗶𝗿𝗸𝗲𝗻 𝗵𝗮𝘁𝗮 𝗼𝗹𝘂𝘀̧𝘁𝘂.\n│\n╰╰𝗢𝗹𝗮𝘀𝗶 𝗦𝗲𝗯𝗲𝗽:- {e}"
                        )
                    theme = await check_theme(chat_id)
                    c_title = CallbackQuery.message.chat.title
                    user_id = db_mem[afk]["user_id"]
                    chat_title = await specialfont_to_normal(c_title)
                    thumb = await gen_thumb(
                        thumbnail, title, user_id, theme, chat_title
                    )
                    buttons = primary_markup(
                        videoid, user_id, duration_min, duration_min
                    )
                    mention = db_mem[afk]["username"]
                    await mystic.delete()
                    final_output = await CallbackQuery.message.reply_photo(
                        photo=thumb,
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=(
                            f"<b>__𝗔𝘁𝗹𝗮𝗻𝗮𝗻 𝗚𝗼̈𝗿𝘂̈𝗻𝘁𝘂̈𝗹𝘂̈ 𝗦𝗼𝗵𝗯𝗲𝘁__</b>\n│\n╰🎥<b>__𝗩𝗶𝗱𝗲𝗼 𝗢𝘆𝗻𝗮𝘁𝗺𝗮𝘆𝗮 𝗕𝗮𝘀̧𝗹𝗮𝗱𝗶:__ </b>[{title[:25]}](https://www.youtube.com/watch?v={videoid}) \n│\n╰☑️**__𝗧𝗮𝗹𝗲𝗽 𝗲𝗱𝗲𝗻:__** {mention}"
                        ),
                    )
                    os.remove(thumb)
                    await start_timer(
                        videoid,
                        duration_min,
                        duration_sec,
                        final_output,
                        CallbackQuery.message.chat.id,
                        CallbackQuery.message.from_user.id,
                        aud,
                    )
            else:
                await CallbackQuery.message.delete()
                await CallbackQuery.answer(
                    "𝗔𝘁𝗹𝗮𝘁𝗶𝗹𝗱𝗶! 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶 𝗖̧𝗮𝗹𝗺𝗮....", show_alert=True
                )
                mystic = await CallbackQuery.message.reply_text(
                    f"**{MUSIC_BOT_NAME} 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶 𝗜̇𝘀̧𝗹𝗲𝘃𝗶**\n│\n╰__𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗱𝗲𝗻 𝗦𝗼𝗻𝗿𝗮𝗸𝗶 𝗠𝘂̈𝘇𝗶𝗸𝗹𝗲𝗿𝗶 𝗜̇𝗻𝗱𝗶𝗿𝗺𝗲....__\n│\n╰𝗞𝘂𝗹𝗹𝗮𝗻𝗮𝗻 𝗞𝗶𝘀̧𝗶 :- {CallbackQuery.from_user.mention}"
                )
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                ) = get_yt_info_id(videoid)
                await mystic.edit(
                    f"**{MUSIC_BOT_NAME} 𝗜̇𝗡𝗗𝗜̇𝗥𝗜̇𝗖𝗜̇**\n│\n╰**𝗜̇𝘀𝗶𝗺:** {title[:50]}\n│\n╰0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%"
                )
                downloaded_file = await loop.run_in_executor(
                    None, download, videoid, mystic, title
                )
                raw_path = await convert(downloaded_file)
                await skip_stream(chat_id, raw_path)
                theme = await check_theme(chat_id)
                chat_title = await specialfont_to_normal(
                    CallbackQuery.message.chat.title
                )
                thumb = await gen_thumb(
                    thumbnail,
                    title,
                    CallbackQuery.from_user.id,
                    theme,
                    chat_title,
                )
                buttons = primary_markup(
                    videoid,
                    CallbackQuery.from_user.id,
                    duration_min,
                    duration_min,
                )
                await mystic.delete()
                mention = db_mem[videoid]["username"]
                final_output = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=(
                        f"<b>__𝗔𝘁𝗹𝗮𝗻𝗮𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁__</b>\n│\n╰🎥<b>__𝗢𝘆𝗻𝗮𝘁𝗺𝗮𝘆𝗮 𝗕𝗮𝘀̧𝗹𝗮𝗱𝗶:__ </b>[{title[:25]}](https://www.youtube.com/watch?v={videoid}) \n│\n╰⏳<b>__𝗦𝘂̈𝗿𝗲:__</b> {duration_min} 𝗗𝗮𝗸𝗶𝗸𝗮\n│\n╰☑️**__𝗧𝗮𝗹𝗲𝗽 𝗘𝗱𝗲𝗻:__** {mention}"
                    ),
                )
                os.remove(thumb)
                await start_timer(
                    videoid,
                    duration_min,
                    duration_sec,
                    final_output,
                    CallbackQuery.message.chat.id,
                    CallbackQuery.message.from_user.id,
                    aud,
                )


@app.on_callback_query(filters.regex("play_playlist"))
async def play_playlist(_, CallbackQuery):
    global get_queue
    loop = asyncio.get_event_loop()
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    user_id, smex, type = callback_request.split("|")
    chat_title = CallbackQuery.message.chat.title
    user_id = int(user_id)
    if chat_id not in db_mem:
        db_mem[chat_id] = {}
    if smex == "third":
        _playlist = await get_playlist_names(user_id, type)
        try:
            user = await app.get_users(user_id)
            third_name = user.first_name
        except:
            third_name = "Deleted Account"
    elif smex == "Personal":
        if CallbackQuery.from_user.id != int(user_id):
            return await CallbackQuery.answer(
                "𝗕𝘂 𝘀𝗲𝗻𝗶𝗻 𝗶𝗰̧𝗶𝗻 𝗱𝗲𝗴̆𝗶𝗹 𝗗𝗼𝘀𝘁𝘂𝗺! 𝗞𝗲𝗻𝗱𝗶 𝗰̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝗻𝗶𝘇𝗶 𝗼𝘆𝗻𝗮𝘁", show_alert=True
            )
        _playlist = await get_playlist_names(user_id, type)
        third_name = CallbackQuery.from_user.first_name
    elif smex == "Group":
        _playlist = await get_playlist_names(
            CallbackQuery.message.chat.id, type
        )
        user_id = CallbackQuery.message.chat.id
        third_name = chat_title
    else:
        return await CallbackQuery.answer("𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗱𝗲 𝗛𝗮𝘁𝗮.")
    if CallbackQuery.message.chat.id not in db_mem:
        db_mem[CallbackQuery.message.chat.id] = {}
    try:
        read1 = db_mem[CallbackQuery.message.chat.id]["live_check"]
        if read1:
            return await CallbackQuery.answer(
                "𝗖𝗮𝗻𝗹𝗶 𝗬𝗮𝘆𝗶𝗻 𝗢𝘆𝗻𝗮𝘁𝗶𝗹𝗶𝘆𝗼𝗿... 𝗖̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶 𝗶𝗰̧𝗶𝗻 𝗱𝘂𝗿𝗱𝘂𝗿",
                show_alert=True,
            )
        else:
            pass
    except:
        pass
    if not _playlist:
        return await CallbackQuery.answer(
            f"𝗕𝘂 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗰𝗶𝗻𝗶𝗻 𝘀𝘂𝗻𝘂𝗰𝘂𝗹𝗮𝗿𝗱𝗮 𝗰̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶 𝘆𝗼𝗸.", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()
        mystic = await CallbackQuery.message.reply_text(
            f"𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶 𝗕𝗮𝘀̧𝗹𝗮𝘁𝗶𝗹𝗶𝘆𝗼𝗿 {third_name}.\n│\n╰𝗜̇𝘀𝘁𝗲𝘆𝗲𝗻:- {CallbackQuery.from_user.first_name}"
        )
        msg = f"Sıraya Alınan Çalma Listesi:\n\n"
        j = 0
        for_t = 0
        for_p = 0
        for shikhar in _playlist:
            _note = await get_playlist(user_id, shikhar, type)
            title = _note["title"]
            videoid = _note["videoid"]
            url = f"https://www.youtube.com/watch?v={videoid}"
            duration = _note["duration"]
            if await is_active_chat(chat_id):
                position = await Queues.put(chat_id, file=videoid)
                j += 1
                for_p = 1
                msg += f"{j}- {title[:50]}\n"
                msg += f"Kuyruğa Atılmış Konum- {position}\n\n"
                if videoid not in db_mem:
                    db_mem[videoid] = {}
                db_mem[videoid]["username"] = CallbackQuery.from_user.mention
                db_mem[videoid]["chat_title"] = chat_title
                db_mem[videoid]["user_id"] = user_id
                got_queue = get_queue.get(CallbackQuery.message.chat.id)
                title = title
                user = CallbackQuery.from_user.first_name
                duration = duration
                to_append = [title, user, duration]
                got_queue.append(to_append)
            else:
                loop = asyncio.get_event_loop()
                send_video = videoid
                for_t = 1
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                ) = get_yt_info_id(videoid)
                mystic = await mystic.edit(
                    f"**{MUSIC_BOT_NAME} 𝗜̇𝗡𝗗𝗜̇𝗥𝗜̇𝗖𝗜̇**\n│\n╰**𝗜̇𝘀𝗶𝗺:** {title[:50]}\n│\n╰0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%"
                )
                downloaded_file = await loop.run_in_executor(
                    None, download, videoid, mystic, title
                )
                raw_path = await convert(downloaded_file)
                if not await join_stream(chat_id, raw_path):
                    return await mystic.edit(
                        "𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁𝗲 𝗞𝗮𝘁𝗶𝗹𝗺𝗮 𝗛𝗮𝘁𝗮𝘀𝗶. 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁'𝗶𝗻 𝗘𝘁𝗸𝗶𝗻 𝗼𝗹𝗱𝘂𝗴̆𝘂𝗻𝗱𝗮𝗻 𝗲𝗺𝗶𝗻 𝗼𝗹𝘂𝗻."
                    )
                theme = await check_theme(chat_id)
                chat_title = await specialfont_to_normal(chat_title)
                thumb = await gen_thumb(
                    thumbnail,
                    title,
                    CallbackQuery.from_user.id,
                    theme,
                    chat_title,
                )
                buttons = primary_markup(
                    videoid,
                    CallbackQuery.from_user.id,
                    duration_min,
                    duration_min,
                )
                await mystic.delete()
                get_queue[CallbackQuery.message.chat.id] = []
                got_queue = get_queue.get(CallbackQuery.message.chat.id)
                title = title
                user = CallbackQuery.from_user.first_name
                duration = duration_min
                to_append = [title, user, duration]
                got_queue.append(to_append)
                await music_on(chat_id)
                await add_active_chat(chat_id)
                cap = f"🎥<b>__𝗢𝘆𝗻𝗮𝘁𝗶𝗹𝗮𝗻:__ </b>[{title[:25]}](https://www.youtube.com/watch?v={videoid}) \n│\n╰💡<b>__𝗕𝗶𝗹𝗴𝗶:__</b> [Ek Bilgi Al](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n│\n╰☑️**__𝗧𝗮𝗹𝗲𝗽 𝗲𝗱𝗲𝗻:__** {CallbackQuery.from_user.mention}"
                final_output = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=cap,
                )
                os.remove(thumb)
        await mystic.delete()
        if for_p == 1:
            m = await CallbackQuery.message.reply_text(
                "𝗦𝗶𝗿𝗮𝘆𝗮 𝗔𝗹𝗶𝗻𝗮𝗻 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗶 𝗗𝗲𝗽𝗼 𝗚𝗼̈𝘇𝘂̈𝗻𝗲 𝗬𝗮𝗽𝗶𝘀̧𝘁𝗶𝗿𝗺𝗮"
            )
            link = await paste_queue(msg)
            preview = link + "/preview.png"
            url = link + "/index.txt"
            buttons = paste_queue_markup(url)
            if await isPreviewUp(preview):
                await CallbackQuery.message.reply_photo(
                    photo=preview,
                    caption=f"𝗕𝘂 {third_name} 𝗢̈𝗴̆𝗲𝘀𝗶𝗻𝗶𝗻 𝗦𝗶𝗿𝗮𝘆𝗮 𝗔𝗹𝗶𝗻𝗺𝗶𝘀̧ 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶𝗱𝗶𝗿..\n│\n╰𝗧𝗮𝗹𝗲𝗽 𝗲𝗱𝗲𝗻 :- {CallbackQuery.from_user.mention}",
                    quote=False,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                await m.delete()
            else:
                await CallbackQuery.message.reply_text(
                    text=msg, reply_markup=audio_markup2
                )
                await m.delete()
        else:
            await CallbackQuery.message.reply_text(
                "𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗱𝗲 𝗦𝗮𝗱𝗲𝗰𝗲 𝟭 𝗠𝘂̈𝘇𝗶𝗸.. 𝗞𝘂𝘆𝗿𝘂𝗴̆𝗮 𝗲𝗸𝗹𝗲𝗻𝗲𝗰𝗲𝗸 𝗺𝘂̈𝘇𝗶𝗸 𝘆𝗼𝗸."
            )
        if for_t == 1:
            await start_timer(
                send_video,
                duration_min,
                duration_sec,
                final_output,
                CallbackQuery.message.chat.id,
                CallbackQuery.message.from_user.id,
                0,
            )


@app.on_callback_query(filters.regex("add_playlist"))
async def group_playlist(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, type, genre = callback_request.split("|")
    if type == "Personal":
        user_id = CallbackQuery.from_user.id
    elif type == "Group":
        a = await app.get_chat_member(
            CallbackQuery.message.chat.id, CallbackQuery.from_user.id
        )
        if not a.can_manage_voice_chats:
            return await CallbackQuery.answer(
                "Bu eylemi gerçekleştirmek için gerekli izniniz yok.\n│\n╰Gerekli izin: SESLİ SOHBETLERİ YÖNETME",
                show_alert=True,
            )
        user_id = CallbackQuery.message.chat.id
    _count = await get_playlist_names(user_id, genre)
    if not _count:
        sex = await CallbackQuery.message.reply_text(
            f"Welcome To {MUSIC_BOT_NAME}'s Çalma Listesi Özelliği.\n│\n╰Veritabanında Çalma Listeniz Oluşturuluyor... Lütfen bekleyin.\n│\n╰Tarz:- {genre}"
        )
        await asyncio.sleep(2)
        await sex.delete()
        count = len(_count)
    else:
        count = len(_count)
    count = int(count)
    if count == 50:
        return await CallbackQuery.answer(
            "Pardon! Bir çalma listesinde yalnızca 50 müzik olabilir.",
            show_alert=True,
        )
    loop = asyncio.get_event_loop()
    await CallbackQuery.answer()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    _check = await get_playlist(user_id, videoid, genre)
    title = title[:50]
    if _check:
        return await CallbackQuery.message.reply_text(
            f"{CallbackQuery.from_user.mention}, Zaten Çalma Listesinde!"
        )
    assis = {
        "videoid": videoid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(user_id, videoid, assis, genre)
    Name = CallbackQuery.from_user.first_name
    return await CallbackQuery.message.reply_text(
        f"Eklenen {type}'s {genre} Çalma listesi: {CallbackQuery.from_user.mention}"
    )


@app.on_callback_query(filters.regex("check_playlist"))
async def check_playlist(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    type, genre = callback_request.split("|")
    if type == "Personal":
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
    elif type == "Group":
        user_id = CallbackQuery.message.chat.id
        user_name = CallbackQuery.message.chat.title
    _playlist = await get_playlist_names(user_id, genre)
    if not _playlist:
        return await CallbackQuery.answer(
            f"Hayır {genre} Sunucularda çalma listesi. Çalma listesine müzik eklemeyi deneyin.",
            show_alert=True,
        )
    else:
        j = 0
        await CallbackQuery.answer()
        await CallbackQuery.message.delete()
        msg = f"Getirilen Çalma Listesi:\n\n"
        for shikhar in _playlist:
            j += 1
            _note = await get_playlist(user_id, shikhar, genre)
            title = _note["title"]
            duration = _note["duration"]
            msg += f"{j}- {title[:60]}\n"
            msg += f"    Duration- {duration} Min(s)\n\n"
        m = await CallbackQuery.message.reply_text("Çalma Listesini Depo Gözüne Yapıştırma")
        link = await paste_queue(msg)
        preview = link + "/preview.png"
        url = link + "/index.txt"
        buttons = fetch_playlist(
            user_name, type, genre, CallbackQuery.from_user.id, url
        )
        if await isPreviewUp(preview):
            await CallbackQuery.message.reply_photo(
                photo=preview,
                caption=f"Bu çalma listesidir {user_name}.",
                quote=False,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            await m.delete()
        else:
            await CallbackQuery.message.reply_text(
                text=msg, reply_markup=audio_markup2
            )
            await m.delete()


@app.on_callback_query(filters.regex("delete_playlist"))
async def del_playlist(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    type, genre = callback_request.split("|")
    if str(type) == "Personal":
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
    elif str(type) == "Group":
        a = await app.get_chat_member(
            CallbackQuery.message.chat.id, CallbackQuery.from_user.id
        )
        if not a.can_manage_voice_chats:
            return await CallbackQuery.answer(
                "Bu eylemi gerçekleştirmek için gerekli izniniz yok.\n│\n╰Gerekli izin: SESLİ SOHBETLERİ YÖNETME",
                show_alert=True,
            )
        user_id = CallbackQuery.message.chat.id
        user_name = CallbackQuery.message.chat.title
    _playlist = await get_playlist_names(user_id, genre)
    if not _playlist:
        return await CallbackQuery.answer(
            "Grup Botun Sunucusunda Çalma Listesi yok", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
        for shikhar in _playlist:
            await delete_playlist(user_id, shikhar, genre)
    await CallbackQuery.message.reply_text(
        f"Başarıyla silindi {type}'s {genre} tüm çalma listesi\n│\n╰Tarafından Talep Eden :- {CallbackQuery.from_user.mention}"
    )


@app.on_callback_query(filters.regex("audio_video_download"))
async def down_playlisyts(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = download_markup(videoid, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"good"))
async def good(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = download_markup(videoid, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )
