from pyrogram import filters
from pyrogram.types import Message
from vcbot import app
from helpers import download_song, run_async


def to_seconds(duration : str):
    d = duration.split(":")
    min = int(d[1])
    sec = int(d[2])
    return int(min*60 + sec)


def progress(current, total):
    print(f"{current * 100 / total:.1f}%")


@app.on_message(filters.command('song'))
async def download(client, message : Message):
    msg = await message.reply("Processing...")
    try:
        link = message.command[1]
    except:
        await msg.edit("Give a link of a song")
        return

    await msg.edit("Downloading...")
    path, thum_path, title, length, cap = await run_async(download_song, link, message)

    # def progress_pyro(current, total, width=80):
    #     progress_msg = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    #     asyncio.ensure_future(msg.edit(progress_msg))
    #     asyncio.sleep(1)

    # def progress(current, total):
    #     try:
    #         asyncio.ensure_future(msg.edit(f"Uploading : {current * 100 / total:.1f}%"))
    #     except:
    #         print("Fload Wait")

    
    await msg.edit("Uploading...")
    await app.send_audio(message.chat.id, path, 
                        caption=cap, 
                        thumb=thum_path, 
                        title=title,
                        duration=to_seconds(length))
    await msg.delete()

def bar_custom(current, total, width=80):
    percentage = current/total * 100

