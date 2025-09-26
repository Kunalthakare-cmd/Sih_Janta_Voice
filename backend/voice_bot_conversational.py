# import speech_recognition as sr
# from gtts import gTTS
# import pygame
# import time
# import os
# import random
# import google.generativeai as genai
# from flask import Flask, request, jsonify, send_file
# import json
# from datetime import datetime
# import tempfile
# import uuid

# # Initialize pygame mixer once
# pygame.mixer.init()

# # Configure Gemini API
# genai.configure(api_key="AIzaSyDQ8agyfEwaijZ0VpByd1I71cnzIuKuXvc")  # Replace with your actual API key

# # Initialize Gemini model
# model = genai.GenerativeModel('gemini-1.5-flash')

# class ConversationalVoiceBot:
#     def __init__(self):
#         self.conversation_sessions = {}
#         self.audio_cache_dir = "audio_cache"
#         if not os.path.exists(self.audio_cache_dir):
#             os.makedirs(self.audio_cache_dir)
    
#     def speak_hindi(self, text, session_id=None):
#         """Convert text to speech in Hindi and return audio file path"""
#         try:
#             # Cache audio files to avoid repeated TTS generation
#             filename = f"{self.audio_cache_dir}/voice_{hash(text)}_{session_id or 'default'}.mp3"
            
#             if not os.path.exists(filename):
#                 tts = gTTS(text=text, lang='hi')
#                 tts.save(filename)
            
#             return filename
#         except Exception as e:
#             print(f"⚠️ Voice Error: {e}")
#             return None

#     def listen_hindi(self, timeout=8, phrase_time_limit=10):
#         """Listen for Hindi speech and return transcribed text"""
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             r.adjust_for_ambient_noise(source, duration=0.5)
#             print("सुन रहा हूँ...")
#             try:
#                 audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
#             except sr.WaitTimeoutError:
#                 return None

#         try:
#             text = r.recognize_google(audio, language="hi-IN")
#             print(f"आपने कहा: {text}")
#             return text
#         except (sr.UnknownValueError, sr.RequestError) as e:
#             print(f"Speech recognition error: {e}")
#             return None

#     def get_gemini_response(self, user_message, conversation_context, current_step):
#         """Get intelligent response from Gemini API based on conversation context"""
        
#         # Create comprehensive prompt for Gemini
#         system_prompt = f"""
#         आप एक बुद्धिमान शिकायत सहायक हैं जो नागरिकों की शिकायतें दर्ज करने में मदद करते हैं। 
#         आपका काम है उपयोगकर्ता से प्रासंगिक प्रश्न पूछकर पूरी शिकायत की जानकारी एकत्रित करना।

#         वर्तमान चरण: {current_step}
#         बातचीत का संदर्भ: {json.dumps(conversation_context, ensure_ascii=False)}
        
#         उपयोगकर्ता का जवाब: "{user_message}"

#         निर्देश:
#         1. केवल हिंदी में जवाब दें
#         2. संक्षिप्त और स्पष्ट प्रश्न पूछें  
#         3. शिकायत के प्रकार, विवरण, तात्कालिकता, और अन्य जरूरी जानकारी इकट्ठा करें
#         4. उपयोगकर्ता के जवाब के आधार पर अगला उपयुक्त प्रश्न पूछें
#         5. यदि पर्याप्त जानकारी मिल गई है तो बातचीत समाप्त करने का संकेत दें

#         शिकायत की श्रेणियां: सड़क, पानी, बिजली, सफाई, शोर, यातायात, भ्रष्टाचार, अन्य

#         JSON प्रारूप में जवाब दें:
#         {{
#             "bot_message": "आपका हिंदी संदेश यहाँ",
#             "next_step": "current_step_name",
#             "extracted_info": {{
#                 "complaint_type": "",
#                 "description": "",
#                 "urgency": "",
#                 "additional_details": ""
#             }},
#             "is_complete": false,
#             "confidence": 0.8
#         }}
#         """

#         try:
#             response = model.generate_content(system_prompt)
#             response_text = response.text.strip()
            
#             # Clean up response if it contains markdown code blocks
#             if response_text.startswith('```json'):
#                 response_text = response_text.replace('```json', '').replace('```', '').strip()
            
#             # Parse JSON response
#             gemini_response = json.loads(response_text)
#             return gemini_response
            
#         except json.JSONDecodeError as e:
#             print(f"JSON parsing error: {e}")
#             # Fallback response
#             return {
#                 "bot_message": "खेद है, कुछ तकनीकी समस्या हुई। कृपया अपनी शिकायत फिर से बताएं।",
#                 "next_step": current_step,
#                 "extracted_info": {},
#                 "is_complete": False,
#                 "confidence": 0.1
#             }
#         except Exception as e:
#             print(f"Gemini API error: {e}")
#             return {
#                 "bot_message": "माफ करें, मुझे समझने में समस्या हो रही है। कृपया फिर से बताएं।",
#                 "next_step": current_step,
#                 "extracted_info": {},
#                 "is_complete": False,
#                 "confidence": 0.1
#             }

#     def start_conversation(self, user_name, session_id):
#         """Initialize a new conversation session"""
        
#         greeting_messages = [
#             f"नमस्ते {user_name} जी! मैं आपकी शिकायत दर्ज करने में मदद करूंगा। कृपया अपनी समस्या के बारे में बताएं।",
#             f"आदाब {user_name} जी! मैं आपका शिकायत सहायक हूं। आपकी क्या समस्या है?",
#             f"प्रणाम {user_name} जी! आज आपकी कौन सी शिकायत है जिसमें मैं सहायता कर सकूं?"
#         ]
        
#         greeting = random.choice(greeting_messages)
        
#         # Initialize session data
#         self.conversation_sessions[session_id] = {
#             "user_name": user_name,
#             "step": "greeting",
#             "conversation_data": {
#                 "complaint_type": "",
#                 "description": "",
#                 "urgency": "medium",
#                 "additional_details": "",
#                 "follow_up_answers": []
#             },
#             "conversation_history": [],
#             "created_at": datetime.now().isoformat()
#         }
        
#         return {
#             "message": greeting,
#             "session_id": session_id,
#             "step": "initial_complaint"
#         }

#     def process_user_response(self, session_id, user_message, current_step=None):
#         """Process user response and generate next question using Gemini"""
        
#         if session_id not in self.conversation_sessions:
#             return {"error": "Session not found"}
        
#         session = self.conversation_sessions[session_id]
        
