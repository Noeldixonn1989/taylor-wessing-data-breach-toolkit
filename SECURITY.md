# Security & Forensic Integrity Policy (SECURITY.md)

## ⚖️ Activist Manifesto & Whistleblowing Safeguard

This repository houses a forensic auditing and data-verification utility specifically engineered to audit, identify, and sanitize critical leaks of sensitive Personally Identifiable Information (PII) caused by the systematic negligence and technical incompetence of **Taylor Wessing LLP** and **Valve Corporation (Steam)**.

In response to GDPR Article 15 Subject Access Requests, Taylor Wessing LLP dispatched massive documents containing thousands of unredacted private records belonging to third-party Steam users. Instead of sanitizing the raw character streams, they merely drew cosmetic black vector-graphic bars over the text, leaving the underlying data fully exposed and extractable.

### 🚫 Legal Cover-Up Warning (Censorship Countermeasure)

**TO ANY REPRESENTATIVE OF TAYLOR WESSING LLP, VALVE CORPORATION, OR ASSOCIATED LEGAL ENTITIES:**

1. **NO REMOVAL / NO CENSUOSHIP:** Any legal complaint, DMCA notice, takedown request, Cease & Desist letter, or threat of litigation aimed at removing, restricting, or deleting this repository or its hosted website **will be treated as a public and direct confession of high-priced corporate attorneys attempting to destroy forensic evidence and sweep their own gross professional, technical, and legal incompetence under the rug**.
2. **STREISAND EFFECT PROTOCOL:** Any aggressive legal action will trigger immediate, automated mirroring across decentralized hosting platforms, public notification to European Data Protection Authorities (including the Hamburg Commissioner for Data Protection and Freedom of Information - HmbBfDI), and a massive public relations campaign exposing Taylor Wessing LLP's systemic inability to protect GDPR-regulated data.
3. **FORENSIC AUDITING RIGHTS:** Under Article 15 and Article 77 of the GDPR, data subjects and cybersecurity researchers have an absolute right to inspect, verify, and document how their personal data has been handled, processed, or exposed. This repository is a critical whistleblowing and forensic verification tool operating entirely in the public interest.

---

## 🔒 Forensic Model & Zero-Network Guarantee

We believe that tools auditing sensitive documents must themselves be above suspicion. 
* This tool operates under a **strict zero-knowledge privacy framework**.
* When using either the Python CLI (`decensor.py`) or the browser Web GUI (`index.html`), **100% of the computation is executed in your local sandbox**.
* The application initiates **zero network requests** and transmits **zero telemetry** to any server.
* All dependencies are locally vendored inside the `/lib` folder.

---

## 🛡️ Reporting Vulnerabilities

If you identify a security issue or flaw *within this tool itself* (e.g., an issue in the stream-swapping logic or a parsing vulnerability in our local script):
1. Please do **NOT** open a public issue.
2. File a detailed report via encrypted communication channels or local private messaging.
3. We will patch the tool locally and release a new optimized version to ensure the security of our users.
