# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import logging
# import os
# import time
# import threading
# from datetime import datetime
# # Telegram Bot
# import telegram1
# from voice_bot_conversational import create_voice_bot_routes, voice_bot

# # HuggingFace                                   
# # from transformers import pipeline

# # Routes
# from routes.complaint_routes import complaint_routes
# from routes.admin_routes import admin_routes
# from routes.voice_routes import voice_routes

# from routes.auth import auth_bp



# # Voice Bot
# from voice_bot.enhanced_jantavoice import start_conversation

# # ✅ Import schemes
# from schemes_data import SCHEMES  

# # ---------------- Logging Setup ----------------
# LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
# logging.basicConfig(
#     level=LOG_LEVEL,
#     format="%(asctime)s [%(levelname)s] - %(name)s - %(message)s",
#     handlers=[
#         logging.StreamHandler(),
#         logging.FileHandler("server.log", encoding="utf-8")
#     ],
# )
# logger = logging.getLogger("JantaVoice")

# # ---------------- Flask Setup ----------------
# app = Flask(__name__)
# CORS(app, supports_credentials=True)
# app.secret_key = os.environ.get("APP_SECRET_KEY", "super_secret_key_change_later")

# # Register Blueprints
# app.register_blueprint(complaint_routes)                 
# app.register_blueprint(admin_routes)                   
# app.register_blueprint(voice_routes)  
# app.register_blueprint(auth_bp)                 

# # ---------------- HuggingFace Model ----------------
# # HF_MODEL_NAME = os.environ.get("HF_MODEL_NAME", "bigscience/bloom-560m")

# # GEN_MAX_LENGTH = int(os.environ.get("GEN_MAX_LENGTH", "256"))
# # GEN_TEMPERATURE = float(os.environ.get("GEN_TEMPERATURE", "0.8"))
# # GEN_TOP_P = float(os.environ.get("GEN_TOP_P", "0.95"))
# # GEN_DO_SAMPLE = os.environ.get("GEN_DO_SAMPLE", "true").lower() == "true"

# # chatbot = None
# # try:
# #     logger.info(f"Loading Hugging Face model: {HF_MODEL_NAME}")
# #     chatbot = pipeline("text-generation", model=HF_MODEL_NAME)
# #     logger.info("✅ Chatbot model loaded successfully.")
# # except Exception as e:
# #     logger.exception(f"❌ Failed to load Hugging Face model: {e}")
# #     chatbot = None 

# # # ---------------- Helpers ----------------
# # def _build_prompt(user_text: str) -> str:
# #     return (
# #         "आप एक सहायक हैं जो भारत सरकार की योजनाओं की जानकारी"
# #         " बहुत ही सरल हिंदी में गरीब लोगों को समझाते हैं।\n\n"
# #         f"सवाल: {user_text.strip()}\n\n"
# #         "उत्तर आसान, छोटे बिंदुओं में, और स्पष्ट हिंदी में दें।\n"
# #         "अगर योजना का नाम, पात्रता, आवेदन प्रक्रिया और लाभ बता सकें तो शामिल करें।\n\n"
# #         "उत्तर:\n"
# #     )

# # def _postprocess_generated(user_prompt: str, generated_text: str) -> str:
# #     try:
# #         if generated_text.startswith(user_prompt):
# #             generated_text = generated_text[len(user_prompt):]
# #         return generated_text.strip()
# #     except Exception:
# #         return generated_text.strip()

# # def find_scheme_info(user_text: str):
# #     for scheme_name, data in SCHEMES.items():
# #         if scheme_name in user_text:
# #             return scheme_name, data
# #     return None, None

# # ---------------- Routes ----------------
# # @app.route("/", methods=["GET"])
# # def health_check():
# #     logger.info("Health check pinged")
# #     return jsonify({
# #         "status": "running",
# #         "message": "JantaVoice API is live 🚀",
# #         "version": "2.0",
# #         "timestamp_utc": datetime.utcnow().isoformat() + "Z",
# #         "chatbot_model": HF_MODEL_NAME,
# #         "chatbot_loaded": chatbot is not None
# #     }), 200