#         # Add user message to history
#         session["conversation_history"].append({
#             "type": "user",
#             "message": user_message,
#             "timestamp": datetime.now().isoformat()
#         })
        
#         # Get intelligent response from Gemini
#         gemini_response = self.get_gemini_response(
#             user_message, 
#             session["conversation_data"],
#             current_step or session["step"]
#         )
        
#         # Update session data with extracted information
#         if gemini_response.get("extracted_info"):
#             for key, value in gemini_response["extracted_info"].items():
#                 if value and value.strip():
#                     session["conversation_data"][key] = value
        
#         # Add follow-up answer if it's a detailed response
#         if len(user_message) > 10 and user_message not in [item.get("message", "") for item in session["conversation_history"][-5:]]:
#             session["conversation_data"]["follow_up_answers"].append(user_message)
        
#         # Update session step
#         session["step"] = gemini_response.get("next_step", session["step"])
        
#         # Add bot response to history
#         session["conversation_history"].append({
#             "type": "bot",
#             "message": gemini_response["bot_message"],
#             "timestamp": datetime.now().isoformat()
#         })
        
#         return {
#             "bot_message": gemini_response["bot_message"],
#             "next_step": gemini_response.get("next_step"),
#             "updated_data": session["conversation_data"],
#             "is_complete": gemini_response.get("is_complete", False),
#             "confidence": gemini_response.get("confidence", 0.5)
#         }

#     def get_session_data(self, session_id):
#         """Get complete session data"""
#         return self.conversation_sessions.get(session_id, {})

#     def cleanup_old_sessions(self, max_age_hours=24):
#         """Clean up old conversation sessions"""
#         current_time = datetime.now()
#         to_remove = []
        
#         for session_id, session_data in self.conversation_sessions.items():
#             created_at = datetime.fromisoformat(session_data["created_at"])
#             age_hours = (current_time - created_at).total_seconds() / 3600
            
#             if age_hours > max_age_hours:
#                 to_remove.append(session_id)
        
#         for session_id in to_remove:
#             del self.conversation_sessions[session_id]
#             print(f"Cleaned up old session: {session_id}")

# # Flask app integration
# voice_bot = ConversationalVoiceBot()

# def create_voice_bot_routes(app):
#     """Add voice bot routes to Flask app"""
    
#     @app.route('/api/voice-bot/start', methods=['POST'])
#     def start_voice_conversation():
#         try:
#             data = request.get_json()
#             user_name = data.get('user_name', 'उपयोगकर्ता')
#             session_id = str(uuid.uuid4())
            
#             result = voice_bot.start_conversation(user_name, session_id)
#             result["session_id"] = session_id
            
#             return jsonify({
#                 "success": True,
#                 "message": result["message"],
#                 "session_id": session_id,
#                 "step": result["step"]
#             })
#         except Exception as e:
#             return jsonify({"success": False, "error": str(e)}), 500

#     @app.route('/api/voice-bot/speak', methods=['POST'])
#     def speak_text():
#         try:
#             data = request.get_json()
#             text = data.get('text', '')
#             session_id = data.get('session_id', 'default')
            
#             audio_file = voice_bot.speak_hindi(text, session_id)
            
#             if audio_file:
#                 return jsonify({
#                     "success": True,
#                     "audio_file": f"/audio/{os.path.basename(audio_file)}"
#                 })
#             else:
#                 return jsonify({"success": False, "error": "TTS failed"}), 500
#         except Exception as e:
#             return jsonify({"success": False, "error": str(e)}), 500

#     @app.route('/api/voice-bot/listen', methods=['POST'])
#     def listen_user():
#         try:
#             user_text = voice_bot.listen_hindi()
            
#             return jsonify({
#                 "success": True,
#                 "user_text": user_text
#             })
#         except Exception as e:
#             return jsonify({"success": False, "error": str(e)}), 500

#     @app.route('/api/voice-bot/process', methods=['POST'])
#     def process_conversation():
#         try:
#             data = request.get_json()
#             session_id = data.get('session_id')
#             user_message = data.get('user_message', '')
#             current_step = data.get('conversation_step')
            
#             if not session_id:
#                 return jsonify({"success": False, "error": "Session ID required"}), 400
            
#             result = voice_bot.process_user_response(session_id, user_message, current_step)
            
#             if "error" in result:
#                 return jsonify({"success": False, "error": result["error"]}), 400
            
#             return jsonify({
#                 "success": True,
#                 **result
#             })
#         except Exception as e:
#             return jsonify({"success": False, "error": str(e)}), 500

#     @app.route('/api/voice-bot/session/<session_id>', methods=['GET'])
#     def get_session(session_id):
#         try:
#             session_data = voice_bot.get_session_data(session_id)
#             return jsonify({
#                 "success": True,
#                 "session_data": session_data
#             })
#         except Exception as e:
#             return jsonify({"success": False, "error": str(e)}), 500

#     @app.route('/audio/<filename>')
#     def serve_audio(filename):
#         try:
#             audio_path = os.path.join(voice_bot.audio_cache_dir, filename)
#             return send_file(audio_path, mimetype='audio/mpeg')
#         except Exception as e:
#             return jsonify({"error": str(e)}), 404

# # Standalone testing
# if __name__ == "__main__":
#     # Test the conversational bot
#     bot = ConversationalVoiceBot()
#     session_id = str(uuid.uuid4())
    
#     print("=== Testing Conversational Voice Bot ===")
    
#     # Start conversation
#     result = bot.start_conversation("राहुल", session_id)
#     print(f"Bot: {result['message']}")
    
#     # Simulate conversation
#     test_responses = [
#         "मेरे इलाके में सड़क की बहुत खराब हालत है",
#         "सड़क में बड़े-बड़े गड्ढे हैं जिससे एक्सीडेंट का डर रहता है",
#         "यह बहुत जरूरी है क्योंकि बच्चे स्कूल जाते समय परेशानी होती है",
#         "रोज सुबह शाम की समस्या है"
#     ]
    
#     for response in test_responses:
#         print(f"\nUser: {response}")
#         result = bot.process_user_response(session_id, response)
#         print(f"Bot: {result['bot_message']}")
#         print(f"Step: {result.get('next_step')}")
#         print(f"Complete: {result.get('is_complete')}")
        
#         if result.get('is_complete'):
#             print("\n=== Final Data ===")
#             print(json.dumps(result['updated_data'], indent=2, ensure_ascii=False))
#             break
        
#         time.sleep(1)  # Simulate conversation pace


