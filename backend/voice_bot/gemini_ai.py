# # import google.generativeai as genai
# # import json
# # import re
# # from dotenv import load_dotenv
# # import os

# # load_dotenv()
# # API_KEY = os.getenv("AIzaSyDUClq0SgIcsHqjtQzpHpr7FcPkyVQMWOM")
# # genai.configure(api_key=API_KEY)
# # model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# # PROMPT_TEMPLATE = """
# # तुम एक स्मार्ट नागरिक शिकायत प्रणाली हो...  # shortened for brevity
# # Conversation:
# # {conversation_log}
# # """


# # def ask_gemini_followup_or_result(conversation_log):
# #     prompt = PROMPT_TEMPLATE.format(conversation_log=conversation_log)
# #     response = model.generate_content(prompt)
# #     text = response.text.strip()
# #     print("🔁 Gemini Response:", text)
# #     return text


# # def is_structured_json(text):
# #     try:
# #         match = re.search(r"\{[\s\S]*\}", text)
# #         if match:
# #             parsed = json.loads(match.group())
# #             if "शिकायत" in parsed:
# #                 return parsed
# #     except json.JSONDecodeError:
# #         return None
# #     return None

# # import google.generativeai as genai
# # import json
# # import re

# # # ✅ Use your API key directly
# # #AIzaSyDQ8agyfEwaijZ0VpByd1I71cnzIuKuXvc
# # #AIzaSyDUClq0SgIcsHqjtQzpHpr7FcPkyVQMWOM
# # API_KEY = "AIzaSyDQ8agyfEwaijZ0VpByd1I71cnzIuKuXvc"
# # genai.configure(api_key=API_KEY)

# # # Gemini model
# # model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# # # ✅ Only ONE correct version of this function
# # def ask_gemini_followup_or_result(conversation_log):
# #     prompt = f"""
# #     तुम एक नागरिक सहायता बोट हो जो यूज़र से क्रमशः एक-एक कर के जानकारी लेती हो।

# #     अभी तक की बातचीत:
# #     {conversation_log}

# #     अब जो जानकारी नहीं ली गई है, केवल उसका अगला सवाल पूछो।
# #     यदि सभी ज़रूरी जानकारी मिल चुकी है, तो कृपया एक JSON उत्तर दो जिसमें ये फ़ील्ड हों:
# #     {{
# #       "शिकायत": "...",
# #       "स्थान": "...",
# #       "शिकायतकर्ता का नाम": "...",
# #       "मोबाइल नंबर": "...",
# #       "बोलने_लायक_सारांश": "...",
# #       "अंतिम_घोषणा": "...",
# #       "विभाग": "..."
# #     }}
# #     """
# #     response = model.generate_content(prompt)
# #     text = response.text.strip()
# #     print("🤖 Gemini Response:", text)  # Optional for debugging
# #     return text

# # # ✅ JSON detection logic
# # def is_structured_json(text):
# #     try:
# #         match = re.search(r"\{[\s\S]*\}", text)
# #         if match:
# #             parsed = json.loads(match.group())
# #             if "शिकायत" in parsed:
# #                 return parsed
# #     except json.JSONDecodeError:
# #         return None
# #     return None



# import google.generativeai as genai
# import json
# import re
# import time
# from datetime import datetime

# # ✅ Use your API key directly
# API_KEY = "AIzaSyDQ8agyfEwaijZ0VpByd1I71cnzIuKuXvc"
# genai.configure(api_key=API_KEY)

# # Gemini model
# model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# # Cache for reducing API calls
# response_cache = {}


# def generate_complaint_id():
#     """Generate unique complaint ID"""
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     return f"CMP-{timestamp}"


# def get_department_from_complaint(complaint_text):
#     """Simple rule-based department detection to save API calls"""
#     complaint_lower = complaint_text.lower()
    
#     # Road related
#     if any(word in complaint_lower for word in ["सड़क", "गड्ढा", "road", "street", "pothole"]):
#         return "सड़क विभाग"
    
