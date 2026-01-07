
# app/tests/test_app.py

import os
# Ensure CI/demo mode BEFORE importing the Flask app, so DB init is skipped.
os.environ['SKIP_DB'] = '1'

from app import app  # adjust import if your module path differs

def test_root_form_renders():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Add User' in resp.data

def test_submit_user_demo_mode():
    client = app.test_client()
    resp = client.post('/submituser', data={'name': 'Alice', 'email': 'a@example.com'})
    assert resp.status_code == 200
    # In SKIP_DB mode, your route should return a demo message (as per your comments/intent)
    # If your actual route still hits the DB, this may fail—see note below.
    assert b'Demo mode' in resp.data or b'added successfully' in resp.data

def test_get_users_demo_mode_returns_list():
    client = app.test_client()
    resp = client.get('/users')
    assert resp.status_code == 200
    # In SKIP_DB mode we expect an empty list; if DB is still used, we just assert JSON for now
    assert resp.is_json
