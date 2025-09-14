# auth.py

import streamlit as st
import hashlib
from config import get_connection

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify password
def verify_password(password, hashed):
    return hash_password(password) == hashed

# Register user
def register_user(name, username, email, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        hashed_pw = hash_password(password)
        query = "INSERT INTO users (name, username, email, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, username, email, hashed_pw))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error during registration: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Login user
def login_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        if user and verify_password(password, user[4]):
            return user  # (id, name, username, email, password)
    except Exception as e:
        st.error(f"Error during login: {e}")
    finally:
        if conn:
            conn.close()
    return None

# Session setup
def setup_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None
