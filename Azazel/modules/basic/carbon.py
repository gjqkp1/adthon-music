
import asyncio
from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message
from . import *
from Azazel import aiosession
from ubotlibs.ubot.helper.PyroHelpers import ReplyCheck


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@Ubot(["carbon"], "كربون")
async def carbon_func(client: Client, message: Message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ex = await message.reply("`تحضير الكربون . . .`")
    carbon = await make_carbon(text)
    await ex.edit("`يتم الرفع . . .`")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"**Carbonised by** {client.me.mention}",
            reply_to_message_id=ReplyCheck(message),
        ),
    )
    carbon.close()


add_command_help(
    "كربزن",
    [
        [f"carbon او كربون <بالرد>", ".ينشئ صورة كربونية"],
    ],
)