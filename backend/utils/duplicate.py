# Add these imports to the TOP of your complaint_routes.py file (after existing imports)
import difflib
import math
from datetime import datetime, timedelta
from collections import defaultdict
from config import users_collection , complaints_collection, logger
from flask import request, jsonify
from routes.complaint_routes import get_user_from_token, is_database_available, _to_float, analyze_complaint, get_estimated_resolution_time
import routes.complaint_routes as complaint_routes
from utils.generate_id import generate_complaint_id, generate_token
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Try to import sklearn components with fallback
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    print("Warning: scikit-learn not available. Text similarity will use basic methods only.")
    SKLEARN_AVAILABLE = False

# Helper function to calculate text similarity
def calculate_text_similarity(text1, text2):
    """
    Calculate similarity between two texts using multiple methods
    Returns similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0
    
    # Clean and normalize texts
    text1 = text1.lower().strip()
    text2 = text2.lower().strip()
    
    if text1 == text2:
        return 1.0
    
    # Method 1: Sequence similarity using difflib (always available)
    seq_similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
    
    # Method 2: TF-IDF Cosine similarity (if sklearn available)
    cosine_sim = 0.0
    if SKLEARN_AVAILABLE:
        try:
            vectorizer = TfidfVectorizer(stop_words=None, ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except Exception as e:
            logger.warning(f"TF-IDF similarity calculation failed: {e}")
            cosine_sim = 0.0
    
    # Method 3: Word overlap similarity
    words1 = set(text1.split())
    words2 = set(text2.split())
    if words1 or words2:
        word_overlap = len(words1 & words2) / len(words1 | words2)
    else:
        word_overlap = 0.0
    
    # Combined weighted similarity score
    if SKLEARN_AVAILABLE:
        combined_similarity = (seq_similarity * 0.3) + (cosine_sim * 0.5) + (word_overlap * 0.2)
    else:
        # Fallback when sklearn not available
        combined_similarity = (seq_similarity * 0.7) + (word_overlap * 0.3)
    
    return min(combined_similarity, 1.0)

def calculate_location_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula
    Returns distance in meters
    """
    if not all([lat1, lon1, lat2, lon2]):
        return float('inf')
    
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

def find_similar_complaints(new_complaint_text, new_location, new_lat, new_lng, department=None):
    """
    Find similar complaints based on text content and location proximity
    Returns list of similar complaints with similarity scores
    """
    try:
        # Build query to find potential duplicates
        # Look for complaints from the last 30 days to avoid old resolved issues
        recent_date = datetime.now() - timedelta(days=30)
        
        query = {
            "timestamp": {"$gte": recent_date},
            "status": {"$in": ["Pending", "In Progress"]}  # Only active complaints
        }
        
        # Filter by department if provided
        if department and department != 'सामान्य':
            query["department"] = department
        
        # Get recent complaints
        recent_complaints = list(complaints_collection.find(query))
        
        similar_complaints = []
        
        for complaint in recent_complaints:
            complaint_text = complaint.get('complaint') or complaint.get('description', '')
            complaint_location = complaint.get('location', '')
            complaint_lat = complaint.get('latitude')
            complaint_lng = complaint.get('longitude')
            
            # Skip if no text to compare
            if not complaint_text.strip():
                continue
            
            # Calculate text similarity
            text_similarity = calculate_text_similarity(new_complaint_text, complaint_text)
            
            # Calculate location similarity (if coordinates available)
            location_distance = float('inf')
            location_similarity = 0.0
            
            if complaint_lat and complaint_lng and new_lat and new_lng:
                location_distance = calculate_location_distance(new_lat, new_lng, complaint_lat, complaint_lng)
                # Location similarity decreases with distance (within 500m = high, within 2km = medium)
                if location_distance <= 500:  # Within 500m
                    location_similarity = 1.0 - (location_distance / 500) * 0.3  # High similarity
                elif location_distance <= 2000:  # Within 2km
                    location_similarity = 0.7 - ((location_distance - 500) / 1500) * 0.5  # Medium similarity
                else:
                    location_similarity = 0.1  # Low similarity for far locations
            else:
                # Fall back to text-based location comparison
                if complaint_location and new_location:
                    location_text_similarity = calculate_text_similarity(new_location, complaint_location)
                    location_similarity = location_text_similarity * 0.6  # Reduce weight for text-only comparison
            
            # Combined similarity score with weights
            # Text similarity: 60%, Location similarity: 40%
            combined_similarity = (text_similarity * 0.6) + (location_similarity * 0.4)
            
            # Consider it similar if combined similarity > 0.7 OR (text > 0.8 AND location > 0.3)
            is_similar = (combined_similarity > 0.7) or (text_similarity > 0.8 and location_similarity > 0.3)
            
            if is_similar:
                similar_complaints.append({
                    'complaint_id': complaint.get('id'),
                    'complaint_text': complaint_text[:200] + '...' if len(complaint_text) > 200 else complaint_text,
                    'location': complaint_location,
                    'department': complaint.get('department'),
                    'status': complaint.get('status'),
                    'timestamp': complaint.get('timestamp'),
                    'submitted_by': complaint.get('name'),
                    'user_id': complaint.get('userId'),
                    'text_similarity': round(text_similarity, 3),
                    'location_similarity': round(location_similarity, 3),
                    'location_distance': round(location_distance) if location_distance != float('inf') else None,
                    'combined_similarity': round(combined_similarity, 3),
                    'upvotes': len(complaint.get('upvotes', [])),
                    'downvotes': len(complaint.get('downvotes', [])),
                    'similar_users_count': len(complaint.get('similar_submissions', []))
                })
        
        # Sort by similarity score (highest first)
        similar_complaints.sort(key=lambda x: x['combined_similarity'], reverse=True)
        
        return similar_complaints[:5]  # Return top 5 similar complaints
        
    except Exception as e:
        logger.error(f"Error finding similar complaints: {str(e)}")
        return []

