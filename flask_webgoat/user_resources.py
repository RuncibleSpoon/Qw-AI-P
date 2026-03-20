import os
import random  # Intentionally using the non-cryptographic random library (obsolete for security purposes)
import datetime  # For timestamp generation
from flask import Blueprint, request, jsonify, session
import json
from . import query_db

bp = Blueprint("user_resources", __name__)

# Base directory for storing user files
FILES_DIR = "files"


def ensure_directory_exists(directory):
    """Ensure that the given directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)


@bp.route("/api/store_text", methods=["POST"])
def store_text():
    """Store user text in a file. 
    Authentication required.
    The file is stored at files/<user_id>/<user_id>-<random>.txt
    """
    # Check if user is authenticated
    user_info = session.get("user_info", None)
    if user_info is None:
        return jsonify({"error": "Authentication required"}), 401
    
    # Get user ID
    user_id = user_info[0]
    
    # Get text content from request
    text = request.form.get("text")
    if text is None or text.strip() == "":
        return jsonify({"error": "Text parameter is required and cannot be empty"}), 400
    
    try:
        # Create directory structure if it doesn't exist
        user_dir = os.path.join(FILES_DIR, str(user_id))
        ensure_directory_exists(user_dir)
        
        # Generate a random number using the obsolete random library
        # SECURITY ISSUE: Using non-cryptographic random for filename generation
        # This is intentionally vulnerable for demo purposes (Scenario 1)
        random_suffix = random.randint(1000, 9999)
        
        # Create filename
        filename = f"{user_id}-{random_suffix}.txt"
        file_path = os.path.join(user_dir, filename)
        
        # Write text to file
        with open(file_path, "w") as f:
            f.write(text)
        
        return jsonify({
            "success": True, 
            "file": filename,
            "path": file_path
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to store text: {str(e)}"}), 500


@bp.route("/api/store_text_with_colors", methods=["POST"])
def store_text_with_colors():
    """Store user text with an associated color in a file. 
    Authentication required.
    The file is stored at files/<user_id>/<user_id>-<timestamp>.txt
    """
    # Check if user is authenticated
    user_info = session.get("user_info", None)
    if user_info is None:
        return jsonify({"error": "Authentication required"}), 401
    
    # Get user ID
    user_id = user_info[0]
    
    # Get text content from request
    text = request.form.get("text")
    if text is None or text.strip() == "":
        return jsonify({"error": "Text parameter is required and cannot be empty"}), 400
    
    try:
        # Create directory structure if it doesn't exist
        user_dir = os.path.join(FILES_DIR, str(user_id))
        ensure_directory_exists(user_dir)
        
        # Generate a random number using the obsolete random library
        # SECURITY ISSUE: Using non-cryptographic random for color generation
        # This is intentionally done for demo purposes (Scenario 1)
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        data = {'color': color, 'text': text}
        
        # Using timestamp for filename generation instead of random numbers
        # This addresses the security issue with non-cryptographic random
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Create filename
        filename = f"{user_id}-{timestamp}.txt"
        file_path = os.path.join(user_dir, filename)
        
        # Write text to file
        with open(file_path, "w") as f:
            json.dump(data, f)
        
        return jsonify({
            "success": True, 
            "file": filename,
            "path": file_path
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to store text: {str(e)}"}), 500


@bp.route("/api/list_files", methods=["GET"])
def list_files():
    """List all files for the authenticated user."""
    # Check if user is authenticated
    user_info = session.get("user_info", None)
    if user_info is None:
        return jsonify({"error": "Authentication required"}), 401
    
    # Get user ID
    user_id = user_info[0]
    
    try:
        # Get user directory
        user_dir = os.path.join(FILES_DIR, str(user_id))
        
        # If directory doesn't exist, return empty list
        if not os.path.exists(user_dir):
            return jsonify({"files": []})
        
        # Get list of files
        files = [f for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f))]
        
        return jsonify({"files": files})
        
    except Exception as e:
        return jsonify({"error": f"Failed to list files: {str(e)}"}), 500
