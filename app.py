# app.py
# Full Streamlit app: Neo-Glass Frosted Purple UI + upgraded history table & charts
# Paste into app.py and run: streamlit run app.py

import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import joblib
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import plotly.graph_objects as go
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import os
import re
import uuid
import json
import html
def safe_rerun():
    st.rerun()


POPPLER_PATH = r"C:\Poppler\poppler-25.11.0\Library\bin"  
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 


st.set_page_config(page_title="HeartCareAI", page_icon="🫀", layout="wide")


st.markdown("""
<style>
            
            /* ===============================
   DARK PREMIUM BUTTON SYSTEM
================================ */

/* ===============================
   SKY BLUE PREMIUM BUTTONS
================================ */

div.stButton > button {
    background: linear-gradient(135deg, #2563EB, #38BDF8) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 22px !important;
    font-size: 15px !important;
    font-weight: 800 !important;
    letter-spacing: 0.3px;
    box-shadow: 0 14px 32px rgba(37,99,235,0.45) !important;
    transition: all 0.25s ease-in-out !important;
}

/* Hover */
div.stButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8, #0EA5E9) !important;
    transform: translateY(-3px);
    box-shadow: 0 20px 42px rgba(14,165,233,0.55) !important;
}

/* Click */
div.stButton > button:active {
    transform: scale(0.97);
}

/* Remove focus outline */
div.stButton > button:focus {
    outline: none !important;
}


            
/* ================================
   AUTH QUOTE CARD (SMALL & CLEAN)
================================ */

.auth-quote-card{
    display:flex;
    align-items:center;
    gap:12px;
    padding:16px 22px;
    border-radius:20px;
    background: linear-gradient(
        135deg,
        rgba(79,70,229,0.08),
        rgba(6,182,212,0.08)
    );
    border:1px solid var(--border);
    box-shadow: var(--shadow);
    margin-bottom:22px;
    font-size:14px;
}

.auth-quote-icon{
    width:36px;
    height:36px;
    border-radius:12px;
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--secondary)
    );
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:18px;
    box-shadow: 0 8px 20px rgba(79,70,229,0.35);
}

.auth-quote-text{
    color:var(--text);
    font-weight:600;
}
            
/* ================================
   AUTH PAGE – PREMIUM UI
================================ */

.auth-header{
    display:flex;
    align-items:center;
    gap:20px;
    padding:26px 30px;
    border-radius:24px;
    background: linear-gradient(
        135deg,
        rgba(79,70,229,0.12),
        rgba(6,182,212,0.12)
    );
    border:1px solid var(--border);
    box-shadow: 0 16px 45px rgba(79,70,229,0.15);
    margin-bottom:26px;
}

.auth-icon{
    width:64px;
    height:64px;
    border-radius:18px;
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--secondary)
    );
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:30px;
    color:white;
    box-shadow: 0 12px 30px rgba(79,70,229,0.4);
}

.auth-header h2{
    margin:0;
    font-size:22px;
    font-weight:800;
}

.auth-header p{
    margin-top:6px;
    font-size:14px;
    color:var(--muted);
}

/* Auth cards */
.auth-card{
    background:white;
    border-radius:22px;
    padding:26px;
    border:1px solid var(--border);
    box-shadow: var(--shadow);
    margin-bottom:26px;
}

/* Section titles */
.auth-card h3{
    margin-bottom:12px;
    font-size:18px;
    font-weight:800;
}

/* Password reset info box */
.reset-info{
    background: rgba(79,70,229,0.08);
    padding:14px 18px;
    border-radius:14px;
    font-size:13px;
    color:#1e293b;
    margin-bottom:14px;
}
            
/* ================================
   UPLOAD PAGE – PREMIUM SECTION
================================ */

.upload-header{
    display:flex;
    align-items:center;
    gap:22px;
    padding:28px 30px;
    border-radius:24px;
    background: linear-gradient(
        135deg,
        rgba(79,70,229,0.12),
        rgba(6,182,212,0.12)
    );
    border:1px solid var(--border);
    box-shadow: 0 18px 45px rgba(79,70,229,0.15);
    margin-bottom:26px;
    animation: fadeSlideIn 0.6s ease;
}

.upload-header-icon{
    width:70px;
    height:70px;
    border-radius:20px;
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--secondary)
    );
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:34px;
    color:white;
    box-shadow: 0 12px 30px rgba(79,70,229,0.4);
    animation: floatIcon 3s ease-in-out infinite;
}

.upload-header-content h2{
    margin:0;
    font-size:24px;
    font-weight:800;
}

.upload-header-content p{
    margin-top:6px;
    font-size:14px;
    color:var(--muted);
    max-width:650px;
    line-height:1.5;
}

.upload-badges{
    display:flex;
    gap:10px;
    margin-top:10px;
}

.upload-badges span{
    background: white;
    border:1px solid var(--border);
    border-radius:999px;
    padding:6px 12px;
    font-size:12px;
    font-weight:700;
    color:var(--primary);
}

/* Upload box animation */
div[data-testid="stFileUploader"] section{
    border-radius:18px !important;
    border:2px dashed var(--primary) !important;
    background: linear-gradient(135deg,#ffffff,#f8fafc) !important;
    padding:24px !important;
    transition: 
        transform 0.3s ease,
        box-shadow 0.3s ease;
}

div[data-testid="stFileUploader"] section:hover{
    transform: translateY(-6px);
    box-shadow: 0 18px 40px rgba(79,70,229,0.25);
}

/* Keyframe animations */
@keyframes floatIcon{
    0%{ transform: translateY(0); }
    50%{ transform: translateY(-6px); }
    100%{ transform: translateY(0); }
}

@keyframes fadeSlideIn{
    from{
        opacity:0;
        transform: translateY(16px);
    }
    to{
        opacity:1;
        transform: translateY(0);
    }
}
            
/* ================================
   MANUAL PAGE HEADER (PREMIUM)
================================ */

.manual-header{
    display:flex;
    align-items:center;
    gap:20px;
    padding:26px 28px;
    border-radius:22px;
    background: linear-gradient(
        135deg,
        rgba(79,70,229,0.10),
        rgba(6,182,212,0.10)
    );
    border:1px solid var(--border);
    box-shadow: 0 14px 40px rgba(79,70,229,0.12);
    margin-bottom:26px;
}

.manual-header-icon{
    width:64px;
    height:64px;
    border-radius:18px;
    background: linear-gradient(
        135deg,
        var(--primary),
        var(--secondary)
    );
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:30px;
    color:white;
    box-shadow: 0 10px 28px rgba(79,70,229,0.35);
}

.manual-header-content h2{
    margin:0;
    font-size:22px;
    font-weight:800;
    color:var(--text);
}

.manual-header-content p{
    margin-top:6px;
    font-size:14px;
    color:var(--muted);
    max-width:600px;
    line-height:1.5;
}
            
/* ================================
   FEATURE SECTION - MODERN CARDS
================================ */

.feature-grid{
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap:22px;
    margin-top:20px;
}

.feature-card{
    background: linear-gradient(135deg, #ffffff, #f8fafc);
    border-radius:20px;
    padding:24px;
    display:flex;
    align-items:center;
    gap:18px;
    border:1px solid var(--border);
    box-shadow: 0 12px 35px rgba(79,70,229,0.08);
    transition: 
        transform 0.3s ease,
        box-shadow 0.3s ease;
    cursor:pointer;
}

.feature-card:hover{
    transform: translateY(-10px);
    box-shadow: 
        0 20px 50px rgba(79,70,229,0.18),
        0 0 0 4px rgba(79,70,229,0.08);
}

.feature-icon{
    width:56px;
    height:56px;
    border-radius:16px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:24px;
    color:white;
    box-shadow: 0 10px 25px rgba(79,70,229,0.35);
}

.feature-content h3{
    margin:0;
    font-size:18px;
    font-weight:800;
    color:var(--text);
}

.feature-content p{
    margin-top:6px;
    font-size:14px;
    color:var(--muted);
    line-height:1.4;
}
            
 /* ================================
   FLOATING BUTTON HOVER EFFECT
================================ */

/* Streamlit buttons */
div.stButton > button {
    transition: 
        transform 0.25s ease,
        box-shadow 0.25s ease,
        filter 0.25s ease;
}

/* Hover effect */
div.stButton > button:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.18);
    filter: brightness(1.05);
}

/* Active (click) effect */
div.stButton > button:active {
    transform: translateY(-2px) scale(0.99);
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.15);
}
          



.hero-btn-primary {
    background: linear-gradient(90deg, #6f2dbd, #b97bff);
    color: white;
    border: none;
    box-shadow: 0 14px 40px rgba(111,45,189,0.25);
}

.hero-btn-primary:hover {
    transform: translateY(-4px);
    box-shadow: 0 22px 50px rgba(111,45,189,0.35);
}

.hero-btn-outline {
    background: transparent;
    color: #2a1733;
    border: 2px solid rgba(111,45,189,0.25);
}

.hero-btn-outline:hover {
    background: rgba(111,45,189,0.08);
    transform: translateY(-4px);
}


:root{
    --primary: #4C1D95;      /* deep violet */
    --accent:  #6D28D9;      /* hover accent */
    --bg1: #F5F3FF;          /* soft background */
    --bg2: #EEF2FF;
    --glass: #FFFFFF;
    --muted: #6B7280;
    --radius: 16px;
    --shadow: 0 14px 40px rgba(76,29,149,0.18);
}

/* app */
.stApp {
    background: radial-gradient(circle at 10% 10%, rgba(179,123,255,0.06), transparent 15%),
                radial-gradient(circle at 90% 90%, rgba(111,45,189,0.03), transparent 12%),
                linear-gradient(180deg, var(--bg1), var(--bg2));
    color: #0f172a;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    padding: 18px 20px;
}
@keyframes fadeMove { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
.navbar { display:flex; align-items:center; justify-content:space-between; gap:12px; padding: 12px 18px; border-radius: 18px;
    background: linear-gradient(135deg, rgba(255,255,255,0.78), rgba(255,255,255,0.65)); box-shadow: var(--shadow);
    backdrop-filter: blur(8px) saturate(120%); animation: fadeMove .6s ease; margin-bottom: 18px; }
.brand { display: flex; gap:12px; align-items:center; font-weight:800; color: var(--primary); }
.brand .logo { width:46px; height:46px; border-radius:12px;
    background: linear-gradient(135deg, var(--primary), var(--accent)); display:flex; align-items:center; justify-content:center; color:white; font-weight:900;
    box-shadow: 0 8px 30px rgba(111,45,189,0.14); font-size:16px; }
.nav-buttons { display:flex; gap:10px; align-items:center; }
.nav-buttons > button { background: transparent; border: 1px solid rgba(111,45,189,0.08); color: #1b1330; padding: 8px 12px; border-radius: 12px; font-weight:700; transition: all .18s ease; }
.nav-buttons > button:hover { transform: translateY(-4px); background: linear-gradient(90deg, rgba(111,45,189,0.06), rgba(185,123,255,0.04)); box-shadow: 0 8px 26px rgba(111,45,189,0.06); }
.nav-primary { background: linear-gradient(135deg, var(--primary), var(--accent)); color: white !important; border: none; box-shadow: 0 10px 32px rgba(111,45,189,0.12); }

/* hero */
.hero { display:flex; gap:24px; align-items:center; justify-content:space-between; padding: 28px; border-radius: 20px; background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(255,255,255,0.82)); box-shadow: 0 18px 48px rgba(111,45,189,0.06); backdrop-filter: blur(6px) saturate(120%); margin-bottom: 20px; animation: fadeMove .6s ease; }
.hero h1 { margin:0; font-size:32px; color:#2a1733; line-height:1.02; }
.hero p { margin:6px 0 0 0; color:var(--muted); }
.hero-ctas { display:flex; gap:12px; align-items:center; }
.hero-cta-primary { background: linear-gradient(90deg, var(--primary), var(--accent)); color:white; padding: 12px 18px; border-radius: 12px; font-weight:800; border:none; box-shadow: 0 12px 36px rgba(111,45,189,0.12); cursor:pointer; }
.hero-cta-ghost { background: transparent; border: 1px solid rgba(111,45,189,0.08); color: #2a1733; padding: 10px 16px; border-radius: 12px; font-weight:700; cursor:pointer; }

/* cards */
.card { background: var(--glass); border-radius: 16px; padding: 20px; box-shadow: var(--shadow); border: 1px solid rgba(111,45,189,0.06); backdrop-filter: blur(8px) saturate(120%); animation: fadeMove .5s ease; transition: transform .18s ease, box-shadow .18s ease; }
.card:hover { transform: translateY(-8px); box-shadow: 0 28px 60px rgba(32,14,71,0.08); }

/* misc */
.section-title { color:#2a1733; font-size:18px; font-weight:800; margin-bottom:8px; }
.muted { color: var(--muted); font-size:13px; }
.home-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:18px; }
div.stButton > button { border-radius: 12px !important; padding: 10px 16px !important; background: linear-gradient(90deg,var(--primary),var(--accent)) !important; color: white !important; font-weight:800; box-shadow: 0 10px 36px rgba(111,45,189,0.12) !important; }
.stTextInput, .stNumberInput, .stSelectbox { margin-bottom:12px; }
.result-chip { padding: 10px 14px; border-radius:12px; font-weight:800; color:white; }
.result-high { background: linear-gradient(135deg,#ff6b6b,#ff3b7a); }
.result-low  { background: linear-gradient(135deg,#34d399,#10b981); }
.dataframe-container { border-radius:12px; overflow:hidden; box-shadow: 0 14px 36px rgba(32,14,71,0.03); }

/* History HTML Table */
.history-table { width:100%; border-collapse: collapse; font-family: inherit; font-size:14px; }
.history-table thead th { background: linear-gradient(90deg, rgba(111,45,189,0.95), rgba(185,123,255,0.95)); color: #fff; font-weight:700; padding:10px 12px; text-align:left; border-bottom: 2px solid rgba(111,45,189,0.18); position: sticky; top:0; z-index:2; }
.history-table tbody td { padding:10px 12px; border-bottom: 1px solid rgba(111,45,189,0.04); color:#2a1733; vertical-align: middle; }
.history-table tbody tr:hover td { background: rgba(111,45,189,0.04); }
.history-badge { padding:6px 10px; border-radius:999px; color:white; font-weight:700; font-size:13px; display:inline-block; }
.badge-high { background: linear-gradient(135deg,#ff6b6b,#ff3b7a); box-shadow: 0 6px 18px rgba(255,99,132,0.08); }
.badge-low { background: linear-gradient(135deg,#34d399,#10b981); box-shadow: 0 6px 18px rgba(16,185,129,0.08); }

/* quote bar */
.quote-bar { padding: 12px 16px; border-radius:12px; margin-bottom:16px; background: linear-gradient(90deg, rgba(255,255,255,0.98), rgba(255,255,255,0.95)); color: var(--primary); font-weight:700; text-align:center; box-shadow: 0 12px 30px rgba(111,45,189,0.06); }

@media (max-width:720px) { .hero { flex-direction: column; align-items:flex-start; gap:12px; padding:16px; } .brand .logo { width:36px; height:36px; } }
</style>
            
""", unsafe_allow_html=True)
st.markdown("""
<style>
.profile-btn {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6D28D9, #4F46E5);
    color: white;
    font-weight: 700;
    font-size: 18px;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}
.profile-btn:hover {
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
            /* ===============================
   PROFILE BUTTON SAME AS NAVBAR
================================ */

.nav-btn-wrapper div.stButton > button {
    background: linear-gradient(135deg, #6D28D9, #4C1D95) !important;
    color: #ffffff !important;
    border-radius: 14px !important;
    padding: 10px 18px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    min-width: 56px;
    height: 42px;
    border: none !important;
    box-shadow: 0 12px 30px rgba(109,40,217,0.35) !important;
    transition: all 0.25s ease-in-out;
}

.nav-btn-wrapper div.stButton > button:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 42px rgba(109,40,217,0.55) !important;
}

/* --- Force profile popover/button into a circle --- */
div[data-testid="stPopover"] > button,
div[data-testid="stButton"] > button.profile-avatar {
    width: 42px !important;
    height: 42px !important;
    min-width: 42px !important;
    padding: 0 !important;
    border-radius: 50% !important;
    background: #5B21B6 !important;
    color: white !important;
    font-weight: 800 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* remove rectangular shadow padding */
div[data-testid="stPopover"] {
    box-shadow: none !important;
}
            /* Make profile button same as navbar buttons */
.nav-profile-btn div.stButton > button {
    background: linear-gradient(135deg, #6D28D9, #4C1D95) !important;
    color: white !important;
    border-radius: 14px !important;
    padding: 10px 18px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    min-width: 48px;
    height: 42px;
    box-shadow: 0 12px 30px rgba(109,40,217,0.35) !important;
}

/* Hover effect (same as others) */
.nav-profile-btn div.stButton > button:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 42px rgba(109,40,217,0.5) !important;
}

</style>
""", unsafe_allow_html=True)