# # ---------------- Telegram Bot Routes ----------------
# @app.route('/bot/status')
# def bot_status():
#     """Check if Telegram bot is running"""
#     if hasattr(telegram1, 'telegram_app') and telegram1.telegram_app and telegram1.telegram_app.running:
#         return jsonify({
#             "status": "running",
#             "message": "Telegram bot is active",
#             "active_sessions": len(telegram1.user_sessions)
#         })
#     else:
#         return jsonify({
#             "status": "stopped",
#             "message": "Telegram bot is not running"
#         })

# @app.route('/bot/sessions')
# def bot_sessions():
#     """Get active Telegram bot sessions"""
#     return jsonify({
#         "active_sessions": len(telegram1.user_sessions),
#         "sessions": {
#             user_id: {
#                 "step": session["step"],
#                 "data_keys": list(session["data"].keys())
#             }
#             for user_id, session in telegram1.user_sessions.items()
#         }
#     })
# # @app.route('/')
# # def health_check1():
# #     """Basic health check endpoint"""
# #     return {
# #         "status": "healthy",
# #         "message": "Municipality Complaint System API is running",
# #         "features": [
# #             "Smart complaint classification with NLP",
# #             "Multi-language support (Hindi/English)",
# #             "Photo upload with geo-tagging",
# #             "Live location capture",
# #             "Voice-to-text conversion",
# #             "Automatic department routing",
# #             "Priority-based urgency detection"
# #         ]
# #     }

# # @app.route('/api/health')
# # def api_health():
# #     """API health check"""
# #     return {"status": "ok", "api_version": "1.0"}


# @app.errorhandler(404)
# def not_found(error):
#     return {"success": False, "message": "Endpoint not found"}, 404

# @app.errorhandler(500)
# def internal_error(error):
#     return {"success": False, "message": "Internal server error"}, 500

# # @app.route("/api/chat", methods=["POST"])
# # def chat():
# #     try:
# #         if chatbot is None:
# #             return jsonify({"reply": "Chatbot model not loaded."}), 500

# #         data = request.get_json(silent=True) or {}
# #         prompt = data.get("message", "").strip()

# #         if not prompt:
# #             return jsonify({"reply": "Message is empty"}), 400

# #         # Step 1: Predefined schemes
# #         scheme_name, scheme_data = find_scheme_info(prompt)
# #         if scheme_data:
# #             reply = f"👉 *{scheme_name}*\n\n"
# #             reply += f"🌐 आधिकारिक लिंक: {scheme_data['link']}\n\n"
# #             reply += f"📌 पात्रता: {scheme_data['eligibility']}\n\n"
# #             reply += f"🎯 लाभ: {scheme_data['benefits']}\n\n"
# #             reply += "📝 आवेदन की प्रक्रिया:\n"
# #             for i, step in enumerate(scheme_data["steps"], 1):
# #                 reply += f"{i}. {step}\n"

# #             return jsonify({"reply": reply}), 200

# #         # Step 2: LLM fallback
# #         full_prompt = _build_prompt(prompt)
# #         outputs = chatbot(
# #             full_prompt,
# #             max_length=GEN_MAX_LENGTH,
# #             do_sample=GEN_DO_SAMPLE,
# #             top_p=GEN_TOP_P,
# #             temperature=GEN_TEMPERATURE,
# #             num_return_sequences=1,
# #             pad_token_id=None
# #         )
# #         raw_text = outputs[0].get("generated_text", "")
# #         reply = _postprocess_generated(full_prompt, raw_text)

# #         return jsonify({"reply": reply}), 200

# #     except Exception as e:
# #         logger.exception("Chat error")
# #         return jsonify({"reply": f"Error: {str(e)}"}), 500

# @app.route("/api/voice-complaint", methods=["POST"])
# def voice_complaint():
#     try:
#         logger.info("Voice complaint endpoint triggered")
#         result = start_conversation()
#         if result:
#             return jsonify({
#                 "status": "success",
#                 "message": "Voice complaint submitted successfully!",
#                 "data": result,
#                 "complaint_id": result.get("complaint_id", "Unknown")
#             }), 200
#         else:
#             return jsonify({"status": "error", "message": "Failed to process voice complaint"}), 500
#     except Exception as e:
#         logger.exception("Voice complaint error")
#         return jsonify({"status": "error", "message": str(e)}), 500

