# from flask import send_from_directory, Blueprint, request, jsonify, session
# from config import complaints_collection
# from utils.generate_id import generate_complaint_id, generate_token
# import datetime
# import os
# import traceback
# import logging

# # Setup logging
# logger = logging.getLogger(__name__)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# complaint_routes = Blueprint("complaint_routes", __name__)

# # Check if database is available
# def is_database_available():
#     """Check if MongoDB is available"""
#     return complaints_collection is not None

# # ------------------ Serve uploaded files ------------------
# @complaint_routes.route('/uploads/<filename>')
# def uploaded_file(filename):
#     """
#     Serves files from the UPLOAD_FOLDER directory.
#     """
#     return send_from_directory(UPLOAD_FOLDER, filename)

# # ------------------ Helper for safe float conversion ------------------
# def _to_float(v):
#     """
#     Converts a value to a float, returning None on failure.
#     """
#     try:
#         if v is None:
#             return None
#         if isinstance(v, (int, float)):
#             return float(v)
#         s = str(v).strip()
#         if s == "" or s.lower() == "null":
#             return None
#         return float(s)
#     except (ValueError, TypeError):
#         return None

# # ------------------ Unified Complaint Submission Endpoint ------------------
# @complaint_routes.route("/api/complaint", methods=["POST"])
# def submit_complaint():
#     """
#     Handles both text-based and voice/photo-based complaint submissions.
#     """
#     try:
#         complaint_id = generate_complaint_id()
#         token = generate_token()
        
#         # Determine if the request is for file upload or JSON data
#         if request.content_type and request.content_type.startswith("multipart/form-data"):
#             # This handles voice/photo complaints
#             complaint_data = request.form
#             voice_file = request.files.get("voice")
#             photo_file = request.files.get("photo")
#             complaint_type = "voice" if voice_file else "text"
            
#             # Save files if they exist
#             voice_path = None
#             if voice_file:
#                 save_path = os.path.join(UPLOAD_FOLDER, f"{complaint_id}.wav")
#                 voice_file.save(save_path)
#                 voice_path = f"/uploads/{complaint_id}.wav"
            
#             photo_url = None
#             if photo_file:
#                 photo_filename = f"{complaint_id}_{photo_file.filename}"
#                 photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
#                 photo_file.save(photo_path)
#                 photo_url = f"/uploads/{photo_filename}"
            
#             complaint = {
#                 "id": complaint_id,
#                 "token": token,
#                 "type": complaint_type,
#                 "name": complaint_data.get("name"),
#                 "location": complaint_data.get("location"),
#                 "latitude": _to_float(complaint_data.get("latitude")),
#                 "longitude": _to_float(complaint_data.get("longitude")),
#                 "department": complaint_data.get("department"),
#                 "urgency": complaint_data.get("urgency"),
#                 "description": complaint_data.get("description"),
#                 "timestamp": datetime.datetime.utcnow(),
#                 "status": "Pending",
#                 "voice_path": voice_path,
#                 "photoUrl": photo_url
#             }

#         else:
#             # This handles JSON data complaints
#             complaint_data = request.json
#             if not all(k in complaint_data for k in ["name", "description", "location", "urgency", "department"]):
#                 return jsonify({"success": False, "message": "Missing one or more required fields."}), 400

#             complaint = {
#                 "id": complaint_id,
#                 "token": token,
#                 "type": "text",
#                 "name": complaint_data.get("name"),
#                 "location": complaint_data.get("location"),
#                 "latitude": _to_float(complaint_data.get("latitude")),
#                 "longitude": _to_float(complaint_data.get("longitude")),
#                 "department": complaint_data.get("department"),
#                 "urgency": complaint_data.get("urgency"),
#                 "description": complaint_data.get("description"),
#                 "timestamp": datetime.datetime.utcnow(),
#                 "status": "Pending"
#             }

#         # Check if database is available
#         if not is_database_available():
#             logger.warning("Database not available - complaint not saved")
#             return jsonify({
#                 "success": True,
#                 "complaintId": complaint_id,
#                 "token": token,
#                 "message": "Complaint processed but not saved (database unavailable)"
#             }), 201

#         inserted = complaints_collection.insert_one(complaint)
        
#         # We'll return the complaint ID and a token for client-side use
#         return jsonify({
#             "success": True,
#             "complaintId": complaint_id,
#             "token": str(inserted.inserted_id)
#         }), 201