#     # Water related
#     elif any(word in complaint_lower for word in ["पानी", "नल", "water", "tap", "pipe"]):
#         return "जल विभाग"
    
#     # Electricity related
#     elif any(word in complaint_lower for word in ["बिजली", "light", "electricity", "power"]):
#         return "विद्युत विभाग"
    
#     # Sanitation related
#     elif any(word in complaint_lower for word in ["कूड़ा", "गंदगी", "garbage", "waste", "cleaning"]):
#         return "स्वच्छता विभाग"
    
#     # Health related
#     elif any(word in complaint_lower for word in ["अस्पताल", "doctor", "health", "medical"]):
#         return "स्वास्थ्य विभाग"
    
#     # Education related
#     elif any(word in complaint_lower for word in ["स्कूल", "school", "education", "teacher"]):
#         return "शिक्षा विभाग"
    
#     # Default
#     else:
#         return "सामान्य प्रशासन"


# def ask_gemini_followup_or_result(conversation_log):
#     """
#     Simplified version - only use AI for complex cases
#     This saves API quota for your free account
#     """
    
#     # Check cache first
#     cache_key = hash(conversation_log)
#     if cache_key in response_cache:
#         return response_cache[cache_key]
    
#     # Simple prompt to save tokens
#     prompt = f"""
#     बातचीत: {conversation_log}
    
#     अगला सवाल पूछो या JSON बनाओ:
#     {{
#       "शिकायत": "...",
#       "स्थान": "...",
#       "शिकायतकर्ता का नाम": "...",
#       "मोबाइल नंबर": "...",
#       "विभाग": "..."
#     }}
#     """
    
#     try:
#         response = model.generate_content(prompt)
#         text = response.text.strip()
        
#         # Cache the response
#         response_cache[cache_key] = text
        
#         print("🤖 Gemini Response:", text[:100] + "..." if len(text) > 100 else text)
#         return text
        
#     except Exception as e:
#         print(f"❌ Gemini API Error: {e}")
#         # Fallback response
#         return "कृपया अपनी समस्या के बारे में और बताएं।"


# def ask_smart_followup(current_data, missing_fields):
#     """
#     Smart followup questions without using API
#     This saves your quota significantly
#     """
    
#     if "शिकायत" in missing_fields:
#         return "आपकी मुख्य समस्या क्या है? कृपया विस्तार से बताएं।"
    
#     elif "स्थान" in missing_fields:
#         return "यह समस्या कहाँ हो रही है? कृपया पूरा पता बताएं।"
    
#     elif "शिकायतकर्ता का नाम" in missing_fields:
#         return "आपका नाम क्या है?"
    
#     elif "मोबाइल नंबर" in missing_fields:
#         return "कृपया अपना मोबाइल नंबर बताएं ताकि हम आपसे संपर्क कर सकें।"
    
#     else:
#         # All info collected, create final JSON
#         department = get_department_from_complaint(current_data.get("शिकायत", ""))
        
#         final_data = {
#             "शिकायत": current_data.get("शिकायत", ""),
#             "स्थान": current_data.get("स्थान", ""),
#             "शिकायतकर्ता का नाम": current_data.get("शिकायतकर्ता का नाम", ""),
#             "मोबाइल नंबर": current_data.get("मोबाइल नंबर", ""),
#             "विभाग": department,
#             "complaint_id": generate_complaint_id(),
#             "बोलने_लायक_सारांश": f"आपकी शिकायत {department} को भेजी जा रही है।",
#             "अंतिम_घोषणा": "आपकी शिकायत सफलतापूर्वक दर्ज हो गई है। धन्यवाद!"
#         }
        
#         return json.dumps(final_data, ensure_ascii=False)


# def is_structured_json(text):
#     """Enhanced JSON detection logic"""
#     try:
#         # Look for JSON pattern
#         match = re.search(r"\{[\s\S]*\}", text)
#         if match:
#             json_str = match.group()
#             parsed = json.loads(json_str)
            
