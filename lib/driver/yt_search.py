import os

from yt_dlp import YoutubeDL
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from lib.helpers.decorators import blacklist_users


@Client.on_message(filters.command("search"))
@blacklist_users
async def ytsearch(client, message):
    try:
        if len(message.command) <2:
            await message.reply("Give me some title")
            return
        query = " ".join(message.command[1:])
        msg = await message.reply("`searching...`")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
        except:
            await msg.edit("Give me something to play")
        try:
            toxxt = "**Select the song you want to play**\n\n"
            j = 0
            useer = user_name
            emojilist = [
                "1️⃣",
                "2️⃣",
                "3️⃣",
                "4️⃣",
                "5️⃣",
            ]

            while j < 5:
                toxxt += f"{emojilist[j]} <b>Title - [{results[j]['title']}](https://youtube.com{results[j]['url_suffix']})</b>\n"
                toxxt += f" ╚ <b>Duration</b> - {results[j]['duration']}\n"
                toxxt += f" ╚ <b>Views</b> - {results[j]['views']}\n"
                toxxt += f" ╚ <b>Channel</b> - {results[j]['channel']}\n\n"

                j += 1
            koyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "1️⃣", callback_data=f"plll 0|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "2️⃣", callback_data=f"plll 1|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "3️⃣", callback_data=f"plll 2|{query}|{user_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "4️⃣", callback_data=f"plll 3|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "5️⃣", callback_data=f"plll 4|{query}|{user_id}"
                        ),
                    ],
                    [InlineKeyboardButton(text="❌ Close", callback_data="cls")],
                ]
            )
            await msg.edit(toxxt, reply_markup=koyboard, disable_web_page_preview=True)
    except Exception as e:
        await message.reply(e)


@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def youtube_cb(b, cb):
    cbd = cb.data.strip()
    chat_id = cb.message.chat.id
    typed_ = cbd.split(None, 1)[1]
    try:
        x, query, useer_id = typed_.split("|")
    except:
        await cb.message.edit("Song Not Found")
        return
    useer_id = int(useer_id)
    if cb.from_user.id != useer_id:
        await cb.answer(
            "You ain't the person who requested to play the song!", show_alert=True
        )
        return
    await cb.message.edit("`Downloading...`")
    x = int(x)
    results = YoutubeSearch(query, max_results=5).to_dict()
    resultss = results[x]["url_suffix"]
    title = results[x]["title"][:40]
    thumbnail = results[x]["thumbnails"][0]
    duration = results[x]["duration"]
    views = results[x]["views"]
    url = f"https://youtube.com{resultss}"
    try:
       preview = wget.download(thumbnail)
    except BaseException:
       pass
    with YoutubeDL(ydl_opts) as ydl:
       info_dict = ydl.extract_info(url, download=False)
       audio_file = ydl.prepare_filename(info_dict)
       ydl.process_info(info_dict)
    await cb.message.edit("`Uploading to telegram server...`")
    await b.message.reply_audio(
        audio_file,
        thumb=preview,
        duration=int(info_dict["duration"]),
        caption=info_dict['title'])
    )
    try:
       os.remove(audio_file)
       os.remove(preview)
       await cb.message.delete()
    except BaseException:
       pass
