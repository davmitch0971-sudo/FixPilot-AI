# Security Policy — FixPilot‑AI

FixPilot‑AI is designed with safety, integrity, and responsible AI execution in mind.  
This document explains how to report vulnerabilities, how security issues are handled, and what users should expect when interacting with the system.

---

## 🔐 Supported Versions

| Version | Supported |
|--------|-----------|
| Main branch | ✔ Active |
| Development builds | ✔ Active |
| Older snapshots | ✖ Not supported |

Only the **main branch** receives security patches.

---

## 🛡 Reporting a Vulnerability

If you discover a vulnerability, please report it responsibly.

### 📬 How to report:
- Open a private security issue on GitHub  
  https://github.com/davmitch0971-sudo/FixPilot-AI/security/advisories  
- OR email (coming soon)

### Include:
- Description of the issue  
- Steps to reproduce  
- Impact assessment  
- Logs or screenshots (if safe to share)

**Do NOT** publicly post zero‑day vulnerabilities.

---

## ⚠ Responsible Disclosure Expectations

We commit to:
- Acknowledging your report within **72 hours**
- Providing a fix or mitigation plan within **7–14 days**
- Keeping communication private until a patch is released

You commit to:
- Not exploiting the vulnerability  
- Not sharing it publicly before a fix is deployed  
- Providing enough detail for reproduction  

---

## 🔒 Security Features in FixPilot‑AI

FixPilot‑AI includes built‑in safeguards:

- Engine isolation  
- Sandboxed execution  
- Integrity verification  
- Logging & audit trails  
- No destructive system calls  
- No unauthorized network access  
- No self‑modifying code outside approved modules  

---

## 🧪 Safe Testing Guidelines

When testing FixPilot‑AI:
- Use a non‑production environment  
- Avoid running engines with elevated privileges  
- Do not test on systems containing sensitive data  
- Review logs for unexpected behavior  

---

## 🚫 Prohibited Use

FixPilot‑AI must **not** be used for:
- Unauthorized system access  
- Malware creation  
- Network intrusion  
- Bypassing security controls  
- Any illegal or harmful activity  

---

## 🤝 Contributing to Security

Security‑focused pull requests are welcome.  
If submitting a fix, reference the advisory number in your PR.

