from flask import g, redirect, request, session, url_for
from db.add_and_update import log_user_visit
from db.connection import user_preferences


def load_user():
    g.user = session.get("user")
    g.route = request.path
    if g.user:
        log_user_visit(g.route)
        g.preferences = user_preferences.find_one({"google_id": g.user['id']})
    else:
        g.preferences = None
        g.user = None


def check_authentication(): 
    protected_paths = ['/account', '/preferences']
    if request.path in protected_paths: 
        if not g.user: 
            return redirect(url_for('login'))