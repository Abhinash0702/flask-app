
# app/tests/test_app.py
import os
# Ensure CI/demo mode BEFORE importing the Flask app
os.environ['SKIP_DB'] = '1'

from app import app

def test_root_form_renders():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Add User' in resp.data

def test_submit_user_demo_mode():
    client = app.test_client()
    resp = client.post('/submituser', data={'name': 'Alice', 'email': 'a@example.com'})
    assert resp.status_code == 200
    assert b'Demo mode' in resp.data

def test_get_users_demo_mode_returns_empty_list():
    client = app.test_client()
    resp = client.get('/users')
    assert resp.status_code == 200
    assert resp.is_json
    assert resp.get_json() == []
