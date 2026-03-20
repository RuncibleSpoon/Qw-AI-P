import os
import sqlite3
from pathlib import Path

from flask import Flask, g

import os

# Use absolute path to ensure database is created in the application directory
DB_FILENAME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database.db")


def query_db(query, args=(), one=False, commit=False):
    with sqlite3.connect(DB_FILENAME) as conn:
        # vulnerability: Sensitive Data Exposure
        conn.set_trace_callback(print)
        cur = conn.cursor().execute(query, args)
        if commit:
            conn.commit()
        return cur.fetchone() if one else cur.fetchall()


def create_app():
    app = Flask(__name__)
    # vulnerability (ext, out-of-scope): Hardcoded secret
    app.secret_key = "aeZ1iwoh2ree2mo0Eereireong4baitixaixu5Ee"

    # Connect to the database without deleting it first
    conn = sqlite3.connect(DB_FILENAME)
    create_table_query = """CREATE TABLE IF NOT EXISTS user
    (id INTEGER PRIMARY KEY, username TEXT, password TEXT, access_level INTEGER, nickname TEXT)"""
    conn.execute(create_table_query)

    # vulnerability (ext, out-of-scope): Hardcoded password secret
    insert_admin_query = """INSERT OR IGNORE INTO user (id, username, password, access_level, nickname)
    VALUES (1, 'admin', 'maximumentropy', 0, 'SeriousAdmin')"""
    conn.execute(insert_admin_query)
    conn.commit()
    conn.close()

    with app.app_context():
        from . import actions
        from . import auth
        from . import status
        from . import ui
        from . import users
        from . import user_resources

        app.register_blueprint(actions.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(status.bp)
        app.register_blueprint(ui.bp)
        app.register_blueprint(user_resources.bp)
        app.register_blueprint(users.bp)
        return app
