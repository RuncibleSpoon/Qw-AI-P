from flask import Blueprint, request, jsonify, session, redirect, url_for
import re
from urllib.parse import urlparse
from . import query_db

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None or password is None:
        return (
            jsonify({"error": "username and password parameter have to be provided"}),
            400,
        )

    # vulnerability: SQL Injection
    query = (
        "SELECT id, username, access_level FROM user WHERE username = '%s' AND password = '%s'"
        % (username, password)
    )
    result = query_db(query, [], True)
    if result is None:
        return jsonify({"bad_login": True}), 400
    session["user_info"] = (result[0], result[1], result[2])
    return jsonify({"success": True})


@bp.route("/login_and_redirect")
def login_and_redirect():
    username = request.args.get("username")
    password = request.args.get("password")
    url = request.args.get("url")
    if username is None or password is None or url is None:
        return (
            jsonify(
                {"error": "username, password, and url parameters have to be provided"}
            ),
            400,
        )

    # sanitizer: SQL Injection    
    query = "SELECT id, username, access_level FROM user WHERE username = ? AND password = ?"
    result = query_db(query, (username, password), True)
    if result is None:
        # vulnerability: Open Redirect
        return redirect(url)
    session["user_info"] = (result[0], result[1], result[2])
    return jsonify({"success": True})


def is_safe_url(url):
    """Check if the URL is safe to redirect to."""
    if not url:
        return False
        
    # Only allow relative URLs or URLs to trusted domains
    parsed_url = urlparse(url)
    
    # 1. Check if it's a relative URL (no netloc, no scheme)
    if not parsed_url.netloc and not parsed_url.scheme:
        return True
        
    # 2. Check against trusted domains
    trusted_domains = ['localhost', '127.0.0.1']
    return parsed_url.netloc in trusted_domains


@bp.route("/login_and_redirect_safely")
def login_and_redirect_safely():
    username = request.args.get("username")
    password = request.args.get("password")
    url = request.args.get("url")
    if username is None or password is None or url is None:
        return (
            jsonify(
                {"error": "username, password, and url parameters have to be provided"}
            ),
            400,
        )

    # sanitizer: SQL Injection    
    query = "SELECT id, username, access_level FROM user WHERE username = ? AND password = ?"
    result = query_db(query, (username, password), True)
    if result is None:
        # Check if the URL is safe before redirecting
        if is_safe_url(url):
            # sanitizer: Open Redirect
            return redirect(url)
        else:
            # Default fallback if URL is not safe
            return jsonify({"error": "Invalid redirect URL"}), 400
    
    session["user_info"] = (result[0], result[1], result[2])
    return jsonify({"success": True})


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    # Check if user is logged in
    if "user_info" in session:
        # Store username for confirmation message
        username = session["user_info"][1]
        # Clear the user_info from session
        session.pop("user_info", None)
        return jsonify({"success": True, "message": f"User {username} successfully logged out"})
    else:
        return jsonify({"success": False, "message": "No user currently logged in"}), 401