#             # Check if it's a complaint JSON
#             if "शिकायत" in parsed or "complaint" in str(parsed).lower():
#                 return parsed
                
#         # Try to parse the entire text as JSON
#         parsed = json.loads(text)
#         if isinstance(parsed, dict) and "शिकायत" in parsed:
#             return parsed
            
#     except (json.JSONDecodeError, AttributeError):
#         pass
    
#     return None


# def validate_phone_number(phone):
#     """Simple phone number validation"""
#     import re
#     # Remove spaces and common characters
#     phone = re.sub(r'[^\d]', '', phone)
    
#     # Check if it's a valid Indian mobile number
#     if len(phone) == 10 and phone.startswith(('6', '7', '8', '9')):
#         return True
#     elif len(phone) == 13 and phone.startswith('91'):
#         return True
    
#     return False


# def create_final_complaint(complaint_data):
#     """Create final complaint JSON with all validations"""
    
#     # Validate required fields
#     required_fields = ["शिकायत", "स्थान", "शिकायतकर्ता का नाम", "मोबाइल नंबर"]
    
#     for field in required_fields:
#         if not complaint_data.get(field, "").strip():
#             return None
    
#     # Validate phone number
#     if not validate_phone_number(complaint_data["मोबाइल नंबर"]):
#         return None
    
#     # Get department
#     department = get_department_from_complaint(complaint_data["शिकायत"])
    
#     # Create final structure
#     final_complaint = {
#         "complaint_id": generate_complaint_id(),
#         "शिकायत": complaint_data["शिकायत"].strip(),
#         "स्थान": complaint_data["स्थान"].strip(),
#         "शिकायतकर्ता का नाम": complaint_data["शिकायतकर्ता का नाम"].strip(),
#         "मोबाइल नंबर": complaint_data["मोबाइल नंबर"].strip(),
#         "विभाग": department,
#         "timestamp": datetime.now().isoformat(),
#         "status": "दर्ज",
#         "priority": "medium",
#         "बोलने_लायक_सारांश": f"आपकी शिकायत संख्या {generate_complaint_id()[:8]} दर्ज हो गई है। यह {department} को भेजी जा रही है।",
#         "अंतिम_घोषणा": "आपकी शिकायत सफलतापूर्वक दर्ज हो गई है। जल्द ही कार्रवाई की जाएगी। धन्यवाद!"
#     }
    
#     return final_complaint


import google.generativeai as genai
import json
import re
import time
from datetime import datetime

# Configure Gemini API
API_KEY = "AIzaSyDQ8agyfEwaijZ0VpByd1I71cnzIuKuXvgfc" 
#AIzaSyDQ8agyfEwaijZ0VpByd1I71cnzIuKuXvc
genai.configure(api_key=API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 1000,
    }
)

# Cache for reducing API calls
response_cache = {}



def ask_gemini_for_followup(conversation_text, initial_complaint):
    """Ask Gemini to generate intelligent follow-up questions"""
    
    # Create cache key
    cache_key = hash(conversation_text + initial_complaint)
    if cache_key in response_cache:
        return response_cache[cache_key]
    
    prompt = f"""
तुम एक सरकारी शिकायत सहायक हो। नागरिक की शिकायत को समझने के लिए बुद्धिमानी से अगला सवाल पूछो।

मुख्य शिकायत: {initial_complaint}

अब तक की बातचीत:
{conversation_text}

निर्देश:
1. अगर जरूरी जानकारी मिल गई है तो "COMPLETE" लिखो
2. अगर और जानकारी चाहिए तो एक स्पष्ट, व्यावहारिक सवाल पूछो
3. सिर्फ हिंदी में जवाब दो
4. बहुत लंबा सवाल न पूछो

अगला सवाल:"""

    try:
        response = model.generate_content(prompt)
        follow_up = response.text.strip()
        
        # Cache the response
        response_cache[cache_key] = follow_up
        
        print(f"🤖 Gemini Follow-up: {follow_up}")
        return follow_up
        
    except Exception as e:
        print(f"❌ Gemini Follow-up Error: {e}")
        # Fallback questions
        fallback_questions = [
            
            "यह समस्या कितने दिनों से चल रही है?",
            "इससे कितने लोग प्रभावित हैं?",
            "क्या आपने पहले इस समस्या के लिए किसी से संपर्क किया है?",

        ]
        
        import random
        return random.choice(fallback_questions)


