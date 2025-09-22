# # from flask import Blueprint, request, jsonify
# # from werkzeug.security import generate_password_hash, check_password_hash
# # import uuid
# # import datetime
# # import os
# # from config import users_collection

# # auth_bp = Blueprint("auth_bp", __name__)
# # UPLOAD_FOLDER = "uploads"
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # @auth_bp.route("/api/auth/register", methods=["POST"])
# # def register():
# #     try:
# #         name = request.form.get("name")
# #         email = request.form.get("email")
# #         password = request.form.get("password")
# #         phone = request.form.get("phone")
# #         address = request.form.get("address")
# #         photo = request.files.get("photo")

# #         if not all([name, email, password, phone, address]):
# #             return jsonify({"success": False, "message": "All fields required"}), 400

# #         # Check duplicate email or phone
# #         if users_collection.find_one({"$or": [{"email": email}, {"phone": phone}]}):
# #             return jsonify({"success": False, "message": "Email or phone already exists"}), 400

# #         photo_path = None
# #         if photo:
# #             filename = f"{uuid.uuid4()}_{photo.filename}"
# #             filepath = os.path.join(UPLOAD_FOLDER, filename)
# #             photo.save(filepath)
# #             photo_path = filepath

# #         user = {
# #             "userId": str(uuid.uuid4()),
# #             "name": name,
# #             "email": email,
# #             "phone": phone,
# #             "address": address,
# #             "photo": photo_path,
# #             "passwordHash": generate_password_hash(password),
# #             "createdAt": datetime.datetime.utcnow()
# #         }

# #         users_collection.insert_one(user)

# #         return jsonify({
# #             "success": True,
# #             "message": "User registered successfully",
# #             "userId": user["userId"]
# #         }), 201

# #     except Exception as e:
# #         return jsonify({"success": False, "message": "Registration failed", "error": str(e)}), 500


# # @auth_bp.route("/api/auth/login", methods=["POST"])
# # def login():
# #     try:
# #         data = request.json
# #         identifier = data.get("email") or data.get("phone")
# #         password = data.get("password")

# #         if not identifier or not password:
# #             return jsonify({"success": False, "message": "Email/Phone and password required"}), 400

# #         user = users_collection.find_one({"$or": [{"email": identifier}, {"phone": identifier}]})

# #         if not user or not check_password_hash(user["passwordHash"], password):
# #             return jsonify({"success": False, "message": "Invalid credentials"}), 401

# #         return jsonify({
# #             "success": True,
# #             "userId": user["userId"],
# #             "name": user["name"],
# #             "email": user["email"],
# #             "phone": user["phone"],
# #             "address": user["address"],
# #             "photo": user.get("photo")
# #         }), 200

# #     except Exception as e:
# #         return jsonify({"success": False, "message": "Login failed", "error": str(e)}), 500


# # backend/route/auth.py
# from flask import Blueprint, request, jsonify
# from werkzeug.security import generate_password_hash, check_password_hash
# import uuid
# import datetime
# import os
# import jwt
# from config import users_collection

# auth_bp = Blueprint("auth_bp", __name__)
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # JWT Secret Key - Change this to a secure random key in production
# JWT_SECRET_KEY = "your-secret-key-change-in-production"

# @auth_bp.route("/api/auth/register", methods=["POST"])
# def register():
#     try:
#         name = request.form.get("name")
#         email = request.form.get("email")
#         password = request.form.get("password")
#         phone = request.form.get("phone")
#         address = request.form.get("address")
#         photo = request.files.get("photo")

#         if not all([name, email, password, phone, address]):
#             return jsonify({"success": False, "message": "All fields required"}), 400

#         # Check duplicate email or phone
#         if users_collection.find_one({"$or": [{"email": email}, {"phone": phone}]}):
#             return jsonify({"success": False, "message": "Email or phone already exists"}), 400

#         photo_path = None
#         if photo:
#             filename = f"{uuid.uuid4()}_{photo.filename}"
#             filepath = os.path.join(UPLOAD_FOLDER, filename)
#             photo.save(filepath)
#             photo_path = filepath

