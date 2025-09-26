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
from config import complaints_collection, users_collection
from utils.generate_id import generate_complaint_id, generate_token
from datetime import datetime
import os
import traceback
import logging
import re
import jwt
from collections import Counter


# Setup logging
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

complaint_routes = Blueprint("complaint_routes", __name__)

# JWT Secret Key - should match the one in auth.py
JWT_SECRET_KEY = "your-secret-key-change-in-production"

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

# Helper function to extract user info from token
def get_user_from_token(request):
    """
    Extract user information from JWT token
    Returns user data or None if invalid/missing token
    """
    try:
        token = request.headers.get('Authorization')
        if not token:
            return None
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Verify token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        
        # If it's an admin token, return admin info
        if payload.get('role') == 'admin':
            return {
                'userId': 'admin',
                'name': 'System Administrator',
                'email': payload.get('email'),
                'role': 'admin',
                'isAdmin': True
            }
        
        # For regular users, get user data from database
        user_id = payload.get('userId')
        if not user_id:
            return None
        
        user = users_collection.find_one({"userId": user_id})
        if not user or not user.get("isActive", True):
            return None
            
        return {
            'userId': user['userId'],
            'name': user['name'],
            'email': user['email'],
            'phone': user.get('phone'),
            'address': user.get('address'),
            'role': user.get('role', 'user'),
            'isAdmin': False
        }
        
    except jwt.ExpiredSignatureError:
        logger.warning("Expired token provided")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid token provided")
        return None
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return None