# import speech_recognition as sr
# from gtts import gTTS
# import pygame
# import time
# import os
# import random
# import google.generativeai as genai
# from flask import Flask, request, jsonify, send_file
# import json
# from datetime import datetime
# import tempfile
# import uuid
# import threading
# from queue import Queue

# # Initialize pygame mixer once
# pygame.mixer.init()

# # Configure Gemini API
# genai.configure(api_key="AIzaSyBpVKC1p-ghwEjYlwVNlmJun87Ne-jSum0")  # Replace with your actual API key

# # Initialize Gemini model models/gemini-1.5-flash
# model = genai.GenerativeModel("models/gemini-2.0-flash")

# class ConversationalVoiceBot:
#     def __init__(self):
#         self.conversation_sessions = {}
#         self.audio_cache_dir = "audio_cache"
#         self.conversation_states = {}  # Track conversation state per session
#         if not os.path.exists(self.audio_cache_dir):
#             os.makedirs(self.audio_cache_dir)
    
#     def speak_hindi(self, text, session_id=None):
#         """Convert text to speech in Hindi and return audio file path"""
#         try:
#             # Cache audio files to avoid repeated TTS generation
#             filename = f"{self.audio_cache_dir}/voice_{hash(text)}_{session_id or 'default'}.mp3"
            
#             if not os.path.exists(filename):
#                 tts = gTTS(text=text, lang='hi')
#                 tts.save(filename)
            
#             return filename
#         except Exception as e:
#             print(f"⚠️ Voice Error: {e}")
#             return None

#     def listen_hindi(self, timeout=10, phrase_time_limit=15):
#         """Listen for Hindi speech and return transcribed text"""
#         r = sr.Recognizer()
#         r.energy_threshold = 300
#         r.pause_threshold = 1.5
#         r.dynamic_energy_threshold = True
        
#         with sr.Microphone() as source:
#             print("🎤 Adjusting for ambient noise...")
#             r.adjust_for_ambient_noise(source, duration=1)
#             print("🎤 सुन रहा हूँ... बोलें...")
            
#             try:
#                 audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
#                 print("🎤 ऑडियो प्राप्त हुआ, पहचान की जा रही है...")
#             except sr.WaitTimeoutError:
#                 print("⏰ समय समाप्त - कोई आवाज़ नहीं सुनी गई")
#                 return None

#         try:
#             # Try Hindi recognition first
#             text = r.recognize_google(audio, language="hi-IN")
#             print(f"✅ आपने कहा: {text}")
#             return text
#         except sr.UnknownValueError:
#             print("❌ आवाज़ समझ नहीं आई")
#             return None
#         except sr.RequestError as e:
#             print(f"❌ गूगल सेवा में त्रुटि: {e}")
#             return None

#     def get_gemini_response(self, user_message, conversation_context, current_step, conversation_history):
#         """Get intelligent response from Gemini API based on conversation context"""
        
#         # Build conversation history string
#         history_text = ""
#         if conversation_history:
#             recent_history = conversation_history[-4:]  # Last 4 exchanges
#             for msg in recent_history:
#                 role = "असिस्टेंट" if msg["type"] == "bot" else "उपयोगकर्ता"
#                 history_text += f"{role}: {msg['message']}\n"
        
#         # Create comprehensive prompt for Gemini
#         system_prompt = f"""
# आप एक बुद्धिमान शिकायत सहायक हैं जो नागरिकों की शिकायतें दर्ज करने में मदद करते हैं। 
# आपका काम है उपयोगकर्ता से प्रासंगिक प्रश्न पूछकर पूरी शिकायत की जानकारी एकत्रित करना।

# वर्तमान चरण: {current_step}

# पिछली बातचीत:
# {history_text}

# मौजूदा शिकायत डेटा: {json.dumps(conversation_context, ensure_ascii=False)}

# उपयोगकर्ता का नया जवाब: "{user_message}"

# निर्देश:
# 1. केवल हिंदी में जवाब दें
# 2. संक्षिप्त और स्पष्ट प्रश्न पूछें (अधिकतम 2-3 वाक्य)
# 3. शिकायत के प्रकार, विस्तृत विवरण, तात्कालिकता, और स्थान की जानकारी इकट्ठा करें
# 4. उपयोगकर्ता के जवाब का विश्लेषण करें और relevant जानकारी निकालें
# 5. विवरण (description) को हमेशा **बिंदुओं (•)** में लिखें, प्रत्येक बिंदु छोटा और स्पष्ट हो
# 6. यदि पर्याप्त जानकारी मिल गई है (कम से कम समस्या का प्रकार और विवरण) तो बातचीत समाप्त करने का संकेत दें
# 7. यदि उत्तर अस्पष्ट है तो स्पष्टीकरण मांगें

# शिकायत की मुख्य श्रेणियां: सड़क, पानी, बिजली, सफाई, शोर, यातायात, भ्रष्टाचार, स्वास्थ्य, शिक्षा, अन्य

# बातचीत का प्रवाह:
# - यदि यह पहला जवाब है: समस्या का प्रकार और मूल विवरण पूछें
# - यदि समस्या का प्रकार मिला: अधिक विस्तार और कब से यह समस्या है, पूछें  
# - यदि सभी मुख्य जानकारी मिली: धन्यवाद दें और बातचीत समाप्त करें

# JSON प्रारूप में जवाब दें:
# {{
#     "bot_message": "आपका हिंदी संदेश यहाँ",
#     "next_step": "अगला कदम",
#     "extracted_info": {{
#         "complaint_type": "निकाली गई शिकायत का प्रकार",
#         "description": [
#             "• बिंदु 1",
#             "• बिंदु 2",
#             "• बिंदु 3"
#         ],
#         "urgency": "कम/मध्यम/अधिक",
#         "additional_details": "अतिरिक्त जानकारी"
#     }},
#     "is_complete": false,
#     "confidence": 0.8
# }}
# """


#         try:
#             response = model.generate_content(system_prompt)
#             response_text = response.text.strip()
            
#             # Clean up response if it contains markdown code blocks
#             if response_text.startswith('```json'):
#                 response_text = response_text.replace('```json', '').replace('```', '').strip()
#             elif response_text.startswith('```'):
#                 response_text = response_text.replace('```', '').strip()
            
#             # Parse JSON response
#             gemini_response = json.loads(response_text)
#             return gemini_response
            
