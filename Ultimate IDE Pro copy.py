import streamlit as st
from streamlit_ace import st_ace
import subprocess
import os

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Lucas Omega IDE", page_icon=":computer:", layout="wide")

# --- 2. STYLISH BUTTON CSS ---
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
    div.stDownloadButton > button:hover, div.stButton > button:hover {
        background-color: #a29bfe !important;
        transform: translateY(-2px) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("Settings")
    # Added powershell and batch to the list
    language = st.selectbox("Language", 
        ["python", "java", "bash", "powershell", "batch", "cpp", "c", "go", "ruby", "rust", "php", "javascript", "lua", "perl", "sql", "html"], index=0)
    theme = st.selectbox("Editor Theme", ["monokai", "github", "dracula", "solarized_dark"])
    font_size = st.slider("Font Size", 12, 24, 14)

# --- 4. THE CODE EDITOR ---
code = st_ace(language=language if language != "batch" else "sh", theme=theme, font_size=font_size, auto_update=True, key="editor")

# --- 5. FILE NAMING ---
file_name_input = st.text_input("Enter file name", value="main")
extensions = {
    "python": ".py", "java": ".java", "bash": ".sh", "powershell": ".ps1", 
    "batch": ".bat", "cpp": ".cpp", "c": ".c", "go": ".go", "ruby": ".rb", 
    "rust": ".rs", "php": ".php", "javascript": ".js", "lua": ".lua", 
    "perl": ".pl", "sql": ".sql", "html": ".html"
}
extension = extensions.get(language, ".txt")
final_file_name = f"{file_name_input}{extension}"

# --- 6. ACTION BUTTONS ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Run Code"):
        try:
            result = None
            env = os.environ.copy()
            
            # --- POWERSHELL ---
            if language == "powershell":
                with open("temp.ps1", "w") as f: f.write(code)
                result = subprocess.run(["pwsh", "-File", "temp.ps1"], capture_output=True, text=True, env=env)

            # --- PYTHON ---
            elif language == "python":
                with open("temp.py", "w") as f: f.write(code)
                result = subprocess.run(["python3", "temp.py"], capture_output=True, text=True, env=env)

            # --- RUST ---
            elif language == "rust":
                with open("temp.rs", "w") as f: f.write(code)
                cp = subprocess.run(["rustc", "temp.rs", "-o", "temp_rust"], capture_output=True, text=True)
                if cp.returncode == 0:
                    result = subprocess.run(["./temp_rust"], capture_output=True, text=True)
                else: result = cp

            # --- RUBY ---
            elif language == "ruby":
                with open("temp.rb", "w") as f: f.write(code)
                result = subprocess.run(["ruby", "temp.rb"], capture_output=True, text=True, env=env)

            # --- JAVASCRIPT ---
            elif language == "javascript":
                with open("temp.js", "w") as f: f.write(code)
                result = subprocess.run(["node", "temp.js"], capture_output=True, text=True, env=env)

            # --- C++ ---
            elif language == "cpp":
                with open("temp.cpp", "w") as f: f.write(code)
                cp = subprocess.run(["g++", "temp.cpp", "-o", "temp_cpp"], capture_output=True, text=True)
                if cp.returncode == 0:
                    result = subprocess.run(["./temp_cpp"], capture_output=True, text=True)
                else: result = cp

            # --- C ---
            elif language == "c":
                with open("temp.c", "w") as f: f.write(code)
                cp = subprocess.run(["gcc", "temp.c", "-o", "temp_c"], capture_output=True, text=True)
                if cp.returncode == 0:
                    result = subprocess.run(["./temp_c"], capture_output=True, text=True)
                else: result = cp

            # --- JAVA ---
            elif language == "java":
                with open("Main.java", "w") as f: f.write(code)
                cp = subprocess.run(["javac", "Main.java"], capture_output=True, text=True)
                if cp.returncode == 0:
                    result = subprocess.run(["java", "Main"], capture_output=True, text=True)
                else: result = cp

            # --- GO ---
            elif language == "go":
                with open("main.go", "w") as f: f.write(code)
                result = subprocess.run(["go", "run", "main.go"], capture_output=True, text=True, env=env)

            # --- LUA ---
            elif language == "lua":
                with open("temp.lua", "w") as f: f.write(code)
                result = subprocess.run(["lua", "temp.lua"], capture_output=True, text=True, env=env)

            # --- PERL ---
            elif language == "perl":
                with open("temp.pl", "w") as f: f.write(code)
                result = subprocess.run(["perl", "temp.pl"], capture_output=True, text=True, env=env)

            # --- BASH ---
            elif language == "bash":
                with open("temp.sh", "w") as f: f.write(code)
                result = subprocess.run(["bash", "temp.sh"], capture_output=True, text=True, env=env)

            # --- PHP ---
            elif language == "php":
                with open("temp.php", "w") as f: f.write(code)
                result = subprocess.run(["php", "temp.php"], capture_output=True, text=True, env=env)

            # --- OUTPUT DISPLAY ---
            if result:
                st.subheader("Output:")
                if result.stdout: st.code(result.stdout)
                if result.stderr: st.error(result.stderr)
            elif language in ["html", "sql", "batch"]:
                st.info(f"Download to use your {language} file!")

        except Exception as e:
            st.error(f"System Error: {e}")

with col2:
    st.download_button(label=f"📥 Download {final_file_name}", data=code, file_name=final_file_name)

st.divider()
st.caption("Lucas IDE Pro v3.5 🚀")