#         user_id = str(uuid.uuid4())
#         user = {
#             "userId": user_id,
#             "name": name,
#             "email": email,
#             "phone": phone,
#             "address": address,
#             "photo": photo_path,
#             "passwordHash": generate_password_hash(password),
#             "createdAt": datetime.datetime.utcnow(),
#             "isActive": True
#         }

#         users_collection.insert_one(user)

#         # Generate JWT token
#         token_payload = {
#             'userId': user_id,
#             'email': email,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Token expires in 7 days
#         }
#         token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm='HS256')

#         return jsonify({
#             "success": True,
#             "message": "User registered successfully",
#             "userId": user["userId"],
#             "name": name,
#             "email": email,
#             "phone": phone,
#             "address": address,
#             "photo": photo_path,
#             "token": token
#         }), 201

#     except Exception as e:
#         return jsonify({"success": False, "message": "Registration failed", "error": str(e)}), 500


# @auth_bp.route("/api/auth/login", methods=["POST"])
# # backend/route/auth.py - Updated login route
# def login():
#     try:
#         data = request.json
#         identifier = data.get("email") or data.get("phone")  # Can accept email or phone
#         password = data.get("password")

#         if not identifier or not password:
#             return jsonify({
#                 "success": False, 
#                 "message": "Email/Phone and password required",
#                 "error": "Email/Phone and password required"
#             }), 400

#         # Find user by email or phone
#         user = users_collection.find_one({"$or": [{"email": identifier}, {"phone": identifier}]})

#         if not user:
#             return jsonify({
#                 "success": False, 
#                 "message": "User not found",
#                 "error": "User not found"
#             }), 404

#         if not user.get("isActive", True):
#             return jsonify({
#                 "success": False, 
#                 "message": "Account is deactivated",
#                 "error": "Account is deactivated"
#             }), 403

#         if not check_password_hash(user["passwordHash"], password):
#             return jsonify({
#                 "success": False, 
#                 "message": "Invalid password",
#                 "error": "Invalid password"
#             }), 401

#         # Generate JWT token
#         token_payload = {
#             'userId': user['userId'],
#             'email': user['email'],
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
#         }
#         token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm='HS256')

#         # Update last login time
#         users_collection.update_one(
#             {"userId": user["userId"]},
#             {"$set": {"lastLoginAt": datetime.datetime.utcnow()}}
#         )

#         # Return complete user data for frontend
#         return jsonify({
#             "success": True,
#             "message": "Login successful",
#             "token": token,
#             "userId": user["userId"],
#             "name": user["name"],
#             "email": user["email"],
#             "phone": user["phone"],
#             "address": user["address"],
#             "photo": user.get("photo"),
#             "createdAt": user["createdAt"].isoformat() if user.get("createdAt") else None
#         }), 200

#     except Exception as e:
#         print(f"Login error: {str(e)}")  # For debugging
#         return jsonify({
#             "success": False, 
#             "message": "Login failed", 
#             "error": str(e)
#         }), 500


# @auth_bp.route("/api/auth/verify-token", methods=["POST"])
# def verify_token():
#     """Verify if the provided token is valid"""
#     try:
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({"success": False, "message": "Token missing"}), 401
        
#         # Remove 'Bearer ' prefix if present
#         if token.startswith('Bearer '):
#             token = token[7:]
        
#         # Verify token
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
#         user_id = payload['userId']
        
#         # Get user data
#         user = users_collection.find_one({"userId": user_id})
#         if not user:
#             return jsonify({"success": False, "message": "User not found"}), 404
            
#         return jsonify({
#             "success": True,
#             "userId": user["userId"],
#             "name": user["name"],
#             "email": user["email"],
#             "phone": user["phone"],
#             "address": user["address"],
#             "photo": user.get("photo")
#         }), 200
        
#     except jwt.ExpiredSignatureError:
#         return jsonify({"success": False, "message": "Token expired"}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({"success": False, "message": "Invalid token"}), 401
#     except Exception as e:
#         return jsonify({"success": False, "message": "Token verification failed", "error": str(e)}), 500