#         except json.JSONDecodeError as e:
#             print(f"JSON parsing error: {e}")
#             print(f"Raw response: {response_text}")
#             # Fallback response
#             return {
#                 "bot_message": "खेद है, कुछ तकनीकी समस्या हुई। कृपया अपनी शिकायत फिर से संक्षेप में बताएं।",
#                 "next_step": "retry",
#                 "extracted_info": {},
#                 "is_complete": False,
#                 "confidence": 0.1
#             }
#         except Exception as e:
#             print(f"Gemini API error: {e}")
#             return {
#                 "bot_message": "माफ करें, मुझे समझने में समस्या हो रही है। कृपया फिर से बताएं।",
#                 "next_step": "retry",
#                 "extracted_info": {},
#                 "is_complete": False,
#                 "confidence": 0.1
#             }

#     def start_conversation(self, user_name, session_id):
#         """Initialize a new conversation session"""
        
#         greeting_messages = [
#             f"नमस्ते {user_name} जी! मैं आपकी शिकायत दर्ज करने में मदद करूंगा। कृपया बताएं आपकी क्या समस्या है?",
#             f"प्रणाम {user_name} जी! मैं शिकायत सहायक हूं। आपकी कौन सी समस्या है जिसे हल करना है?",
#             f"नमस्कार {user_name} जी! आज आपकी कोई शिकायत है? कृपया विस्तार से बताएं।"
#         ]
        
#         greeting = random.choice(greeting_messages)
        
#         # Initialize session data
#         self.conversation_sessions[session_id] = {
#             "user_name": user_name,
#             "step": "initial_complaint",
#             "conversation_data": {
#                 "complaint_type": "",
#                 "description": "",
#                 "urgency": "medium",
#                 "additional_details": "",
#                 "follow_up_answers": []
#             },
#             "conversation_history": [],
#             "created_at": datetime.now().isoformat(),
#             "is_active": True,
#             "current_state": "greeting"
#         }
        
#         # Set conversation state for controlled flow
#         self.conversation_states[session_id] = {
#             "speaking": False,
#             "listening": False,
#             "waiting_for_response": True,
#             "conversation_complete": False
#         }
        
#         return {
#             "message": greeting,
#             "session_id": session_id,
#             "step": "initial_complaint"
#         }

#     def continue_conversation(self, session_id):
#         """Main conversation loop - handles speak then listen cycle"""
#         if session_id not in self.conversation_sessions:
#             return {"error": "Session not found"}
        
#         session = self.conversation_sessions[session_id]
#         state = self.conversation_states[session_id]
        
#         # If conversation is complete, don't continue
#         if state["conversation_complete"]:
#             return {"completed": True, "data": session["conversation_data"]}
        
#         try:
#             # Step 1: Get the current bot message (either greeting or generated response)
#             if session["conversation_history"]:
#                 current_bot_message = session["conversation_history"][-1]["message"]
#             else:
#                 # First greeting
#                 greeting_messages = [
#                     f"नमस्ते {session['user_name']} जी! कृपया अपनी शिकायत बताएं।",
#                 ]
#                 current_bot_message = greeting_messages[0]
#                 session["conversation_history"].append({
#                     "type": "bot",
#                     "message": current_bot_message,
#                     "timestamp": datetime.now().isoformat()
#                 })
            
#             # Step 2: Speak the bot message
#             print(f"🤖 बोल रहा हूं: {current_bot_message}")
#             state["speaking"] = True
#             audio_file = self.speak_hindi(current_bot_message, session_id)
            
#             if audio_file:
#                 # Play audio and wait for completion
#                 pygame.mixer.music.load(audio_file)
#                 pygame.mixer.music.play()
                
#                 # Wait for audio to finish playing
#                 while pygame.mixer.music.get_busy():
#                     time.sleep(0.1)
            
#             state["speaking"] = False
#             time.sleep(1)  # Small pause after speaking
            
#             # Step 3: Listen for user response
#             print("🎤 अब उपयोगकर्ता की प्रतिक्षा...")
#             state["listening"] = True
#             user_response = self.listen_hindi(timeout=15, phrase_time_limit=20)
#             state["listening"] = False
            
#             if not user_response:
#                 # No response received
#                 retry_message = "मुझे आपकी आवाज़ सुनाई नहीं दी। कृपया फिर से स्पष्ट आवाज़ में बताएं।"
#                 session["conversation_history"].append({
#                     "type": "bot",
#                     "message": retry_message,
#                     "timestamp": datetime.now().isoformat()
#                 })
                
#                 return {
#                     "success": True,
#                     "bot_message": retry_message,
#                     "user_response": None,
#                     "continue": True,
#                     "retry": True
#                 }
            
#             # Step 4: Add user response to history
#             session["conversation_history"].append({
#                 "type": "user", 
#                 "message": user_response,
#                 "timestamp": datetime.now().isoformat()
#             })
            
#             # Step 5: Process response with Gemini and get next question
#             print(f"📝 प्रोसेसिंग: {user_response}")
#             gemini_response = self.get_gemini_response(
#                 user_response,
#                 session["conversation_data"],
#                 session["step"],
#                 session["conversation_history"]
#             )
            
#             # Step 6: Update session data with extracted info
#             if gemini_response.get("extracted_info"):
#                 for key, value in gemini_response["extracted_info"].items():
#                     if value and value.strip():
#                         session["conversation_data"][key] = value
#                     elif isinstance(value, list) and value:
#                         session["conversation_data"][key] = " ".join(map(str, value))

            
#             # Add user response to follow-up answers if substantial
#             if len(user_response.strip()) > 5:
#                 session["conversation_data"]["follow_up_answers"].append(user_response)
            
#             # Update session step
#             session["step"] = gemini_response.get("next_step", session["step"])
            
#             # Step 7: Add bot's next response to history
#             next_bot_message = gemini_response["bot_message"]
#             session["conversation_history"].append({
#                 "type": "bot",
#                 "message": next_bot_message,
#                 "timestamp": datetime.now().isoformat()
#             })
            
#             # Step 8: Check if conversation is complete
#             is_complete = gemini_response.get("is_complete", False)
#             if is_complete:
#                 state["conversation_complete"] = True
#                 session["is_active"] = False
                
#                 # Compile final description
#                 final_description = self.compile_final_description(session["conversation_data"])
#                 session["conversation_data"]["compiled_description"] = final_description
            
#             return {
#                 "success": True,
#                 "bot_message": next_bot_message,
#                 "user_response": user_response,
#                 "updated_data": session["conversation_data"],
#                 "is_complete": is_complete,
#                 "continue": not is_complete,
#                 "confidence": gemini_response.get("confidence", 0.5)
#             }
            