# NEW: Get User Profile Endpoint
@complaint_routes.route("/api/user/profile", methods=["GET"])
def get_user_profile():
    """
    Get authenticated user's profile information
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        if not user_info or not user_info['userId']:
            return jsonify({"success": False, "message": "Authentication required"}), 401

        # Get fresh user data from database
        if user_info['userId'] != 'admin':  # Don't query DB for admin
            user = users_collection.find_one(
                {"userId": user_info['userId']}, 
                {"passwordHash": 0}  # Exclude password hash
            )
            if not user:
                return jsonify({"success": False, "message": "User not found"}), 404

            # Clean up user data
            user.pop('_id', None)
            if user.get('createdAt'):
                user['createdAt'] = user['createdAt'].isoformat()
            if user.get('lastLoginAt'):
                user['lastLoginAt'] = user['lastLoginAt'].isoformat()
            
            return jsonify({
                "success": True,
                "user": user
            }), 200
        else:
            # Return admin info
            return jsonify({
                "success": True,
                "user": {
                    "userId": "admin",
                    "name": "System Administrator", 
                    "email": user_info['email'],
                    "role": "admin",
                    "isAdmin": True
                }
            }), 200

    except Exception as e:
        logger.error(f"User profile fetch error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch user profile", 
            "error": str(e)
        }), 500

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
    Handles complaint submissions with NLP analysis, smart routing, and user authentication
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        # For backwards compatibility, allow anonymous complaints but log a warning
        if not user_info:
            logger.warning("Anonymous complaint submission - consider requiring authentication")
            user_info = {
                'userId': None,
                'name': 'Anonymous User',
                'email': None,
                'phone': None,
                'address': None,
                'role': 'anonymous',
                'isAdmin': False
            }

        complaint_id = generate_complaint_id()
        token = generate_token()
        
        # Handle multipart form data (with files)
        if request.content_type and request.content_type.startswith("multipart/form-data"):
            complaint_text = request.form.get("complaint", "")
            location = request.form.get("location", "")
            # Use authenticated user's name, fallback to form data, then default
            name = user_info['name'] or request.form.get("name", "Anonymous User")
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
                
                # User Information
                "userId": user_info['userId'],
                "name": name,
                "email": user_info['email'],
                "phone": user_info['phone'],
                "userAddress": user_info['address'],  # User's registered address
                "userRole": user_info['role'],
                
                # Complaint Details
                "complaint": complaint_text,
                "description": complaint_text,  # Dashboard compatibility
                "location": location,  # Complaint location (different from user address)
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
                "auto_classified": True,
                "is_authenticated": bool(user_info['userId'])
            }

        else:
            # Handle JSON data
            complaint_data = request.json
            if not complaint_data.get("complaint") and not complaint_data.get("description"):
                return jsonify({"success": False, "message": "Complaint text is required"}), 400

            complaint_text = complaint_data.get("complaint") or complaint_data.get("description", "")
            location = complaint_data.get("location", "")
            # Use authenticated user's name, fallback to request data, then default
            name = user_info['name'] or complaint_data.get("name", "Anonymous User")
            
            # Perform NLP analysis
            analysis = analyze_complaint(complaint_text, location)

            complaint = {
                "id": complaint_id,
                "token": token,
                "type": "json",
                
                # User Information
                "userId": user_info['userId'],
                "name": name,
                "email": user_info['email'],
                "phone": user_info['phone'],
                "userAddress": user_info['address'],
                "userRole": user_info['role'],
                
                # Complaint Details
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
                "auto_classified": not bool(complaint_data.get("department")),
                "is_authenticated": bool(user_info['userId'])
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
        user_identifier = user_info['name'] if user_info['name'] != 'Anonymous User' else 'Anonymous'
        logger.info(f"New complaint {complaint_id} by {user_identifier}: {complaint.get('department')} ({complaint.get('urgency')}) - {complaint_text[:100]}...")
        
        return jsonify({
            "success": True,
            "message": "Complaint submitted successfully",
            "complaintId": complaint_id,  # Keep this for backward compatibility
            "token": token,  # Keep this for backward compatibility
            "complaint": {
                "complaintId": complaint_id,
                "submittedBy": user_info['name'],
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
    Dedicated endpoint for Women & Child complaints with priority handling and user authentication
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        # For women-child complaints, we strongly recommend authentication
        if not user_info or not user_info['userId']:
            return jsonify({
                "success": False, 
                "message": "Authentication required for women & child complaints"
            }), 401

        complaint_id = generate_complaint_id()
        token = generate_token()

        if request.content_type and request.content_type.startswith("multipart/form-data"):
            complaint_text = request.form.get("text") or request.form.get("description", "")
            location = request.form.get("location", "")
            # Use authenticated user's name
            name = user_info['name']
            
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
                
                # User Information
                "userId": user_info['userId'],
                "name": name,
                "email": user_info['email'],
                "phone": user_info['phone'],
                "userAddress": user_info['address'],
                "userRole": user_info['role'],
                
                # Complaint Details
                "complaint": complaint_text,
                "description": complaint_text,  # Dashboard compatibility
                "location": location,
                "latitude": _to_float(request.form.get("latitude")),
                "longitude": _to_float(request.form.get("longitude")),
                "department": "महिला एवं बाल विभाग",
                "urgency": "high",  # Always high priority
                "timestamp": datetime.now(),
                "status": "Pending",
                "voice_path": voice_path,
                "photoUrl": photo_url,
                "priority": "critical",
                "confidential": True,
                "estimated_resolution": "1-2 hours",
                "is_authenticated": True
            }

        else:
            complaint_data = request.json
            complaint = {
                "id": complaint_id,
                "token": token,
                "type": "women-child",
                "category": "Women-Child",
                
                # User Information
                "userId": user_info['userId'],
                "name": user_info['name'],
                "email": user_info['email'],
                "phone": user_info['phone'],
                "userAddress": user_info['address'],
                "userRole": user_info['role'],
                
                # Complaint Details
                "complaint": complaint_data.get("description", ""),
                "description": complaint_data.get("description", ""),  # Dashboard compatibility
                "location": complaint_data.get("location", ""),
                "latitude": _to_float(complaint_data.get("latitude")),
                "longitude": _to_float(complaint_data.get("longitude")),
                "department": "महिला एवं बाल विभाग",
                "urgency": "high",
                "timestamp": datetime.now(),
                "status": "Pending",
                "priority": "critical",
                "confidential": True,
                "estimated_resolution": "1-2 hours",
                "is_authenticated": True
            }
        
        inserted = complaints_collection.insert_one(complaint)
        
        # Immediate notification for women-child complaints
        logger.critical(f"URGENT: Women-Child complaint {complaint_id} by {user_info['name']} - {complaint_text[:50]}...")

        return jsonify({
            "success": True,
            "message": "Urgent complaint submitted - immediate attention required",
            "complaintId": complaint_id,  # Keep for backward compatibility
            "token": token,  # Keep for backward compatibility
            "complaint": {
                "complaintId": complaint_id,
                "submittedBy": user_info['name'],
                "department": "महिला एवं बाल विभाग",
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

# UPDATED: Get User's Complaints with proper pagination and filtering
@complaint_routes.route("/api/user/complaints", methods=["GET"])
def get_user_complaints():
    """
    Get all complaints submitted by the authenticated user with enhanced filtering
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        if not user_info or not user_info['userId']:
            return jsonify({"success": False, "message": "Authentication required"}), 401

        # Get query parameters
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 10)), 100)  # Cap at 100
        status = request.args.get('status')
        department = request.args.get('department')
        urgency = request.args.get('urgency')
        
        # Build query for user's complaints
        query = {"userId": user_info['userId']}
        if status and status != 'all':
            query['status'] = status
        if department and department != 'all':
            query['department'] = department  
        if urgency and urgency != 'all':
            query['urgency'] = urgency

        # Get total count
        total_count = complaints_collection.count_documents(query)
        
        # Get complaints with pagination
        complaints = list(complaints_collection.find(query, {'token': 0})  # Exclude token
                         .sort("timestamp", -1)
                         .skip((page - 1) * limit)
                         .limit(limit))

        # Clean up complaints for response
        for complaint in complaints:
            complaint.pop('_id', None)
            if complaint.get('timestamp'):
                complaint['timestamp'] = complaint['timestamp'].isoformat()
                # Add createdAt for frontend compatibility
                complaint['createdAt'] = complaint['timestamp']

        return jsonify({
            "success": True,
            "complaints": complaints,
            "user": {
                "name": user_info['name'],
                "email": user_info['email'],
                "userId": user_info['userId']
            },
            "pagination": {
                "total_count": total_count,
                "page": page,
                "limit": limit,
                "total_pages": (total_count + limit - 1) // limit
            }
        }), 200

    except Exception as e:
        logger.error(f"User complaints fetch error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch complaints", 
            "error": str(e)
        }), 500

