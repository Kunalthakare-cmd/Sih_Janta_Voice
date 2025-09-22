const TelegramBot = require('node-telegram-bot-api');
const { MongoClient } = require('mongodb');
const fs = require('fs');
const path = require('path');
const https = require('https');

// IMPORTANT: Replace with your actual bot token from @BotFather
const TELEGRAM_TOKEN = '8103339340:AAGtFb78LdkdvghslKvbxSzn7yvTZD7TBWI';
const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });

// IMPORTANT: Replace with your actual database name
const MONGO_URL = 'mongodb://localhost:27017';
const DB_NAME = 'janta_voice'; // Change this to your actual database name
const COLLECTION_NAME = 'complaints';

// Create uploads directory if it doesn't exist
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// User sessions storage
const userSessions = new Map();

// Question flow
const questions = {
  name: "🙋‍♂ कृपया अपना नाम बताएं:\nPlease provide your name:",
  location: "📍 शिकायत का स्थान बताएं या location share करें:\nPlease provide location or share location:",
  department: "🏢 विभाग चुनें:\n1. Public Works\n2. Water Supply\n3. Electricity\n4. Roads\n5. Sanitation\n6. Other\n\nSelect department (1-6):",
  urgency: "⚡ गंभीरता चुनें:\n1. Normal\n2. Urgent\n3. Critical\n\nSelect urgency (1-3):",
  description: "📝 समस्या का विस्तार से वर्णन करें:\nPlease describe the problem:",
  photo: "📸 समस्या की जगह की फोटो भेजें:\nPlease send photo of the problem area:"
};

const departments = {
   '1': 'पब्लिक वर्क्स',
    '2': 'जल विभाग',
    '3': 'बिजली विभाग',
    '4': 'सड़क विभाग',
    '5': 'सफाई विभाग',
    '6': 'अन्य'
};

const urgencyLevels = {
 '1': 'Low', 
    '2': 'Medium', 
    '3': 'High'};

// Database functions
async function connectDB() {
  try {
    const client = new MongoClient(MONGO_URL);
    await client.connect();
    console.log('✅ Connected to MongoDB');
    return client.db(DB_NAME);
  } catch (error) {
    console.error('❌ MongoDB connection failed:', error);
    throw error;
  }
}

async function saveComplaint(complaintData) {
  try {
    const db = await connectDB();
    const collection = db.collection(COLLECTION_NAME);
    
    const complaint = {
      id: generateComplaintId(),
      token: generateToken(),
      type: complaintData.photoUrl ? 'image' : 'text',
      name: complaintData.name,
      location: complaintData.location,
      latitude: complaintData.latitude || null,
      longitude: complaintData.longitude || null,
      department: complaintData.department,
      urgency: complaintData.urgency,
      description: complaintData.description,
      timestamp: new Date(),
      status: 'Pending',
      voice_path: null,
      photoUrl: complaintData.photoUrl || null,
      telegramUserId: complaintData.telegramUserId,
      telegramUsername: complaintData.telegramUsername
    };
    
    console.log('💾 Saving complaint:', { id: complaint.id, name: complaint.name });
    const result = await collection.insertOne(complaint);
    console.log('✅ Complaint saved successfully');
    
    return { success: true, complaintId: complaint.id, insertedId: result.insertedId };
  } catch (error) {
    console.error('❌ Database save error:', error);
    return { success: false, error: error.message };
  }
}

