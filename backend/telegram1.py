import os
import logging
import asyncio
import aiohttp
import aiofiles
import threading
from datetime import datetime
from pathlib import Path
import random
import string

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# IMPORTANT: Replace with your actual bot token from @BotFather
TELEGRAM_TOKEN = '8103339340:AAGtFb78LdkdvghslKvbxSzn7yvTZD7TBWI'

# IMPORTANT: Replace with your actual database name
MONGO_URL = 'mongodb://localhost:27017'
DB_NAME = 'janta_voice'  # Change this to your actual database name
COLLECTION_NAME = 'complaints'

# Create uploads directory if it doesn't exist
uploads_dir = Path(__file__).parent / 'uploads'
uploads_dir.mkdir(exist_ok=True)

# User sessions storage
user_sessions =  {}

# Question flow
questions = {
    "name": "🙋‍♂ कृपया अपना नाम बताएं:\nPlease provide your name:",
    "location": "📍 शिकायत का स्थान बताएं या location share करें:\nPlease provide location or share location:",
    "department": "🏢 विभाग चुनें:\n1. पब्लिक वर्क्स\n2. जल विभाग\n3. बिजली विभाग\n4. सड़क विभाग\n5. सफाई विभाग\n6. अन्य\n\nविभाग चुनें (1-6):",
    "urgency": "⚡ गंभीरता चुनें:\n1. Low\n2. Medium\n3. High\n\nSelect urgency (1-3):",
    "description": "📝 समस्या का विस्तार से वर्णन करें:\nPlease describe the problem:",
    "photo": "📸 समस्या की जगह की फोटो भेजें:\nPlease send photo of the problem area:"
}

departments = {
    '1': 'पब्लिक वर्क्स',
    '2': 'जल विभाग',
    '3': 'बिजली विभाग',
    '4': 'सड़क विभाग',
    '5': 'सफाई विभाग',
    '6': 'अन्य'
}


urgency_levels = {
    '1': 'Low', 
    '2': 'Medium', 
    '3': 'High'
}

# Global variable to store the bot application
telegram_app = None

# Database functions
def connect_db():
    """Connect to MongoDB and return database instance"""
    try:
        client = MongoClient(MONGO_URL)
        # Test connection
        client.server_info()
        return client[DB_NAME]
    except Exception as error:
        print(f'❌ MongoDB connection failed: {error}')
        raise error

async def save_complaint(complaint_data):
    """Save complaint to MongoDB"""
    try:
        db = connect_db()
        collection = db[COLLECTION_NAME]
        
        complaint = {
            'id': generate_complaint_id(),
            'token': generate_token(),
            'type': 'image' if complaint_data.get('photoUrl') else 'text',
            'name': complaint_data['name'],
            'location': complaint_data['location'],
            'latitude': complaint_data.get('latitude'),
            'longitude': complaint_data.get('longitude'),
            'department': complaint_data['department'],
            'urgency': complaint_data['urgency'],
            'description': complaint_data['description'],
            'timestamp': datetime.now(),
            'status': 'Pending',
            'voice_path': None,
            'photoUrl': complaint_data.get('photoUrl'),
            'telegramUserId': complaint_data['telegramUserId'],
            'telegramUsername': complaint_data['telegramUsername']
        }
        
        print(f'💾 Saving complaint: {complaint["id"]} - {complaint["name"]}')
        result = collection.insert_one(complaint)
        print('✅ Complaint saved successfully')
        
        return {'success': True, 'complaintId': complaint['id'], 'insertedId': str(result.inserted_id)}
    except Exception as error:
        print(f'❌ Database save error: {error}')
        return {'success': False, 'error': str(error)}

def generate_complaint_id():
    """Generate 6-digit complaint ID"""
    return str(random.randint(100000, 999999))

def generate_token():
    """Generate random token"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=13))

# Session management
def init_session(user_id):
    """Initialize new user session"""
    user_sessions[user_id] = {
        'step': 'name',
        'data': {},
        'active': True
    }
    print(f'📱 New session started for user {user_id}')

def get_session(user_id):
    """Get user session"""
    return user_sessions.get(user_id)

def update_session(user_id, data):
    """Update user session data"""
    session = get_session(user_id)
    if session:
        session['data'].update(data)
        user_sessions[user_id] = session
        print(f'📝 Session updated for user {user_id}: {list(data.keys())}')

def next_step(user_id):
    """Move to next step in complaint process"""
    session = get_session(user_id)
    if session:
        steps = ['name', 'location', 'department', 'urgency', 'description', 'photo', 'complete']
        current_index = steps.index(session['step'])
        if current_index < len(steps) - 1:
            session['step'] = steps[current_index + 1]
            user_sessions[user_id] = session
            print(f'➡ User {user_id} moved to step: {session["step"]}')

# Download photo from Telegram
async def download_photo(file_url, local_path):
    """Download photo from Telegram servers"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                if response.status == 200:
                    async with aiofiles.open(local_path, 'wb') as file:
                        async for chunk in response.content.iter_chunked(8192):
                            await file.write(chunk)
                    print(f'📸 Photo saved to: {local_path}')
                    return local_path
                else:
                    raise Exception(f'HTTP {response.status}')
    except Exception as error:
        print(f'❌ Photo download error: {error}')
        raise error