#         except Exception as e:
#             print(f"Conversation error: {e}")
#             return {
#                 "success": False,
#                 "error": str(e),
#                 "bot_message": "खेद है, कुछ तकनीकी समस्या हुई। कृपया फिर से प्रयास करें।"
#             }

#     def compile_final_description(self, conversation_data):
#         """Compile final complaint description from conversation data"""
#         description = ""
        
#         if conversation_data.get("complaint_type"):
#             description += f"शिकायत का प्रकार: {conversation_data['complaint_type']}\n\n"
        
#         if conversation_data.get("description"):
#             description += f"समस्या का विवरण: {conversation_data['description']}\n\n"
        
#         if conversation_data.get("urgency"):
#             description += f"तात्कालिकता: {conversation_data['urgency']}\n\n"
        
#         if conversation_data.get("additional_details"):
#             description += f"अतिरिक्त जानकारी: {conversation_data['additional_details']}\n\n"
        
#         if conversation_data.get("follow_up_answers"):
#             description += "विस्तृत बातचीत:\n"
#             for i, answer in enumerate(conversation_data["follow_up_answers"], 1):
#                 description += f"{i}. {answer}\n"
        
#         return description.strip()

#     def get_session_data(self, session_id):
#         """Get complete session data"""
#         return self.conversation_sessions.get(session_id, {})

#     def get_session_state(self, session_id):
#         """Get current conversation state"""
#         return self.conversation_states.get(session_id, {})

#     def cleanup_old_sessions(self, max_age_hours=24):
#         """Clean up old conversation sessions"""
#         current_time = datetime.now()
#         to_remove = []
        
#         for session_id, session_data in self.conversation_sessions.items():
#             created_at = datetime.fromisoformat(session_data["created_at"])
#             age_hours = (current_time - created_at).total_seconds() / 3600
            
#             if age_hours > max_age_hours:
#                 to_remove.append(session_id)
        
#         for session_id in to_remove:
#             if session_id in self.conversation_sessions:
#                 del self.conversation_sessions[session_id]
#             if session_id in self.conversation_states:
#                 del self.conversation_states[session_id]
#             print(f"Cleaned up old session: {session_id}")

# # Flask app integration
# voice_bot = ConversationalVoiceBot()

# def create_voice_bot_routes(app):
#     """Add voice bot routes to Flask app"""
    
#     @app.route('/api/voice-bot/start', methods=['POST'])
#     def start_voice_conversation():
#         try:
#             data = request.get_json()
#             user_name = data.get('user_name', 'उपयोगकर्ता')
#             session_id = str(uuid.uuid4())
            
#             result = voice_bot.start_conversation(user_name, session_id)
            
#             return jsonify({
#                 "success": True,
#                 "message": result["message"],
#                 "session_id": session_id,
#                 "step": result["step"]
#             })
#         except Exception as e:
#             return jsonify({"success": False, "error": str(e)}), 500

#     @app.route('/api/voice-bot/continue/<session_id>', methods=['POST'])
#     def continue_conversation(session_id):
#         """Main endpoint that handles the complete speak->listen->process cycle"""
#         try:
#             result = voice_bot.continue_conversation(session_id)
            
#             if "error" in result:
#                 return jsonify({"success": False, "error": result["error"]}), 400
            
#             return jsonify({
#                 "success": True,
#                 **result
#             })
#         except Exception as e:
#             print(f"Continue conversation error: {e}")
#             return jsonify({"success": False, "error": str(e)}), 500

#     @app.route('/api/voice-bot/status/<session_id>', methods=['GET'])
#     def get_conversation_status(session_id):
#         """Get current conversation status"""
#         try:
#             session_data = voice_bot.get_session_data(session_id)
#             session_state = voice_bot.get_session_state(session_id)
            
#             return jsonify({
#                 "success": True,
#                 "session_data": session_data,
#                 "session_state": session_state,
#                 "exists": bool(session_data)
#             })
#         except Exception as e:
#             return jsonify({"success": False, "error": str(e)}), 500

#     @app.route('/api/voice-bot/stop/<session_id>', methods=['POST'])
#     def stop_conversation(session_id):
#         """Stop an active conversation"""
#         try:
#             if session_id in voice_bot.conversation_sessions:
#                 voice_bot.conversation_sessions[session_id]["is_active"] = False
#             if session_id in voice_bot.conversation_states:
#                 voice_bot.conversation_states[session_id]["conversation_complete"] = True
                
#             return jsonify({"success": True, "message": "Conversation stopped"})
#         except Exception as e:
#             return jsonify({"success": False, "error": str(e)}), 500

#     @app.route('/audio/<filename>')
#     def serve_audio(filename):
#         try:
#             audio_path = os.path.join(voice_bot.audio_cache_dir, filename)
#             if os.path.exists(audio_path):
#                 return send_file(audio_path, mimetype='audio/mpeg')
#             else:
#                 return jsonify({"error": "Audio file not found"}), 404
#         except Exception as e:
#             return jsonify({"error": str(e)}), 404

# # Standalone testing
# if __name__ == "__main__":
#     # Test the conversational bot
#     bot = ConversationalVoiceBot()
#     session_id = str(uuid.uuid4())
    
#     print("=== Testing Conversational Voice Bot ===")
    
#     # Start conversation
#     result = bot.start_conversation("राहुल शर्मा", session_id)
#     print(f"Start Result: {result}")
    
#     # Test conversation flow
#     for i in range(5):  # Max 5 exchanges
#         print(f"\n--- Conversation Round {i+1} ---")
#         result = bot.continue_conversation(session_id)
        
#         if result.get("error"):
#             print(f"Error: {result['error']}")
#             break
            
#         print(f"Success: {result.get('success')}")
#         print(f"Bot Message: {result.get('bot_message')}")
#         print(f"User Response: {result.get('user_response')}")
#         print(f"Complete: {result.get('is_complete')}")
        
#         if result.get('is_complete'):
#             print(f"\n=== Final Data ===")
#             print(json.dumps(result.get('updated_data'), indent=2, ensure_ascii=False))
#             break
        
#         if not result.get('continue'):
#             break
            
#         time.sleep(2)  # Pause between rounds

import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import os
import random
from flask import Flask, request, jsonify, send_file
import json
from datetime import datetime
import tempfile
import uuid
import threading
from queue import Queue
import re

# Initialize pygame mixer once
pygame.mixer.init()

