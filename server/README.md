## 🧭 How Secure-Comm Is Used

Secure-Comm follows a **centralized client–server architecture**.

There are **two distinct roles**:

---

### 🖥️ Server / Admin (EC2)

The server runs on a **single central machine** (for example, an AWS EC2 instance).

Responsibilities:
- Start and stop the secure server
- Manage users and groups
- Maintain the authentication database
- Remain continuously online

Typical workflow (on EC2):
```bash
sc start
python3 admin_setup.py
