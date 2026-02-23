@echo off
echo 🚀 Lucas IDE Pro: Setting up Windows Environment...

:: Install Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Python...
    winget install Python.Python.3.12
)

:: Install Rust
rustc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Rust...
    winget install Rustlang.Rust.MSVC
)

:: Install OpenJDK (Java)
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Java...
    winget install Oracle.JDK.21
)

pip install streamlit streamlit-ace pyflakes
streamlit run "Ultimate IDE Pro.py"
pause