function generateComplaintId() {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

function generateToken() {
  return Math.random().toString(36).substring(2, 15);
}

// Session management
function initSession(userId) {
  userSessions.set(userId, {
    step: 'name',
    data: {},
    active: true
  });
  console.log(`📱 New session started for user ${userId}`);
}

function getSession(userId) {
  return userSessions.get(userId) || null;
}

function updateSession(userId, data) {
  const session = getSession(userId);
  if (session) {
    session.data = { ...session.data, ...data };
    userSessions.set(userId, session);
    console.log(`📝 Session updated for user ${userId}:`, Object.keys(data));
  }
}

function nextStep(userId) {
  const session = getSession(userId);
  if (session) {
    const steps = ['name', 'location', 'department', 'urgency', 'description', 'photo', 'complete'];
    const currentIndex = steps.indexOf(session.step);
    if (currentIndex < steps.length - 1) {
      session.step = steps[currentIndex + 1];
      userSessions.set(userId, session);
      console.log(`➡ User ${userId} moved to step: ${session.step}`);
    }
  }
}

// Download photo from Telegram
async function downloadPhoto(fileUrl, localPath) {
  return new Promise((resolve, reject) => {
    https.get(fileUrl, (response) => {
      if (response.statusCode !== 200) {
        reject(new Error(`HTTP ${response.statusCode}`));
        return;
      }
      
      const chunks = [];
      response.on('data', (chunk) => chunks.push(chunk));
      response.on('end', () => {
        try {
          const buffer = Buffer.concat(chunks);
          fs.writeFileSync(localPath, buffer);
          console.log('📸 Photo saved to:', localPath);
          resolve(localPath);
        } catch (error) {
          reject(error);
        }
      });
      response.on('error', reject);
    }).on('error', reject);
  });
}

// Bot commands
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  
  console.log(`🚀 /start command from user ${userId}`);
  initSession(userId);
  
  const welcomeMessage = `
🙏 नमस्ते! JantaVoice में आपका स्वागत है!
Welcome to JantaVoice Telegram Bot!

यह बॉट आपकी नागरिक शिकायतों को दर्ज करने में मदद करेगा।
This bot will help register your civic complaints.

${questions.name}
  `;
  
  bot.sendMessage(chatId, welcomeMessage);
});

bot.onText(/\/cancel/, (msg) => {
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  
  userSessions.delete(userId);
  console.log(`❌ Session cancelled for user ${userId}`);
  bot.sendMessage(chatId, '❌ शिकायत रद्द कर दी गई। /start दबाएं।\n\nComplaint cancelled. Press /start for new complaint.');
});

bot.onText(/\/status/, (msg) => {
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  
  const session = getSession(userId);
  if (session && session.active) {
    bot.sendMessage(chatId, `📊 Current step: ${session.step}\nData collected: ${Object.keys(session.data).join(', ')}\n\nType /cancel to start over.`);
  } else {
    bot.sendMessage(chatId, 'कोई सक्रिय शिकायत नहीं। /start दबाएं।\n\nNo active complaint. Press /start.');
  }
});

// Handle text messages
bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  const text = msg.text;
  
  // Skip commands
  if (text && text.startsWith('/')) return;
  
  const session = getSession(userId);
  if (!session || !session.active) {
    bot.sendMessage(chatId, 'कृपया पहले /start दबाएं।\n\nPlease press /start first.');
    return;
  }
  
  console.log(`💬 Message from user ${userId} at step ${session.step}: ${text || 'non-text'}`);
  
  try {
    switch (session.step) {
      case 'name':
        if (text && text.trim()) {
          updateSession(userId, { name: text.trim() });
          nextStep(userId);
          bot.sendMessage(chatId, questions.location);
        } else {
          bot.sendMessage(chatId, '❌ कृपया वैध नाम दर्ज करें।\nPlease enter a valid name.');
        }
        break;
        
      case 'location':
        if (msg.location) {
          updateSession(userId, { 
            location: 'Live Location Captured',
            latitude: msg.location.latitude,
            longitude: msg.location.longitude
          });
        } else if (text && text.trim()) {
          updateSession(userId, { location: text.trim() });
        } else {
          bot.sendMessage(chatId, '❌ कृपया स्थान बताएं।\nPlease provide location.');
          return;
        }
        nextStep(userId);
        bot.sendMessage(chatId, questions.department);
        break;
        
      case 'department':
        const dept = departments[text] || departments[text?.toLowerCase()] || 'Other';
        updateSession(userId, { department: dept });
        nextStep(userId);
        bot.sendMessage(chatId, questions.urgency);
        break;
        
      case 'urgency':
        const urgency = urgencyLevels[text] || urgencyLevels[text?.toLowerCase()] || 'normal';
        updateSession(userId, { urgency: urgency });
        nextStep(userId);
        bot.sendMessage(chatId, questions.description);
        break;
        
      case 'description':
        if (text && text.trim()) {
          updateSession(userId, { description: text.trim() });
          nextStep(userId);
          bot.sendMessage(chatId, questions.photo);
        } else {
          bot.sendMessage(chatId, '❌ कृपया समस्या का वर्णन करें।\nPlease describe the problem.');
        }
        break;
        
      case 'photo':
        bot.sendMessage(chatId, '📸 कृपया फोटो भेजें, टेक्स्ट नहीं।\nPlease send photo, not text.');
        break;
        
      default:
        bot.sendMessage(chatId, 'कुछ गलत हुआ। /start दबाएं।\nSomething went wrong. Press /start.');
    }
  } catch (error) {
    console.error('❌ Error handling message:', error);
    bot.sendMessage(chatId, '❌ तकनीकी समस्या। /start दबाएं।\nTechnical error. Press /start.');
  }
});