# REPLACE your existing submit_complaint endpoint with this enhanced version
@complaint_routes.route("/api/complaint", methods=["POST"])
def submit_complaint_with_duplicate_check():
    """
    Enhanced complaint submission with duplicate detection
    """
    try:
        # Get user information from token
        user_info = get_user_from_token(request)
        
        if not user_info or not user_info['userId']:
            return jsonify({"success": False, "message": "Authentication required"}), 401

        complaint_id = generate_complaint_id()
        token = generate_token()
        
        # Handle multipart form data (with files)
        if request.content_type and request.content_type.startswith("multipart/form-data"):
            complaint_text = request.form.get("complaint", "")
            location = request.form.get("location", "")
            name = user_info['name']
            latitude = _to_float(request.form.get("latitude"))
            longitude = _to_float(request.form.get("longitude"))
            force_new = request.form.get("forceNew", "false").lower() == "true"
            
            # Handle photo upload
            photo_file = request.files.get("photo")
            photo_url = None
            if photo_file:
                photo_filename = f"{complaint_id}_{photo_file.filename}"
                photo_path = os.path.join(UPLOAD_FOLDER, photo_filename)
                photo_file.save(photo_path)
                photo_url = f"/uploads/{photo_filename}"
        else:
            # Handle JSON data
            complaint_data = request.json
            complaint_text = complaint_data.get("complaint") or complaint_data.get("description", "")
            location = complaint_data.get("location", "")
            name = user_info['name']
            latitude = _to_float(complaint_data.get("latitude"))
            longitude = _to_float(complaint_data.get("longitude"))
            force_new = complaint_data.get("forceNew", False)
            photo_url = None

        if not complaint_text.strip():
            return jsonify({"success": False, "message": "Complaint text is required"}), 400

        # Perform NLP analysis
        analysis = analyze_complaint(complaint_text, location)
        
        # DUPLICATE DETECTION - Check for similar complaints (unless forcing new)
        similar_complaints = []
        if not force_new:
            similar_complaints = find_similar_complaints(
                complaint_text, location, latitude, longitude, analysis['department']
            )
        
        # If similar complaints found, decide whether to merge or create new
        if similar_complaints and not force_new:
            # Get the most similar complaint
            most_similar = similar_complaints[0]
            
            # High similarity threshold for automatic merging
            if most_similar['combined_similarity'] > 0.85:
                # MERGE WITH EXISTING COMPLAINT
                existing_complaint_id = most_similar['complaint_id']
                
                # Update the existing complaint with similar submission data
                similar_submission = {
                    "userId": user_info['userId'],
                    "userName": user_info['name'],
                    "userEmail": user_info['email'],
                    "complaint_text": complaint_text,
                    "location": location,
                    "latitude": latitude,
                    "longitude": longitude,
                    "timestamp": datetime.now(),
                    "photo_url": photo_url,
                    "similarity_score": most_similar['combined_similarity']
                }
                
                # Add to similar_submissions array in existing complaint
                update_result = complaints_collection.update_one(
                    {"id": existing_complaint_id},
                    {
                        "$push": {"similar_submissions": similar_submission},
                        "$inc": {"similar_users_count": 1},
                        "$set": {
                            "last_similar_submission": datetime.now(),
                            "updated_urgency": "high" if len(similar_complaints) >= 3 else analysis['urgency']
                        }
                    }
                )
                
                # Log the merge
                logger.info(f"Complaint {complaint_id} merged with existing complaint {existing_complaint_id} (similarity: {most_similar['combined_similarity']:.3f})")
                
                return jsonify({
                    "success": True,
                    "message": "Your complaint has been added to an existing similar issue",
                    "action": "merged",
                    "primary_complaint_id": existing_complaint_id,
                    "similarity_score": most_similar['combined_similarity'],
                    "similar_complaints": [{
                        "id": most_similar['complaint_id'],
                        "text_preview": most_similar['complaint_text'],
                        "location": most_similar['location'],
                        "status": most_similar['status'],
                        "total_similar_users": most_similar['similar_users_count'] + 1,
                        "department": most_similar['department']
                    }],
                    "user_submission": {
                        "your_complaint": complaint_text,
                        "your_location": location,
                        "timestamp": datetime.now().isoformat()
                    }
                }), 201
        
        # CREATE NEW COMPLAINT (no duplicates found or similarity below threshold)
        complaint = {
            "id": complaint_id,
            "token": token,
            "type": "form",
            
            # User Information
            "userId": user_info['userId'],
            "name": name,
            "email": user_info['email'],
            "phone": user_info['phone'],
            "userAddress": user_info['address'],
            "userRole": user_info['role'],
            
            # Complaint Details
            "complaint": complaint_text,
            "description": complaint_text,
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
            
            # Duplicate Detection Results
            "similar_complaints_found": len(similar_complaints),
            "similarity_scores": [s['combined_similarity'] for s in similar_complaints] if similar_complaints else [],
            "similar_submissions": [],  # Array to store similar submissions
            "similar_users_count": 0,
            
            # Additional metadata
            "has_photo": bool(photo_url),
            "has_geo_location": bool(latitude and longitude),
            "auto_classified": True,
            "is_authenticated": True,
            "duplicate_checked": True,
            "created_as_new": True,
            "sklearn_available": SKLEARN_AVAILABLE
        }

        # Check if database is available
        if not is_database_available():
            logger.warning("Database not available - complaint not saved")
            return jsonify({
                "success": True,
                "message": "Complaint processed but not saved (database unavailable)",
                "action": "processed",
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
        logger.info(f"New complaint {complaint_id} by {user_info['name']}: {complaint.get('department')} ({complaint.get('urgency')}) - {complaint_text[:100]}...")
        
        response_data = {
            "success": True,
            "message": "Complaint submitted successfully",
            "action": "created_new",
            "complaintId": complaint_id,
            "token": token,
            "complaint": {
                "complaintId": complaint_id,
                "submittedBy": user_info['name'],
                "department": complaint.get('department'),
                "urgency": complaint.get('urgency'),
                "estimatedResolutionTime": complaint.get('estimated_resolution'),
                "status": "pending",
                "confidence": complaint.get('confidence'),
                "duplicate_check_performed": True,
                "similar_found": len(similar_complaints),
                "ml_features_available": SKLEARN_AVAILABLE
            }
        }
        
        # Include similar complaints info if found but not merged
        if similar_complaints:
            response_data["similar_complaints_detected"] = {
                "count": len(similar_complaints),
                "highest_similarity": similar_complaints[0]['combined_similarity'],
                "message": f"Found {len(similar_complaints)} similar complaints, but created new due to differences",
                "similar_list": [
                    {
                        "id": s['complaint_id'],
                        "text_preview": s['complaint_text'][:100] + "...",
                        "location": s['location'],
                        "similarity": s['combined_similarity'],
                        "status": s['status']
                    } for s in similar_complaints[:3]
                ]
            }
        
        return jsonify(response_data), 201

    except Exception as e:
        logger.error(f"Complaint submission error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False, 
            "message": "Complaint submission failed", 
            "error": str(e)
        }), 500

# NEW ENDPOINT: Get similar complaints for a specific complaint
@complaint_routes.route("/api/complaint/<complaint_id>/similar", methods=["GET"])
def get_similar_complaints(complaint_id):
    """
    Get all similar complaints for a specific complaint ID
    """
    try:
        # Get user information from token (admin or complaint owner)
        user_info = get_user_from_token(request)
        
        if not user_info:
            return jsonify({"success": False, "message": "Authentication required"}), 401

        # Get the main complaint
        main_complaint = complaints_collection.find_one({"id": complaint_id})
        if not main_complaint:
            return jsonify({"success": False, "message": "Complaint not found"}), 404

        # Check permissions
        if not user_info['isAdmin'] and main_complaint.get('userId') != user_info['userId']:
            return jsonify({"success": False, "message": "Unauthorized"}), 403

        # Get similar submissions
        similar_submissions = main_complaint.get('similar_submissions', [])
        
        # Clean up similar submissions data
        for submission in similar_submissions:
            if submission.get('timestamp'):
                submission['timestamp'] = submission['timestamp'].isoformat()

        response_data = {
            "success": True,
            "main_complaint": {
                "id": main_complaint.get('id'),
                "complaint": main_complaint.get('complaint'),
                "location": main_complaint.get('location'),
                "department": main_complaint.get('department'),
                "status": main_complaint.get('status'),
                "submitted_by": main_complaint.get('name'),
                "timestamp": main_complaint.get('timestamp').isoformat() if main_complaint.get('timestamp') else None
            },
            "similar_submissions": similar_submissions,
            "total_similar_users": len(similar_submissions),
            "summary": {
                "total_users_affected": len(similar_submissions) + 1,  # +1 for original submitter
                "locations_affected": list(set(s.get('location', '') for s in similar_submissions if s.get('location'))),
                "average_similarity": sum(s.get('similarity_score', 0) for s in similar_submissions) / max(len(similar_submissions), 1)
            }
        }

        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"Error fetching similar complaints: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Failed to fetch similar complaints", 
            "error": str(e)
        }), 500
    