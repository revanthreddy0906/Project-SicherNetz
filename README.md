<pre style="font-family: monospace; white-space: pre; line-height: 1.1;">
███████╗██╗ ██████╗██╗  ██╗███████╗██████╗     ███╗   ██╗███████╗████████╗███████╗
██╔════╝██║██╔════╝██║  ██║██╔════╝██╔══██╗    ████╗  ██║██╔════╝╚══██╔══╝╚════██║
███████╗██║██║     ███████║█████╗  ██████╔╝    ██╔██╗ ██║█████╗     ██║      ██╔╝
╚════██║██║██║     ██╔══██║██╔══╝  ██╔══██╗    ██║╚██╗██║██╔══╝     ██║     ██╔╝  
███████║██║╚██████╗██║  ██║███████╗██║  ██║    ██║ ╚████║███████╗   ██║    ███████╗
╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══════╝

                     Secure Communication System
</pre>

# Project-SicherNetz 🔐
**A Secure Client–Server Communication System**

---

## 📌 Overview
Project-SicherNetz is a secure client–server communication system built to demonstrate
**secure networking principles**, **user authentication**, and **encrypted data exchange**
using Python.

The project focuses on creating a **reliable, privacy-aware communication channel**
between multiple clients and a central server, following **production-grade security
and Git practices**.

---

## 🚀 Features
- TLS/SSL encrypted communication  
- User authentication system  
- Real-time client-to-client messaging  
- Server-side session and connection management  
- Database-backed user handling  
- Secrets and certificates excluded from Git  
- Deployed on a remote Linux server  

---

## 🏗️ Project Structure

```text
secure-comm/
├── client/
│   └── client.py
│
├── server/
│   ├── server.py
│   ├── admin_setup.py
│   ├── db.py
│   └── users.db
│
├── certs/
│
├── .gitignore
├── README.md
└── requirements.txt
```
---

## 🔐 Security Practices
- Private keys and certificates are **never committed**
- Authentication data is hidden from server logs
- `.gitignore` used for secrets and runtime files
- GitHub authentication via **Personal Access Tokens**
- Clean Git history using amend-based fixes
- Separate production and testing branches

---

## ⚙️ Technologies Used
- Python 3  
- Socket Programming  
- SSL/TLS  
- SQLite  
- Linux (Ubuntu Server)  
- Git & GitHub  

---

## 🖥️ How It Works
1. The server listens on a secure port using SSL/TLS.
2. Clients establish encrypted connections to the server.
3. Users authenticate before accessing communication features.
4. The server manages active sessions and routes messages.
5. Client disconnections are handled gracefully.

---
