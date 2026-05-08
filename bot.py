from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 39188641
API_HASH = "5197eef07d0ae6434711d49219739aaa"
BOT_TOKEN = "8549703368:AAGvs6DGowwCaKTQv-ohGH4s3RN2y_9GT_w"
BOT_USERNAME = "Allmoviex_bot"
CHANNEL_ID = -1003954020823

bot = Client(
    "AnishDeepLinkBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Search in Group
@bot.on_message(filters.group & filters.text)
async def search_files(client, message):
    query = message.text

    found = False

    async for msg in bot.search_messages(CHANNEL_ID, query=query, limit=5):
        found = True

        file_id = msg.document.file_id if msg.document else msg.video.file_id
        file_name = msg.document.file_name if msg.document else msg.video.file_name

        deep_link = f"https://t.me/{BOT_USERNAME}?start={file_id}"

        await message.reply_text(
            f"📁 {file_name}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📥 Get File", url=deep_link)]]
            )
        )

    if not found:
        await message.reply_text("❌ File not found")


# Start Command
@bot.on_message(filters.private & filters.command("start"))
async def start_command(client, message):

    if len(message.command) > 1:
        file_id = message.command[1]

        try:
            await client.send_cached_media(
                chat_id=message.chat.id,
                file_id=file_id,
                caption="📥 Here is your file"
            )

        except Exception as e:
            await message.reply_text(str(e))

    else:
        await message.reply_text(
            "👋 Welcome to Anish Auto Filter Bot\n\nSend movie name in group to get files."
        )


bot.run()