# @auth_bp.route("/api/users/<user_id>", methods=["GET"])
# def get_user(user_id):
#     """Get user profile data"""
#     try:
#         # Verify token
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({"success": False, "message": "Token missing"}), 401
        
#         if token.startswith('Bearer '):
#             token = token[7:]
        
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
#         if payload['userId'] != user_id:
#             return jsonify({"success": False, "message": "Unauthorized"}), 403
        
#         # Get user data
#         user = users_collection.find_one({"userId": user_id}, {"passwordHash": 0})  # Exclude password
#         if not user:
#             return jsonify({"success": False, "message": "User not found"}), 404
        
#         # Convert ObjectId to string for JSON serialization
#         if '_id' in user:
#             user['_id'] = str(user['_id'])
            
#         return jsonify({
#             "success": True,
#             "user": user
#         }), 200
        
#     except jwt.ExpiredSignatureError:
#         return jsonify({"success": False, "message": "Token expired"}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({"success": False, "message": "Invalid token"}), 401
#     except Exception as e:
#         return jsonify({"success": False, "message": "Failed to get user data", "error": str(e)}), 500



from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import datetime
import os
import jwt
from config import users_collection
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth_bp", __name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# JWT Secret Key - Change this to a secure random key in production
JWT_SECRET_KEY = "your-secret-key-change-in-production"

# Admin credentials (in production, store in database)
ADMIN_CREDENTIALS = {
    "admin@municipality.gov.in": {
        "password": "admin123",  # Change this in production
        "role": "admin",
        "name": "System Administrator",
        "departments": ["all"]
    }
}

@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """User registration endpoint"""
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        address = request.form.get("address")
        photo = request.files.get("photo")

        if not all([name, email, password, phone, address]):
            return jsonify({"success": False, "message": "All fields required"}), 400

        # Check duplicate email or phone
        if users_collection.find_one({"$or": [{"email": email}, {"phone": phone}]}):
            return jsonify({"success": False, "message": "Email or phone already exists"}), 400

        photo_path = None
        if photo:
            filename = f"{uuid.uuid4()}_{photo.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            photo.save(filepath)
            photo_path = filepath

        user_id = str(uuid.uuid4())
        user = {
            "userId": user_id,
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "photo": photo_path,
            "passwordHash": generate_password_hash(password),
            "role": "user",  # Default role
            "createdAt": datetime.datetime.utcnow(),
            "isActive": True
        }

        users_collection.insert_one(user)

        # Generate JWT token
        token_payload = {
            'userId': user_id,
            'email': email,
            'role': 'user',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm='HS256')

        logger.info(f"New user registered: {email}")

        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "userId": user["userId"],
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "photo": photo_path,
            "role": "user",
            "token": token
        }), 201

    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({"success": False, "message": "Registration failed", "error": str(e)}), 500


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """Enhanced login endpoint supporting both users and admins"""
    try:
        data = request.json
        identifier = data.get("email") or data.get("phone")
        password = data.get("password")

        if not identifier or not password:
            return jsonify({
                "success": False, 
                "message": "Email/Phone and password required",
                "error": "Email/Phone and password required"
            }), 400

        # Check if it's an admin login
        if identifier in ADMIN_CREDENTIALS:
            admin = ADMIN_CREDENTIALS[identifier]
            if password == admin["password"]:  # In production, use hashed passwords
                # Set admin session
                session["admin_logged_in"] = True
                session["admin_email"] = identifier
                session["admin_role"] = admin["role"]
                
                # Generate admin token
                token_payload = {
                    'email': identifier,
                    'role': 'admin',
                    'departments': admin["departments"],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Shorter expiry for admin
                }
                token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm='HS256')
                
                logger.info(f"Admin login: {identifier}")
                
                return jsonify({
                    "success": True,
                    "message": "Admin login successful",
                    "token": token,
                    "role": "admin",
                    "name": admin["name"],
                    "email": identifier,
                    "departments": admin["departments"]
                }), 200
            else:
                return jsonify({
                    "success": False, 
                    "message": "Invalid admin credentials",
                    "error": "Invalid admin credentials"
                }), 401

        # Regular user login
        user = users_collection.find_one({"$or": [{"email": identifier}, {"phone": identifier}]})

        if not user:
            return jsonify({
                "success": False, 
                "message": "User not found",
                "error": "User not found"
            }), 404

        if not user.get("isActive", True):
            return jsonify({
                "success": False, 
                "message": "Account is deactivated",
                "error": "Account is deactivated"
            }), 403

        if not check_password_hash(user["passwordHash"], password):
            return jsonify({
                "success": False, 
                "message": "Invalid password",
                "error": "Invalid password"
            }), 401

        # Generate JWT token for regular user
        token_payload = {
            'userId': user['userId'],
            'email': user['email'],
            'role': user.get('role', 'user'),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm='HS256')

        # Update last login time
        users_collection.update_one(
            {"userId": user["userId"]},
            {"$set": {"lastLoginAt": datetime.datetime.utcnow()}}
        )

        logger.info(f"User login: {user['email']}")

        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token,
            "userId": user["userId"],
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
            "address": user["address"],
            "photo": user.get("photo"),
            "role": user.get("role", "user"),
            "createdAt": user["createdAt"].isoformat() if user.get("createdAt") else None
        }), 200

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Login failed", 
            "error": str(e)
        }), 500