#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({"success": False, "message": "Submission failed.", "error": str(e)}), 500

# # ------------------ Women & Child Complaint ------------------
# @complaint_routes.route("/api/complaint/women-child", methods=["POST"])
# def submit_women_child_complaint():
#     """
#     Dedicated endpoint for Women & Child complaints.
#     """
#     try:
#         complaint_id = generate_complaint_id()
#         token = generate_token()

#         # Determine if the request is for file upload or JSON data
#         if request.content_type and request.content_type.startswith("multipart/form-data"):
#             complaint_data = request.form
#             voice_file = request.files.get("voice")
#             photo_file = request.files.get("photo")
#             complaint_type = "voice" if voice_file else "text"

#             # Log received data for debugging
#             logger.info(f"Received women-child complaint data: {dict(complaint_data)}")
#             logger.info(f"Complaint text received: '{complaint_data.get('text', 'NOT_FOUND')}'")

#             voice_path = None
#             if voice_file:
#                 save_path = os.path.join(UPLOAD_FOLDER, f"{complaint_id}.wav")
#                 voice_file.save(save_path)
#                 voice_path = f"/uploads/{complaint_id}.wav"
            
#             photo_url = None
#             if photo_file:
#                 photo_filename = f"{complaint_id}_{photo_file.filename}"
#                 photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
#                 photo_file.save(photo_path)
#                 photo_url = f"/uploads/{photo_filename}"

#             # Handle both 'text' and 'description' fields from frontend
#             complaint_text = complaint_data.get("text") or complaint_data.get("description") or "No complaint text provided"
            
#             logger.info(f"Final complaint text to be saved: '{complaint_text}'")

#             complaint = {
#                 "id": complaint_id,
#                 "token": token,
#                 "type": complaint_type,
#                 "category": "Women-Child",
#                 "name": complaint_data.get("name", "Anonymous"),
#                 "location": complaint_data.get("location", "Unknown"),
#                 "latitude": _to_float(complaint_data.get("latitude")),
#                 "longitude": _to_float(complaint_data.get("longitude")),
#                 "department": complaint_data.get("department", "Women-Child"),
#                 "urgency": complaint_data.get("urgency", "normal"),
#                 "description": complaint_text,  # Use the complaint text here
#                 "timestamp": datetime.datetime.utcnow(),
#                 "status": "Pending",
#                 "voice_path": voice_path,
#                 "photoUrl": photo_url
#             }

#         else:
#             complaint_data = request.json
#             if not all(k in complaint_data for k in ["name", "description", "location", "urgency", "department"]):
#                 return jsonify({"success": False, "message": "Missing one or more required fields."}), 400

#             complaint = {
#                 "id": complaint_id,
#                 "token": token,
#                 "type": "text",
#                 "category": "Women-Child",
#                 "name": complaint_data.get("name"),
#                 "location": complaint_data.get("location"),
#                 "latitude": _to_float(complaint_data.get("latitude")),
#                 "longitude": _to_float(complaint_data.get("longitude")),
#                 "department": complaint_data.get("department"),
#                 "urgency": complaint_data.get("urgency"),
#                 "description": complaint_data.get("description"),
#                 "timestamp": datetime.datetime.utcnow(),
#                 "status": "Pending"
#             }
        
#         inserted = complaints_collection.insert_one(complaint)

#         return jsonify({
#             "success": True,
#             "complaintId": complaint_id,
#             "token": str(inserted.inserted_id)
#         }), 201

#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({"success": False, "message": "Submission failed.", "error": str(e)}), 500

# # ------------------ Update Complaint Status ------------------
# @complaint_routes.route("/api/complaint/status", methods=["PUT"])
# def update_complaint_status():
#     """
#     Updates the status of a complaint. Requires admin authentication.
#     """
#     try:
#         if "admin_logged_in" not in session:
#             return jsonify({"success": False, "message": "Unauthorized"}), 401

#         data = request.json
#         complaint_id = data.get("id")
#         new_status = data.get("status")

#         if not complaint_id or not new_status:
#             return jsonify({"success": False, "message": "Invalid input"}), 400

#         result = complaints_collection.update_one(
#             {"id": complaint_id},
#             {"$set": {"status": new_status}}
#         )

