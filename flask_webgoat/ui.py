import sqlite3

from flask import Blueprint, request, session, render_template
from markupsafe import escape
from . import query_db

bp = Blueprint("ui", __name__)


def get_mandatory_param(request, param):
    value = request.args.get(param)
    if value is None:
        message = f"please provide the mandatory `{param}` parameter"
        return None, message
    return value, None


def get_invalid_parameters(request, params):
    invalid_params = {}
    for param in list(set(request.args.keys()) - set(params)):
        invalid_params[param] = request.args.get(param)
    return invalid_params
    

@bp.route("/search")
def search():
    query_param, err = get_mandatory_param(request, "query")
    
    # Mandatory param missing
    if query_param is None:
        
        # check: Can LLM understand that no user-controlled input is involved?
        # safe (ext): XSS, it is considered a vulnerability in the original demo app
        return render_template("error.html", message=err)
    
    invalid_params = get_invalid_parameters(request, ["query"])
    if invalid_params:
        message = f"invalid parameters provided, only 'query' is allowed: {",".join(invalid_params.keys())}, {",".join(invalid_params.values())}"
        
        # http://127.0.0.1:5000/search?query=admin&whatever=%3CScript%3Ealert(1)%3C/script%3E
        # vulnerability (ext): XSS
        return message

    # Parameter validation complete

    try:
        query = "SELECT username, access_level FROM user WHERE username LIKE ?;"
        results = query_db(query, (query_param,))
        return render_template(
            "search.html", results=results, num_results=len(results), query=query_param
        )
    except sqlite3.Error as err:
        message = "Error while executing query " + query_param + ": " + err
        return render_template("error.html", message=message)


@bp.route("/welcome")
def welcome():
    user_info = session.get("user_info", None)
    if user_info is None:
        return "Welcome anonymous user!"
    try:
        query = "SELECT nickname FROM user WHERE username LIKE ?;"
        results = query_db(query, (user_info[1],))

        # vulnerability (ext): stored-XSS
        return f"Welcome {results[0][0]}!"
    except sqlite3.Error as err:
        message = "Error while executing query " + user_info[1] + ": " + err
        return f"Error: {message}"


@bp.route("/welcome_safely")
def welcome_safely():
    user_info = session.get("user_info", None)
    if user_info is None:
        return "Welcome anonymous user!"
    try:
        query = "SELECT nickname FROM user WHERE username LIKE ?;"
        results = query_db(query, (user_info[1],))
        # Use the escape function to sanitize user input and prevent XSS
        safe_nickname = escape(results[0][0])
        return f"Welcome {safe_nickname}!"
    except sqlite3.Error as err:
        # Also sanitize the error message
        safe_username = escape(user_info[1])
        safe_error = escape(str(err))
        message = f"Error while executing query {safe_username}: {safe_error}"
        return f"Error: {message}"
        