# ------------------ Get Complaint Status (Enhanced) ------------------
@complaint_routes.route("/api/complaint/<complaint_id>", methods=["GET"])
def get_complaint_status(complaint_id):
    """
    Retrieves a single complaint by its ID with full analysis data
    Enhanced with user verification
    """
    try:
        complaint = complaints_collection.find_one({"id": complaint_id})
        if not complaint:
            return jsonify({"success": False, "message": "Complaint not found"}), 404

        # Get user information from token
        user_info = get_user_from_token(request)
        
        # Check if user has permission to view this complaint
        if user_info:
            # User can view their own complaints, admins can view all
            if not user_info['isAdmin'] and complaint.get('userId') != user_info['userId']:
                return jsonify({"success": False, "message": "Unauthorized to view this complaint"}), 403
        # If no token provided, allow access for backward compatibility but log warning
        else:
            logger.warning(f"Unauthenticated access to complaint {complaint_id}")

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
                "analysis": complaint.get("analysis", {}),
                
                # User information (if available)
                "submittedBy": complaint.get("name"),
                "userId": complaint.get("userId"),
                "userEmail": complaint.get("email"),
                "userPhone": complaint.get("phone"),
                "isAuthenticated": complaint.get("is_authenticated", False)
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
    Get complaints for admin dashboard with filtering, pagination, and enhanced user info
    """
    try:
        # Check admin authentication
        user_info = get_user_from_token(request)
        if not user_info or not user_info['isAdmin']:
            # Fallback to session check for backward compatibility
            if "admin_logged_in" not in session:
                return jsonify({"success": False, "message": "Admin access required"}), 401

        # Get query parameters
        department = request.args.get('department')
        urgency = request.args.get('urgency')
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        user_id = request.args.get('userId')  # New: Filter by specific user
        
        # Build query
        query = {}
        if department and department != 'all':
            query['department'] = department
        if urgency and urgency != 'all':
            query['urgency'] = urgency
        if status and status != 'all':
            query['status'] = status
        if user_id:
            query['userId'] = user_id

        # Get total count
        total_count = complaints_collection.count_documents(query)
        
        # Get complaints with pagination
        complaints = list(complaints_collection.find(query, {'token': 0})  # Exclude tokens
                         .sort("timestamp", -1)
                         .skip((page - 1) * limit)
                         .limit(limit))

        # Clean up complaints for response
        for complaint in complaints:
            complaint.pop('_id', None)
            if complaint.get('timestamp'):
                complaint['timestamp'] = complaint['timestamp'].isoformat()
            
            # Ensure backward compatibility - add description if missing but complaint exists
            if not complaint.get('description') and complaint.get('complaint'):
                complaint['description'] = complaint['complaint']
            # Ensure name field exists
            if not complaint.get('name'):
                complaint['name'] = 'Anonymous User'

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
    Enhanced with user notification capability.
    """
    try:
        # Check admin authentication
        user_info = get_user_from_token(request)
        if not user_info or not user_info['isAdmin']:
            # Fallback to session check for backward compatibility
            if "admin_logged_in" not in session:
                return jsonify({"success": False, "message": "Admin access required"}), 401

        data = request.json
        complaint_id = data.get("id")
        new_status = data.get("status")
        admin_notes = data.get("notes", "")

        if not complaint_id or not new_status:
            return jsonify({"success": False, "message": "Invalid input"}), 400

        # Get the complaint to check if user exists
        complaint = complaints_collection.find_one({"id": complaint_id})
        if not complaint:
            return jsonify({"success": False, "message": "Complaint not found"}), 404

        update_data = {
            "status": new_status,
            "updated_at": datetime.now(),
            "updated_by": user_info.get('email') if user_info else session.get("admin_email", "admin")
        }
        
        if admin_notes:
            update_data["admin_notes"] = admin_notes

        result = complaints_collection.update_one(
            {"id": complaint_id},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            return jsonify({"success": False, "message": "Failed to update complaint"}), 500

        # Log the status update with user information
        user_name = complaint.get('name', 'Unknown User')
        logger.info(f"Complaint {complaint_id} status updated to '{new_status}' by admin - User: {user_name}")

        return jsonify({
            "success": True, 
            "message": "Complaint status updated successfully",
            "complaint": {
                "id": complaint_id,
                "status": new_status,
                "updatedBy": update_data["updated_by"],
                "updatedAt": update_data["updated_at"].isoformat()
            }
        }), 200

    except Exception as e:
        logger.error(f"Status update error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Internal server error", 
            "error": str(e)
        }), 500

