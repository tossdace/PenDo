# PenDo

# 🕵️‍♂️ PenDo – The Ultimate Brute-Force Testing Framework

![PenDo Banner](https://img.shields.io/badge/Security-Research-green)
![PenDo Status](https://img.shields.io/badge/Status-Active-brightgreen)
![MIT License](https://img.shields.io/badge/License-MIT-blue)

---

PenDo (**Penetration Dojo**) is a **professional brute-force testing and security research tool** for penetration testers, red teamers, and cybersecurity enthusiasts.  
It features a **matrix-style terminal UI, blazing-fast modular design, and clean codebase** ready for customization.  

> ⚠️ Ethical Use Disclaimer:  
> PenDo is strictly for **educational and authorized security testing**. Misuse is your responsibility.

---

## 🚀 Features

- 🔥 **Hacker-Style UI**: Green matrix terminal with ASCII art banners  
- 🔑 **Brute Force Simulation**: Test passwords against dummy targets or your own systems  
- 📂 **Wordlist Support**: Easily swap in custom password lists  
- 🛠 **Modular Codebase**: Extend functionality in `utils/` folder  
- ⚡ **Fast & Efficient**: Optimized loops with simulated delays  
- 📜 **MIT Licensed**: Open-source & free for all

---

---

## 🧩 Project Structure

```text
PenDo/
├── pendo_main.py          # Main entry point
├── utils/
│   ├── __init__.py
│   ├── utils_ui.py        # UI animations, banners
│   ├── utils_logger.py    # Logging & reporting
│   └── utils_bruteforce.py# Brute force logic
├── sample_wordlist.txt    # Example passwords
├── README.md
├── LICENSE
└── .gitignore

## ⚙️ Installation & Usage

PenDo works seamlessly on **Windows**, **Linux (Kali)**, and **Termux (Android)**.  

---

### 🔹 On Kali Linux / Any Linux Distro

```bash
# Update your system
sudo apt update && sudo apt upgrade -y

# Install Python & Git
sudo apt install python3 python3-pip git -y

# Clone the repository
git clone https://github.com/YourGitHubUsername/PenDo.git
cd PenDo

# Install dependencies
pip3 install colorama tqdm

# Run PenDo
python3 pendo_main.py --username admin --wordlist sample_wordlist.txt




# Install Termux from F-Droid (recommended)
# Then run:
pkg update && pkg upgrade -y
pkg install python git -y

# Clone the repository
git clone https://github.com/YourGitHubUsername/PenDo.git
cd PenDo

# Install dependencies
pip install colorama tqdm

# Run PenDo
python pendo_main.py --username admin --wordlist sample_wordlist.txt


# Install Python 3 from python.org
# Install Git from git-scm.com

# Clone repo
git clone https://github.com/YourGitHubUsername/PenDo.git
cd PenDo

# Install dependencies
pip install colorama tqdm

# Run PenDo
python pendo_main.py --username admin --wordlist sample_wordlist.txt




