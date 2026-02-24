import streamlit as st
from streamlit_ace import st_ace
import subprocess
import shutil
import os
import json
import uuid
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. PAGE CONFIG & UI ---
st.set_page_config(
    page_title="Lucas IDE Pro Edition",
    page_icon="💻",
    layout="wide"
)

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
        box-shadow: 0px 4px 15px rgba(108, 92, 231, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        background-color: #a29bfe !important;
    }

    /* Glassmorphic Cards */
    .cloud-card, .preview-card {
        background: rgba(108, 92, 231, 0.1);
        border: 1px dashed #6c5ce7;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CLOUD VAULT ENGINE (FIRESTORE) ---
# Grabbing the global variables provided by the environment
app_id = st.secrets.get("__app_id", "lucas-ide-pro")

@st.cache_resource
def init_firebase():
    try:
        # Check if already initialized
        firebase_admin.get_app()
    except ValueError:
        if "__firebase_config" in st.secrets:
            config = json.loads(st.secrets["__firebase_config"])
            cred = credentials.Certificate(config)
            firebase_admin.initialize_app(cred)
        else:
            return None
    return firestore.client()

db = init_firebase()

# --- 3. SESSION STATE ---
if "current_code" not in st.session_state:
    st.session_state.current_code = ""

# --- 4. SIDEBAR ---
# SQL REMOVED PER REQUEST 🚫
LANGUAGES = [
    "python", "javascript", "java", "cpp", "c", "rust", "go", "php", 
    "ruby", "bash", "powershell", "batch", "lua", "perl", "csharp", "css", "html"
]

with st.sidebar:
    st.title("🛠️ Lucas IDE Pro")
    language = st.selectbox("Select Language", LANGUAGES)
    theme_choice = st.selectbox("Editor Theme", ["monokai", "dracula", "github", "tomorrow_night"])
    
    st.divider()
    st.markdown('<div class="cloud-card">☁️ <b>Cloud Vault</b></div>', unsafe_allow_html=True)
    
    # --- SAVE TO CLOUD ---
    with st.expander("📁 Sync to Cloud"):
        proj_name = st.text_input("Project Name", value="My_Pro_Script")
        if st.button("✨ Save Now"):
            if db:
                try:
                    # RULE 1: Strict Paths - artifacts/{appId}/public/data/{collection}
                    doc_ref = db.collection("artifacts").document(app_id).collection("public").document("data").collection("projects").document(proj_name)
                    doc_ref.set({
                        "code": st.session_state.current_code,
                        "language": language,
                        "last_updated": firestore.SERVER_TIMESTAMP
                    })
                    st.success(f"'{proj_name}' synced to cloud! 🚀")
                except Exception as e:
                    st.error(f"Sync error: {e}")
            else:
                st.warning("Cloud Brain not connected! (Check secrets)")

    # --- LOAD FROM CLOUD ---
    with st.expander("📚 Load Project"):
        if db:
            try:
                # RULE 2: Simple Query
                docs = db.collection("artifacts").document(app_id).collection("public").document("data").collection("projects").stream()
                projects = {doc.id: doc.to_dict() for doc in docs}
                
                if projects:
                    selected = st.selectbox("Select Project", list(projects.keys()))
                    if st.button("📥 Load Selected"):
                        st.session_state.current_code = projects[selected]["code"]
                        st.rerun()
                else:
                    st.write("Vault is empty.")
            except Exception as e:
                st.write("Searching for projects...")
        else:
            st.info("Load feature requires Cloud connection.")

# --- 5. EDITOR ---
templates = {
    "python": "print('Lucas IDE Pro Online 🚀')",
    "html": "<!-- Preview disabled. Download to view! -->\n<h1>Hello Lucas!</h1>",
    "css": "/* Style your masterpiece */\nbody { background: #0e1117; }",
    "csharp": "using System;\nclass Program { static void Main() { Console.WriteLine(\"C# Engine Ready!\"); } }"
}

# Load current state or template
val = st.session_state.current_code if st.session_state.current_code else templates.get(language, "")

code = st_ace(
    value=val, 
    language=language if language not in ["bash", "csharp"] else ("sh" if language == "bash" else "csharp"), 
    theme=theme_choice, 
    height=500, 
    key=f"ace_{language}"
)
st.session_state.current_code = code

# --- 6. EXECUTION ENGINE ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Run Code"):
        if not code.strip():
            st.warning("Write code first!")
        elif language in ["html", "css"]:
            st.warning(f"Language {language} not supported for direct execution! Please download.")
        else:
            with st.status("Executing Lucas-Level Code...", expanded=True):
                try:
                    ext_map = {
                        "python": ".py", "java": ".java", "cpp": ".cpp", "c": ".c",
                        "rust": ".rs", "go": ".go", "javascript": ".js", "ruby": ".rb",
                        "php": ".php", "lua": ".lua", "perl": ".pl", "powershell": ".ps1",
                        "csharp": ".cs"
                    }
                    ext = ext_map.get(language, ".txt")
                    tmp_file = f"temp_script{ext}"
                    with open(tmp_file, "w") as f: f.write(code)
                    
                    # Command Map
                    res = None
                    if language == "python":
                        res = subprocess.run(["python3", tmp_file], capture_output=True, text=True)
                    elif language == "javascript":
                        res = subprocess.run(["node", tmp_file], capture_output=True, text=True)
                    elif language == "csharp":
                        c_res = subprocess.run(["mcs", tmp_file], capture_output=True, text=True)
                        if c_res.returncode == 0:
                            res = subprocess.run(["mono", "temp_script.exe"], capture_output=True, text=True)
                        else: res = c_res
                    elif language == "java":
                        with open("Main.java", "w") as f: f.write(code)
                        c_res = subprocess.run(["javac", "Main.java"], capture_output=True, text=True)
                        if c_res.returncode == 0: res = subprocess.run(["java", "Main"], capture_output=True, text=True)
                        else: res = c_res
                    
                    if res:
                        if res.stdout: st.code(res.stdout)
                        if res.stderr: st.error(res.stderr)
                except Exception as e:
                    st.error(f"Critical Engine Error: {e}")

with col2:
    st.download_button(label="📥 Download locally", data=code, file_name=f"main.{language}")

st.divider()
st.caption("Lucas IDE Pro v5.0 | Cloud Vault Active | Thinking Outside the Box 🌊🔥")
