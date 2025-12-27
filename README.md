███████╗██╗ ██████╗██╗  ██╗███████╗██████╗     ███╗   ██╗███████╗████████╗███████╗
██╔════╝██║██╔════╝██║  ██║██╔════╝██╔══██╗    ████╗  ██║██╔════╝╚══██╔══╝╚════██║
███████╗██║██║     ███████║█████╗  ██████╔╝    ██╔██╗ ██║█████╗     ██║      ██╔╝
╚════██║██║██║     ██╔══██║██╔══╝  ██╔══██╗    ██║╚██╗██║██╔══╝     ██║     ██╔╝  
███████║██║╚██████╗██║  ██║███████╗██║  ██║    ██║ ╚████║███████╗   ██║    ███████╗
╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══════╝

                     Secure Communication System


Project-SicherNetz 🔐
A Secure Client–Server Communication System

⸻

📌 Overview

Project-SicherNetz is a secure client–server communication system designed to demonstrate secure networking principles, authentication, and encrypted data exchange using Python.

The project focuses on building a reliable, privacy-aware communication channel between multiple clients and a central server and follows production-grade security and Git practices.

⸻

🚀 Features
	•	🔒 TLS/SSL encrypted communication
	•	👤 User authentication system
	•	💬 Real-time client-to-client messaging
	•	🧠 Server-side session and connection management
	•	🗂️ Database-backed user handling
	•	🛡️ Secrets and certificates excluded from Git
	•	🌐 Deployed on a remote Linux server

⸻

🏗️ Project Structure

secure-comm/
│
├── client/
│   └── client.py          # Client-side application
│
├── server/
│   ├── server.py          # Core server logic
│   ├── admin_setup.py     # Admin-controlled DB setup
│   ├── db.py              # Database utilities
│   └── users.db           # User database (ignored if sensitive)
│
├── certs/                 # TLS certificates (ignored in Git)
│
├── .gitignore
├── README.md
└── requirements.txt


🔐 Security Practices
	•	❌ Private keys and certificates are never committed
	•	❌ Authentication data hidden from logs
	•	✅ .gitignore used for secrets and runtime files
	•	✅ GitHub authentication via Personal Access Tokens
	•	✅ Clean Git history with amend-based fixes
	•	✅ Production and testing branch separation

⸻

⚙️ Technologies Used
	•	Python 3
	•	Socket Programming
	•	SSL/TLS
	•	SQLite
	•	Linux (Ubuntu Server)
	•	Git & GitHub

⸻

🖥️ How It Works
	1.	The server listens on a secure port using SSL/TLS.
	2.	Clients establish encrypted connections.
	3.	Users authenticate before accessing communication features.
	4.	The server manages active sessions and routes messages.
	5.	Client disconnections are handled gracefully.
