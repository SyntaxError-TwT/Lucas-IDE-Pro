💻 Lucas IDE Pro Edition v6.0

Welcome to the Lucas IDE Pro Edition, a high-performance, stylish, and multi-language web-based development environment. Built for speed, security, and aesthetics. 🚀✨

💎 Features

18+ Language Support: Write and execute Python, Java, C#, C++, Rust, Go, Ruby, and many more!

Pro UI Architecture: Beautiful glassmorphic design with a custom purple "Pro" theme. 🎨

Cloud Vault: Secure project syncing to keep your progress locked in the cloud. ☁️

System Health Dashboard: Real-time diagnostic tool to check the status of your compilers (GCC, JDK, Mono, etc.). 🩺

Cloud-Shield Security: Optimized for Streamlit Cloud with an isolated execution sandbox. 🛡️

Asset Tracker: Live sidebar view of generated scripts and binary files. 📁

🛠️ Supported Languages

The engine is currently tuned for:

Backend: Python, Java, C#, C++, C, Rust, Go, PHP, Ruby, Lua, Perl.

Shell: Bash, PowerShell, Batch.

Web (Download-Only): HTML, CSS, SQL. 📥

👀Sneak Peak

![0223](https://github.com/user-attachments/assets/fba6f1b9-b932-4c25-b3fa-7ce2dabca600)

🚀 Quick Start

1. Open your browser

2. Type in https://online-ide.streamlit.app

Or:

1. Download Ultimate IDE Pro.py

2. Requirements

Make sure you have Python installed, then grab the essentials:

`pip install streamlit streamlit-ace`


3. System Engines (packages.txt)

To run languages like C#, Java, or Rust on your server, you'll need the following system packages:

build-essential (C/C++)

mono-complete (C#)

default-jdk (Java)

rustc (Rust)

golang-go (Go)

**MacOS:** `brew install {Package_Name}`

**Linux (Kali, Ubuntu, Debian):** `sudo apt update`
                                  `sudo apt install {Package_Name}`

**Windows:** Download installer from their own website, i.e. https://www.oracle.com/java/technologies/downloads/#java21, Run the downloaded launcher, and your done.             


3. Launch the IDE

Run the following command in your terminal:

**MacOS:** `python3 -m streamlit run {PATH for the IDE}/Ultimate\ IDE\ Pro.py` if python3 does not work, try to specify the **exact** version of your Python like python3.14 -m...

**Windows:** Navigate to the folder where you saved the IDE, Hold `Shift + Right Click` in that folder and select "Open PowerShell window here", type streamlit run {IDE file name}.py

**Linux (Linux Mint, Kali, Ubuntu, Debian):** Open your terminal with `Ctrl + alt + t`, type `sudo apt update && sudo apt upgrade -y`, type `sudo apt install build-essential mono-complete default-jdk golang-go nodejs npm ruby-full rustc php-cli lua5.3 perl sqlite3 -y` in the terminal, then, type `sudo apt install python3-pip -y` and `pip install streamlit streamlit-ace pandas` in the terminal, then, go to the saved folder using `cd ~/{Path the file is in}` and type `streamlit run {Name of IDE}.py`

**Note For Linux Installation:** If you get an error while running `pip install streamlit streamlit-ace pandas`, consider adding --break-system-packages (this might sound scary but it won't acctually break anything)

Built with ❤️ by SyntaxError-TwT | Thinking outside the box. 🌊🔥

Credits: Proxlight (Original Code)