def analyze_complaint_with_gemini(conversation_text):
    """Use Gemini to analyze the full conversation and extract structured data"""
    
    prompt = f"""
तुम एक सरकारी शिकायत विश्लेषक हो। इस बातचीत से जानकारी निकालकर JSON format में दो।

बातचीत:
{conversation_text}

निम्नलिखित JSON format में जवाब दो:
{{
    "department": "विभाग का नाम",
    "priority": "urgency level",
    "description": "समस्या का पूरा विवरण "
}}

विभाग के विकल्प:
- जल विभाग (पानी, नल, पाइप की समस्या)
- विद्युत विभाग (बिजली, लाइट की समस्या) 
- सड़क विभाग (सड़क, गड्ढे की समस्या)
- स्वच्छता विभाग (कूड़ा, गंदगी की समस्या)
- स्वास्थ्य विभाग (अस्पताल, डॉक्टर की समस्या)
- शिक्षा विभाग (स्कूल, शिक्षा की समस्या)
- सामान्य प्रशासन (अन्य समस्याएं)

Priority के विकल्प: "low", "medium", "high"

सिर्फ JSON में जवाब दो, कुछ और न लिखो।"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        print(f"🤖 Gemini Analysis Response: {response_text}")
        
        # Extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            json_str = json_match.group()
            try:
                analysis_data = json.loads(json_str)
                print(f"✅ Parsed Analysis: {analysis_data}")
                return analysis_data
            except json.JSONDecodeError as e:
                print(f"❌ JSON Parse Error: {e}")
                return None
        else:
            print("❌ No JSON found in response")
            return None
            
    except Exception as e:
        print(f"❌ Gemini Analysis Error: {e}")
        return None


def is_conversation_complete(conversation_text, current_data):
    """Check if enough information has been gathered"""
    
    prompt = f"""
इस बातचीत को देखकर बताओ कि क्या शिकायत दर्ज करने के लिए पर्याप्त जानकारी मिल गई है।

बातचीत:
{conversation_text}

वर्तमान डेटा:
शिकायत: {current_data.get('complaint', '')}

सिर्फ "YES" या "NO" में जवाब दो।
YES - अगर मुख्य समस्या स्पष्ट है और बुनियादी जानकारी मिल गई है
NO - अगर और जानकारी की जरूरत है"""

    try:
        response = model.generate_content(prompt)
        result = response.text.strip().upper()
        
        print(f"🤖 Conversation Complete Check: {result}")
        return result == "YES"
        
    except Exception as e:
        print(f"❌ Completion Check Error: {e}")
        # Fallback logic - check if we have basic info
        return len(conversation_text) > 200 and current_data.get('complaint', '')


def create_conversation_summary(conversation_history):
    """Create a summary of the conversation for the admin dashboard"""
    
    if not conversation_history:
        return "कोई बातचीत रिकॉर्ड नहीं मिली।"
    
    # Format conversation for summary
    conversation_text = "\n".join([
        f"{entry['speaker']}: {entry['message']}" 
        for entry in conversation_history
    ])
    
    prompt = f"""
इस बातचीत का एक संक्षिप्त सारांश तैयार करो जो admin dashboard में दिखाया जा सके।

बातचीत:
{conversation_text}

