import streamlit as st
from streamlit_ace import st_ace
import subprocess
import os
import re

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(
    page_title="Lucas IDE Pro Edition",
    page_icon="💻",
    layout="wide"
)

# --- 2. CSS STYLING (PURPLE THEME) ---
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Custom Button Styling */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #6c5ce7 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        height: 3em !important;
        width: 100% !important;
        font-weight: bold !important;
        box-shadow: 0px 4px 15px rgba(108, 92, 231, 0.3) !important;
        transition: 0.3s;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #a29bfe !important;
        transform: translateY(-2px);
    }
    
    /* Error and Success Box Styling */
    .stAlert { border-radius: 10px !important; border: 1px solid #6c5ce7 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE & CALLBACKS ---
if 'download_status' not in st.session_state:
    st.session_state.download_status = False

def notify_download():
    st.session_state.download_status = True
    st.toast("✅ File ready for download!", icon="📥")

# --- 4. SIDEBAR SETTINGS ---
with st.sidebar:
    st.title("🛠️ Lucas IDE Pro")
    language = st.selectbox("Select Language", [
        "python", "java", "cpp", "c", "rust", "go", 
        "powershell", "bash", "ruby", "javascript", "php"
    ])
    theme = st.selectbox("Editor Theme", ["monokai", "dracula", "github", "solarized_dark"])
    font_size = st.slider("Font Size", 12, 32, 16)
    st.divider()
    st.info("Status: Cloud Shield Active 🛡️")

# --- 5. EDITOR & FILE NAMING ---
# Map display name to Ace Editor internals
ace_lang = "sh" if language in ["powershell", "bash"] else language

# Templates to prevent the "Main Class" error
templates = {
    "java": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello Lucas!\");\n    }\n}",
    "rust": "fn main() {\n    println!(\"Rust is working!\");\n}",
    "cpp": "#include <iostream>\nint main() {\n    std::cout << \"C++ Pro Mode\";\n    return 0;\n}"
}

code = st_ace(
    value=templates.get(language, ""),
    language=ace_lang,
    theme=theme,
    font_size=font_size,
    height=450,
    key="lucas_editor"
)

file_name_input = st.text_input("📁 Filename (no extension)", value="main")
ext_map = {
    "python": ".py", "java": ".java", "cpp": ".cpp", "c": ".c", 
    "rust": ".rs", "go": ".go", "powershell": ".ps1", "bash": ".sh", 
    "ruby": ".rb", "javascript": ".js", "php": ".php"
}
final_filename = f"{file_name_input}{ext_map.get(language, '.txt')}"

# --- 6. EXECUTION ENGINE ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Run Code"):
        if not code.strip():
            st.warning("Write some code first!")
        else:
            with st.status("🏗️ Compiling and Running...", expanded=True) as status:
                try:
                    res = None
                    # --- Python ---
                    if language == "python":
                        with open("temp.py", "w") as f: f.write(code)
                        res = subprocess.run(["python3", "temp.py"], capture_output=True, text=True)
                    
                    # --- Java ---
                    elif language == "java":
                        with open("Main.java", "w") as f: f.write(code)
                        compile_res = subprocess.run(["javac", "Main.java"], capture_output=True, text=True)
                        if compile_res.returncode == 0:
                            res = subprocess.run(["java", "Main"], capture_output=True, text=True)
                        else: res = compile_res

                    # --- Rust ---
                    elif language == "rust":
                        with open("temp.rs", "w") as f: f.write(code)
                        compile_res = subprocess.run(["rustc", "temp.rs", "-o", "temp_rust"], capture_output=True, text=True)
                        if compile_res.returncode == 0:
                            res = subprocess.run(["./temp_rust"], capture_output=True, text=True)
                        else: res = compile_res

                    # --- PowerShell (Linux Pwsh) ---
                    elif language == "powershell":
                        with open("temp.ps1", "w") as f: f.write(code)
                        res = subprocess.run(["pwsh", "temp.ps1"], capture_output=True, text=True)

                    # --- C++ ---
                    elif language == "cpp":
                        with open("temp.cpp", "w") as f: f.write(code)
                        compile_res = subprocess.run(["g++", "temp.cpp", "-o", "temp_cpp"], capture_output=True, text=True)
                        if compile_res.returncode == 0:
                            res = subprocess.run(["./temp_cpp"], capture_output=True, text=True)
                        else: res = compile_res

                    status.update(label="✅ Run Finished", state="complete")
                    
                    if res:
                        st.subheader("Console Output")
                        if res.stdout: st.code(res.stdout)
                        if res.stderr: st.error(res.stderr)
                        
                except Exception as e:
                    st.error(f"System Error: {e}")

with col2:
    st.download_button(
        label=f"📥 Download {final_filename}",
        data=code,
        file_name=final_filename,
        on_click=notify_download
    )

if st.session_state.download_status:
    st.success(f"**{final_filename}** has finished downloading! 🚀")
    st.session_state.download_status = False

st.divider()
st.caption("Lucas IDE Pro Edition v4.9 | Open Source Build")