class ConversationalVoiceBot:
    def __init__(self):
        self.conversation_sessions = {}
        self.audio_cache_dir = "audio_cache"
        self.conversation_states = {}  # Track conversation state per session
        if not os.path.exists(self.audio_cache_dir):
            os.makedirs(self.audio_cache_dir)
        
        # Rule-based conversation flow
        self.complaint_types = {
            'सड़क': ['सड़क', 'रोड', 'गड्ढे', 'गड्ढा', 'टूटी', 'खराब', 'पक्की'],
            'पानी': ['पानी', 'वाटर', 'नल', 'टंकी', 'लीकेज', 'गंदा', 'साफ नहीं'],
            'बिजली': ['बिजली', 'लाइट', 'करंट', 'पावर', 'कट', 'गुल', 'ट्रांसफार्मर'],
            'सफाई': ['सफाई', 'गंदगी', 'कचरा', 'कूड़ा', 'झाड़ू', 'साफ नहीं'],
            'शोर': ['शोर', 'आवाज़', 'तेज़', 'परेशानी', 'रात में', 'सोने नहीं दे'],
            'यातायात': ['ट्रैफिक', 'यातायात', 'जाम', 'गाड़ी', 'बस', 'ऑटो'],
            'भ्रष्टाचार': ['भ्रष्टाचार', 'रिश्वत', 'पैसे मांगे', 'गलत काम'],
            'स्वास्थ्य': ['अस्पताल', 'डॉक्टर', 'दवा', 'इलाज', 'स्वास्थ्य'],
            'शिक्षा': ['स्कूल', 'पढ़ाई', 'टीचर', 'शिक्षा', 'बच्चे']
        }
        
        self.urgency_keywords = {
            'अधिक': ['तुरंत', 'जल्दी', 'आपातकाल', 'बहुत परेशान', 'बहुत जरूरी', 'इमरजेंसी'],
            'मध्यम': ['जल्दी', 'परेशानी', 'समस्या', 'दिक्कत'],
            'कम': ['धीरे', 'कभी भी', 'फुर्सत में', 'जब समय मिले']
        }
        
        self.conversation_flow = {
            'initial_complaint': {
                'questions': [
                    "आपकी क्या समस्या है?",
                    "कृपया अपनी शिकायत बताएं।",
                    "आज आपकी कोई समस्या है?"
                ],
                'next_step': 'get_more_details'
            },
            'get_more_details': {
                'questions': [
                    "कुछ और विवरण बताएं।",
                    "और कोई जानकारी?",
                    "कुछ और जोड़ना चाहते हैं?"
                ],
                'next_step': 'complete'
            }
        }
    
    def speak_hindi(self, text, session_id=None):
        """Convert text to speech in Hindi and return audio file path"""
        try:
            # Cache audio files to avoid repeated TTS generation
            filename = f"{self.audio_cache_dir}/voice_{hash(text)}_{session_id or 'default'}.mp3"
            
            if not os.path.exists(filename):
                tts = gTTS(text=text, lang='hi')
                tts.save(filename)
            
            return filename
        except Exception as e:
            print(f"⚠️ Voice Error: {e}")
            return None

    def listen_hindi(self, timeout=10, phrase_time_limit=15):
        """Listen for Hindi speech and return transcribed text"""
        r = sr.Recognizer()
        r.energy_threshold = 300
        r.pause_threshold = 1.5
        r.dynamic_energy_threshold = True
        
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("🎤 सुन रहा हूँ... बोलें...")
            
            try:
                audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("🎤 ऑडियो प्राप्त हुआ, पहचान की जा रही है...")
            except sr.WaitTimeoutError:
                print("⏰ समय समाप्त - कोई आवाज़ नहीं सुनी गई")
                return None

        try:
            # Try Hindi recognition first
            text = r.recognize_google(audio, language="hi-IN")
            print(f"✅ आपने कहा: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ आवाज़ समझ नहीं आई")
            return None
        except sr.RequestError as e:
            print(f"❌ गूगल सेवा में त्रुटि: {e}")
            return None

    def extract_complaint_type(self, text):
        """Extract complaint type from user text using keyword matching"""
        text_lower = text.lower()
        
        for complaint_type, keywords in self.complaint_types.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return complaint_type
        
        return "अन्य"

    def extract_urgency(self, text):
        """Extract urgency level from user text"""
        text_lower = text.lower()
        
        for urgency_level, keywords in self.urgency_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return urgency_level
        
        return "मध्यम"

    def format_description_as_bullets(self, text):
        """Convert text to bullet points format"""
        sentences = re.split(r'[।\.\!\?]+', text.strip())
        bullets = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 3:
                bullets.append(f"• {sentence}")
        
        return bullets if bullets else [f"• {text}"]

    def get_rule_based_response(self, user_message, conversation_context, current_step, conversation_history):
        """Rule-based response generation to replace Gemini API"""
        
        # Extract information from user message
        extracted_info = {}
        
        # Determine complaint type
        if not conversation_context.get('complaint_type'):
            extracted_info['complaint_type'] = self.extract_complaint_type(user_message)
        
        # Extract description and format as bullets
        if user_message and len(user_message.strip()) > 5:
            description_bullets = self.format_description_as_bullets(user_message)
            if conversation_context.get('description'):
                if isinstance(conversation_context['description'], list):
                    existing_bullets = conversation_context['description']
                else:
                    existing_bullets = [conversation_context['description']]
                extracted_info['description'] = existing_bullets + description_bullets
            else:
                extracted_info['description'] = description_bullets
        
        # Extract urgency
        extracted_info['urgency'] = self.extract_urgency(user_message)
        
        # Add additional details
        if len(user_message.strip()) > 10:
            extracted_info['additional_details'] = user_message
        
        # Determine next step and response based on current step and information completeness
        has_complaint_type = bool(conversation_context.get('complaint_type') or extracted_info.get('complaint_type'))
        has_description = bool(conversation_context.get('description') or extracted_info.get('description'))
        conversation_length = len(conversation_history)
        
        # Determine completion status and next step
        is_complete = False
        confidence = 0.5
        
        if current_step == 'initial_complaint':
            if has_complaint_type and has_description:
                next_step = 'get_details'
                confidence = 0.8
            else:
                next_step = 'initial_complaint'
                confidence = 0.4
        elif current_step == 'get_details':
            if has_complaint_type and has_description and len(user_message.strip()) > 15:
                next_step = 'get_urgency'
                confidence = 0.8
            else:
                next_step = 'get_details'
                confidence = 0.6
        elif current_step == 'get_urgency':
            if has_complaint_type and has_description:
                next_step = 'final_confirmation'
                confidence = 0.9
            else:
                next_step = 'get_urgency'
                confidence = 0.7
        elif current_step == 'final_confirmation':
            is_complete = True
            next_step = 'complete'
            confidence = 1.0
        else:
            # If we have enough information or conversation is getting long
            if (has_complaint_type and has_description) or conversation_length >= 6:
                is_complete = True
                next_step = 'complete'
                confidence = 0.9
            else:
                next_step = 'get_details'
                confidence = 0.6
        
        # Generate appropriate bot message
        if is_complete:
            completion_messages = [
                "धन्यवाद! आपकी शिकायत सफलतापूर्वक दर्ज हो गई है। हमारी टीम इस पर काम करेगी।",
                "बहुत अच्छे! आपकी शिकायत हमें मिल गई है। जल्दी ही इसका समाधान होगा।",
                "आपकी शिकायत दर्ज हो गई है। हम इसे प्राथमिकता देंगे।"
            ]
            bot_message = random.choice(completion_messages)
        else:
            # Get appropriate question based on next step
            if next_step in self.conversation_flow:
                questions = self.conversation_flow[next_step]['questions']
                
                # Choose question based on what information we already have
                if next_step == 'get_details':
                    if not has_complaint_type:
                        bot_message = "आपकी समस्या किस बारे में है? सड़क, पानी, बिजली या कुछ और?"
                    else:
                        bot_message = random.choice([
                            "इस समस्या के बारे में और बताएं। यह कहाँ है?",
                            "इसकी और जानकारी दें। कब से यह समस्या है?"
                        ])
                elif next_step == 'get_urgency':
                    bot_message = random.choice([
                        "यह कितनी जल्दी हल करनी है? क्या बहुत जरूरी है?",
                        "इस समस्या की तात्कालिकता कैसी है?"
                    ])
                elif next_step == 'initial_complaint':
                    if not user_message or len(user_message.strip()) < 10:
                        bot_message = "कृपया अपनी समस्या के बारे में थोड़ा और विस्तार से बताएं।"
                    else:
                        bot_message = "आपकी और कोई जानकारी है जो मुझे बतानी हो?"
                else:
                    bot_message = random.choice(questions)
            else:
                bot_message = "कृपया अपनी समस्या के बारे में बताएं।"
        
        return {
            "bot_message": bot_message,
            "next_step": next_step,
            "extracted_info": extracted_info,
            "is_complete": is_complete,
            "confidence": confidence
        }

    def start_conversation(self, user_name, session_id):
        """Initialize a new conversation session"""
        
        greeting_messages = [
            f"नमस्ते {user_name} जी! मैं आपकी शिकायत दर्ज करने में मदद करूंगा। कृपया बताएं आपकी क्या समस्या है?",
            f"प्रणाम {user_name} जी! मैं शिकायत सहायक हूं। आपकी कौन सी समस्या है जिसे हल करना है?",
            f"नमस्कार {user_name} जी! आज आपकी कोई शिकायत है? कृपया विस्तार से बताएं।"
        ]
        
        greeting = random.choice(greeting_messages)
        
        # Initialize session data
        self.conversation_sessions[session_id] = {
            "user_name": user_name,
            "step": "initial_complaint",
            "conversation_data": {
                "complaint_type": "",
                "description": "",
                "urgency": "medium",
                "additional_details": "",
                "follow_up_answers": []
            },
            "conversation_history": [],
            "created_at": datetime.now().isoformat(),
            "is_active": True,
            "current_state": "greeting"
        }
        
        # Set conversation state for controlled flow
        self.conversation_states[session_id] = {
            "speaking": False,
            "listening": False,
            "waiting_for_response": True,
            "conversation_complete": False
        }
        
        return {
            "message": greeting,
            "session_id": session_id,
            "step": "initial_complaint"
        }

    def continue_conversation(self, session_id):
        """Main conversation loop - handles speak then listen cycle"""
        if session_id not in self.conversation_sessions:
            return {"error": "Session not found"}
        
        session = self.conversation_sessions[session_id]
        state = self.conversation_states[session_id]
        
        # If conversation is complete, don't continue
        if state["conversation_complete"]:
            return {"completed": True, "data": session["conversation_data"]}
        
        try:
            # Step 1: Get the current bot message (either greeting or generated response)
            if session["conversation_history"]:
                current_bot_message = session["conversation_history"][-1]["message"]
            else:
                # First greeting
                greeting_messages = [
                    f"नमस्ते {session['user_name']} जी! कृपया अपनी शिकायत बताएं।",
                ]
                current_bot_message = greeting_messages[0]
                session["conversation_history"].append({
                    "type": "bot",
                    "message": current_bot_message,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Step 2: Speak the bot message
            print(f"🤖 बोल रहा हूं: {current_bot_message}")
            state["speaking"] = True
            audio_file = self.speak_hindi(current_bot_message, session_id)
            
            if audio_file:
                # Play audio and wait for completion
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                # Wait for audio to finish playing
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            
            state["speaking"] = False
            time.sleep(1)  # Small pause after speaking
            
            # Step 3: Listen for user response
            print("🎤 अब उपयोगकर्ता की प्रतिक्षा...")
            state["listening"] = True
            user_response = self.listen_hindi(timeout=15, phrase_time_limit=20)
            state["listening"] = False
            
            if not user_response:
                # No response received
                retry_message = "मुझे आपकी आवाज़ सुनाई नहीं दी। कृपया फिर से स्पष्ट आवाज़ में बताएं।"
                session["conversation_history"].append({
                    "type": "bot",
                    "message": retry_message,
                    "timestamp": datetime.now().isoformat()
                })
                
                return {
                    "success": True,
                    "bot_message": retry_message,
                    "user_response": None,
                    "continue": True,
                    "retry": True
                }
            
            # Step 4: Add user response to history
            session["conversation_history"].append({
                "type": "user", 
                "message": user_response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Step 5: Process response with rule-based system (replacing Gemini)
            print(f"📝 प्रोसेसिंग: {user_response}")
            rule_based_response = self.get_rule_based_response(
                user_response,
                session["conversation_data"],
                session["step"],
                session["conversation_history"]
            )
            
            # Step 6: Update session data with extracted info
            if rule_based_response.get("extracted_info"):
                for key, value in rule_based_response["extracted_info"].items():
                    if value and value != "":
                        if isinstance(value, list) and value:
                            session["conversation_data"][key] = value
                        elif not isinstance(value, list) and str(value).strip():
                            session["conversation_data"][key] = value

            
            # Add user response to follow-up answers if substantial
            if len(user_response.strip()) > 5:
                session["conversation_data"]["follow_up_answers"].append(user_response)
            
            # Update session step
            session["step"] = rule_based_response.get("next_step", session["step"])
            
            # Step 7: Add bot's next response to history
            next_bot_message = rule_based_response["bot_message"]
            session["conversation_history"].append({
                "type": "bot",
                "message": next_bot_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Step 8: Check if conversation is complete
            is_complete = rule_based_response.get("is_complete", False)
            if is_complete:
                state["conversation_complete"] = True
                session["is_active"] = False
                
                # Compile final description
                final_description = self.compile_final_description(session["conversation_data"])
                session["conversation_data"]["compiled_description"] = final_description
            
            return {
                "success": True,
                "bot_message": next_bot_message,
                "user_response": user_response,
                "updated_data": session["conversation_data"],
                "is_complete": is_complete,
                "continue": not is_complete,
                "confidence": rule_based_response.get("confidence", 0.5)
            }
            
        except Exception as e:
            print(f"Conversation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "bot_message": "खेद है, कुछ तकनीकी समस्या हुई। कृपया फिर से प्रयास करें।"
            }

    def compile_final_description(self, conversation_data):
        """Compile final complaint description from conversation data"""
        description = ""
        
        if conversation_data.get("complaint_type"):
            description += f"शिकायत का प्रकार: {conversation_data['complaint_type']}\n\n"
        
        if conversation_data.get("description"):
            if isinstance(conversation_data["description"], list):
                description += "समस्या का विवरण:\n"
                for bullet in conversation_data["description"]:
                    description += f"{bullet}\n"
                description += "\n"
            else:
                description += f"समस्या का विवरण: {conversation_data['description']}\n\n"
        
        if conversation_data.get("urgency"):
            description += f"तात्कालिकता: {conversation_data['urgency']}\n\n"
        
        if conversation_data.get("additional_details"):
            description += f"अतिरिक्त जानकारी: {conversation_data['additional_details']}\n\n"
        
        if conversation_data.get("follow_up_answers"):
            description += "विस्तृत बातचीत:\n"
            for i, answer in enumerate(conversation_data["follow_up_answers"], 1):
                description += f"{i}. {answer}\n"
        
        return description.strip()

    def get_session_data(self, session_id):
        """Get complete session data"""
        return self.conversation_sessions.get(session_id, {})

    def get_session_state(self, session_id):
        """Get current conversation state"""
        return self.conversation_states.get(session_id, {})

    def cleanup_old_sessions(self, max_age_hours=24):
        """Clean up old conversation sessions"""
        current_time = datetime.now()
        to_remove = []
        
        for session_id, session_data in self.conversation_sessions.items():
            created_at = datetime.fromisoformat(session_data["created_at"])
            age_hours = (current_time - created_at).total_seconds() / 3600
            
            if age_hours > max_age_hours:
                to_remove.append(session_id)
        
        for session_id in to_remove:
            if session_id in self.conversation_sessions:
                del self.conversation_sessions[session_id]
            if session_id in self.conversation_states:
                del self.conversation_states[session_id]
            print(f"Cleaned up old session: {session_id}")

# Flask app integration
voice_bot = ConversationalVoiceBot()

def create_voice_bot_routes(app):
    """Add voice bot routes to Flask app"""
    
    @app.route('/api/voice-bot/start', methods=['POST'])
    def start_voice_conversation():
        try:
            data = request.get_json()
            user_name = data.get('user_name', 'उपयोगकर्ता')
            session_id = str(uuid.uuid4())
            
            result = voice_bot.start_conversation(user_name, session_id)
            
            return jsonify({
                "success": True,
                "message": result["message"],
                "session_id": session_id,
                "step": result["step"]
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/voice-bot/continue/<session_id>', methods=['POST'])
    def continue_conversation(session_id):
        """Main endpoint that handles the complete speak->listen->process cycle"""
        try:
            result = voice_bot.continue_conversation(session_id)
            
            if "error" in result:
                return jsonify({"success": False, "error": result["error"]}), 400
            
            return jsonify({
                "success": True,
                **result
            })
        except Exception as e:
            print(f"Continue conversation error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/voice-bot/status/<session_id>', methods=['GET'])
    def get_conversation_status(session_id):
        """Get current conversation status"""
        try:
            session_data = voice_bot.get_session_data(session_id)
            session_state = voice_bot.get_session_state(session_id)
            
            return jsonify({
                "success": True,
                "session_data": session_data,
                "session_state": session_state,
                "exists": bool(session_data)
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/voice-bot/stop/<session_id>', methods=['POST'])
    def stop_conversation(session_id):
        """Stop an active conversation"""
        try:
            if session_id in voice_bot.conversation_sessions:
                voice_bot.conversation_sessions[session_id]["is_active"] = False
            if session_id in voice_bot.conversation_states:
                voice_bot.conversation_states[session_id]["conversation_complete"] = True
                
            return jsonify({"success": True, "message": "Conversation stopped"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/audio/<filename>')
    def serve_audio(filename):
        try:
            audio_path = os.path.join(voice_bot.audio_cache_dir, filename)
            if os.path.exists(audio_path):
                return send_file(audio_path, mimetype='audio/mpeg')
            else:
                return jsonify({"error": "Audio file not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 404

# Standalone testing
if __name__ == "__main__":
    # Test the conversational bot
    bot = ConversationalVoiceBot()
    session_id = str(uuid.uuid4())
    
    print("=== Testing Rule-Based Conversational Voice Bot ===")
    
    # Start conversation
    result = bot.start_conversation("राहुल शर्मा", session_id)
    print(f"Start Result: {result}")
    
    # Test conversation flow
    for i in range(5):  # Max 5 exchanges
        print(f"\n--- Conversation Round {i+1} ---")
        result = bot.continue_conversation(session_id)
        
        if result.get("error"):
            print(f"Error: {result['error']}")
            break
            
        print(f"Success: {result.get('success')}")
        print(f"Bot Message: {result.get('bot_message')}")
        print(f"User Response: {result.get('user_response')}")
        print(f"Complete: {result.get('is_complete')}")
        
        if result.get('is_complete'):
            print(f"\n=== Final Data ===")
            print(json.dumps(result.get('updated_data'), indent=2, ensure_ascii=False))
            break
        
        if not result.get('continue'):
            break
            
        time.sleep(2)  # Pause between rounds