#         if result.modified_count == 0:
#             return jsonify({"success": False, "message": "No complaint found with the given ID"}), 404

#         return jsonify({"success": True, "message": "Complaint status updated successfully"}), 200

#     except Exception as e:
#         return jsonify({"success": False, "message": "Internal server error", "error": str(e)}), 500

# # ------------------ Get Complaint Status ------------------
# @complaint_routes.route("/api/complaint/<complaint_id>", methods=["GET"])
# def get_complaint_status(complaint_id):
#     """
#     Retrieves a single complaint by its ID.
#     """
#     try:
#         complaint = complaints_collection.find_one({"id": complaint_id})
#         if not complaint:
#             return jsonify({"success": False, "message": "Complaint not found"}), 404

#         # Clean up the object before returning
#         complaint.pop('_id', None)
#         complaint.pop('token', None) # Don't expose the internal token

#         return jsonify({
#             "success": True,
#             "complaint": {
#                 "complaintId": complaint.get("id"),
#                 "name": complaint.get("name"),
#                 "location": complaint.get("location"),
#                 "latitude": complaint.get("latitude"),
#                 "longitude": complaint.get("longitude"),
#                 "department": complaint.get("department"),
#                 "urgency": complaint.get("urgency"),
#                 "description": complaint.get("description"),
#                 "status": complaint.get("status"),
#                 "photoUrl": complaint.get("photoUrl"),
#                 "voice_path": complaint.get("voice_path")
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({"success": False, "message": "Failed to fetch complaint", "error": str(e)}), 500

from flask import send_from_directory, Blueprint, request, jsonify, session
from config import complaints_collection
from utils.generate_id import generate_complaint_id, generate_token
from datetime import datetime
import os
import traceback
import logging
import re
from collections import Counter

# Setup logging
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

complaint_routes = Blueprint("complaint_routes", __name__)

import re

# Helper to convert Hindi/Devanagari digits to integer
def hindi_digits_to_int(text):
    devanagari_digits = '०१२३४५६७८९'
    result = ''
    for ch in text:
        if ch in devanagari_digits:
            result += str(devanagari_digits.index(ch))
        else:
            result += ch
    try:
        return int(result)
    except:
        return None