// Handle photo messages
bot.on('photo', async (msg) => {
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  
  console.log(`📸 Photo received from user ${userId}`);
  
  const session = getSession(userId);
  if (!session || !session.active || session.step !== 'photo') {
    bot.sendMessage(chatId, 'कृपया पहले शिकायत प्रक्रिया पूरी करें।\nPlease complete complaint process first.');
    return;
  }
  
  try {
    bot.sendMessage(chatId, '📤 फोटो सेव हो रही है...\nSaving photo...');
    
    // Get highest resolution photo
    const photo = msg.photo[msg.photo.length - 1];
    const fileId = photo.file_id;
    const file = await bot.getFile(fileId);
    const filePath = file.file_path;
    const fileUrl = `https://api.telegram.org/file/bot${TELEGRAM_TOKEN}/${filePath}`;
    const fileName = `${userId}_${Date.now()}.jpg`;
    const localPath = path.join(uploadsDir, fileName);
    
    console.log('📥 Downloading photo from:', fileUrl);
    
    // Download and save photo
    await downloadPhoto(fileUrl, localPath);
    
    // Prepare complaint data
    const sessionData = session.data;
    const complaintData = {
      ...sessionData,
      photoUrl: `/uploads/${fileName}`,
      telegramUserId: userId,
      telegramUsername: msg.from.username || 'N/A'
    };
    
    console.log('💾 Preparing to save complaint:', complaintData);
    
    // Save to database
    bot.sendMessage(chatId, '💾 डेटाबेस में सेव हो रही है...\nSaving to database...');
    const result = await saveComplaint(complaintData);
    
    if (result.success) {
      const successMessage = `
✅ शिकायत सफलतापूर्वक दर्ज हो गई!
Complaint registered successfully!

🆔 Complaint ID: ${result.complaintId}
👤 Name: ${sessionData.name}
📍 Location: ${sessionData.location}
🏢 Department: ${sessionData.department}
⚡ Urgency: ${sessionData.urgency}
📝 Description: ${sessionData.description}
📸 Photo: Attached

📬 आपकी शिकायत एडमिन को भेज दी गई है।
Your complaint has been sent to admin.

🔄 नई शिकायत के लिए /start दबाएं।
Press /start for new complaint.
      `;
      
      bot.sendMessage(chatId, successMessage);
      console.log(`✅ Complaint ${result.complaintId} saved successfully for user ${userId}`);
      
      // Clear session
      userSessions.delete(userId);
    } else {
      console.error('❌ Failed to save complaint:', result.error);
      bot.sendMessage(chatId, `❌ डेटाबेस में समस्या: ${result.error}\n\nDatabase error. Please try /start again.`);
    }
    
  } catch (error) {
    console.error('❌ Photo handling error:', error);
    bot.sendMessage(chatId, '❌ फोटो अपलोड में समस्या। /start दबाकर फिर कोशिश करें।\n\nPhoto upload failed. Try /start again.');
  }
});

// Error handling
bot.on('error', (error) => {
  console.error('🤖 Telegram Bot Error:', error);
});

bot.on('polling_error', (error) => {
  console.error('📡 Polling Error:', error);
});

// Add token validation
if (!TELEGRAM_TOKEN ) {
  console.error('❌ Invalid or default Telegram bot token. Please set your actual bot token.');
  process.exit(1);
}

// Add proper error cleanup
process.on('uncaughtException', (error) => {
  console.error('❌ Uncaught Exception:', error);
  // Cleanup sessions on fatal error
  userSessions.clear();
});

process.on('unhandledRejection', (error) => {
  console.error('❌ Unhandled Promise Rejection:', error);
});

// Startup
console.log('🤖 JantaVoice Telegram Bot Started!');
console.log('📱 Bot is ready to receive messages');
console.log('📁 Upload directory:', uploadsDir);
console.log(`💾 Database: ${DB_NAME} at ${MONGO_URL}`);

// Test database connection
connectDB().then(() => {
  console.log('✅ Database connection test successful');
}).catch((error) => {
  console.error('❌ Database connection test failed:', error);
});

console.log('\n🔧 SETUP REQUIRED:');
console.log('1. Replace YOUR_BOT_TOKEN_HERE with your actual bot token');
console.log('2. Replace your_database_name with your actual database name');
console.log('3. Make sure MongoDB is running on localhost:27017');
console.log('4. Test with /start command in Telegram\n');