# @app.route("/api/voice-complaint-alt", methods=["POST"])
# def voice_complaint_alt():
#     try:
#         logger.info("Voice complaint (alt) triggered")
#         result = start_conversation()
#         if result:
#             return jsonify({
#                 "message": "Voice complaint submitted successfully!",
#                 "data": result,
#                 "complaint_id": result.get("complaint_id", "Unknown")
#             }), 200
#         else:
#             return jsonify({"error": "Failed to process voice complaint"}), 500
#     except Exception as e:
#         logger.exception("Voice complaint error")
#         return jsonify({"error": str(e)}), 500

# # ---------------- Error Handlers ----------------
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({"error": "Endpoint not found"}), 404

# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({"error": "Internal server error"}), 500

# # ---------------- Main ----------------
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     debug_mode = os.environ.get("DEBUG", "True").lower() == "true"
#     logger.info(f"🚀 Starting JantaVoice server on port {port}")
    
#     # try:
#     #     logger.info("🤖 Starting Telegram Bot...")
#     #     bot_thread = telegram1.start_telegram_bot()
#     #     logger.info("✅ Telegram Bot started successfully")
#     # except Exception as e:
#     #     logger.error(f"❌ Failed to start Telegram Bot: {e}")
    
#     # logger.info(f"🚀 Starting JantaVoice server on port {port}")
#     # logger.info("🌐 Flask Backend + 🤖 Telegram Bot running together")
#     app.run(debug=debug_mode, use_reloader=False, host="0.0.0.0", port=port)


from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import time
import threading
from datetime import datetime
# Telegram Bot
import telegram1
from voice_bot_conversational import create_voice_bot_routes, voice_bot

# HuggingFace                                   
# from transformers import pipeline

# Routes
from routes.complaint_routes import complaint_routes
from routes.admin_routes import admin_routes
# from routes.voice_routes import voice_routes
from routes.auth import auth_bp

# Voice Bot
from voice_bot.enhanced_jantavoice import start_conversation

# ✅ Import schemes
from schemes_data import SCHEMES  

# ---------------- Logging Setup ----------------
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("server.log", encoding="utf-8")
    ],
)
logger = logging.getLogger("JantaVoice")

# ---------------- Flask Setup ----------------
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.environ.get("APP_SECRET_KEY", "super_secret_key_change_later")

# Register Blueprints
app.register_blueprint(complaint_routes)                 
app.register_blueprint(admin_routes)                   
# app.register_blueprint(voice_routes)  
app.register_blueprint(auth_bp)                 

