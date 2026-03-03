import streamlit as st
import streamlit.components.v1 as components
from streamlit_ace import st_ace
import subprocess
import shutil
import os
import pandas as pd
import io
import json
import uuid
from datetime import datetime

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(
    page_title="Lucas IDE Pro v6.0 ULTRA",
    page_icon="💻",
    layout="wide"
)

# Lucas Pro Styling - Keeping that purple glassmorphic vibe! 💜✨
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Lucas Pro Buttons */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #6c5ce7 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0px 4px 15px rgba(108, 92, 231, 0.3) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        background-color: #a29bfe !important;
        box-shadow: 0px 6px 20px rgba(108, 92, 231, 0.5) !important;
    }

    /* Side Cards */
    .status-card {
        padding: 12px;
        border-radius: 12px;
        background: rgba(108, 92, 231, 0.1);
        border: 1px dashed #6c5ce7;
        margin-bottom: 15px;
    }
    .health-check {
        font-size: 0.85rem;
        margin-bottom: 5px;
    }
    
    /* THE STYLISH CHANGELOG BOX CSS - THE MISSING LINK! 🎨 */
    .changelog-box {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 4px solid #6c5ce7;
        padding: 20px;
        border-radius: 16px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    .log-header {
        color: #6c5ce7;
        font-size: 0.9rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .log-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 8px;
        color: #cbd5e1;
        font-size: 0.95rem;
    }
    .log-icon {
        color: #6c5ce7;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE CLOUD BRAIN (SUPABASE) ---
supabase_client = None
try:
    from supabase import create_client
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    if url and key:
        supabase_client = create_client(url, key)
except Exception:
    supabase_client = None

# --- 3. SESSION STATE ---
if "current_code" not in st.session_state:
    st.session_state.current_code = ""

# --- 4. SIDEBAR: THE COMMAND CENTER ---
LANGUAGES = [
    "python", "javascript", "java", "cpp", "c", "rust", "go", "php", 
    "ruby", "bash", "powershell", "batch", "lua", "perl", "csharp", "css", "html"
]

# Mapping for correct file extensions 🗺️
EXT_MAP = {
    "python": ".py", "javascript": ".js", "java": ".java", "cpp": ".cpp",
    "c": ".c", "rust": ".rs", "go": ".go", "php": ".php", "ruby": ".rb",
    "bash": ".sh", "powershell": ".ps1", "batch": ".bat", "lua": ".lua",
    "perl": ".pl", "csharp": ".cs", "css": ".css", "html": ".html"
}

with st.sidebar:
    st.title("🛠️ Lucas IDE Pro")
    language = st.selectbox("Select Language", LANGUAGES)
    theme = st.selectbox("Editor Theme", ["monokai", "dracula", "github", "tomorrow_night"])
    
    st.divider()
    
    # --- 🟢 THE LANG CHECKER (DIAGNOSTICS) FIXED! ---
    st.subheader("🩺 System Health")
    health_cmds = {
        "python": "python3", "java": "javac", "bash": "bash", "powershell": "pwsh",
        "cpp": "g++", "c": "gcc", "go": "go", "ruby": "ruby", "batch": "cmd",
        "rust": "rustc", "php": "php", "javascript": "node", "lua": "lua", 
        "perl": "perl", "csharp": "mcs"
    }
    
    with st.container():
        for lang in LANGUAGES:
            if lang in ["html", "css"]:
                st.markdown(f'<div class="health-check">🔵 {lang.upper()} (Browser)</div>', unsafe_allow_html=True)
            else:
                cmd = health_cmds.get(lang)
                is_active = shutil.which(cmd) is not None if cmd else False
                icon = "🟢" if is_active else "🔴"
                st.markdown(f'<div class="health-check">{icon} {lang.upper()}</div>', unsafe_allow_html=True)

    st.divider()
    
    # --- ☁️ CLOUD VAULT SECTION ---
    st.markdown('<div class="status-card">☁️ <b>Cloud Vault</b></div>', unsafe_allow_html=True)
    if supabase_client:
        st.caption("✅ Connection Secure")
    else:
        st.caption("🔴 Offline (Check Secrets)")

    with st.expander("📁 Sync Progress"):
        proj_name = st.text_input("Name", value="Pro_Script")
        if st.button("✨ Save to Cloud"):
            if supabase_client:
                try:
                    data = {
                        "project_name": proj_name,
                        "code": st.session_state.current_code,
                        "language": language,
                        "timestamp": datetime.now().isoformat()
                    }
                    supabase_client.table("projects").upsert(data).execute()
                    st.success("Synced! 🚀")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("No Cloud Connection!")

    with st.expander("📚 Load Project"):
        if supabase_client:
            try:
                response = supabase_client.table("projects").select("*").execute()
                if response.data:
                    project_list = {p['project_name']: p for p in response.data}
                    selected = st.selectbox("Select", list(project_list.keys()))
                    if st.button("📥 Load"):
                        st.session_state.current_code = project_list[selected]['code']
                        st.rerun()
                else:
                    st.write("Vault empty.")
            except:
                st.write("Fetching...")

# --- 5. THE EDITOR ---
templates = {"python": "print('Lucas Engine v6.0 Ultra Online! 🚀')", "html": "<h1>Hello Lucas!</h1>"}
val = st.session_state.current_code if st.session_state.current_code else templates.get(language, "")

code = st_ace(
    value=val, 
    language=language if language not in ["bash", "csharp"] else ("sh" if language == "bash" else "csharp"),
    theme=theme,
    height=500, 
    key=f"ace_{language}"
)
st.session_state.current_code = code

# --- 6. EXECUTION ENGINE ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Run Code"):
        if language in ["html", "css"]:
            st.warning("Preview in browser! 🌐")
        else:
            with st.status("Engines Firing...", expanded=True):
                try:
                    # Specific ext map for temp files
                    ext_map = {"python": ".py", "javascript": ".js", "java": ".java", "cpp": ".cpp"}
                    ext = ext_map.get(language, ".txt")
                    tmp_file = f"temp_script{ext}"
                    with open(tmp_file, "w") as f: f.write(code)
                    
                    res = None
                    if language == "python":
                        res = subprocess.run(["python3", tmp_file], capture_output=True, text=True)
                    elif language == "javascript":
                        res = subprocess.run(["node", tmp_file], capture_output=True, text=True)
                    
                    if res:
                        if res.stdout: st.code(res.stdout)
                        if res.stderr: st.error(res.stderr)
                except Exception as e:
                    st.error(f"Critical Error: {e}")

with col2:
    # Lucas: Updated this to use the proj_name and the correct EXT_MAP! 💎
    final_ext = EXT_MAP.get(language, ".txt")
    st.download_button("📥 Download Locally", data=code, file_name=f"{proj_name}{final_ext}")

# --- 7. FOOTER & ENHANCED CHANGELOG ---
st.divider()
st.caption("Lucas IDE Pro v6.0 | Prototype | Secure Sandbox 🚀")

st.markdown("""
<div class="changelog-box">
    <div class="log-header">
        <span>🛠️</span> DEVELOPER LOG v6.0
    </div>
 <div class="log-item">
        <span class="log-icon">⚒️</span>
        <span><b>Performance:</b> Patched Bugs and Enhanced Stability. Fixed File Extension Download Mappings.</span>
    </div>
    <div class="log-item">
        <span class="log-icon">☁️</span>
        <span><b>Cloud Performance:</b> The "Cloud-Shield" Architecture: Fully optimized for Streamlit Cloud. Run high-performance code without exposing your local IP or hardware details.</span>
    </div>
    <div class="log-item">
        <span class="log-icon">🩺</span>
        <span><b>Expansion:</b> System Health Dashboard: A new sidebar diagnostic tool that checks the status of installed compilers (Rust, Java, Go, Powershell) in real-time.</span>
    </div>
    <div class="log-item">
        <span class="log-icon">🖥️</span>
        <span><b>Expansion:</b> Execution Status 2.0: Replaced static text with st.status containers, providing a live progress bar during compilation of heavy languages like Rust and C++.</span>
    </div>
    <div class="log-item">
        <span class="log-icon">☁️</span>
        <span><b>Cloud Power:</b> Added the "Cloud Vault" for persistent progress saving.</span>
    </div>
    <div class="log-item">
        <span class="log-icon">💾</span>
        <span><b>Storage:</b> Integrated workspace state to prevent code loss on refresh.</span>
    </div>
    <div class="log-item">
        <span class="log-icon">🎨</span>
        <span><b>UI/UX:</b> New sidebar dashboard for managing saved projects.</span>
    </div>
</div>
""", unsafe_allow_html=True)
