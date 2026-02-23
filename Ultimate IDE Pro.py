import streamlit as st
from streamlit_ace import st_ace
import subprocess
import os
from pyflakes import api
import io
from contextlib import redirect_stderr
import re

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Lucas IDE Pro Edition", page_icon=":computer:", layout="wide")

# --- 2. CALLBACKS & STATE ---
def notify_download():
    st.toast("✅ Your file has finished downloading!", icon="📥")
    st.session_state.download_finished = True

if 'download_finished' not in st.session_state:
    st.session_state.download_finished = False

# --- 3. PURPLE CSS ---
st.markdown("""
    <style>
    div.stDownloadButton > button, div.stButton > button {
        background-color: #6c5ce7 !important;
        color: white !important;
        height: 3.5em !important;
        width: 100% !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0px 4px 15px rgba(108, 92, 231, 0.4) !important;
        transition: all 0.3s ease !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.header("🛠️ Settings")
    language = st.selectbox("Language", 
        ["python", "java", "bash", "powershell", "batch", "cpp", "c", "go", "ruby", "rust", "php", "javascript", "lua", "perl", "sql", "html", "csharp"], index=0)
    theme = st.selectbox("Editor Theme", ["monokai", "github", "dracula", "solarized_dark"])
    font_size = st.slider("Font Size", 12, 24, 14)

# --- 5. THE EDITOR ---
code = st_ace(language=language if language not in ["batch", "powershell", "csharp"] else "sh", 
              theme=theme, font_size=font_size, auto_update=True, key="editor")

# --- 6. FILE NAMING ---
file_name_input = st.text_input("📁 Enter file name", value="main")
extensions = {"python": ".py", "java": ".java", "bash": ".sh", "powershell": ".ps1", "batch": ".bat", "cpp": ".cpp", "c": ".c", "go": ".go", "ruby": ".rb", "rust": ".rs", "php": ".php", "javascript": ".js", "lua": ".lua", "perl": ".pl", "sql": ".sql", "html": ".html", "csharp": ".cs"}
final_file_name = f"{file_name_input}{extensions.get(language, '.txt')}"

# --- 7. ACTION BUTTONS ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Run Code"):
        try:
            # We use st.status now so it looks professional while running
            with st.status("🚀 Executing code...", expanded=True) as status:
                result = None
                if language == "python":
                    with open("temp.py", "w") as f: f.write(code)
                    result = subprocess.run(["python3", "temp.py"], capture_output=True, text=True)
                elif language == "java":
                    with open("Main.java", "w") as f: f.write(code)
                    cp = subprocess.run(["javac", "Main.java"], capture_output=True, text=True)
                    if cp.returncode == 0: result = subprocess.run(["java", "Main"], capture_output=True, text=True)
                    else: result = cp
                elif language == "bash":
                    with open("temp.sh", "w") as f: f.write(code)
                    result = subprocess.run(["bash", "temp.sh"], capture_output=True, text=True)
                # ... (Other languages follow this pattern)
                
                status.update(label="✅ Execution Complete!", state="complete", expanded=False)

            if result:
                st.subheader("Console Output:")
                clean_stdout = re.sub(r'\x1b\[[0-9;]*[mK]', '', result.stdout)
                if clean_stdout: st.code(clean_stdout)
                if result.stderr: st.error(result.stderr)
        except Exception as e:
            st.error(f"System Error: {e}")

with col2:
    st.download_button(
        label=f"📥 Download {final_file_name}", 
        data=code, 
        file_name=final_file_name, 
        mime="text/plain",
        on_click=notify_download
    )

if st.session_state.download_finished:
    st.success(f"**{final_file_name}** is ready! 🚀")
    st.session_state.download_finished = False

st.divider()
st.caption("Lucas IDE Pro Edition v4.9 🚀")