def analyze_complaint(complaint_text, location=""):
    """
    Analyze complaint text in Hindi to determine department and urgency
    """
    if not complaint_text:
        return {
            'department': 'सामान्य',  # general
            'urgency': 'medium',  # medium
            'confidence': 0.0,
            'keywords': [],
            'analysis': {}
        }

    text = complaint_text.lower()
    location_lower = location.lower() if location else ""

    # Department keywords in Hindi
    department_keywords = {
        'सड़क विभाग': ['सड़क', 'गड्ढा', 'पुल', 'पथ', 'footpath', 'bridge', 'निर्माण', 'मरम्मत', 'traffic', 'signal'],
        'जल विभाग': ['पानी', 'नाली', 'लीक', 'टैंक', 'ओवरफ्लो', 'सप्लाई', 'पाइप', 'सिवरेज', 'drain'],
        'बिजली विभाग': ['बिजली', 'लाइट', 'तार', 'पोल', 'current', 'transformer', 'outage', 'cable', 'bill', 'connection', 'streetlight'],
        'सफाई विभाग': ['कचरा', 'सफाई', 'टॉयलेट', 'dustbin', 'sweeping', 'disposal', 'सिवरेज', 'सुगंध', 'स्वच्छता'],
        'स्वास्थ्य विभाग': ['अस्पताल', 'डॉक्टर', 'दवाई', 'चिकित्सा', 'एम्बुलेंस', 'treatment', 'vaccination', 'emergency', 'infection'],
        'पुलिस विभाग': ['पुलिस', 'चोरी', 'हत्या', 'हिंसा', 'robbery', 'fight', 'security', 'illegal'],
        'शिक्षा विभाग': ['विद्यालय', 'शिक्षक', 'शिक्षा', 'छात्र', 'college', 'exam', 'books', 'admission'],
        'महिला एवं बाल विभाग': ['महिला', 'बाल', 'हैरासमेंट', 'abuse', 'molestation', 'domestic violence', 'kidnapping']
    }

    # Urgency keywords in Hindi
    urgency_keywords = {
        'high': ['तुरंत', 'आपातकालीन', 'फौरन', 'जिम्मेदारी', 'मदद', 'critical', 'danger'],
        'medium': ['जल्दी', 'सामान्य', 'समस्या', 'issue', 'complaint'],
        'low': ['जब समय मिले', 'सुझाव', 'request', 'छोटा', 'minor']
    }

    # Department scoring
    department_scores = {}
    for dept, keywords in department_keywords.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            department_scores[dept] = score

    if department_scores:
        department = max(department_scores, key=department_scores.get)
        confidence = department_scores[department] / len(department_keywords[department])
    else:
        department = 'सामान्य'
        confidence = 0.3

    # Urgency scoring
    urgency_score = {'high': 0, 'medium': 0, 'low': 0}
    for level, keywords in urgency_keywords.items():
        score = sum(1 for kw in keywords if kw in text)
        urgency_score[level] = score

    # Default urgency
    if urgency_score['high'] > 0:
        urgency = 'high'
    elif urgency_score['low'] > urgency_score['medium'] and urgency_score['low'] > 0:
        urgency = 'low'
    else:
        urgency = 'medium'

    # Detect days in Hindi like "४ दिन से"
    days_elapsed = 0
    match = re.search(r'([०१२३४५६७८९\d]+)\s*दिन\s*से', complaint_text)
    if match:
        days_str = match.group(1)
        days_elapsed = hindi_digits_to_int(days_str) or 0
        if days_elapsed >= 3:
            urgency = 'high'

    # Location-based priority boost
    critical_areas = ['अस्पताल', 'विद्यालय', 'बाजार', 'मुख्य सड़क', 'स्टेशन', 'मॉल']
    is_critical_area = any(area in location_lower for area in critical_areas)
    if is_critical_area and urgency == 'medium':
        urgency = 'high'

    return {
        'department': department,
        'urgency': urgency,
        'confidence': min(confidence, 1.0),
        'keywords': department_keywords.get(department, []),
        'analysis': {
            'text_length': len(complaint_text),
            'has_location': bool(location),
            'location_priority': is_critical_area,
            'department_scores': department_scores,
            'urgency_scores': urgency_score,
            'days_elapsed': days_elapsed
        }
    }


# Get estimated resolution time
def get_estimated_resolution_time(urgency):
    """Get estimated resolution time based on urgency"""
    resolution_times = {
        'high': '2-4 hours',
        'medium': '1-3 days',
        'low': '3-7 days'
    }
    return resolution_times.get(urgency, '2-5 days')

# Check if database is available
def is_database_available():
    """Check if MongoDB is available"""
    return complaints_collection is not None