# NEW: Get User Statistics with better analysis
@complaint_routes.route("/api/user/stats", methods=["GET"])
def get_user_stats():
    """
    Get comprehensive statistics for the authenticated user's complaints
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        if not user_info or not user_info['userId']:
            return jsonify({"success": False, "message": "Authentication required"}), 401

        # Get date range parameter
        days = int(request.args.get('days', 30))
        start_date = datetime.now() - datetime.timedelta(days=days) if days > 0 else None

        # Build base query
        query = {"userId": user_info['userId']}
        if start_date:
            query["timestamp"] = {"$gte": start_date}

        # Get user's complaint statistics using aggregation pipeline
        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": {
                    "status": "$status",
                    "urgency": "$urgency", 
                    "department": "$department"
                },
                "count": {"$sum": 1}
            }}
        ]

        results = list(complaints_collection.aggregate(pipeline))
        
        # Process results
        stats = {
            "total_complaints": 0,
            "by_status": {},
            "by_urgency": {},
            "by_department": {},
            "period_days": days
        }

        for result in results:
            status = result["_id"]["status"]
            urgency = result["_id"]["urgency"]
            department = result["_id"]["department"]
            count = result["count"]

            stats["total_complaints"] += count
            stats["by_status"][status] = stats["by_status"].get(status, 0) + count
            stats["by_urgency"][urgency] = stats["by_urgency"].get(urgency, 0) + count
            stats["by_department"][department] = stats["by_department"].get(department, 0) + count

        # Get recent activity
        recent_complaints = list(complaints_collection.find(
            {"userId": user_info['userId']}, 
            {'_id': 0, 'token': 0}
        ).sort("timestamp", -1).limit(5))

        for complaint in recent_complaints:
            if complaint.get('timestamp'):
                complaint['timestamp'] = complaint['timestamp'].isoformat()

        return jsonify({
            "success": True,
            "stats": stats,
            "recent_complaints": recent_complaints,
            "user": {
                "name": user_info['name'],
                "email": user_info['email'],
                "userId": user_info['userId']
            }
        }), 200

    except Exception as e:
        logger.error(f"User stats error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch user statistics", 
            "error": str(e)
        }), 500

# ------------------ Analytics Route ------------------
@complaint_routes.route("/api/admin/analytics", methods=["GET"])
def get_complaint_analytics():
    """
    Get complaint analytics for admin dashboard with enhanced user insights
    """
    try:
        # Check admin authentication
        user_info = get_user_from_token(request)
        if not user_info or not user_info['isAdmin']:
            # Fallback to session check for backward compatibility
            if "admin_logged_in" not in session:
                return jsonify({"success": False, "message": "Admin access required"}), 401

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
                    "status": "$status",
                    "is_authenticated": "$is_authenticated"
                },
                "count": {"$sum": 1}
            }}
        ]

        results = list(complaints_collection.aggregate(pipeline))
        
        # Process results
        analytics = {
            "total_complaints": 0,
            "by_department": {},
            "by_urgency": {},
            "by_status": {},
            "authenticated_vs_anonymous": {"authenticated": 0, "anonymous": 0},
            "period_days": days
        }

        for result in results:
            dept = result["_id"]["department"]
            urgency = result["_id"]["urgency"]
            status = result["_id"]["status"]
            is_authenticated = result["_id"].get("is_authenticated", False)
            count = result["count"]

            analytics["total_complaints"] += count
            analytics["by_department"][dept] = analytics["by_department"].get(dept, 0) + count
            analytics["by_urgency"][urgency] = analytics["by_urgency"].get(urgency, 0) + count
            analytics["by_status"][status] = analytics["by_status"].get(status, 0) + count
            
            if is_authenticated:
                analytics["authenticated_vs_anonymous"]["authenticated"] += count
            else:
                analytics["authenticated_vs_anonymous"]["anonymous"] += count

        # Get user engagement statistics
        user_engagement_pipeline = [
            {"$match": {"timestamp": {"$gte": start_date}, "userId": {"$ne": None}}},
            {"$group": {
                "_id": "$userId",
                "complaint_count": {"$sum": 1},
                "user_name": {"$first": "$name"},
                "user_email": {"$first": "$email"}
            }},
            {"$sort": {"complaint_count": -1}},
            {"$limit": 10}
        ]

        top_users = list(complaints_collection.aggregate(user_engagement_pipeline))
        analytics["top_users"] = top_users

        return jsonify({
            "success": True,
            "analytics": analytics
        }), 200

    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch analytics", 
            "error": str(e)
        }), 500

# ------------------ Search Complaints by User ------------------
@complaint_routes.route("/api/admin/complaints/search", methods=["GET"])
def search_complaints():
    """
    Search complaints by user email, name, or complaint text (admin only)
    """
    try:
        # Check admin authentication
        user_info = get_user_from_token(request)
        if not user_info or not user_info['isAdmin']:
            if "admin_logged_in" not in session:
                return jsonify({"success": False, "message": "Admin access required"}), 401

        search_term = request.args.get('q', '').strip()
        if not search_term:
            return jsonify({"success": False, "message": "Search term required"}), 400

        # Search in multiple fields
        search_query = {
            "$or": [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"email": {"$regex": search_term, "$options": "i"}},
                {"complaint": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}},
                {"location": {"$regex": search_term, "$options": "i"}},
                {"id": {"$regex": search_term, "$options": "i"}}
            ]
        }

        # Get pagination parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        # Get total count
        total_count = complaints_collection.count_documents(search_query)
        
        # Get complaints with pagination
        complaints = list(complaints_collection.find(search_query, {'token': 0})
                         .sort("timestamp", -1)
                         .skip((page - 1) * limit)
                         .limit(limit))

        # Clean up complaints for response
        for complaint in complaints:
            complaint.pop('_id', None)
            if complaint.get('timestamp'):
                complaint['timestamp'] = complaint['timestamp'].isoformat()

        return jsonify({
            "success": True,
            "complaints": complaints,
            "search_term": search_term,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "limit": limit,
                "total_pages": (total_count + limit - 1) // limit
            }
        }), 200

    except Exception as e:
        logger.error(f"Search complaints error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to search complaints", 
            "error": str(e)
        }), 500

# ------------------ Get User Profile with Complaint History ------------------
@complaint_routes.route("/api/admin/user/<user_id>/profile", methods=["GET"])
def get_user_profile_with_complaints(user_id):
    """
    Get user profile with their complaint history (admin only)
    """
    try:
        # Check admin authentication
        user_info = get_user_from_token(request)
        if not user_info or not user_info['isAdmin']:
            if "admin_logged_in" not in session:
                return jsonify({"success": False, "message": "Admin access required"}), 401

        # Get user data
        user = users_collection.find_one({"userId": user_id}, {"passwordHash": 0})
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        # Get user's complaints
        user_complaints = list(complaints_collection.find({"userId": user_id}, {'token': 0})
                              .sort("timestamp", -1)
                              .limit(50))  # Latest 50 complaints

        # Clean up complaints
        for complaint in user_complaints:
            complaint.pop('_id', None)
            if complaint.get('timestamp'):
                complaint['timestamp'] = complaint['timestamp'].isoformat()

        # Get user statistics
        stats_pipeline = [
            {"$match": {"userId": user_id}},
            {"$group": {
                "_id": {
                    "status": "$status",
                    "urgency": "$urgency",
                    "department": "$department"
                },
                "count": {"$sum": 1}
            }}
        ]

        stats_results = list(complaints_collection.aggregate(stats_pipeline))
        
        stats = {
            "total_complaints": 0,
            "by_status": {},
            "by_urgency": {},
            "by_department": {}
        }

        for result in stats_results:
            status = result["_id"]["status"]
            urgency = result["_id"]["urgency"]
            department = result["_id"]["department"]
            count = result["count"]

            stats["total_complaints"] += count
            stats["by_status"][status] = stats["by_status"].get(status, 0) + count
            stats["by_urgency"][urgency] = stats["by_urgency"].get(urgency, 0) + count
            stats["by_department"][department] = stats["by_department"].get(department, 0) + count

        # Clean up user data
        user.pop('_id', None)
        if user.get('createdAt'):
            user['createdAt'] = user['createdAt'].isoformat()
        if user.get('lastLoginAt'):
            user['lastLoginAt'] = user['lastLoginAt'].isoformat()

        return jsonify({
            "success": True,
            "user": user,
            "complaints": user_complaints,
            "stats": stats
        }), 200

    except Exception as e:
        logger.error(f"User profile fetch error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch user profile", 
            "error": str(e)
        }), 500


        # Add this to your complaint_routes.py file

import math
from collections import defaultdict

# Helper function to calculate distance between two coordinates using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula
    Returns distance in meters
    """
    if not all([lat1, lon1, lat2, lon2]):
        return float('inf')  # Return infinity if any coordinate is missing
    
    try:
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of Earth in meters
        r = 6371000
        
        return c * r
    except (ValueError, TypeError):
        return float('inf')

