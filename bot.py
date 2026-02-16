import os
import asyncio
import aiohttp
import aiofiles
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from datetime import datetime
import mimetypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot credentials (use environment variables in production!)
BOT_TOKEN = os.environ.get('BOT_TOKEN', '6120476403:AAGF7I7HWwmkEFIp4V_g3_xfORqUBLyWY5U')

# ========================================
# UPLOAD FUNCTIONS - 20 SITES
# ========================================

async def upload_to_transfersh(file_path, file_name):
    """Transfer.sh - 14 days, unlimited"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = await f.read()
                async with session.put(
                    f'https://transfer.sh/{file_name}',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        return (await response.text()).strip()
    except Exception as e:
        logger.error(f"Transfer.sh error: {e}")
    return None

async def upload_to_0x0(file_path, file_name):
    """0x0.st - 1 year, 512MB"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://0x0.st',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        return (await response.text()).strip()
    except Exception as e:
        logger.error(f"0x0.st error: {e}")
    return None

async def upload_to_catbox(file_path):
    """Catbox.moe - Permanent, 200MB"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('reqtype', 'fileupload')
                data.add_field('fileToUpload', await f.read())
                async with session.post(
                    'https://catbox.moe/user/api.php',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        return (await response.text()).strip()
    except Exception as e:
        logger.error(f"Catbox error: {e}")
    return None

async def upload_to_fileio(file_path):
    """File.io - 1 download, 100MB"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read())
                async with session.post(
                    'https://file.io',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('success'):
                            return result['link']
    except Exception as e:
        logger.error(f"File.io error: {e}")
    return None

async def upload_to_pixeldrain(file_path, file_name):
    """Pixeldrain - Permanent, unlimited"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://pixeldrain.com/api/file/',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        return f"https://pixeldrain.com/u/{result['id']}"
    except Exception as e:
        logger.error(f"Pixeldrain error: {e}")
    return None

async def upload_to_bashupload(file_path, file_name):
    """Bashupload - 3 days"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://bashupload.com',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        text = await response.text()
                        if 'wget' in text:
                            url = text.split('wget ')[1].split()[0]
                            return url.strip()
    except Exception as e:
        logger.error(f"Bashupload error: {e}")
    return None

async def upload_to_tmpfiles(file_path, file_name):
    """Tmpfiles.org - 1 hour to 1 week"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://tmpfiles.org/api/v1/upload',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('status') == 'success':
                            url = result['data']['url']
                            return url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
    except Exception as e:
        logger.error(f"Tmpfiles error: {e}")
    return None

async def upload_to_uguu(file_path, file_name):
    """Uguu.se - 48 hours, 128MB"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('files[]', await f.read(), filename=file_name)
                async with session.post(
                    'https://uguu.se/upload',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('success'):
                            return result['files'][0]['url']
    except Exception as e:
        logger.error(f"Uguu error: {e}")
    return None

async def upload_to_litterbox(file_path, file_name):
    """Litterbox - 1-72 hours, 1GB"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('reqtype', 'fileupload')
                data.add_field('time', '72h')
                data.add_field('fileToUpload', await f.read(), filename=file_name)
                async with session.post(
                    'https://litterbox.catbox.moe/resources/internals/api.php',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        return (await response.text()).strip()
    except Exception as e:
        logger.error(f"Litterbox error: {e}")
    return None

async def upload_to_gofile(file_path, file_name):
    """GoFile.io - Permanent"""
    try:
        async with aiohttp.ClientSession() as session:
            # Get server
            async with session.get('https://api.gofile.io/getServer') as resp:
                if resp.status == 200:
                    server_data = await resp.json()
                    server = server_data['data']['server']
                else:
                    server = 'store1'
            
            # Upload
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    f'https://{server}.gofile.io/uploadFile',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result['status'] == 'ok':
                            return result['data']['downloadPage']
    except Exception as e:
        logger.error(f"GoFile error: {e}")
    return None

async def upload_to_anonfiles(file_path, file_name):
    """Anonfiles - Permanent"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://api.anonfiles.com/upload',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('status'):
                            return result['data']['file']['url']['full']
    except Exception as e:
        logger.error(f"Anonfiles error: {e}")
    return None

async def upload_to_bayfiles(file_path, file_name):
    """Bayfiles - Permanent"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://api.bayfiles.com/upload',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('status'):
                            return result['data']['file']['url']['full']
    except Exception as e:
        logger.error(f"Bayfiles error: {e}")
    return None

async def upload_to_filebin(file_path, file_name):
    """Filebin.net - 1 week"""
    try:
        bin_id = f"bin{datetime.now().strftime('%Y%m%d%H%M%S')}"
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = await f.read()
                async with session.post(
                    f'https://filebin.net/{bin_id}/{file_name}',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 201:
                        return f'https://filebin.net/{bin_id}/{file_name}'
    except Exception as e:
        logger.error(f"Filebin error: {e}")
    return None

async def upload_to_fileditch(file_path, file_name):
    """Fileditch - Permanent"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('files[]', await f.read(), filename=file_name)
                async with session.post(
                    'https://up1.fileditch.com/upload.php',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('files'):
                            return result['files'][0]['url']
    except Exception as e:
        logger.error(f"Fileditch error: {e}")
    return None

async def upload_to_krakenfiles(file_path, file_name):
    """Krakenfiles - Permanent"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://krakenfiles.com/api/server/file/upload',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('status') == 'ok':
                            return result['data']['file']['url']
    except Exception as e:
        logger.error(f"Krakenfiles error: {e}")
    return None

async def upload_to_fileupload(file_path, file_name):
    """File.upload - 30 days"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://www.file-upload.com/upload',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        text = await response.text()
                        if 'download' in text:
                            # Extract download link from HTML
                            return f"Uploaded (check logs)"
    except Exception as e:
        logger.error(f"File-upload error: {e}")
    return None

async def upload_to_x0(file_path, file_name):
    """x0.at - Similar to 0x0.st"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://x0.at',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        return (await response.text()).strip()
    except Exception as e:
        logger.error(f"x0.at error: {e}")
    return None

async def upload_to_uploadfiles(file_path, file_name):
    """UploadFiles.io - 30 days, 5GB"""
    try:
        async with aiohttp.ClientSession() as session:
            # Get upload session
            async with session.post('https://uploadfiles.io/api/v1/file/create_session') as resp:
                if resp.status == 200:
                    session_data = await resp.json()
                    session_id = session_data.get('session_id')
                    
                    if session_id:
                        async with aiofiles.open(file_path, 'rb') as f:
                            data = aiohttp.FormData()
                            data.add_field('file', await f.read(), filename=file_name)
                            data.add_field('session_id', session_id)
                            
                            async with session.post(
                                'https://uploadfiles.io/api/v1/file/upload',
                                data=data,
                                timeout=aiohttp.ClientTimeout(total=600)
                            ) as upload_resp:
                                if upload_resp.status == 200:
                                    result = await upload_resp.json()
                                    if result.get('url'):
                                        return result['url']
    except Exception as e:
        logger.error(f"UploadFiles error: {e}")
    return None

async def upload_to_racaty(file_path, file_name):
    """Racaty - Permanent"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://racaty.io/api/server/file/upload',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('status') == 'ok':
                            return result['data']['file']['url']
    except Exception as e:
        logger.error(f"Racaty error: {e}")
    return None

async def upload_to_sendspace(file_path, file_name):
    """Send.cm - 30 days"""
    try:
        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', await f.read(), filename=file_name)
                async with session.post(
                    'https://send.cm/api/upload',
                    data=data,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('url'):
                            return result['url']
    except Exception as e:
        logger.error(f"Send.cm error: {e}")
    return None

# ========================================
# BOT HANDLERS
# ========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    await update.message.reply_text(
        "🚀 **Multi-Site File Upload Bot**\n\n"
        "📁 Send me any file and I'll upload it to **20 different sites**!\n\n"
        "**Features:**\n"
        "✅ 20 upload mirrors\n"
        "✅ No account needed\n"
        "✅ Fast parallel upload\n"
        "✅ All file types supported\n"
        "✅ Max: 20MB per file\n"
        "✅ 24/7 online\n\n"
        "**Commands:**\n"
        "/start - Show this message\n"
        "/help - Get help\n"
        "/sites - View all 20 sites\n"
        "/stats - Bot statistics\n\n"
        "Just send me a file to get started! 🎯",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📖 **How to Use:**\n\n"
        "**Step 1:** Send any file\n"
        "📄 Documents, 🖼️ Photos, 🎥 Videos, 🎵 Audio\n\n"
        "**Step 2:** Wait for upload\n"
        "⏱️ Usually 30-120 seconds\n\n"
        "**Step 3:** Get 20 download links!\n"
        "🔗 Multiple mirrors for reliability\n\n"
        "**Tips:**\n"
        "💡 Smaller files = Faster upload\n"
        "💡 Use /sites to see all hosting sites\n"
        "💡 Some links expire, others are permanent\n\n"
        "**File Size Limit:** 20MB\n"
        "**Upload Speed:** Depends on file size\n\n"
        "Need more help? Contact @YourSupport",
        parse_mode='Markdown'
    )

async def sites_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all upload sites"""
    sites_text = (
        "🌐 **20 Upload Sites:**\n\n"
        "1️⃣ Transfer.sh - 14 days\n"
        "2️⃣ 0x0.st - 1 year (512MB)\n"
        "3️⃣ Catbox.moe - Permanent (200MB)\n"
        "4️⃣ File.io - 1 download (100MB)\n"
        "5️⃣ Pixeldrain - Permanent\n"
        "6️⃣ Bashupload - 3 days\n"
        "7️⃣ Tmpfiles - 1 week\n"
        "8️⃣ Uguu.se - 48 hours (128MB)\n"
        "9️⃣ Litterbox - 72 hours (1GB)\n"
        "🔟 GoFile.io - Permanent\n\n"
        "1️⃣1️⃣ Anonfiles - Permanent\n"
        "1️⃣2️⃣ Bayfiles - Permanent\n"
        "1️⃣3️⃣ Filebin - 1 week\n"
        "1️⃣4️⃣ Fileditch - Permanent\n"
        "1️⃣5️⃣ Krakenfiles - Permanent\n"
        "1️⃣6️⃣ File-upload - 30 days\n"
        "1️⃣7️⃣ x0.at - 100 days\n"
        "1️⃣8️⃣ UploadFiles - 30 days (5GB)\n"
        "1️⃣9️⃣ Racaty - Permanent\n"
        "2️⃣0️⃣ Send.cm - 30 days\n\n"
        "🎯 **Maximum Availability!**"
    )
    await update.message.reply_text(sites_text, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stats command"""
    await update.message.reply_text(
        "📊 **Bot Statistics:**\n\n"
        f"🤖 Status: ✅ Online (24/7)\n"
        f"🌐 Server: Render.com\n"
        f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}\n\n"
        "📈 **Performance:**\n"
        "🔗 Upload Sites: 20\n"
        "📁 Max File Size: 20MB\n"
        "⚡ Avg Upload Time: 30-120s\n"
        "🔄 Success Rate: ~80-90%\n\n"
        "⚙️ Version: 3.0\n"
        "💻 Framework: python-telegram-bot",
        parse_mode='Markdown'
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all file uploads"""
    
    # Determine file type
    if update.message.document:
        file = update.message.document
        file_name = file.file_name
        file_type = "📄 Document"
    elif update.message.photo:
        file = update.message.photo[-1]
        file_name = f"photo_{file.file_unique_id}.jpg"
        file_type = "🖼️ Photo"
    elif update.message.video:
        file = update.message.video
        file_name = file.file_name or f"video_{file.file_unique_id}.mp4"
        file_type = "🎥 Video"
    elif update.message.audio:
        file = update.message.audio
        file_name = file.file_name or f"audio_{file.file_unique_id}.mp3"
        file_type = "🎵 Audio"
    else:
        return
    
    # Size check
    file_size_mb = file.file_size / (1024 * 1024)
    if file_size_mb > 20:
        await update.message.reply_text(
            f"⚠️ **File Too Large!**\n\n"
            f"Your file: **{file_size_mb:.2f} MB**\n"
            f"Maximum: **20 MB**\n\n"
            f"Please compress or send a smaller file.",
            parse_mode='Markdown'
        )
        return
    
    # Processing message
    processing_msg = await update.message.reply_text(
        f"⏳ **Uploading to 20 sites...**\n\n"
        f"{file_type}\n"
        f"📄 Name: `{file_name}`\n"
        f"📊 Size: **{file_size_mb:.2f} MB**\n\n"
        f"⏱️ Estimated: {int(file_size_mb * 5)}-{int(file_size_mb * 10)} seconds\n"
        f"🔄 Progress: 0%\n\n"
        f"_Please wait, this may take a while..._",
        parse_mode='Markdown'
    )
    
    try:
        # Download from Telegram
        telegram_file = await context.bot.get_file(file.file_id)
        file_path = f"downloads/{file_name}"
        os.makedirs("downloads", exist_ok=True)
        
        await telegram_file.download_to_drive(file_path)
        
        # Update progress
        await processing_msg.edit_text(
            f"⚡ **Uploading to 20 sites...**\n\n"
            f"{file_type}\n"
            f"📄 `{file_name}`\n"
            f"📊 {file_size_mb:.2f} MB\n\n"
            f"🔄 Progress: 10% (Downloaded from Telegram)\n"
            f"⏱️ Now uploading to all servers...",
            parse_mode='Markdown'
        )
        
        # Upload to all 20 sites simultaneously
        upload_tasks = [
            upload_to_transfersh(file_path, file_name),
            upload_to_0x0(file_path, file_name),
            upload_to_catbox(file_path),
            upload_to_fileio(file_path),
            upload_to_pixeldrain(file_path, file_name),
            upload_to_bashupload(file_path, file_name),
            upload_to_tmpfiles(file_path, file_name),
            upload_to_uguu(file_path, file_name),
            upload_to_litterbox(file_path, file_name),
            upload_to_gofile(file_path, file_name),
            upload_to_anonfiles(file_path, file_name),
            upload_to_bayfiles(file_path, file_name),
            upload_to_filebin(file_path, file_name),
            upload_to_fileditch(file_path, file_name),
            upload_to_krakenfiles(file_path, file_name),
            upload_to_fileupload(file_path, file_name),
            upload_to_x0(file_path, file_name),
            upload_to_uploadfiles(file_path, file_name),
            upload_to_racaty(file_path, file_name),
            upload_to_sendspace(file_path, file_name),
        ]
        
        # Wait for all uploads
        results = await asyncio.gather(*upload_tasks, return_exceptions=True)
        
        # Delete local file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Process results
        site_names = [
            "Transfer.sh", "0x0.st", "Catbox", "File.io", "Pixeldrain",
            "Bashupload", "Tmpfiles", "Uguu", "Litterbox", "GoFile",
            "Anonfiles", "Bayfiles", "Filebin", "Fileditch", "Krakenfiles",
            "File-upload", "x0.at", "UploadFiles", "Racaty", "Send.cm"
        ]
        
        links = []
        for i, result in enumerate(results):
            if result and not isinstance(result, Exception) and result != "Uploaded (check logs)":
                links.append(f"🔗 [{site_names[i]}]({result})")
        
        # Send results
        if links:
            # Split into multiple messages if too long
            success_rate = len(links) / 20 * 100
            
            result_text = (
                f"✅ **Upload Complete!**\n\n"
                f"{file_type}\n"
                f"📄 Name: `{file_name}`\n"
                f"📊 Size: {file_size_mb:.2f} MB\n"
                f"🎯 Success: {len(links)}/20 sites ({success_rate:.0f}%)\n\n"
                f"{'═' * 30}\n\n"
                f"**Download Links:**\n\n"
            )
            
            # Add links in batches
            batch_size = 10
            for i in range(0, len(links), batch_size):
                batch = links[i:i+batch_size]
                result_text += "\n".join(batch) + "\n\n"
            
            result_text += (
                f"{'═' * 30}\n\n"
                f"💡 **Tips:**\n"
                f"• Some links expire, others are permanent\n"
                f"• Save multiple links for backup\n"
                f"• Share anywhere you want!\n\n"
                f"⏰ Uploaded: {datetime.now().strftime('%H:%M:%S')}\n"
                f"🚀 Powered by Multi-Upload Bot"
            )
            
            await processing_msg.edit_text(
                result_text,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        else:
            await processing_msg.edit_text(
                "❌ **Upload Failed!**\n\n"
                "All upload sites are currently unavailable.\n"
                "This is rare - please try again in a few minutes.\n\n"
                "If problem persists, contact support.",
                parse_mode='Markdown'
            )
    
    except Exception as e:
        logger.error(f"Error handling file: {e}")
        await processing_msg.edit_text(
            f"❌ **Error Occurred!**\n\n"
            f"Error details: `{str(e)}`\n\n"
            f"Please try again or contact support if this persists.",
            parse_mode='Markdown'
        )

# ========================================
# MAIN FUNCTION
# ========================================

def main():
    """Start the bot"""
    
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found!")
        return
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("sites", sites_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(MessageHandler(
        filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO,
        handle_file
    ))
    
    # Get port
    port = int(os.environ.get('PORT', 8080))
    webhook_url = os.environ.get('RENDER_EXTERNAL_URL', '')
    
    if webhook_url:
        logger.info(f"Starting with webhook on port {port}")
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=BOT_TOKEN,
            webhook_url=f"{webhook_url}/{BOT_TOKEN}"
        )
    else:
        logger.info("Starting with polling (local mode)")
        app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    logger.info("🚀 Bot starting...")
    main()