@auth_bp.route("/api/auth/admin/login", methods=["POST"])
def admin_login():
    """Dedicated admin login endpoint"""
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "success": False, 
                "message": "Email and password required"
            }), 400

        # Check admin credentials
        if email not in ADMIN_CREDENTIALS:
            return jsonify({
                "success": False, 
                "message": "Invalid admin credentials"
            }), 401

        admin = ADMIN_CREDENTIALS[email]
        if password != admin["password"]:  # In production, use hashed passwords
            return jsonify({
                "success": False, 
                "message": "Invalid admin credentials"
            }), 401

        # Set admin session
        session["admin_logged_in"] = True
        session["admin_email"] = email
        session["admin_role"] = admin["role"]
        
        # Generate admin token
        token_payload = {
            'email': email,
            'role': 'admin',
            'departments': admin["departments"],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # 8 hour expiry for admin
        }
        token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm='HS256')
        
        logger.info(f"Admin login: {email}")
        
        return jsonify({
            "success": True,
            "message": "Admin login successful",
            "token": token,
            "role": "admin",
            "name": admin["name"],
            "email": email,
            "departments": admin["departments"]
        }), 200

    except Exception as e:
        logger.error(f"Admin login error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Admin login failed", 
            "error": str(e)
        }), 500


@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """Logout endpoint for both users and admins"""
    try:
        # Clear session
        session.clear()
        
        return jsonify({
            "success": True,
            "message": "Logged out successfully"
        }), 200

    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({
            "success": False, 
            "message": "Logout failed", 
            "error": str(e)
        }), 500


@auth_bp.route("/api/auth/verify-token", methods=["POST"])
def verify_token():
    """Verify if the provided token is valid"""
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"success": False, "message": "Token missing"}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Verify token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        
        # Check if it's an admin token
        if payload.get('role') == 'admin':
            return jsonify({
                "success": True,
                "role": "admin",
                "email": payload.get('email'),
                "departments": payload.get('departments', [])
            }), 200
        
        # Regular user token
        user_id = payload.get('userId')
        if not user_id:
            return jsonify({"success": False, "message": "Invalid token format"}), 401
        
        # Get user data
        user = users_collection.find_one({"userId": user_id})
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        if not user.get("isActive", True):
            return jsonify({"success": False, "message": "Account deactivated"}), 403
            
        return jsonify({
            "success": True,
            "userId": user["userId"],
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
            "address": user["address"],
            "photo": user.get("photo"),
            "role": user.get("role", "user")
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"success": False, "message": "Invalid token"}), 401
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return jsonify({"success": False, "message": "Token verification failed", "error": str(e)}), 500