# NEW: Get nearby complaints for a user
@complaint_routes.route("/api/user/nearby-complaints", methods=["GET"])
def get_nearby_complaints():
    """
    Get complaints within 400m of the authenticated user's location with voting functionality
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        if not user_info or not user_info['userId']:
            return jsonify({"success": False, "message": "Authentication required"}), 401

        # Get user's location from database
        user = users_collection.find_one({"userId": user_info['userId']})
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        user_lat = user.get('latitude')
        user_lng = user.get('longitude')
        
        if not user_lat or not user_lng:
            return jsonify({
                "success": False, 
                "message": "Your location is not available. Please update your profile with location information.",
                "error_code": "NO_USER_LOCATION"
            }), 400

        # Get query parameters
        radius = min(int(request.args.get('radius', 400)), 2000)  # Cap at 2km for performance
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 20)), 50)  # Cap at 50 for performance
        status_filter = request.args.get('status')
        department_filter = request.args.get('department')
        urgency_filter = request.args.get('urgency')

        # Build query - exclude user's own complaints
        query = {
            "userId": {"$ne": user_info['userId']},  # Exclude own complaints
            "latitude": {"$ne": None},
            "longitude": {"$ne": None}
        }
        
        # Add filters
        if status_filter and status_filter != 'all':
            query['status'] = status_filter
        if department_filter and department_filter != 'all':
            query['department'] = department_filter  
        if urgency_filter and urgency_filter != 'all':
            query['urgency'] = urgency_filter

        # Get all complaints with location data (we'll filter by distance after)
        all_complaints = list(complaints_collection.find(query, {'token': 0}))
        
        # Filter complaints by distance and add distance info
        nearby_complaints = []
        for complaint in all_complaints:
            complaint_lat = complaint.get('latitude')
            complaint_lng = complaint.get('longitude')
            
            distance = calculate_distance(user_lat, user_lng, complaint_lat, complaint_lng)
            
            if distance <= radius:
                complaint.pop('_id', None)
                if complaint.get('timestamp'):
                    complaint['timestamp'] = complaint['timestamp'].isoformat()
                
                # Add distance information
                complaint['distance'] = round(distance)
                complaint['distance_text'] = f"{round(distance)}m away" if distance < 1000 else f"{round(distance/1000, 1)}km away"
                
                # Add voting information
                complaint['upvotes'] = complaint.get('upvotes', [])
                complaint['downvotes'] = complaint.get('downvotes', [])
                complaint['upvote_count'] = len(complaint.get('upvotes', []))
                complaint['downvote_count'] = len(complaint.get('downvotes', []))
                complaint['user_voted'] = {
                    'upvoted': user_info['userId'] in complaint.get('upvotes', []),
                    'downvoted': user_info['userId'] in complaint.get('downvotes', [])
                }
                
                # Calculate voting score (upvotes - downvotes)
                complaint['vote_score'] = complaint['upvote_count'] - complaint['downvote_count']
                
                # Hide sensitive user information but keep name for display
                complaint.pop('email', None)
                complaint.pop('phone', None)
                complaint.pop('userAddress', None)
                
                nearby_complaints.append(complaint)
        
        # Sort by distance first, then by vote score
        nearby_complaints.sort(key=lambda x: (x['distance'], -x['vote_score']))
        
        # Apply pagination
        total_count = len(nearby_complaints)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_complaints = nearby_complaints[start_idx:end_idx]

        return jsonify({
            "success": True,
            "complaints": paginated_complaints,
            "user_location": {
                "latitude": float(user_lat),
                "longitude": float(user_lng)
            },
            "filters": {
                "radius": radius,
                "status": status_filter,
                "department": department_filter,
                "urgency": urgency_filter
            },
            "pagination": {
                "total_count": total_count,
                "page": page,
                "limit": limit,
                "total_pages": (total_count + limit - 1) // limit
            },
            "stats": {
                "total_nearby": total_count,
                "radius_searched": radius,
                "departments": list(set(c.get('department') for c in nearby_complaints if c.get('department'))),
                "urgency_levels": list(set(c.get('urgency') for c in nearby_complaints if c.get('urgency')))
            }
        }), 200

    except Exception as e:
        logger.error(f"Nearby complaints fetch error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch nearby complaints", 
            "error": str(e)
        }), 500

# NEW: Vote on a complaint (upvote/downvote)
@complaint_routes.route("/api/complaint/<complaint_id>/vote", methods=["POST"])
def vote_on_complaint(complaint_id):
    """
    Allow users to upvote or downvote nearby complaints
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        if not user_info or not user_info['userId']:
            return jsonify({"success": False, "message": "Authentication required"}), 401

        data = request.json
        vote_type = data.get('vote_type')  # 'upvote', 'downvote', or 'remove'
        
        if vote_type not in ['upvote', 'downvote', 'remove']:
            return jsonify({"success": False, "message": "Invalid vote type"}), 400

        # Get the complaint
        complaint = complaints_collection.find_one({"id": complaint_id})
        if not complaint:
            return jsonify({"success": False, "message": "Complaint not found"}), 404

        # Users cannot vote on their own complaints
        if complaint.get('userId') == user_info['userId']:
            return jsonify({"success": False, "message": "Cannot vote on your own complaint"}), 400

        # Check if complaint is within user's range (optional security check)
        user = users_collection.find_one({"userId": user_info['userId']})
        if user and user.get('latitude') and user.get('longitude'):
            distance = calculate_distance(
                user.get('latitude'), user.get('longitude'),
                complaint.get('latitude'), complaint.get('longitude')
            )
            if distance > 2000:  # 2km max for voting
                return jsonify({"success": False, "message": "Complaint is too far to vote on"}), 400

        user_id = user_info['userId']
        current_upvotes = complaint.get('upvotes', [])
        current_downvotes = complaint.get('downvotes', [])

        # Remove user from both lists first
        new_upvotes = [uid for uid in current_upvotes if uid != user_id]
        new_downvotes = [uid for uid in current_downvotes if uid != user_id]

        # Add user to appropriate list based on vote type
        if vote_type == 'upvote':
            new_upvotes.append(user_id)
        elif vote_type == 'downvote':
            new_downvotes.append(user_id)
        # For 'remove', we just keep the user removed from both lists

        # Update the complaint
        update_data = {
            'upvotes': new_upvotes,
            'downvotes': new_downvotes,
            'vote_updated_at': datetime.now()
        }

        result = complaints_collection.update_one(
            {"id": complaint_id},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            return jsonify({"success": False, "message": "Failed to update vote"}), 500

        # Log the voting activity
        logger.info(f"User {user_info['userId']} {vote_type}d complaint {complaint_id}")

        return jsonify({
            "success": True,
            "message": f"Vote {vote_type}d successfully",
            "vote_counts": {
                "upvotes": len(new_upvotes),
                "downvotes": len(new_downvotes),
                "score": len(new_upvotes) - len(new_downvotes)
            },
            "user_vote": {
                "upvoted": user_id in new_upvotes,
                "downvoted": user_id in new_downvotes
            }
        }), 200

    except Exception as e:
        logger.error(f"Vote complaint error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to vote on complaint", 
            "error": str(e)
        }), 500