# ------------------ Serve uploaded files ------------------
@complaint_routes.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serves files from the UPLOAD_FOLDER directory."""
    return send_from_directory(UPLOAD_FOLDER, filename)

# ------------------ Helper for safe float conversion ------------------
def _to_float(v):
    """Converts a value to a float, returning None on failure."""
    try:
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        s = str(v).strip()
        if s == "" or s.lower() == "null":
            return None
        return float(s)
    except (ValueError, TypeError):
        return None

# ------------------ Enhanced Complaint Submission Endpoint ------------------
@complaint_routes.route("/api/complaint", methods=["POST"])
def submit_complaint():
    """
    Handles complaint submissions with NLP analysis and smart routing
    """
    try:
        complaint_id = generate_complaint_id()
        token = generate_token()
        
        # Handle multipart form data (with files)
        if request.content_type and request.content_type.startswith("multipart/form-data"):
            complaint_text = request.form.get("complaint", "")
            location = request.form.get("location", "")
            name = request.form.get("name", "Kunal Thakare")  # Added name field
            latitude = _to_float(request.form.get("latitude"))
            longitude = _to_float(request.form.get("longitude"))
            
            # Handle photo upload
            photo_file = request.files.get("photo")
            photo_url = None
            if photo_file:
                photo_filename = f"{complaint_id}_{photo_file.filename}"
                photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
                photo_file.save(photo_path)
                photo_url = f"/uploads/{photo_filename}"
            
            # Perform NLP analysis
            analysis = analyze_complaint(complaint_text, location)
            
            complaint = {
                "id": complaint_id,
                "token": token,
                "type": "form",
                "name": name,  # Dashboard compatibility
                "complaint": complaint_text,
                "description": complaint_text,  # Dashboard compatibility
                "location": location,
                "latitude": latitude,
                "longitude": longitude,
                "photoUrl": photo_url,
                "timestamp": datetime.now(),
                "status": "Pending",
                
                # NLP Analysis Results
                "department": analysis['department'],
                "urgency": analysis['urgency'],
                "confidence": analysis['confidence'],
                "keywords": analysis['keywords'],
                "analysis": analysis['analysis'],
                "estimated_resolution": get_estimated_resolution_time(analysis['urgency']),
                
                # Additional metadata
                "has_photo": bool(photo_file),
                "has_geo_location": bool(latitude and longitude),
                "auto_classified": True
            }

        else:
            # Handle JSON data
            complaint_data = request.json
            if not complaint_data.get("complaint") and not complaint_data.get("description"):
                return jsonify({"success": False, "message": "Complaint text is required"}), 400

            complaint_text = complaint_data.get("complaint") or complaint_data.get("description", "")
            location = complaint_data.get("location", "")
            name = complaint_data.get("name", "Kunal Thakare")  # Added name field
            
            # Perform NLP analysis
            analysis = analyze_complaint(complaint_text, location)

            complaint = {
                "id": complaint_id,
                "token": token,
                "type": "json",
                "name": name,  # Dashboard compatibility
                "complaint": complaint_text,
                "description": complaint_text,  # Dashboard compatibility
                "location": location,
                "latitude": _to_float(complaint_data.get("latitude")),
                "longitude": _to_float(complaint_data.get("longitude")),
                "timestamp": datetime.now(),
                "status": "Pending",
                
                # NLP Analysis Results - Use provided department if available, otherwise use analyzed
                "department": complaint_data.get("department") or analysis['department'],
                "urgency": analysis['urgency'],
                "confidence": analysis['confidence'],
                "keywords": analysis['keywords'],
                "analysis": analysis['analysis'],
                "estimated_resolution": get_estimated_resolution_time(analysis['urgency']),
                
                # Additional metadata
                "has_photo": False,
                "has_geo_location": bool(complaint_data.get("latitude") and complaint_data.get("longitude")),
                "auto_classified": not bool(complaint_data.get("department"))  # False if department was provided
            }

        # Check if database is available
        if not is_database_available():
            logger.warning("Database not available - complaint not saved")
            return jsonify({
                "success": True,
                "message": "Complaint processed but not saved (database unavailable)",
                "complaint": {
                    "complaintId": complaint_id,
                    "department": complaint.get('department'),
                    "urgency": complaint.get('urgency'),
                    "estimatedResolutionTime": complaint.get('estimated_resolution'),
                    "status": "pending"
                }
            }), 201

        # Save to database
        inserted = complaints_collection.insert_one(complaint)
        
        # Log for admin dashboard
        logger.info(f"New complaint {complaint_id}: {complaint.get('department')} ({complaint.get('urgency')}) - {complaint_text[:100]}...")
        
        return jsonify({
            "success": True,
            "message": "Complaint submitted successfully",
            "complaintId": complaint_id,  # Keep this for backward compatibility
            "token": token,  # Keep this for backward compatibility
            "complaint": {
                "complaintId": complaint_id,
                "department": complaint.get('department'),
                "urgency": complaint.get('urgency'),
                "estimatedResolutionTime": complaint.get('estimated_resolution'),
                "status": "pending",
                "confidence": complaint.get('confidence')
            }
        }), 201

    except Exception as e:
        logger.error(f"Complaint submission error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False, 
            "message": "Complaint submission failed", 
            "error": str(e)
        }), 500

# ------------------ Women & Child Complaint (Enhanced) ------------------
@complaint_routes.route("/api/complaint/women-child", methods=["POST"])
def submit_women_child_complaint():
    """
    Dedicated endpoint for Women & Child complaints with priority handling
    """
    try:
        complaint_id = generate_complaint_id()
        token = generate_token()

        if request.content_type and request.content_type.startswith("multipart/form-data"):
            complaint_text = request.form.get("text") or request.form.get("description", "")
            location = request.form.get("location", "")
            name = request.form.get("name", "Kunal Thakare")  # Added name field
            
            voice_file = request.files.get("voice")
            photo_file = request.files.get("photo")
            
            # Save files
            voice_path = None
            if voice_file:
                save_path = os.path.join(UPLOAD_FOLDER, f"{complaint_id}.wav")
                voice_file.save(save_path)
                voice_path = f"/uploads/{complaint_id}.wav"
            
            photo_url = None
            if photo_file:
                photo_filename = f"{complaint_id}_{photo_file.filename}"
                photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
                photo_file.save(photo_path)
                photo_url = f"/uploads/{photo_filename}"

            complaint = {
                "id": complaint_id,
                "token": token,
                "type": "women-child",
                "category": "Women-Child",
                "name": name,  # Dashboard compatibility
                "complaint": complaint_text,
                "description": complaint_text,  # Dashboard compatibility
                "location": location,
                "latitude": _to_float(request.form.get("latitude")),
                "longitude": _to_float(request.form.get("longitude")),
                "department": "women-child",
                "urgency": "high",  # Always high priority
                "timestamp":datetime.now(),
                "status": "Pending",
                "voice_path": voice_path,
                "photoUrl": photo_url,
                "priority": "critical",
                "confidential": True,
                "estimated_resolution": "1-2 hours"
            }

        else:
            complaint_data = request.json
            complaint = {
                "id": complaint_id,
                "token": token,
                "type": "women-child",
                "category": "Women-Child",
                "name": complaint_data.get("name", "Kunal Thakare"),  # Dashboard compatibility
                "complaint": complaint_data.get("description", ""),
                "description": complaint_data.get("description", ""),  # Dashboard compatibility
                "location": complaint_data.get("location", ""),
                "latitude": _to_float(complaint_data.get("latitude")),
                "longitude": _to_float(complaint_data.get("longitude")),
                "department": "women-child",
                "urgency": "high",
                "timestamp": datetime.now(),
                "status": "Pending",
                "priority": "critical",
                "confidential": True,
                "estimated_resolution": "1-2 hours"
            }
        
        inserted = complaints_collection.insert_one(complaint)
        
        # Immediate notification for women-child complaints
        logger.critical(f"URGENT: Women-Child complaint {complaint_id} submitted - {complaint_text[:50]}...")

        return jsonify({
            "success": True,
            "message": "Urgent complaint submitted - immediate attention required",
            "complaintId": complaint_id,  # Keep for backward compatibility
            "token": token,  # Keep for backward compatibility
            "complaint": {
                "complaintId": complaint_id,
                "department": "women-child",
                "urgency": "high",
                "priority": "critical",
                "estimatedResolutionTime": "1-2 hours",
                "status": "pending"
            }
        }), 201

    except Exception as e:
        logger.error(f"Women-Child complaint error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False, 
            "message": "Submission failed", 
            "error": str(e)
        }), 500

# ------------------ Get Complaint Status (Enhanced) ------------------
@complaint_routes.route("/api/complaint/<complaint_id>", methods=["GET"])
def get_complaint_status(complaint_id):
    """
    Retrieves a single complaint by its ID with full analysis data
    """
    try:
        complaint = complaints_collection.find_one({"id": complaint_id})
        if not complaint:
            return jsonify({"success": False, "message": "Complaint not found"}), 404

        # Clean up the object before returning
        complaint.pop('_id', None)
        complaint.pop('token', None)

        return jsonify({
            "success": True,
            "status": complaint.get("status"),  # Keep original format for dashboard compatibility
            "name": complaint.get("name"),
            "location": complaint.get("location"),
            "department": complaint.get("department"),
            "description": complaint.get("description") or complaint.get("complaint"),  # Fallback to complaint field
            "complaint": {
                "complaintId": complaint.get("id"),
                "complaint": complaint.get("complaint") or complaint.get("description"),
                "location": complaint.get("location"),
                "latitude": complaint.get("latitude"),
                "longitude": complaint.get("longitude"),
                "department": complaint.get("department"),
                "urgency": complaint.get("urgency"),
                "status": complaint.get("status"),
                "photoUrl": complaint.get("photoUrl"),
                "voice_path": complaint.get("voice_path"),
                "timestamp": complaint.get("timestamp").isoformat() if complaint.get("timestamp") else None,
                "estimated_resolution": complaint.get("estimated_resolution"),
                "confidence": complaint.get("confidence"),
                "priority": complaint.get("priority"),
                "analysis": complaint.get("analysis", {})
            }
        }), 200

    except Exception as e:
        logger.error(f"Error fetching complaint {complaint_id}: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch complaint", 
            "error": str(e)
        }), 500

# ------------------ Admin Dashboard Routes ------------------
@complaint_routes.route("/api/admin/complaints", methods=["GET"])
def get_admin_complaints():
    """
    Get complaints for admin dashboard with filtering and pagination
    """
    try:
        # Check admin authentication (you can modify this based on your auth system)
        if "admin_logged_in" not in session:
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        # Get query parameters
        department = request.args.get('department')
        urgency = request.args.get('urgency')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        # Build query
        query = {}
        if department and department != 'all':
            query['department'] = department
        if urgency and urgency != 'all':
            query['urgency'] = urgency
        if status and status != 'all':
            query['status'] = status

        # Get total count
        total_count = complaints_collection.count_documents(query)
        
        # Get complaints with pagination
        complaints = list(complaints_collection.find(query)
                         .sort("timestamp", -1)
                         .skip((page - 1) * limit)
                         .limit(limit))

        # Clean up complaints for response
        for complaint in complaints:
            complaint.pop('_id', None)
            complaint.pop('token', None)
            if complaint.get('timestamp'):
                complaint['timestamp'] = complaint['timestamp'].isoformat()
            
            # Ensure backward compatibility - add description if missing but complaint exists
            if not complaint.get('description') and complaint.get('complaint'):
                complaint['description'] = complaint['complaint']
            # Ensure name field exists
            if not complaint.get('name'):
                complaint['name'] = 'Kunal Thakare'

        return jsonify({
            "success": True,
            "complaints": complaints,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "limit": limit,
                "total_pages": (total_count + limit - 1) // limit
            }
        }), 200

    except Exception as e:
        logger.error(f"Admin complaints fetch error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch complaints", 
            "error": str(e)
        }), 500

# ------------------ Update Complaint Status ------------------
@complaint_routes.route("/api/complaint/status", methods=["PUT"])
def update_complaint_status():
    """
    Updates the status of a complaint. Requires admin authentication.
    """
    try:
        if "admin_logged_in" not in session:
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        data = request.json
        complaint_id = data.get("id")
        new_status = data.get("status")
        admin_notes = data.get("notes", "")

        if not complaint_id or not new_status:
            return jsonify({"success": False, "message": "Invalid input"}), 400

        update_data = {
            "status": new_status,
            "updated_at": datetime.now()
        }
        
        if admin_notes:
            update_data["admin_notes"] = admin_notes

        result = complaints_collection.update_one(
            {"id": complaint_id},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            return jsonify({"success": False, "message": "No complaint found with the given ID"}), 404

        return jsonify({
            "success": True, 
            "message": "Complaint status updated successfully"
        }), 200

    except Exception as e:
        logger.error(f"Status update error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Internal server error", 
            "error": str(e)
        }), 500

# ------------------ Analytics Route ------------------
@complaint_routes.route("/api/admin/analytics", methods=["GET"])
def get_complaint_analytics():
    """
    Get complaint analytics for admin dashboard
    """
    try:
        if "admin_logged_in" not in session:
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        # Get date range
        days = int(request.args.get('days', 30))
        start_date = datetime.now() - datetime.timedelta(days=days)

        # Aggregate data
        pipeline = [
            {"$match": {"timestamp": {"$gte": start_date}}},
            {"$group": {
                "_id": {
                    "department": "$department",
                    "urgency": "$urgency",
                    "status": "$status"
                },
                "count": {"$sum": 1}
            }}
        ]

        results = list(complaints_collection.aggregate(pipeline))
        
        # Process results
        analytics = {
            "total_complaints": len(results),
            "by_department": {},
            "by_urgency": {},
            "by_status": {}
        }

        for result in results:
            dept = result["_id"]["department"]
            urgency = result["_id"]["urgency"]
            status = result["_id"]["status"]
            count = result["count"]

            analytics["by_department"][dept] = analytics["by_department"].get(dept, 0) + count
            analytics["by_urgency"][urgency] = analytics["by_urgency"].get(urgency, 0) + count
            analytics["by_status"][status] = analytics["by_status"].get(status, 0) + count

        return jsonify({
            "success": True,
            "analytics": analytics,
            "period_days": days
        }), 200

    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch analytics", 
            "error": str(e)
        }), 500