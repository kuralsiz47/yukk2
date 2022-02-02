from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            KeyboardButton, Message, ReplyKeyboardMarkup,
                            ReplyKeyboardRemove)

from Yukki import BOT_ID, BOT_USERNAME, MUSIC_BOT_NAME, SUDOERS, app, db_mem
from Yukki.Database import (_get_playlists, delete_playlist, get_playlist,
                            get_playlist_names, save_playlist)
from Yukki.Decorators.admins import AdminRightsCheck
from Yukki.Decorators.assistant import AssistantAdd
from Yukki.Decorators.checker import checker, checkerCB
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (add_genre_markup, check_genre_markup, check_markup,
                          delete_playlist_markuup, download_markup,
                          others_markup, play_genre_playlist, playlist_markup,
                          third_playlist_markup)

__MODULE__ = "Çalma listesi"
__HELP__ = """


/playplaylist 
- Kaydedilmiş Çalma Listenizi oynatmaya başlayın.


/playlist 
- Sunucularda Kayıtlı Çalma Listenizi Denetleme.


/delmyplaylist
- Çalma listenizdeki kaydedilmiş müzikleri silme


/delgroupplaylist
- Grubunuzun çalma listesindeki kaydedilmiş müzikleri silme [Yönetici Hakları Gerektirir.]
"""