सारांश में शामिल करो:
1. मुख्य समस्या क्या है
2. कोई महत्वपूर्ण विवरण
3. उपयोगकर्ता की प्रतिक्रिया

50 शब्दों में हिंदी में लिखो।"""

    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        
        print(f"📝 Conversation Summary: {summary[:100]}...")
        return summary
        
    except Exception as e:
        print(f"❌ Summary Error: {e}")
        # Fallback summary
        user_messages = [entry['message'] for entry in conversation_history if entry['speaker'] == 'User']
        if user_messages:
            return f"उपयोगकर्ता की मुख्य शिकायत: {user_messages[0]}\n\nकुल संदेश: {len(conversation_history)}"
        else:
            return "वॉइस शिकायत - बातचीत का सारांश उपलब्ध नहीं।"


def get_department_and_priority(complaint_text):
    """Get department and priority using Gemini (fallback function)"""
    
    prompt = f"""
इस शिकायत को देखकर सही विभाग और priority बताओ।

शिकायत: {complaint_text}

JSON format में जवाब दो:
{{
    "department": "विभाग का नाम",
    "priority": "low/medium/high"
}}

विभाग के विकल्प:
- जल विभाग
- विद्युत विभाग  
- सड़क विभाग
- स्वच्छता विभाग
- स्वास्थ्य विभाग
- शिक्षा विभाग
- सामान्य प्रशासन"""

    try:
        response = model.generate_content(prompt)
        json_match = re.search(r'\{[\s\S]*\}', response.text)
        
        if json_match:
            return json.loads(json_match.group())
        else:
            return {"department": "सामान्य प्रशासन", "priority": "medium"}
            
    except Exception as e:
        print(f"❌ Department/Priority Error: {e}")
        return {"department": "सामान्य प्रशासन", "priority": "medium"}


def validate_phone_number(phone_str):
    """Enhanced phone number validation"""
    if not phone_str:
        return False
    
    # Remove all non-digit characters
    phone = re.sub(r'[^\d]', '', str(phone_str))
    
    # Check various Indian phone number patterns
    if len(phone) == 10 and phone[0] in '6789':
        return True
    elif len(phone) == 11 and phone.startswith('0') and phone[1] in '6789':
        return True
    elif len(phone) == 12 and phone.startswith('91') and phone[2] in '6789':
        return True
    elif len(phone) == 13 and phone.startswith('+91') and phone[3] in '6789':
        return True
    
    return False


def clean_phone_number(phone_str):
    """Clean and format phone number"""
    if not phone_str:
        return ""
    
    phone = re.sub(r'[^\d]', '', str(phone_str))
    
    if len(phone) == 10:
        return phone
    elif len(phone) == 11 and phone.startswith('0'):
        return phone[1:]
    elif len(phone) == 12 and phone.startswith('91'):
        return phone[2:]
    elif len(phone) == 13 and phone.startswith('+91'):
        return phone[3:]
    
    return phone


# Test function for debugging
def test_gemini_connection():
    """Test if Gemini API is working"""
    try:
        test_prompt = "हिंदी में 'Hello' लिखो।"
        response = model.generate_content(test_prompt)
        print(f"✅ Gemini Test Success: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Gemini Test Failed: {e}")
        return False


if __name__ == "__main__":
    # Test the connection
    print("🧪 Testing Gemini AI connection...")
    test_gemini_connection()
    
    # Test analysis function
    sample_conversation = """
उपयोगकर्ता: मेरे इलाके में पानी नहीं आ रहा पिछले 5 दिनों से
बॉट: यह समस्या कहाँ हो रही है?
उपयोगकर्ता: गली नंबर 15, सेक्टर 21, नोएडा में
बॉट: आपका नाम क्या है?
उपयोगकर्ता: राज कुमार, मोबाइल नंबर 9876543210
"""
    
    print("\n🧪 Testing conversation analysis...")
    result = analyze_complaint_with_gemini(sample_conversation)
    print(f"Analysis Result: {result}")