# NEW: Get complaint voting details
@complaint_routes.route("/api/complaint/<complaint_id>/votes", methods=["GET"])
def get_complaint_votes(complaint_id):
    """
    Get voting details for a complaint
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        if not user_info or not user_info['userId']:
            return jsonify({"success": False, "message": "Authentication required"}), 401

        complaint = complaints_collection.find_one({"id": complaint_id})
        if not complaint:
            return jsonify({"success": False, "message": "Complaint not found"}), 404

        upvotes = complaint.get('upvotes', [])
        downvotes = complaint.get('downvotes', [])
        user_id = user_info['userId']

        return jsonify({
            "success": True,
            "complaint_id": complaint_id,
            "vote_counts": {
                "upvotes": len(upvotes),
                "downvotes": len(downvotes),
                "score": len(upvotes) - len(downvotes)
            },
            "user_vote": {
                "upvoted": user_id in upvotes,
                "downvoted": user_id in downvotes
            }
        }), 200

    except Exception as e:
        logger.error(f"Get complaint votes error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to get voting details", 
            "error": str(e)
        }), 500

# NEW: Get community engagement stats
@complaint_routes.route("/api/user/community-stats", methods=["GET"])
def get_community_stats():
    """
    Get community engagement statistics for the user's area
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        if not user_info or not user_info['userId']:
            return jsonify({"success": False, "message": "Authentication required"}), 401

        # Get user's location
        user = users_collection.find_one({"userId": user_info['userId']})
        if not user or not user.get('latitude') or not user.get('longitude'):
            return jsonify({
                "success": False, 
                "message": "Location required for community stats"
            }), 400

        user_lat = float(user.get('latitude'))
        user_lng = float(user.get('longitude'))
        radius = int(request.args.get('radius', 400))

        # Get all complaints with location in a reasonable range first
        all_complaints = list(complaints_collection.find({
            "latitude": {"$ne": None},
            "longitude": {"$ne": None}
        }))

        # Filter by distance and calculate stats
        nearby_complaints = []
        for complaint in all_complaints:
            distance = calculate_distance(
                user_lat, user_lng,
                complaint.get('latitude'), complaint.get('longitude')
            )
            if distance <= radius:
                nearby_complaints.append(complaint)

        # Calculate statistics
        total_complaints = len(nearby_complaints)
        departments = defaultdict(int)
        statuses = defaultdict(int)
        urgencies = defaultdict(int)
        total_votes = 0

        for complaint in nearby_complaints:
            departments[complaint.get('department', 'Unknown')] += 1
            statuses[complaint.get('status', 'Unknown')] += 1
            urgencies[complaint.get('urgency', 'medium')] += 1
            total_votes += len(complaint.get('upvotes', [])) + len(complaint.get('downvotes', []))

        return jsonify({
            "success": True,
            "stats": {
                "total_complaints": total_complaints,
                "total_community_votes": total_votes,
                "radius": radius,
                "by_department": dict(departments),
                "by_status": dict(statuses),
                "by_urgency": dict(urgencies),
                "avg_votes_per_complaint": round(total_votes / max(total_complaints, 1), 2),
                "most_common_department": max(departments.items(), key=lambda x: x[1])[0] if departments else "N/A",
                "most_common_issue": max(urgencies.items(), key=lambda x: x[1])[0] if urgencies else "N/A"
            },
            "user_location": {
                "latitude": user_lat,
                "longitude": user_lng
            }
        }), 200

    except Exception as e:
        logger.error(f"Community stats error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch community statistics", 
            "error": str(e)
        }), 500

        # Add this new route to your complaint_routes.py file