# ---------------- Voice Bot Setup ----------------
def setup_voice_bot():
    """Setup conversational voice bot with Gemini AI"""
    try:
        logger.info("🤖 Setting up Conversational Voice Bot...")
        
        # Create audio cache directory
        audio_cache_dir = "audio_cache"
        if not os.path.exists(audio_cache_dir):
            os.makedirs(audio_cache_dir)
            logger.info(f"📁 Created audio cache directory: {audio_cache_dir}")
        
        # Add voice bot routes
        create_voice_bot_routes(app)
        
        # Setup cleanup task for old sessions
        def cleanup_sessions():
            while True:
                time.sleep(3600)  # Run every hour
                try:
                    voice_bot.cleanup_old_sessions(24)  # Remove sessions older than 24 hours
                    logger.info("🧹 Cleaned up old voice bot sessions")
                except Exception as e:
                    logger.error(f"❌ Session cleanup error: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
        cleanup_thread.start()
        
        logger.info("✅ Conversational Voice Bot configured successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to setup voice bot: {e}")
        return False

# Initialize voice bot
voice_bot_status = setup_voice_bot()

# ---------------- HuggingFace Model ----------------
# HF_MODEL_NAME = os.environ.get("HF_MODEL_NAME", "bigscience/bloom-560m")

# GEN_MAX_LENGTH = int(os.environ.get("GEN_MAX_LENGTH", "256"))
# GEN_TEMPERATURE = float(os.environ.get("GEN_TEMPERATURE", "0.8"))
# GEN_TOP_P = float(os.environ.get("GEN_TOP_P", "0.95"))
# GEN_DO_SAMPLE = os.environ.get("GEN_DO_SAMPLE", "true").lower() == "true"

# chatbot = None
# try:
#     logger.info(f"Loading Hugging Face model: {HF_MODEL_NAME}")
#     chatbot = pipeline("text-generation", model=HF_MODEL_NAME)
#     logger.info("✅ Chatbot model loaded successfully.")
# except Exception as e:
#     logger.exception(f"❌ Failed to load Hugging Face model: {e}")
#     chatbot = None 

# # ---------------- Helpers ----------------
# def _build_prompt(user_text: str) -> str:
#     return (
#         "आप एक सहायक हैं जो भारत सरकार की योजनाओं की जानकारी"
#         " बहुत ही सरल हिंदी में गरीब लोगों को समझाते हैं।\n\n"
#         f"सवाल: {user_text.strip()}\n\n"
#         "उत्तर आसान, छोटे बिंदुओं में, और स्पष्ट हिंदी में दें।\n"
#         "अगर योजना का नाम, पात्रता, आवेदन प्रक्रिया और लाभ बता सकें तो शामिल करें।\n\n"
#         "उत्तर:\n"
#     )

# def _postprocess_generated(user_prompt: str, generated_text: str) -> str:
#     try:
#         if generated_text.startswith(user_prompt):
#             generated_text = generated_text[len(user_prompt):]
#         return generated_text.strip()
#     except Exception:
#         return generated_text.strip()

# def find_scheme_info(user_text: str):
#     for scheme_name, data in SCHEMES.items():
#         if scheme_name in user_text:
#             return scheme_name, data
#     return None, None

# ---------------- Routes ----------------
@app.route("/", methods=["GET"])
def health_check():
    logger.info("Health check pinged")
    return jsonify({
        "status": "running",
        "message": "JantaVoice API is live 🚀",
        "version": "2.1",  # Updated version
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "features": {
            "conversational_voice_bot": voice_bot_status,
            "telegram_bot": hasattr(telegram1, 'telegram_app'),
            "complaint_system": True,
            "admin_dashboard": True,
            "authentication": True
        },
        "voice_bot_status": "active" if voice_bot_status else "inactive"
    }), 200

# ---------------- Telegram Bot Routes ----------------
@app.route('/bot/status')
def bot_status():
    """Check if Telegram bot is running"""
    if hasattr(telegram1, 'telegram_app') and telegram1.telegram_app and telegram1.telegram_app.running:
        return jsonify({
            "status": "running",
            "message": "Telegram bot is active",
            "active_sessions": len(telegram1.user_sessions)
        })
    else:
        return jsonify({
            "status": "stopped",
            "message": "Telegram bot is not running"
        })

@app.route('/bot/sessions')
def bot_sessions():
    """Get active Telegram bot sessions"""
    return jsonify({
        "active_sessions": len(telegram1.user_sessions),
        "sessions": {
            user_id: {
                "step": session["step"],
                "data_keys": list(session["data"].keys())
            }
            for user_id, session in telegram1.user_sessions.items()
        }
    })

# ---------------- Voice Bot Status Routes ----------------
@app.route('/api/voice-bot/status')
def voice_bot_status_check():
    """Check conversational voice bot status"""
    try:
        active_sessions = len(voice_bot.conversation_sessions) if voice_bot else 0
        return jsonify({
            "status": "active" if voice_bot_status else "inactive",
            "message": "Conversational Voice Bot with Gemini AI",
            "active_sessions": active_sessions,
            "features": [
                "Hindi speech recognition",
                "Gemini AI-powered conversations", 
                "Intelligent follow-up questions",
                "Context-aware responses",
                "Audio caching for performance"
            ] if voice_bot_status else [],
            "gemini_integration": True if voice_bot_status else False
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Voice bot status check failed: {str(e)}"
        }), 500

@app.route('/api/voice-bot/sessions')
def voice_bot_sessions():
    """Get active voice bot conversation sessions"""
    try:
        if not voice_bot_status:
            return jsonify({"error": "Voice bot not active"}), 503
            
        sessions_info = {}
        for session_id, session_data in voice_bot.conversation_sessions.items():
            sessions_info[session_id] = {
                "user_name": session_data.get("user_name"),
                "step": session_data.get("step"),
                "created_at": session_data.get("created_at"),
                "conversation_length": len(session_data.get("conversation_history", [])),
                "complaint_type": session_data.get("conversation_data", {}).get("complaint_type", ""),
                "urgency": session_data.get("conversation_data", {}).get("urgency", "")
            }
            
        return jsonify({
            "active_sessions": len(voice_bot.conversation_sessions),
            "sessions": sessions_info
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- Enhanced Voice Complaint Routes ----------------
@app.route("/api/voice-complaint", methods=["POST"])
def voice_complaint():
    """Legacy voice complaint endpoint"""
    try:
        logger.info("Voice complaint endpoint triggered")
        result = start_conversation()
        if result:
            return jsonify({
                "status": "success",
                "message": "Voice complaint submitted successfully!",
                "data": result,
                "complaint_id": result.get("complaint_id", "Unknown")
            }), 200
        else:
            return jsonify({"status": "error", "message": "Failed to process voice complaint"}), 500
    except Exception as e:
        logger.exception("Voice complaint error")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/voice-complaint-alt", methods=["POST"])
def voice_complaint_alt():
    """Alternative voice complaint endpoint"""
    try:
        logger.info("Voice complaint (alt) triggered")
        result = start_conversation()
        if result:
            return jsonify({
                "message": "Voice complaint submitted successfully!",
                "data": result,
                "complaint_id": result.get("complaint_id", "Unknown")
            }), 200
        else:
            return jsonify({"error": "Failed to process voice complaint"}), 500
    except Exception as e:
        logger.exception("Voice complaint error")
        return jsonify({"error": str(e)}), 500

@app.route("/api/conversational-voice-complaint", methods=["POST"])
def conversational_voice_complaint():
    """New conversational voice complaint with Gemini AI"""
    try:
        if not voice_bot_status:
            return jsonify({
                "error": "Conversational voice bot is not active",
                "fallback_message": "Please use the standard complaint form"
            }), 503
            
        data = request.get_json() or {}
        user_name = data.get('user_name', 'उपयोगकर्ता')
        
        logger.info(f"Starting conversational voice complaint for user: {user_name}")
        
        # This would integrate with your conversational voice bot
        # For now, return a success message directing to the voice bot endpoints
        return jsonify({
            "status": "success",
            "message": "Conversational voice bot ready",
            "instructions": "Use /api/voice-bot/start to begin conversation",
            "user_name": user_name,
            "next_step": "start_conversation"
        }), 200
        
    except Exception as e:
        logger.exception("Conversational voice complaint error")
        return jsonify({"error": str(e)}), 500

# ---------------- Analytics Routes ----------------
@app.route('/api/analytics/voice-bot')
def voice_bot_analytics():
    """Get voice bot usage analytics"""
    try:
        if not voice_bot_status:
            return jsonify({"error": "Voice bot not active"}), 503
            
        # Basic analytics
        total_sessions = len(voice_bot.conversation_sessions)
        
        # Count by complaint types
        complaint_types = {}
        urgency_levels = {}
        
        for session_data in voice_bot.conversation_sessions.values():
            conv_data = session_data.get("conversation_data", {})
            
            complaint_type = conv_data.get("complaint_type", "Unknown")
            if complaint_type in complaint_types:
                complaint_types[complaint_type] += 1
            else:
                complaint_types[complaint_type] = 1
                
            urgency = conv_data.get("urgency", "Unknown")
            if urgency in urgency_levels:
                urgency_levels[urgency] += 1
            else:
                urgency_levels[urgency] = 1
        
        return jsonify({
            "total_active_sessions": total_sessions,
            "complaint_types_distribution": complaint_types,
            "urgency_levels_distribution": urgency_levels,
            "average_conversation_length": sum(
                len(session.get("conversation_history", []))
                for session in voice_bot.conversation_sessions.values()
            ) / max(total_sessions, 1)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/')
# def health_check1():
#     """Basic health check endpoint"""
#     return {
#         "status": "healthy",
#         "message": "Municipality Complaint System API is running",
#         "features": [
#             "Smart complaint classification with NLP",
#             "Multi-language support (Hindi/English)",
#             "Photo upload with geo-tagging",
#             "Live location capture",
#             "Voice-to-text conversion",
#             "Automatic department routing",
#             "Priority-based urgency detection"
#         ]
#     }

# @app.route('/api/health')
# def api_health():
#     """API health check"""
#     return {"status": "ok", "api_version": "1.0"}

# @app.route("/api/chat", methods=["POST"])
# def chat():
#     try:
#         if chatbot is None:
#             return jsonify({"reply": "Chatbot model not loaded."}), 500

#         data = request.get_json(silent=True) or {}
#         prompt = data.get("message", "").strip()

#         if not prompt:
#             return jsonify({"reply": "Message is empty"}), 400

#         # Step 1: Predefined schemes
#         scheme_name, scheme_data = find_scheme_info(prompt)
#         if scheme_data:
#             reply = f"👉 *{scheme_name}*\n\n"
#             reply += f"🌐 आधिकारिक लिंक: {scheme_data['link']}\n\n"
#             reply += f"📌 पात्रता: {scheme_data['eligibility']}\n\n"
#             reply += f"🎯 लाभ: {scheme_data['benefits']}\n\n"
#             reply += "📝 आवेदन की प्रक्रिया:\n"
#             for i, step in enumerate(scheme_data["steps"], 1):
#                 reply += f"{i}. {step}\n"

#             return jsonify({"reply": reply}), 200

#         # Step 2: LLM fallback
#         full_prompt = _build_prompt(prompt)
#         outputs = chatbot(
#             full_prompt,
#             max_length=GEN_MAX_LENGTH,
#             do_sample=GEN_DO_SAMPLE,
#             top_p=GEN_TOP_P,
#             temperature=GEN_TEMPERATURE,
#             num_return_sequences=1,
#             pad_token_id=None
#         )
#         raw_text = outputs[0].get("generated_text", "")
#         reply = _postprocess_generated(full_prompt, raw_text)

#         return jsonify({"reply": reply}), 200

#     except Exception as e:
#         logger.exception("Chat error")
#         return jsonify({"reply": f"Error: {str(e)}"}), 500

# ---------------- Error Handlers ----------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "message": "Internal server error"}), 500

# ---------------- Environment Configuration Check ----------------
@app.route('/api/config/check')
def config_check():
    """Check important environment configurations"""
    return jsonify({
        "environment": {
            "debug_mode": os.environ.get("DEBUG", "True").lower() == "true",
            "port": int(os.environ.get("PORT", 5000)),
            "log_level": LOG_LEVEL,
            "app_secret_key_set": bool(os.environ.get("APP_SECRET_KEY")),
            "gemini_api_key_set": bool(os.environ.get("GEMINI_API_KEY"))
        },
        "features": {
            "voice_bot": voice_bot_status,
            "telegram_bot": hasattr(telegram1, 'telegram_app'),
            "cors_enabled": True,
            "logging_enabled": True
        },
        "recommendations": [
            "Set GEMINI_API_KEY environment variable for conversational AI",
            "Configure APP_SECRET_KEY for production security",
            "Set LOG_LEVEL to WARNING or ERROR in production"
        ] if not all([
            os.environ.get("GEMINI_API_KEY"),
            os.environ.get("APP_SECRET_KEY") != "super_secret_key_change_later"
        ]) else ["Configuration looks good!"]
    })

# ---------------- Main ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("DEBUG", "True").lower() == "true"
    
    logger.info("🚀 Starting JantaVoice Enhanced Server")
    logger.info(f"📊 Features Status:")
    logger.info(f"   🤖 Conversational Voice Bot: {'✅ Active' if voice_bot_status else '❌ Inactive'}")
    logger.info(f"   📱 Telegram Bot: {'✅ Available' if hasattr(telegram1, 'telegram_app') else '❌ Not Available'}")
    logger.info(f"   🔐 Authentication: ✅ Active")
    logger.info(f"   📝 Complaint System: ✅ Active")
    logger.info(f"   👨‍💼 Admin Dashboard: ✅ Active")
    
    if not voice_bot_status:
        logger.warning("⚠️  Conversational Voice Bot failed to initialize")
        logger.warning("   💡 Check GEMINI_API_KEY environment variable")
        logger.warning("   💡 Ensure required dependencies are installed")
    
    # try:
    #     logger.info("🤖 Starting Telegram Bot...")
    #     bot_thread = telegram1.start_telegram_bot()
    #     logger.info("✅ Telegram Bot started successfully")
    # except Exception as e:
    #     logger.error(f"❌ Failed to start Telegram Bot: {e}")
    
    logger.info(f"🌐 Server starting on port {port}")
    logger.info("🔗 Available endpoints:")
    logger.info("   📋 /api/voice-bot/start - Start conversational voice bot")
    logger.info("   🎙️ /api/voice-bot/process - Process voice conversation")
    logger.info("   📊 /api/voice-bot/status - Voice bot status")
    logger.info("   📈 /api/analytics/voice-bot - Voice bot analytics")
    logger.info("   ⚙️ /api/config/check - Configuration check")
    
    app.run(debug=debug_mode, use_reloader=False, host="0.0.0.0", port=port)