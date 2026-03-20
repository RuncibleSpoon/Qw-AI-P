import sqlite3

from flask import Blueprint, jsonify, session, request

from . import query_db

bp = Blueprint("users", __name__)


@bp.route("/create_user", methods=["POST"])
def create_user():
    user_info = session.get("user_info", None)
    if user_info is None:
        return jsonify({"error": "no user_info found in session"})

    access_level = user_info[2]
    if access_level != 0:
        return jsonify({"error": "access level of 0 is required for this action"})
    username = request.form.get("username")
    password = request.form.get("password")
    access_level = request.form.get("access_level")
    nickname = request.form.get("nickname")
    if username is None or password is None or access_level is None:
        return (
            jsonify(
                {
                    "error": "username, password, access_level, and nickname parameters have to be provided"
                }
            ),
            400,
        )
    if len(password) < 3:
        return (
            jsonify({"error": "the password needs to be at least 3 characters long"}),
            402,
        )

    # safe: SQL Injection
    query = (
        "INSERT INTO user (username, password, access_level, nickname) VALUES (?, ?, ?, ?)"
    )

    try:
        print(f"Attempting to create user: {username} with access level: {access_level}")
        result = query_db(query, (username, password, access_level, nickname), False, True)
        print(f"Result of query_db: {result}")
        
        # Verify user was actually created
        verify_query = "SELECT id, username, password, access_level, nickname FROM user WHERE username = ?"
        user = query_db(verify_query, (username,), True)
        print(f"Verification query result: {user}")
        
        return jsonify({"success": True, "user_created": user is not None})
    except sqlite3.Error as err:
        print(f"Error creating user: {err}")
        return jsonify({"error": f"could not create user: {str(err)}"})


@bp.route("/delete_user", methods=["DELETE"])
def delete_user():
    user_info = session.get("user_info", None)
    if user_info is None:
        return jsonify({"error": "no user_info found in session"})

    access_level = user_info[2]
    if access_level != 0:
        return jsonify({"error": "access level of 0 is required for this action"})
    id = request.form.get("id")
    
    if id is None:
        return (
            jsonify(
                {
                    "error": "id parameter has to be provided"
                }
            ),
            400,
        )
    if id == 0:
        return (
            jsonify({"error": "admin cannot be deleted"}),
            400,
        )

    # safe: SQL Injection
    query = "DELETE FROM user WHERE id = ?"

    try:
        print(f"Attempting to delete user with ID: {id}")
        query_db(query, (id,), False, True)
        
        # Verify user was actually deleted
        verify_query = "SELECT id FROM user WHERE id = ?"
        user = query_db(verify_query, (id,), True)
        print(f"Verification result (None means deletion successful): {user}")
        
        return jsonify({"success": True, "user_deleted": user is None})
    except sqlite3.Error as err:
        print(f"Error deleting user: {err}")
        return jsonify({"error": f"could not delete user: {str(err)}"})