@complaint_routes.route("/api/voice-analysis", methods=["POST"])
def voice_analysis():
    """
    Handles voice complaint analysis only - returns structured data without submission
    This endpoint runs the voice bot conversation and returns analysis results
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        if not user_info or not user_info['userId']:
            return jsonify({
                "status": "error", 
                "message": "Authentication required for voice analysis"
            }), 401

        logger.info(f"Voice analysis started for user: {user_info['name']} ({user_info['userId']})")

        # Import the voice analysis system
        try:
            import sys
            import os
            # Add the voice complaint handler path
            voice_handler_path = os.path.join(os.path.dirname(__file__), '..', 'voice_complaint')
            sys.path.append(voice_handler_path)
            
            from voice_bot.jantavoice import start_conversation
        except ImportError as e:
            logger.error(f"Failed to import voice analysis module: {e}")
            return jsonify({
                "status": "error",
                "message": "Voice analysis system not available",
                "error": str(e)
            }), 503

        # Run the voice conversation analysis
        logger.info("Starting voice conversation analysis...")
        
        try:
            result = start_conversation()
        except Exception as e:
            logger.error(f"Voice conversation error: {e}")
            return jsonify({
                "status": "error",
                "message": "Voice analysis failed during conversation",
                "error": str(e)
            }), 500

        if not result:
            logger.warning("Voice analysis returned no result")
            return jsonify({
                "status": "error",
                "message": "Voice analysis failed - no response from voice system"
            }), 500

        if result.get("status") != "success":
            logger.warning(f"Voice analysis failed: {result.get('message')}")
            return jsonify({
                "status": "error",
                "message": result.get("message", "Voice analysis failed"),
                "error": result.get("error")
            }), 500

        # Extract the analysis data
        analysis_data = result.get("data", {})
        
        # Enhance the response with additional metadata
        enhanced_response = {
            "status": "success",
            "message": "Voice analysis completed successfully",
            "data": {
                # Hindi keys from voice system
                "शिकायत": analysis_data.get("शिकायत", ""),
                "विवरण": analysis_data.get("विवरण", ""),
                "विभाग": analysis_data.get("विभाग", "सामान्य प्रशासन"),
                "प्राथमिकता": analysis_data.get("प्राथमिकता", "medium"),
                "स्थान": analysis_data.get("स्थान", ""),
                
                # English keys for frontend compatibility
                "complaint": analysis_data.get("complaint", ""),
                "description": analysis_data.get("description", ""),
                "department": analysis_data.get("department", "सामान्य प्रशासन"),
                "priority": analysis_data.get("priority", "medium"),
                "location": analysis_data.get("location", ""),
                
                # Additional metadata
                "conversation_summary": analysis_data.get("conversation_summary", ""),
                "conversation_history": analysis_data.get("conversation_history", []),
                "timestamp": analysis_data.get("timestamp"),
                "analysis_completed_at": datetime.now().isoformat(),
                "analyzed_for_user": user_info['userId'],
                "user_name": user_info['name']
            }
        }

        # Log successful analysis
        complaint_preview = analysis_data.get("complaint", "")[:100]
        logger.info(f"Voice analysis completed for {user_info['name']}: {complaint_preview}... -> {analysis_data.get('department')} ({analysis_data.get('priority')})")

        return jsonify(enhanced_response), 200

    except Exception as e:
        logger.error(f"Voice analysis endpoint error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": "Voice analysis system error", 
            "error": str(e)
        }), 500


# Also update the existing voice-complaint endpoint to redirect to the new flow
@complaint_routes.route("/api/voice-complaint", methods=["POST"])
def voice_complaint_deprecated():
    """
    DEPRECATED: Legacy voice complaint endpoint
    This endpoint is deprecated in favor of the new two-step process:
    1. /api/voice-analysis (for voice processing)
    2. /api/complaint (for final submission with location/photo)
    """
    try:
        # Log deprecation warning
        logger.warning("DEPRECATED: /api/voice-complaint endpoint called - should use /api/voice-analysis + /api/complaint")
        
        # Get user info for logging
        user_info = get_user_from_token(request)
        if user_info:
            logger.warning(f"User {user_info['name']} is using deprecated voice complaint endpoint")
        
        return jsonify({
            "status": "error",
            "message": "This endpoint is deprecated. Please use the new voice analysis flow.",
            "deprecated": True,
            "new_endpoints": {
                "voice_analysis": "/api/voice-analysis",
                "complaint_submission": "/api/complaint"
            }
        }), 410  # 410 Gone - indicates deprecated endpoint

    except Exception as e:
        logger.error(f"Deprecated voice complaint endpoint error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Endpoint deprecated and unavailable",
            "error": str(e)
        }), 410