# Bot command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    print(f'🚀 /start command from user {user_id}')
    init_session(user_id)
    
    welcome_message = f"""
🙏 नमस्ते! JantaVoice में आपका स्वागत है!
Welcome to JantaVoice Telegram Bot!

यह बॉट आपकी नागरिक शिकायतों को दर्ज करने में मदद करेगा।
This bot will help register your civic complaints.

{questions['name']}
    """
    
    await context.bot.send_message(chat_id=chat_id, text=welcome_message)

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    print(f'❌ Session cancelled for user {user_id}')
    await context.bot.send_message(
        chat_id=chat_id, 
        text='❌ शिकायत रद्द कर दी गई। /start दबाएं।\n\nComplaint cancelled. Press /start for new complaint.'
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    session = get_session(user_id)
    if session and session.get('active'):
        message = f"📊 Current step: {session['step']}\nData collected: {', '.join(session['data'].keys())}\n\nType /cancel to start over."
        await context.bot.send_message(chat_id=chat_id, text=message)
    else:
        await context.bot.send_message(
            chat_id=chat_id, 
            text='कोई सक्रिय शिकायत नहीं। /start दबाएं।\n\nNo active complaint. Press /start.'
        )

# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    text = update.message.text
    
    session = get_session(user_id)
    if not session or not session.get('active'):
        await context.bot.send_message(
            chat_id=chat_id, 
            text='कृपया पहले /start दबाएं।\n\nPlease press /start first.'
        )
        return
    
    print(f'💬 Message from user {user_id} at step {session["step"]}: {text}')
    
    try:
        step = session['step']
        
        if step == 'name':
            if text and text.strip():
                update_session(user_id, {'name': text.strip()})
                next_step(user_id)
                await context.bot.send_message(chat_id=chat_id, text=questions['location'])
            else:
                await context.bot.send_message(
                    chat_id=chat_id, 
                    text='❌ कृपया वैध नाम दर्ज करें।\nPlease enter a valid name.'
                )
        
        elif step == 'location':
            if update.message.location:
                update_session(user_id, {
                    'location': 'Live Location Captured',
                    'latitude': update.message.location.latitude,
                    'longitude': update.message.location.longitude
                })
                next_step(user_id)
                await context.bot.send_message(chat_id=chat_id, text=questions['department'])
            elif text and text.strip():
                update_session(user_id, {'location': text.strip()})
                next_step(user_id)
                await context.bot.send_message(chat_id=chat_id, text=questions['department'])
            else:
                await context.bot.send_message(
                    chat_id=chat_id, 
                    text='❌ कृपया स्थान बताएं।\nPlease provide location.'
                )
        
        elif step == 'department':
            dept = departments.get(text, departments.get(text.lower() if text else '', 'Other'))
            update_session(user_id, {'department': dept})
            next_step(user_id)
            await context.bot.send_message(chat_id=chat_id, text=questions['urgency'])
        
        elif step == 'urgency':
            urgency = urgency_levels.get(text, urgency_levels.get(text.lower() if text else '', 'normal'))
            update_session(user_id, {'urgency': urgency})
            next_step(user_id)
            await context.bot.send_message(chat_id=chat_id, text=questions['description'])
        
        elif step == 'description':
            if text and text.strip():
                update_session(user_id, {'description': text.strip()})
                next_step(user_id)
                await context.bot.send_message(chat_id=chat_id, text=questions['photo'])
            else:
                await context.bot.send_message(
                    chat_id=chat_id, 
                    text='❌ कृपया समस्या का वर्णन करें।\nPlease describe the problem.'
                )
        
        elif step == 'photo':
            await context.bot.send_message(
                chat_id=chat_id, 
                text='📸 कृपया फोटो भेजें, टेक्स्ट नहीं।\nPlease send photo, not text.'
            )
        
        else:
            await context.bot.send_message(
                chat_id=chat_id, 
                text='कुछ गलत हुआ। /start दबाएं।\nSomething went wrong. Press /start.'
            )
            
    except Exception as error:
        print(f'❌ Error handling message: {error}')
        await context.bot.send_message(
            chat_id=chat_id, 
            text='❌ तकनीकी समस्या। /start दबाएं।\nTechnical error. Press /start.'
        )

# Handle photo messages
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo messages"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    print(f'📸 Photo received from user {user_id}')
    
    session = get_session(user_id)
    if not session or not session.get('active') or session.get('step') != 'photo':
        await context.bot.send_message(
            chat_id=chat_id, 
            text='कृपया पहले शिकायत प्रक्रिया पूरी करें।\nPlease complete complaint process first.'
        )
        return
    
    try:
        await context.bot.send_message(
            chat_id=chat_id, 
            text='📤 फोटो सेव हो रही है...\nSaving photo...'
        )
        
        # Get highest resolution photo
        photo = update.message.photo[-1]
        file_id = photo.file_id
        
        # Get file info from Telegram
        file = await context.bot.get_file(file_id)
        file_url = file.file_path
        
        # Create local filename
        file_name = f"{user_id}_{int(datetime.now().timestamp())}.jpg"
        local_path = uploads_dir / file_name
        
        print(f'📥 Downloading photo from: {file_url}')
        
        # Download and save photo
        await download_photo(file_url, local_path)
        
        # Prepare complaint data
        session_data = session['data']
        complaint_data = {
            **session_data,
            'photoUrl': f'/uploads/{file_name}',
            'telegramUserId': user_id,
            'telegramUsername': update.effective_user.username or 'N/A'
        }
        
        print(f'💾 Preparing to save complaint: {complaint_data}')
        
        # Save to database
        await context.bot.send_message(
            chat_id=chat_id, 
            text='💾 डेटाबेस में सेव हो रही है...\nSaving to database...'
        )
        
        result = await save_complaint(complaint_data)
        
        if result['success']:
            success_message = f"""
✅ शिकायत सफलतापूर्वक दर्ज हो गई!
Complaint registered successfully!

🆔 Complaint ID: {result['complaintId']}
👤 Name: {session_data['name']}
📍 Location: {session_data['location']}
🏢 Department: {session_data['department']}
⚡ Urgency: {session_data['urgency']}
📝 Description: {session_data['description']}
📸 Photo: Attached

📬 आपकी शिकायत एडमिन को भेज दी गई है।
Your complaint has been sent to admin.

🔄 नई शिकायत के लिए /start दबाएं।
Press /start for new complaint.
            """
            
            await context.bot.send_message(chat_id=chat_id, text=success_message)
            print(f'✅ Complaint {result["complaintId"]} saved successfully for user {user_id}')
            
            # Clear session
            if user_id in user_sessions:
                del user_sessions[user_id]
        else:
            print(f'❌ Failed to save complaint: {result["error"]}')
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f'❌ डेटाबेस में समस्या: {result["error"]}\n\nDatabase error. Please try /start again.'
            )
    
    except Exception as error:
        print(f'❌ Photo handling error: {error}')
        await context.bot.send_message(
            chat_id=chat_id, 
            text='❌ फोटो अपलोड में समस्या। /start दबाकर फिर कोशिश करें।\n\nPhoto upload failed. Try /start again.'
        )

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors"""
    logger.error(f'Update {update} caused error {context.error}')

def run_bot():
    """Function to run the bot in a separate thread"""
    global telegram_app
    
    print('🤖 Initializing Telegram Bot...')
    
    # Test database connection
    try:
        connect_db()
        print('✅ Database connection test successful')
    except Exception as error:
        print(f'❌ Database connection test failed: {error}')
        return
    
    # Create application
    telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    telegram_app.add_handler(CommandHandler("start", start_command))
    telegram_app.add_handler(CommandHandler("cancel", cancel_command))
    telegram_app.add_handler(CommandHandler("status", status_command))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    telegram_app.add_handler(MessageHandler(filters.LOCATION, handle_message))
    telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Add error handler
    telegram_app.add_error_handler(error_handler)
    
    print('🤖 JantaVoice Telegram Bot Started!')
    print(f'📁 Upload directory: {uploads_dir}')
    print(f'💾 Database: {DB_NAME} at {MONGO_URL}')
    
    # Start bot
    telegram_app.run_polling(allowed_updates=Update.ALL_TYPES)

def start_telegram_bot():
    """Start telegram bot in a separate thread"""
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print('🤖 Telegram Bot thread started!')
    return bot_thread