@auth_bp.route("/api/auth/verify-admin", methods=["POST"])
def verify_admin():
    """Verify if the user has admin access"""
    try:
        # Check session first
        if session.get("admin_logged_in"):
            return jsonify({
                "success": True,
                "role": "admin",
                "email": session.get("admin_email")
            }), 200

        # Check token
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"success": False, "message": "Not authenticated"}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        
        if payload.get('role') != 'admin':
            return jsonify({"success": False, "message": "Not authorized as admin"}), 403
            
        return jsonify({
            "success": True,
            "role": "admin",
            "email": payload.get('email'),
            "departments": payload.get('departments', [])
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "message": "Admin token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"success": False, "message": "Invalid admin token"}), 401
    except Exception as e:
        logger.error(f"Admin verification error: {str(e)}")
        return jsonify({"success": False, "message": "Admin verification failed", "error": str(e)}), 500


@auth_bp.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get user profile data"""
    try:
        # Verify token
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"success": False, "message": "Token missing"}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        
        # Allow admin to access any user profile
        if payload.get('role') == 'admin':
            pass
        elif payload.get('userId') != user_id:
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        
        # Get user data
        user = users_collection.find_one({"userId": user_id}, {"passwordHash": 0})  # Exclude password
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Convert ObjectId to string for JSON serialization
        if '_id' in user:
            user['_id'] = str(user['_id'])
        
        # Convert datetime to string
        if user.get('createdAt'):
            user['createdAt'] = user['createdAt'].isoformat()
        if user.get('lastLoginAt'):
            user['lastLoginAt'] = user['lastLoginAt'].isoformat()
            
        return jsonify({
            "success": True,
            "user": user
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"success": False, "message": "Invalid token"}), 401
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        return jsonify({"success": False, "message": "Failed to get user data", "error": str(e)}), 500


@auth_bp.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Update user profile"""
    try:
        # Verify token
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"success": False, "message": "Token missing"}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        
        # Only allow user to update their own profile (or admin)
        if payload.get('role') != 'admin' and payload.get('userId') != user_id:
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        
        # Get update data
        data = request.json
        update_fields = {}
        
        allowed_fields = ['name', 'phone', 'address']
        for field in allowed_fields:
            if field in data:
                update_fields[field] = data[field]
        
        if not update_fields:
            return jsonify({"success": False, "message": "No valid fields to update"}), 400
        
        update_fields['updatedAt'] = datetime.datetime.utcnow()
        
        # Update user
        result = users_collection.update_one(
            {"userId": user_id},
            {"$set": update_fields}
        )
        
        if result.matched_count == 0:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"success": False, "message": "Invalid token"}), 401
    except Exception as e:
        logger.error(f"Update user error: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update user", "error": str(e)}), 500


@auth_bp.route("/api/admin/users", methods=["GET"])
def get_all_users():
    """Get all users (admin only)"""
    try:
        # Verify admin access
        if not session.get("admin_logged_in"):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"success": False, "message": "Admin access required"}), 401
            
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            if payload.get('role') != 'admin':
                return jsonify({"success": False, "message": "Admin access required"}), 403

        # Get pagination parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        
        # Build query
        query = {}
        if search:
            query = {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"email": {"$regex": search, "$options": "i"}},
                    {"phone": {"$regex": search, "$options": "i"}}
                ]
            }
        
        # Get total count
        total_count = users_collection.count_documents(query)
        
        # Get users with pagination
        users = list(users_collection.find(query, {"passwordHash": 0})
                    .sort("createdAt", -1)
                    .skip((page - 1) * limit)
                    .limit(limit))
        
        # Clean up users for response
        for user in users:
            user.pop('_id', None)
            if user.get('createdAt'):
                user['createdAt'] = user['createdAt'].isoformat()
            if user.get('lastLoginAt'):
                user['lastLoginAt'] = user['lastLoginAt'].isoformat()
        
        return jsonify({
            "success": True,
            "users": users,
            "pagination": {
                "total_count": total_count,
                "page": page,
                "limit": limit,
                "total_pages": (total_count + limit - 1) // limit
            }
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "message": "Admin token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"success": False, "message": "Invalid admin token"}), 401
    except Exception as e:
        logger.error(f"Get all users error: {str(e)}")
        return jsonify({"success": False, "message": "Failed to get users", "error": str(e)}), 500