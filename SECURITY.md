# Security Policy - GSIS-CLI

## 🛡️ Security Commitment
GSIS-CLI (Secure Sensitive Information Manager) has been designed following the MVC pattern and utilizes enterprise-grade encryption algorithms such as **Argon2id** and **Fernet (AES-256)**. However, no software is 100% invulnerable.

## ⚠️ User Responsibility
The use of this software implies the acceptance of the following conditions:
- **Master Key**: The author cannot recover any data if the master password is forgotten.
- **Anti-Brute Force Protection**: The system automatically deletes the database after 3 failed attempts. It is the user's responsibility to maintain encrypted backups.
- **Environment**: It is highly recommended to run GSIS-CLI on updated operating systems free of malware.

## 🔍 Vulnerability Reporting
If you discover a security flaw, please follow these steps for **responsible disclosure**:

1. **Do NOT open a public Issue**: This would expose other users before a patch is available.
2. **Private Contact**: Send a detailed email to [whoamy0608@gmail.com] or contact the author privately.
3. **Details**: Include steps to reproduce the flaw and, if possible, a proposed solution.
4. **Grace Period**: Please allow a reasonable amount of time to fix the issue before public disclosure.

## ✅ Implemented Best Practices
- **PBKDF2**: 480,000 iterations for key derivation.
- **No Persistence**: Encryption keys are never stored on disk.
- **Safe Logging**: No sensitive data is recorded in log files.

---
**Last updated**: February 19, 2026