@app.on_message(filters.command("playplaylist") & filters.group)
@checker
@PermissionCheck
@AssistantAdd
async def play_playlist_cmd(_, message):
    thumb = "Utils/Playlist.jpg"
    await message.delete()
    if not message.reply_to_message:
        if len(message.command) == 2:
            user = message.text.split(None, 2)[1]
            if "@" in user:
                user = user.replace("@", "")
            try:
                user = int(user)
                try:
                    user = await app.get_users(user)
                    userid = user.id
                    third_name = user.first_name
                except:
                    userid = user
                    third_name = "Silinen Hesap"
            except:
                try:
                    user = await app.get_users(user)
                    userid = user.id
                    third_name = user.first_name
                except Exception as e:
                    return await message.reply_text("User not found")
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            buttons = third_playlist_markup(
                user_name, user_id, third_name, userid, "abcd"
            )
            hmo = await message.reply_photo(
                photo=thumb,
                caption=(
                    f"**{MUSIC_BOT_NAME}'𝘀 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶 𝗢̈𝘇𝗲𝗹𝗹𝗶𝗴̆𝗶**\n│\n╰𝗢𝘆𝗻𝗮𝘁𝗺𝗮𝗸 𝗶𝘀𝘁𝗲𝗱𝗶𝗴̆𝗶𝗻𝗶𝘇 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗶 𝘀𝗲𝗰̧𝗶𝗻!.\n│\n╰𝗕𝗮𝘀̧𝗸𝗮 𝗯𝗶𝗿𝗶𝗻𝗶𝗻 𝗰̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗶 𝗱𝗲 𝗰̧𝗮𝗹𝗮𝗯𝗶𝗹𝗶𝗿𝘀𝗶𝗻𝗶𝘇:-\n│\n╰- /playplaylist [KullanıcıAdı]\n│\n╰- /playplaylist [KULLANICI ID](kullanıcı acc'yi sildiyse)\n│\n╰- /playplaylist [Kullanıcıyı Yanıtlama]"
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
        else:
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            buttons = playlist_markup(user_name, user_id, "abcd")
            await message.reply_photo(
                photo=thumb,
                caption=(
                    f"**{MUSIC_BOT_NAME}'𝘀 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶 𝗢̈𝘇𝗲𝗹𝗹𝗶𝗴̆𝗶**\n│\n╰𝗢𝘆𝗻𝗮𝘁𝗺𝗮𝗸 𝗶𝘀𝘁𝗲𝗱𝗶𝗴̆𝗶𝗻𝗶𝘇 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗶 𝘀𝗲𝗰̧𝗶𝗻!.\n│\n╰𝗕𝗮𝘀̧𝗸𝗮 𝗯𝗶𝗿𝗶𝗻𝗶𝗻 𝗰̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗶 𝗱𝗲 𝗰̧𝗮𝗹𝗮𝗯𝗶𝗹𝗶𝗿𝘀𝗶𝗻𝗶𝘇:-\n│\n╰- /playplaylist [KullanıcıAdı]\n│\n╰- /playplaylist [KULLANICI ID](kullanıcı acc'yi sildiyse)\n│\n╰- /playplaylist [Kullanıcıyı Yanıtlama]"
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return
    else:
        userid = message.reply_to_message.from_user.id
        third_name = message.reply_to_message.from_user.first_name
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        buttons = third_playlist_markup(
            user_name, user_id, third_name, userid, "abcd"
        )
        hmo = await message.reply_photo(
            photo=thumb,
            caption=(
                f"**{MUSIC_BOT_NAME}'𝘀 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶 𝗢̈𝘇𝗲𝗹𝗹𝗶𝗴̆𝗶**\n│\n╰𝗢𝘆𝗻𝗮𝘁𝗺𝗮𝗸 𝗶𝘀𝘁𝗲𝗱𝗶𝗴̆𝗶𝗻𝗶𝘇 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗶 𝘀𝗲𝗰̧𝗶𝗻!.\n│\n╰𝗕𝗮𝘀̧𝗸𝗮 𝗯𝗶𝗿𝗶𝗻𝗶𝗻 𝗰̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗶 𝗱𝗲 𝗰̧𝗮𝗹𝗮𝗯𝗶𝗹𝗶𝗿𝘀𝗶𝗻𝗶𝘇:-\n│\n╰- /playplaylist [Kullanıcıadı]\n│\n╰- /playplaylist [KULLANICI ID](kullanıcı acc'yi silmişse)\n│\n╰- /playplaylist [Kullanıcıya Yanıt Ver]"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        return 

@app.on_message(filters.command("playlist") & filters.group) 
@checker
@PermissionCheck
@AssistantAdd
async def playlist(_, message):
    thumb = "Utils/Playlist.jpg"
    user_id = message.from_user.id
    user_name = message.from_user.first_nauser_name = message.from_user.first_name
    buttons = check_markup(user_name, user_id, "abcd")
    await message.reply_photo(
        photo=thumb,
        caption=(
            f"**{MUSIC_BOT_NAME}'𝘀 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶 𝗢̈𝘇𝗲𝗹𝗹𝗶𝗴̆𝗶**\n│\n╰𝗢𝘆𝗻𝗮𝘁𝗺𝗮𝗸 𝗶𝘀𝘁𝗲𝗱𝗶𝗴̆𝗶𝗻𝗶𝘇 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗶 **𝗦𝗲𝗰̧!**"
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return


options = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "all",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
]

options_Genre = [
    "Rock",
    "Sad",
    "Party",
    "Lofi",
    "Bollywood",
    "Hollywood",
    "Punjabi",
    "Others",
]


@app.on_message(filters.command("delmyplaylist") & filters.group)
async def del_cmd(_, message):
    usage = f"𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗺𝗶:\n│\n╰/delmyplaylist [𝗧𝘂̈𝗿] [𝟭-𝟯𝟬 𝗮𝗿𝗮𝘀𝗶 𝘀𝗮𝘆𝗶𝗹𝗮𝗿] ( 𝗖̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗱𝗲𝗸𝗶 𝗯𝗲𝗹𝗶𝗿𝗹𝗶 𝗯𝗶𝗿 𝗺𝘂̈𝘇𝗶𝗴̆𝗶 𝘀𝗶𝗹𝗺𝗲𝗸 𝗶𝗰̧𝗶𝗻 )\n│\n╰𝘃𝗲𝘆𝗮\n│\n╰/delmyplaylist [𝗧𝘂̈𝗿] 𝘁𝘂̈𝗺𝘂̈ ( 𝘁𝘂̈𝗺 𝗰̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗶 𝘀𝗶𝗹𝗺𝗲𝗸 𝗶𝗰̧𝗶𝗻 )\n│\n╰**𝗧𝘂̈𝗿𝗹𝗲𝗿:-**\n{' | '.join(options_Genre)}"
    if len(message.command) < 3:
        return await message.reply_text(usage)
    genre = message.text.split(None, 2)[1].strip()
    count = message.text.split(None, 2)[2].strip()
    if not count:
        return await message.reply_text(usage)
    if count not in options:
        return await message.reply_text(usage)
    if genre not in options_Genre:
        return await message.reply_text(usage)
    if str(count) == "all":
        buttons = delete_playlist_markuup("Personal", genre)
        return await message.reply_text(
            f"𝗢𝗻𝗮𝘆!!\n│\n╰𝗧𝘂̈𝗺𝘂̈𝗻𝘂̈𝘇𝘂̈ 𝘀𝗶𝗹𝗺𝗲𝗸 𝗶𝘀𝘁𝗲𝗱𝗶𝗴̆𝗶𝗻𝗶𝘇𝗱𝗲𝗻 𝗲𝗺𝗶𝗻 𝗺𝗶𝘀𝗶𝗻𝗶𝘇? {genre} 𝗖̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶?",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        _playlist = await get_playlist_names(message.from_user.id, genre)
    if not _playlist:
        await message.reply_text(
            f"𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝗻𝗶 𝗮𝗰̧𝗶𝗸 𝗱𝗲𝗴̆𝗶𝗹 {MUSIC_BOT_NAME}'𝘂𝗻 𝗦𝘂𝗻𝘂𝗰𝘂𝘀𝘂"
        )
    else:
        titlex = []
        j = 0
        count = int(count)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.from_user.id, note, genre)
            if j == count:
                deleted = await delete_playlist(
                    message.from_user.id, note, genre
                )
                if deleted:
                    return await message.reply_text(
                        f"**𝗦𝗶𝗹𝗶𝗻𝗱𝗶. {count} 𝗖̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗱𝗲𝗸𝗶 𝗺𝘂̈𝘇𝗶𝗸**"
                    )
                else:
                    return await message.reply_text(
                        f"**𝗖̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗱𝗲 𝗯𝗼̈𝘆𝗹𝗲 𝗸𝗮𝘆𝗱𝗲𝗱𝗶𝗹𝗺𝗶𝘀̧ 𝗺𝘂̈𝘇𝗶𝗸 𝘆𝗼𝗸.**"
                    )
        await message.reply_text("𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶'𝗻𝗱𝗲 𝗯𝗼̈𝘆𝗹𝗲 𝗯𝗶𝗿 𝗺𝘂̈𝘇𝗶𝗴̆𝗶𝗻𝗶𝘇 𝘆𝗼𝗸.")


@app.on_message(filters.command("delgroupplaylist") & filters.group)
@AdminRightsCheck
async def delgroupplaylist(_, message):
    usage = f"𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗺𝗶:\n│\n╰/delgroupplaylist [𝗧𝘂̈𝗿] [𝟭-𝟯𝟬 𝗮𝗿𝗮𝘀𝗶 𝘀𝗮𝘆𝗶𝗹𝗮𝗿] ( 𝗖̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗱𝗲𝗸𝗶 𝗯𝗲𝗹𝗶𝗿𝗹𝗶 𝗯𝗶𝗿 𝗺𝘂̈𝘇𝗶𝗴̆𝗶 𝘀𝗶𝗹𝗺𝗲𝗸 𝗶𝗰̧𝗶𝗻 )\n│\n╰𝘃𝗲𝘆𝗮\n│\n╰ /delgroupplaylist [𝗧𝘂̈𝗿] 𝘁𝘂̈𝗺𝘂̈ ( 𝘁𝘂̈𝗺 𝗰̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗶 𝘀𝗶𝗹𝗺𝗲𝗸 𝗶𝗰̧𝗶𝗻 )\n│\n╰**𝗧𝘂̈𝗿𝗹𝗲𝗿:-**\n{' | '.join(options_Genre)}"
    if len(message.command) < 3:
        return await message.reply_text(usage)
    genre = message.text.split(None, 2)[1].strip()
    count = message.text.split(None, 2)[2].strip()
    if not count:
        return await message.reply_text(usage)
    if count not in options:
        return await message.reply_text(usage)
    if genre not in options_Genre:
        return await message.reply_text(usage)
    if str(count) == "all":
        buttons = delete_playlist_markuup("Group", genre)
        return await message.reply_text(
            f"𝗢𝗻𝗮𝘆!!\n│\n╰𝗚𝗿𝘂𝗽'𝘂𝗻 𝘁𝗮𝗺𝗮𝗺𝗶𝗻𝗶 𝘀𝗶𝗹𝗺𝗲𝗸 𝗶𝘀𝘁𝗲𝗱𝗶𝗴̆𝗶𝗻𝗶𝘇𝗱𝗲𝗻 𝗲𝗺𝗶𝗻 𝗺𝗶𝘀𝗶𝗻𝗶𝘇? {genre} 𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶?",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        _playlist = await get_playlist_names(message.chat.id, genre)
    if not _playlist:
        await message.reply_text(
            f"𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝗻𝗶 𝗮𝗰̧𝗶𝗸 𝗱𝗲𝗴̆𝗶𝗹 {MUSIC_BOT_NAME}'𝘂𝗻 𝗦𝘂𝗻𝘂𝗰𝘂"
        )
    else:
        titlex = []
        j = 0
        count = int(count)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.chat.id, note, genre)
            if j == count:
                deleted = await delete_playlist(message.chat.id, note, genre)
                if deleted:
                    return await message.reply_text(
                        f"**𝗦𝗶𝗹𝗶𝗻𝗱𝗶. {count} 𝗚𝗿𝘂𝗯𝘂𝗻 𝗰̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗱𝗲𝗸𝗶 𝗺𝘂̈𝘇𝗶𝗸**"
                    )
                else:
                    return await message.reply_text(
                        f"**𝗚𝗿𝘂𝗽 𝗰̧𝗮𝗹𝗺𝗮 𝗹𝗶𝘀𝘁𝗲𝘀𝗶𝗻𝗱𝗲 𝗯𝗼̈𝘆𝗹𝗲 𝗸𝗮𝘆𝗱𝗲𝗱𝗶𝗹𝗺𝗶𝘀̧ 𝗺𝘂̈𝘇𝗶𝗸 𝘆𝗼𝗸.**"
                    )
        await message.reply_text("𝗖̧𝗮𝗹𝗺𝗮 𝗟𝗶𝘀𝘁𝗲𝘀𝗶'𝗻𝗱𝗲 𝗯𝗼̈𝘆𝗹𝗲 𝗯𝗶𝗿 𝗺𝘂̈𝘇𝗶𝗴̆𝗶𝗻𝗶𝘇 𝘆𝗼𝗸.")


@app.on_callback_query(filters.regex(pattern=r"show_genre"))
async def show_genre(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    a, b, c = callback_request.split("|")
    buttons = play_genre_playlist(a, b, "abcd")
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"playlist_check"))
async def playlist_check(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    a, b, c = callback_request.split("|")
    print(b)
    buttons = check_genre_markup(b, "abcd", userid)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"main_playlist"))
async def main_playlist(_, CallbackQuery):
    await CallbackQuery.answer()
    user_id = CallbackQuery.from_user.id
    user_name = CallbackQuery.from_user.first_name
    buttons = playlist_markup(user_name, user_id, "abcd")
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"your_playlist"))
async def your_playlist(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = add_genre_markup(user_id, "Personal", videoid)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"group_playlist"))
async def group_playlist(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = add_genre_markup(user_id, "Group", videoid)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"other"))
async def otherhuvai(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = others_markup(videoid, user_id)
    db_mem[videoid]["check"] = 1
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"goback"))
async def goback(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = others_markup(videoid, user_id)
    try:
        await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        pass