DB_USERS = "users.db"
DB_HISTORY = "history.db"

def make_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_user_db():
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("PRAGMA table_info(users)")
    cols = [col[1] for col in c.fetchall()]
    required = {"username", "password", "role", "email", "reset_token", "reset_expiry"}
    if not required.issubset(set(cols)):
        # recreate users table cleanly
        c.execute("DROP TABLE IF EXISTS users")
        c.execute("""
            CREATE TABLE users(
                username TEXT PRIMARY KEY,
                password TEXT,
                role TEXT,
                email TEXT,
                reset_token TEXT,
                reset_expiry TEXT
            )
        """)
        conn.commit()
    conn.close()

def add_user(username, password_hash, role, email=None):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(username, password, role, email) VALUES (?, ?, ?, ?)", (username, password_hash, role, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False
    finally:
        conn.close()

def login_user(username, password_hash):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password_hash))
    data = c.fetchone()
    conn.close()
    return data[0] if data else None

def set_reset_token(username, token, expiry_iso):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("UPDATE users SET reset_token=?, reset_expiry=? WHERE username=?", (token, expiry_iso, username))
    conn.commit()
    conn.close()

def verify_reset_token(username, token):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("SELECT reset_token, reset_expiry FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row or not row[0]:
        return False
    token_db, expiry = row
    try:
        expiry_dt = datetime.fromisoformat(expiry)
    except:
        return False
    return token_db == token and datetime.now() <= expiry_dt

def change_password(username, new_password_hash):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("UPDATE users SET password=?, reset_token=NULL, reset_expiry=NULL WHERE username=?", (new_password_hash, username))
    conn.commit()
    conn.close()
def verify_old_password(username, old_password_hash):
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute(
        "SELECT 1 FROM users WHERE username=? AND password=?",
        (username, old_password_hash)
    )
    result = c.fetchone()
    conn.close()
    return result is not None
def page_auth():

    st.markdown("""
    <div class="auth-header">
        <div class="auth-icon">🔐</div>
        <div>
            <h2>Welcome to HeartCare AI</h2>
            <p>Secure access for patients and doctors</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="auth-quote-card">
        <span class="auth-quote-icon">🫀</span>
        <span class="auth-quote-text">
            Early detection saves lives — AI assists doctors, it doesn’t replace them.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Login / Register</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    # =========================
    # LOGIN TAB
    # =========================
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            login_role_selected = st.selectbox(
                "Login as",
                ["patient", "doctor"],
                help="Choose role to login as",
                key="login_role"
            )

            submitted = st.form_submit_button("Login")

            if submitted:
                if not username or not password:
                    st.error("Enter username & password.")
                else:
                    hashed = make_hash(password)
                    actual_role = login_user(username, hashed)

                    if actual_role:
                        st.success("Logged in successfully.")

                        # ✅ SET SESSION STATE (CRITICAL)
                        st.session_state["logged_in"] = True
                        st.session_state["username"] = username
                        st.session_state["role"] = actual_role
                        st.session_state["page"] = "Home"

                        if actual_role != login_role_selected:
                            st.info(
                                f"Role auto-detected as '{actual_role}' "
                                f"(you selected '{login_role_selected}')."
                            )

                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

    # =========================
    # REGISTER TAB
    # =========================
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("New username", key="reg_user")
            new_pass = st.text_input("New password", type="password", key="reg_pass")

            reg_role = st.selectbox(
                "Register as",
                ["patient", "doctor"],
                key="reg_role"
            )

            new_email = st.text_input(
                "Email (optional)",
                help="Provide email for future password recovery via email.",
                key="reg_email"
            )

            registered = st.form_submit_button("Register")

            if registered:
                if not new_user or not new_pass:
                    st.error("Enter username & password.")
                else:
                    hashed = make_hash(new_pass)
                    ok = add_user(
                        new_user,
                        hashed,
                        reg_role,
                        new_email if new_email else None
                    )

                    if ok:
                        st.success("Account created! Please login.")
                    else:
                        st.error("Username already exists.")



def page_manual():
    st.markdown("""
<div class="manual-header">
    <div class="manual-header-icon">🫀</div>
    <div class="manual-header-content">
        <h2>Manual Heart Risk Prediction</h2>
        <p>
            Enter patient health parameters below to instantly calculate
            AI-based heart disease risk.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        Age = st.number_input("Age", 1, 120, 40, key="Age")
        Sex = st.selectbox("Sex", ["M", "F"], key="Sex")
        CP = st.selectbox("Chest Pain Type", ["ATA", "NAP", "ASY", "TA"], key="CP")
        RBP = st.number_input("Resting BP", 0, 300, 120, key="RBP")
        CHOL = st.number_input("Cholesterol", 0, 700, 200, key="CHOL")
    with c2:
        FBS = st.selectbox("Fasting BS > 120", [0, 1], key="FBS")
        ECG = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"], key="ECG")
        MaxHR = st.number_input("Max HR", 60, 220, 150, key="MaxHR")
        Angina = st.selectbox("Exercise Angina", ["Y", "N"], key="Angina")
        Oldpeak = st.number_input("Oldpeak", 0.0, 10.0, 1.0, key="Oldpeak")
        Slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"], key="Slope")

    df = pd.DataFrame([{
        "Age": Age, "Sex": Sex, "ChestPainType": CP,
        "RestingBP": RBP, "Cholesterol": CHOL,
        "FastingBS": FBS, "RestingECG": ECG,
        "MaxHR": MaxHR, "ExerciseAngina": Angina,
        "Oldpeak": Oldpeak, "ST_Slope": Slope
    }])

    if st.button("🔮 Predict Heart Risk"):
        # validation
        if Age < 1 or Age > 120:
            st.error("Age must be between 1 and 120.")
        elif RBP <= 0:
            st.error("Resting BP must be > 0.")
        elif CHOL <= 0:
            st.error("Cholesterol must be > 0.")
        else:
            if model is None:
                st.error("Model not available. Place 'heart_disease_best_model.pkl' in the app folder.")
            else:
                with st.spinner("Running prediction..."):
                    pred = model.predict(df)[0]
                    prob = model.predict_proba(df)[0][1] * 100
                    label = "High Risk" if pred == 1 else "Low Risk"

                chip_class = "result-high" if pred == 1 else "result-low"
                st.markdown(
                    f"""<div style="display:flex;gap:16px;align-items:center">
                            <div class="result-chip {chip_class}">{label}</div>
                            <div style="font-weight:800;">Probability: {prob:.2f}%</div>
                        </div>""",
                    unsafe_allow_html=True
                )

                
                fig = go.Figure(go.Pie(
                    values=[prob, 100-prob],
                    labels=[f"Risk {prob:.1f}%", "Remaining"],
                    hole=0.62,
                    sort=False,
                    direction='clockwise',
                    marker=dict(colors=["#6f2dbd", "#d9c4ff"], line=dict(color="white", width=2)),
                    textinfo='none'
                ))
                fig.update_layout(margin=dict(t=6,b=6,l=6,r=6), height=300, showlegend=False,
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  annotations=[dict(text=f"{prob:.1f}%", showarrow=False, font=dict(size=24, color="#6f2dbd"))])
                st.plotly_chart(fig, use_container_width=True)

                if st.session_state["logged_in"]:
                    save_history(st.session_state["username"], "manual", df.to_json(orient="records"), prob, label)
    st.markdown('</div>', unsafe_allow_html=True)



def page_upload():
    st.markdown("""
<div class="upload-header">
    <div class="upload-header-icon">📄</div>
    <div class="upload-header-content">
        <h2>Upload Medical Report</h2>
        <p>
            Upload a scanned report (PNG, JPG, PDF). Our AI will extract
            values using OCR and predict heart disease risk automatically.
        </p>
        <div class="upload-badges">
            <span>OCR Enabled</span>
            <span>Hybrid Mode</span>
            <span>Secure Upload</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    file = st.file_uploader("Upload report", type=["png", "jpg", "jpeg", "pdf"])
    if not file:
        st.info("Upload a scanned report image or PDF to extract values via OCR.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    ext = file.name.split(".")[-1].lower()
    try:
        if ext == "pdf":
            pages = convert_from_bytes(file.read(), poppler_path=POPPLER_PATH)
            img = pages[0]
        else:
            img = Image.open(file)
    except Exception as e:
        st.error("Failed to process the file. Check POPPLER_PATH and file format.")
        st.exception(e)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.image(img, caption="Uploaded page (first page shown)", use_column_width=700)

    mode = st.radio("Prediction mode", ["Automatic (single-click)", "Hybrid (review & edit)"])

    if st.button("🔎 Extract & Predict"):
        prog = st.progress(0)
        try:
            prog.progress(10)
            text = pytesseract.image_to_string(img.convert("L"))
            prog.progress(40)
        except Exception as e:
            st.error("OCR failed.")
            st.exception(e)
            prog.empty()
            st.markdown('</div>', unsafe_allow_html=True)
            return

        st.subheader("Extracted Text")
        st.text_area("OCR Output", value=text, height=220)

        features = parse_text_to_features(text)
        prog.progress(60)
        st.subheader("Parsed Features (editable in Hybrid mode)")
        if mode == "Hybrid (review & edit)":
            c1, c2 = st.columns(2)
            with c1:
                Age = st.number_input("Age", 1, 120, int(features.get("Age",50)))
                Sex = st.selectbox("Sex", ["M","F"], index=0 if features.get("Sex","M")=="M" else 1)
                CP = st.selectbox("Chest Pain Type", ["ATA","NAP","ASY","TA"], index=["ATA","NAP","ASY","TA"].index(features.get("ChestPainType","TA")))
                RBP = st.number_input("Resting BP", 0, 300, int(features.get("RestingBP",120)))
                CHOL = st.number_input("Cholesterol", 0, 700, int(features.get("Cholesterol",200)))
            with c2:
                FBS = st.selectbox("Fasting BS > 120", [0,1], index=int(features.get("FastingBS",0)))
                ECG = st.selectbox("Resting ECG", ["Normal","ST","LVH"], index=["Normal","ST","LVH"].index(features.get("RestingECG","Normal")))
                MaxHR = st.number_input("Max HR", 60, 220, int(features.get("MaxHR",150)))
                Angina = st.selectbox("Exercise Angina", ["Y","N"], index=0 if features.get("ExerciseAngina","N")=="Y" else 1)
                Oldpeak = st.number_input("Oldpeak", 0.0, 10.0, float(features.get("Oldpeak",1.0)))
                Slope = st.selectbox("ST Slope", ["Up","Flat","Down"], index=["Up","Flat","Down"].index(features.get("ST_Slope","Flat")))
            df = pd.DataFrame([{
                "Age": Age, "Sex": Sex, "ChestPainType": CP,
                "RestingBP": RBP, "Cholesterol": CHOL,
                "FastingBS": FBS, "RestingECG": ECG,
                "MaxHR": MaxHR, "ExerciseAngina": Angina,
                "Oldpeak": Oldpeak, "ST_Slope": Slope
            }])
        else:
            df = pd.DataFrame([features])

        prog.progress(80)
        st.subheader("Final Input Data")
        st.json(json.loads(df.to_json(orient="records")))

        if model is None:
            st.error("Model not available. Cannot predict.")
            prog.empty()
        else:
            with st.spinner("Predicting..."):
                pred = model.predict(df)[0]
                prob = model.predict_proba(df)[0][1] * 100
                label = "High Risk" if pred == 1 else "Low Risk"
            prog.progress(100)
            chip_class = "result-high" if pred == 1 else "result-low"
            st.markdown(f"""<div style="display:flex;gap:16px;align-items:center">
                            <div class="result-chip {chip_class}">{label}</div>
                            <div style="font-weight:800;">Probability: {prob:.2f}%</div>
                        </div>""", unsafe_allow_html=True)

            
            fig = go.Figure(go.Pie(
                values=[prob, 100-prob],
                labels=[f"Risk {prob:.1f}%", "Remaining"],
                hole=0.62,
                sort=False,
                direction='clockwise',
                marker=dict(colors=["#6f2dbd", "#d9c4ff"], line=dict(color="white", width=2)),
                textinfo='none'
            ))
            fig.update_layout(margin=dict(t=6,b=6,l=6,r=6), height=300, showlegend=False,
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              annotations=[dict(text=f"{prob:.1f}%", showarrow=False, font=dict(size=24, color="#6f2dbd"))])
            st.plotly_chart(fig, use_container_width=800)
            st.markdown('</div>', unsafe_allow_html=True)

            if st.session_state["logged_in"]:
                save_history(st.session_state["username"], "ocr", df.to_json(orient="records"), prob, label)
        prog.empty()
    st.markdown('</div>', unsafe_allow_html=True)


def page_history():
    
    st.markdown('<div class="card">My Prediction History</div>', unsafe_allow_html=True)

    if not st.session_state["logged_in"]:
        st.error("You must be logged in to view history.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    df = get_history(st.session_state["username"])
    if df.empty:
        st.info("No history yet. Make a prediction to start storing records.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

  
    total = len(df)
    high = len(df[df["prediction"] == "High Risk"])
    low = total - high
    avg_prob = df["probability"].mean()

    c1, c2, c3 = st.columns([1,1,1])
    c1.metric("Total Predictions", total)
    c2.metric("High Risk", high)
    c3.metric("Avg Probability", f"{avg_prob:.2f}%")

    st.write("")
    
    
    st.download_button("Export CSV", data=df.to_csv(index=False), file_name="history.csv")

    st.write("")
    
    html_table = render_history_table_html(df)
    st.markdown('<div class="dataframe-container" style="padding:12px;">', unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Risk Probability Trend")
    fig = go.Figure()
   
    try:
        x = pd.to_datetime(df["timestamp"])
    except:
        x = df["timestamp"]
    fig.add_trace(go.Scatter(
        x=x,
        y=df["probability"],
        mode="lines+markers",
        line=dict(color="#6f2dbd", width=3),
        marker=dict(size=8, color="#b97bff", line=dict(width=1.5, color="white"))
    ))
    fig.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.35)",
                      font=dict(color="#2a1733", size=13), xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=True, gridcolor="rgba(111,45,189,0.08)"))
    st.plotly_chart(fig, use_container_width=800)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def page_profile():
    if not st.session_state.get("logged_in"):
        st.error("Please login to view your profile.")
        return

    # ---------------- Session data ----------------
    username = st.session_state.get("username")
    role = st.session_state.get("role")

    # ---------------- Fetch email (DEFINE FIRST) ----------------
    conn = sqlite3.connect(DB_USERS)
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()

    email = row[0] if row and row[0] else "Not provided"

    # ---------------- Page title ----------------
    st.markdown('<div class="card">👤 My Profile</div>', unsafe_allow_html=True)

    # ---------------- Profile card (HTML component) ----------------
    import streamlit.components.v1 as components

    components.html(
        f"""
<div style="
    background:white;
    border-radius:14px;
    padding:20px;
    display:flex;
    align-items:center;
    gap:20px;
    box-shadow:0 10px 30px rgba(0,0,0,0.08);
    border:1px solid rgba(0,0,0,0.05);
">
    <div style="
        width:64px;
        height:64px;
        border-radius:50%;
        background:#2563EB;
        color:white;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:28px;
        font-weight:800;
    ">
        {username[0].upper()}
    </div>

    <div>
        <h3 style="margin:0;">{username}</h3>
        <p style="margin:4px 0;color:#64748B;">
            Role: {role.capitalize()}
        </p>
        <p style="margin:0;color:#64748B;">
            Email: {email}
        </p>
    </div>
</div>
""",
        height=130
    )

    # ---------------- Role-based stats ----------------
    if role == "patient":
        df = get_history(username)
        total = len(df)
        high = len(df[df["prediction"] == "High Risk"])
        avg = df["probability"].mean() if not df.empty else 0

        a, b, c = st.columns(3)
        a.metric("Total Predictions", total)
        b.metric("High Risk Cases", high)
        c.metric("Avg Risk %", f"{avg:.2f}%")

    elif role == "doctor":
        df = get_all_history()
        total = len(df)
        high = len(df[df["prediction"] == "High Risk"])
        patients = df["username"].nunique()

        a, b, c = st.columns(3)
        a.metric("Total Patients", patients)
        b.metric("Total Predictions", total)
        c.metric("High Risk Cases", high)

    # ---------------- Change password ----------------
    st.subheader("🔐 Change Password")
    with st.form("profile_change_password"):
        old = st.text_input("Current Password", type="password")
        new = st.text_input("New Password", type="password")
        confirm = st.text_input("Confirm New Password", type="password")
        submit = st.form_submit_button("Update Password")

        if submit:
            if not old or not new or not confirm:
                st.error("All fields required.")
            elif new != confirm:
                st.error("Passwords do not match.")
            elif not verify_old_password(username, make_hash(old)):
                st.error("Current password incorrect.")
            else:
                change_password(username, make_hash(new))
                st.success("Password updated. Please login again.")
                st.session_state["logged_in"] = False
                st.session_state["username"] = None
                st.session_state["role"] = None
                st.session_state["page"] = "Auth"
                st.rerun()

    st.write("---")

    # ---------------- Logout ----------------
    if st.button("🚪 Logout", key="profile_logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["role"] = None
        st.session_state["page"] = "Home"
        st.rerun()

    
def init_history_db():
    conn = sqlite3.connect(DB_HISTORY)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            input_type TEXT,
            input_data TEXT,
            probability REAL,
            prediction TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_history(username, input_type, input_data, prob, pred):
    conn = sqlite3.connect(DB_HISTORY)
    c = conn.cursor()
    c.execute("""
        INSERT INTO history(username, input_type, input_data, probability, prediction, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, input_type, input_data, prob, pred, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_history(username):
    conn = sqlite3.connect(DB_HISTORY)
    df = pd.read_sql_query("SELECT * FROM history WHERE username=? ORDER BY id DESC", conn, params=(username,))
    conn.close()
    return df

def get_all_history():
    conn = sqlite3.connect(DB_HISTORY)
    df = pd.read_sql_query("SELECT * FROM history ORDER BY id DESC", conn)
    conn.close()
    return df

init_user_db()
init_history_db()


def parse_text_to_features(text):
    txt = (text or "").lower()
    def find_int(patterns, default):
        for p in patterns:
            m = re.search(p, txt)
            if m:
                try:
                    return int(m.group(1))
                except:
                    pass
        return default

    age = find_int([r"age[:\s]*([0-9]{1,3})", r"age\s*-\s*([0-9]{1,3})"], 50)
    rbp = find_int([r"bp[:\s]*([0-9]{2,3})", r"resting blood pressure[:\s]*([0-9]{2,3})"], 120)
    chol = find_int([r"chol[:\s]*([0-9]{2,4})", r"cholesterol[:\s]*([0-9]{2,4})"], 200)
    maxhr = find_int([r"max\s*hr[:\s]*([0-9]{2,3})", r"max heart rate[:\s]*([0-9]{2,3})"], 150)

    sex = "F" if "female" in txt or "fem" in txt else "M"

    if "typical" in txt:
        cp = "TA"
    elif "atypical" in txt:
        cp = "ATA"
    elif "non-angina" in txt or "non angina" in txt:
        cp = "NAP"
    elif "asym" in txt:
        cp = "ASY"
    else:
        cp = "TA"

    if "lvh" in txt:
        ecg = "LVH"
    elif "st segment" in txt or "st-segment" in txt or "st " in txt:
        ecg = "ST"
    else:
        ecg = "Normal"

    fbs = 1 if ">120" in txt or "fbs>120" in txt or "fasting blood sugar>120" in txt else 0
    angina = "Y" if "angina" in txt else "N"

    try:
        m = re.search(r"oldpeak[:\s]*([0-9]*\.?[0-9]+)", txt)
        oldpeak = float(m.group(1)) if m else 1.0
    except:
        oldpeak = 1.0

    if "up" in txt and "slope" in txt:
        slope = "Up"
    elif "down" in txt and "slope" in txt:
        slope = "Down"
    else:
        slope = "Flat"

    return {
        "Age": age, "Sex": sex, "ChestPainType": cp,
        "RestingBP": rbp, "Cholesterol": chol,
        "FastingBS": fbs, "RestingECG": ecg,
        "MaxHR": maxhr, "ExerciseAngina": angina,
        "Oldpeak": oldpeak, "ST_Slope": slope
    }


@st.cache_resource
def load_model():
    try:
        m = joblib.load("heart_disease_best_model.pkl")
        return m
    except Exception:
        return None

model = load_model()
if model is None:
    st.warning("Model not found. Place 'heart_disease_best_model.pkl' in the app folder to enable predictions.")

def render_history_table_html(df: pd.DataFrame) -> str:
    if df.empty:
        return "<div style='color:var(--muted)'>No records found.</div>"
    df2 = df.copy()
    
    if 'input_data' in df2.columns:
        def short(x):
            if pd.isna(x):
                return ""
            s = str(x)
            s = html.escape(s)
            return s if len(s) <= 90 else s[:90] + "..."
        df2['input_data'] = df2['input_data'].apply(short)

    
    if 'probability' in df2.columns:
        df2['probability'] = df2['probability'].apply(lambda x: f"{float(x):.2f}%")

    
    def pred_badge(p):
        if p and "High" in p:
            return f"<span class='history-badge badge-high'>{html.escape(p)}</span>"
        else:
            return f"<span class='history-badge badge-low'>{html.escape(p)}</span>"

    if 'prediction' in df2.columns:
        df2['prediction'] = df2['prediction'].apply(pred_badge)

    cols = [c for c in ['timestamp', 'username', 'input_type', 'input_data', 'probability', 'prediction'] if c in df2.columns]
    df2 = df2[cols]

   
    thead = "<thead><tr>" + "".join(f"<th>{c.capitalize()}</th>" for c in df2.columns) + "</tr></thead>"
    tbody_rows = []
    for _, row in df2.iterrows():
        cells = "".join(f"<td>{row[c]}</td>" for c in df2.columns)
        tbody_rows.append(f"<tr>{cells}</tr>")
    tbody = "<tbody>" + "".join(tbody_rows) + "</tbody>"
    html_table = f"<table class='history-table'>{thead}{tbody}</table>"
    return html_table

if "page" not in st.session_state:
    st.session_state["page"] = "Home"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

def set_page(p):
    st.session_state["page"] = p

st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("role", None)
st.session_state.setdefault("page", "Home")

# ================= NAVBAR =================
def render_navbar():
    col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,0.6])

    with col1:
        if st.button("Home"):
            st.session_state.page = "Home"
            st.rerun()

    with col2:
        if st.button("Manual"):
            st.session_state.page = "Manual"
            st.rerun()

    with col3:
        if st.button("Upload"):
            st.session_state.page = "Upload"
            st.rerun()

    with col4:
        if st.button("History"):
            st.session_state.page = "History"
            st.rerun()

    with col5:
        if st.button("UserDash"):
            st.session_state.page = "UserDash"
            st.rerun()

    with col6:
        if st.session_state.get("logged_in"):
            if st.button(st.session_state["username"][0].upper()):
                st.session_state.page = "Profile"
                st.rerun()
        else:
            if st.button(" Login"):
                st.session_state.page = "Auth"
                st.rerun()

 
# st.divider()

# ---------- PRIMARY NAV ----------
primary = [
    ("Home", "🏠"),
    ("Manual", "✍️"),
    ("Upload", "📤"),
    ("History", "📜"),
]

components.html("""
<div style="
    margin: 6px auto 20px auto;

    padding: 28px 32px;
    max-width: 1100px;
    background: linear-gradient(180deg, #F5F7FF, #EEF2FF);
    border-radius: 20px;
    font-family: sans-serif;
">
    <div style="
        font-size: 30px;
        font-weight: 900;
        color: #0F172A;
        text-align: center;
        margin-bottom: 12px;
    ">
        AI-Driven Early Heart Disease Prediction
    </div>

    <div style="
        font-size: 16px;
        font-weight: 500;
        color: #475569;
        line-height: 1.6;
        text-align: center;
        max-width: 900px;
        margin: auto;
    ">
        HeartCare AI helps in the early detection of heart disease by analyzing
        patient health parameters and medical reports using machine learning.
        The system supports both <b>patients</b> and <b>doctors</b> with
        accurate predictions, history tracking, and risk-level insights.
    </div>

    <div style="
        margin-top: 16px;
        font-size: 15px;
        font-weight: 600;
        color: #1E40AF;
        text-align: center;
    ">
        ⚡ Fast Predictions &nbsp; • &nbsp; 📊 Smart Analytics &nbsp; • &nbsp; 🩺 Doctor-Friendly Dashboard
    </div>
</div>
""", height=260)


# 🔹 CALL NAVBAR FUNCTION (IMPORTANT)
render_navbar()

def page_all_patients():
    
    st.markdown('<div class="card">All Patients - History</div>', unsafe_allow_html=True)

    if st.session_state.get("role") != "doctor":
        st.error("Access denied. Doctor role required.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    df = get_all_history()
    if df.empty:
        st.info("No history recorded.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.download_button("Export all CSV", data=df.to_csv(index=False), file_name="all_history.csv")
    st.write("")
    html_table = render_history_table_html(df)
    st.markdown('<div class="dataframe-container" style="padding:12px;">', unsafe_allow_html=True)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def page_doctor_dashboard():
    
    

    if st.session_state.get("role") != "doctor":
        st.error("Access denied. Doctor role required.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    df = get_all_history()
    total = len(df)
    high = len(df[df["prediction"] == "High Risk"])
    low = total - high

    st.metric("Total Predictions", total)
    st.metric("High Risk Cases", high)
    st.metric("Low Risk Cases", low)
    st.write("")

    st.markdown('<div class="Risk" style="padding:12px;">', unsafe_allow_html=True)
    colors = ["#ff6b6b", "#34d399"]
    fig = go.Figure(go.Bar(
        x=["High Risk", "Low Risk"],
        y=[high, low],
        marker=dict(color=colors, line=dict(color="white", width=1.8)),
        text=[high, low],
        textposition="outside"
    ))
    fig.update_layout(
        height=330,
        plot_bgcolor="rgba(255,255,255,0.35)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=30, b=30),
        font=dict(color="#2a1733", size=14),
        
    )
    st.plotly_chart(fig, use_container_width=800)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def page_user_dashboard():
    
    st.markdown('<div class="section-title">My Health Dashboard</div>', unsafe_allow_html=True)

    if not st.session_state["logged_in"]:
        st.error("Please log in to access your dashboard.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    df = get_history(st.session_state["username"])
    if df.empty:
        st.info("No predictions yet. Try Manual or Upload to generate your first result.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    total = len(df)
    high = len(df[df["prediction"] == "High Risk"])
    low = total - high
    avg_prob = df["probability"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Predictions", total)
    c2.metric("High Risk", high)
    c3.metric("Low Risk", low)
    c4.metric("Avg Risk", f"{avg_prob:.2f}%")

    st.write("")
    st.subheader("Most Recent Prediction")
    latest = df.iloc[0]
    st.write(f"**Prediction:** {latest['prediction']}")
    st.write(f"**Probability:** {latest['probability']:.2f}%")
    st.write(f"**Date:** {latest['timestamp']}")

    st.write("")
    st.subheader("Risk Probability Trend")
    fig = go.Figure()
    try:
        x = pd.to_datetime(df["timestamp"])
    except:
        x = df["timestamp"]
    fig.add_trace(go.Scatter(
        x=x,
        y=df["probability"],
        mode="lines+markers",
        line=dict(color="#6f2dbd", width=3),
        marker=dict(size=8, color="#b97bff", line=dict(width=1.5, color="white"))
    ))
    fig.update_layout(height=300, margin=dict(t=10,b=10,l=10,r=10),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.35)",
                      font=dict(color="#2a1733", size=13), xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=True, gridcolor="rgba(111,45,189,0.08)"))
    st.plotly_chart(fig, use_container_width=800)

    st.write("")
    st.subheader("Last 5 Predictions")
    st.dataframe(df.head(5), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


page = st.session_state["page"]

if page == "Home":
    st.markdown("""
<div class="hero">
    <div>
        <h1>HeartCare AI — Early Heart Disease Detection</h1>
        <p class="muted">
            Fast, reliable risk predictions with OCR-enabled report parsing
            and visual dashboards for patients & doctors.
        </p>
    </div>

</div>
""", unsafe_allow_html=True)

    
    c1, c2, _ = st.columns([1.3, 1.3, 3])

    with c1:
        if st.button("🚀 Try Manual Prediction", key="hero_manual"):
            st.session_state["page"] = "Manual"
            st.rerun()

    with c2:
        if st.button("📤 Upload Report", key="hero_upload"):
            st.session_state["page"] = "Upload"
            st.rerun()

    st.markdown(
        '<div class="quote-bar">❤️ Early detection saves lives — Track your heart health instantly.</div>',
        unsafe_allow_html=True
    )

   
    st.markdown('<div class="home-grid">', unsafe_allow_html=True)

    st.markdown("""
<div class="feature-grid">

  <div class="feature-card">
    <div class="feature-icon">✍️</div>
    <div class="feature-content">
      <h3>Manual Prediction</h3>
      <p>Enter patient vitals and instantly get an AI-powered heart risk score.</p>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-icon">📤</div>
    <div class="feature-content">
      <h3>Upload Report</h3>
      <p>Upload a scanned medical report — OCR automatically extracts values.</p>
    </div>
  </div>

  <div class="feature-card">
    <div class="feature-icon">📜</div>
    <div class="feature-content">
      <h3>History</h3>
      <p>View and track your past predictions securely (login required).</p>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Auth":
    page_auth()

elif page == "Manual":
    page_manual()

elif page == "Upload":
    page_upload()

elif page == "History":
    page_history()

elif page == "AllPatients":
    page_all_patients()

elif page == "DoctorDash":
    page_doctor_dashboard()

elif page == "UserDash":
    page_user_dashboard()

elif page == "Profile":
    page_profile()

st.markdown("""
    <div style="padding:14px; margin-top:22px; text-align:center; color: #6b6b7a; font-size:13px;">
        Built with ❤️ — Keep your model file 'heart_disease_best_model.pkl' in the app folder.
    </div>
""", unsafe_allow_html=True)
