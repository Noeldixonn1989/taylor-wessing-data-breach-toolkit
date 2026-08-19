# 📡 THE TAYLOR WESSING DATA BREACH TOOLKIT
### 🐕 "My Dog vs. Elite GDPR Lawyers" — Exposing Valve's Systemic Data Leaks & Corporate Lawyer Hubris

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-red.svg?style=for-the-badge" alt="License: MIT">
  <img src="https://img.shields.io/badge/Security-100%25_Offline_Local-green.svg?style=for-the-badge" alt="Security: 100% Offline">
  <img src="https://img.shields.io/badge/Status-Active_OSINT_Forensics-orange.svg?style=for-the-badge" alt="Status: Active OSINT">
</p>

---

Welcome to the official, offline-first forensic audit suite engineered to dismantle, analyze, and expose the catastrophic, multi-million dollar "DIY" PDF redaction failures of elite international law firm **Taylor Wessing LLP** and **Valve Corporation (Steam)**. 

This repository is a monument to high-priced corporate lawyer incompetence and a powerful weapon for public interest whistleblowing.

---

## 📖 THE STORY: My Dog vs. Elite GDPR Lawyers

In response to a standard EU GDPR Article 15 Subject Access Request regarding stolen Steam account data, Valve's elite external counsel—**Taylor Wessing LLP**—attempted to redact thousands of sensitive private user records.

Instead of purchasing standard, industry-certified PDF redaction software, their developers and lawyers decided to build a custom, automated "DIY" PDF generator script using *Aspose.PDF for .NET*.

### The Catastrophic Blunder
Their DIY tool made a hilarious, amateur mistake: it merely programmatically searched the coordinates of sensitive fields and drew **solid black vector shapes** (using PDF's `re` and `f`/`F`/`b`/`B` operators) right on top of the text, thinking that visually covering the text was equivalent to deleting it.

They completely forgot that visual drawing overlays **do not alter or destroy the raw text arrays underneath**. As a result, they successfully dispatched **830 pages of fake visual redactions** directly to us, completely leaking thousands of unredacted private Steam account logins, emails, security logs, and de-anonymized minor's data directly to the public.

---

> [!CAUTION]
> ### 🚨 DIALOGUE WITH DR. PATRICK (THE COVER-UP)
> We formally contacted **Dr. Patrick** (DPO/Partner) at Taylor Wessing LLP regarding this massive, systematic exposure of Steam users' PII under GDPR Article 32. 
> 
> Their response confirmed that the firm is completely inadequate, deeply incompetent, and has **absolutely no intention of notifying affected data subjects, taking accountability, or warning the public**. 
> 
> They thought they could silence the community with expensive legal threats, but they forgot one thing: **the truth is written losslessly inside the byte streams.**

### 📚 MUST-READ INVESTIGATIVE WRITEUPS:
* **🔬 Read the Full Case Study:** [Valve's Profits From Stolen Steam Accounts](https://phishdestroy.io/valve-profits-from-stolen-accounts)
* **📰 Read Part 1 on Medium:** [My Dog vs. Elite GDPR Lawyers: The Valve Data Breach Nobody is Talking About](https://phishdestroy.medium.com/my-dog-vs-elite-gdpr-lawyers-the-valve-data-breach-nobody-is-talking-about-f6f7683d813d)
* **📰 Read Part 2 on Medium:** [My Dog vs. Elite Lawyers Part 2: The 5-Year PDF Vulnerability Exposing Global Corporations](https://phishdestroy.medium.com/my-dog-vs-elite-lawyers-part-2-the-5-year-pdf-vulnerability-exposing-global-corporations-81cdad269253)

---

## 🛠️ MULTI-TOOL CAPABILITIES

This suite offers two complementary, fully client-side modes to analyze and dismantle fake visual redactions from Taylor Wessing or any other incompetent organization:

| Mode / Feature | Technology | Target Elements | Output Format |
| :--- | :--- | :--- | :--- |
| **📡 Mode 1: X-Ray Scanner** | PDF.js (Mozilla) | Searchable Text Layers | Live Terminal Stream |
| **✂️ Mode 2: Layer Stripper** | PDF-Lib (Indirect Objects) | Vector Paths (`re`, `f`, `b`) | Lossless Clean PDF |
| **🔎 Mode 3: Collision Audit** | PyMuPDF (Fitz Layout) | Overlapping Text & Graphics | `.txt` Leaks Report |

<br>

<details>
<summary><b>🛰️ Expand Mode 1 Details (X-Ray Live Terminal)</b></summary>
<br>

Splits your workspace into a responsive dual-pane view:
* **Left Pane:** Renders the visual PDF, displaying the black masking blocks.
* **Right Pane:** A synchronized green-on-black terminal that losslessly pulls the underlying unredacted text characters in real-time as you flip pages. You see the black box, but you read the secret instantly.
</details>

<details>
<summary><b>✂️ Expand Mode 2 Details (Surgical Layer Stripper)</b></summary>
<br>

A surgical, global stream-level sanitization engine:
* **Deep Stream Swapping:** Scans every single xref indirect object in the PDF—including Page Contents and nested **Form XObjects** (where template drawings are hidden).
* **Operator Purge:** Replaces rectangular visual paint commands (`re f`, `re F`, `re b`, `re B`, etc.) with the `n` (no-paint) operator. It physically deletes the black bars, dropping Page 1 black drawings to **exactly 0**, leaving a clean, naked document for download.
</details>

---

## 💻 CLI USAGE (`decensor.py`)

<details>
<summary><b>🔧 Click to Expand CLI Setup & Requirements</b></summary>
<br>

### Requirements
- Python 3.x
- PyMuPDF library

Install the required library on your local system:
```bash
pip install pymupdf
```
</details>

<details>
<summary><b>📡 Click to Expand CLI Command Reference</b></summary>
<br>

```bash
# 1. Decompose PDF to raw text layers (Strips all drawings, lines, and masks globally)
python decensor.py -i compromised.pdf -d -o naked_document.pdf

# 2. Extract and save all text hidden under black visual shapes to a leaks text report
python decensor.py -i compromised.pdf -e verified_leaks.txt

# 3. List page-by-page structural element counts (drawings, images, text blocks)
python decensor.py -i compromised.pdf -l

# 4. Standard stream-level sanitization
python decensor.py -i compromised.pdf -o unmasked.pdf
```
</details>

---

## 📝 CODE WALKTHROUGH

<details>
<summary><b>🐍 View Python Global Stream Sanitizer</b></summary>
<br>

The core script uses PyMuPDF's low-level stream reading interfaces. It parses the decompressed cross-reference (`xref`) stream of each page and resource, applies a whitespace-preserving regular expression to swap visual fill operators with a non-painting operator, and reconstructs the PDF stream with full garbage collection and stream deflation.

```python
import re, fitz

def strip_black_bars_global(input_path, output_path):
    doc = fitz.open(input_path)
    for xref in range(1, doc.xref_length()):
        if not doc.is_stream(xref):
            continue
        try:
            # Skip binary streams (Fonts, Images, Halftones)
            obj_dict = doc.xref_object(xref)
            if any(m in obj_dict for m in ["/Type /Font", "/Subtype /Image", "/Type /Halftone"]):
                continue
                
            stream_bytes = doc.xref_stream(xref)
            text = stream_bytes.decode('latin-1')
            
            # Swap rectangular painting operators with no-fill 're n', preserving newlines
            modified_text, count = re.subn(
                r'\bre\s+([fFbB]\*?)(?=\s|$)',
                lambda m: f"re{m.group(0)[2:-len(m.group(1))]}n",
                text
            )
            if count > 0:
                doc.update_stream(xref, modified_text.encode('latin-1'))
        except Exception:
            continue
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()
```
</details>

<details>
<summary><b>☕ View Javascript Browser-Side Sanitizer</b></summary>
<br>

The Web GUI performs the identical structural modifications in-memory using `pdf-lib` via low-level object context mapping.

```javascript
async function sanitizePdfClientSide(rawPdfBytes) {
    const { PDFDocument, PDFName, decodePDFRawStream } = PDFLib;
    const pdfDocInstance = await PDFDocument.load(rawPdfBytes);
    const context = pdfDocInstance.context;
    const indirectObjects = context.enumerateIndirectObjects();
    
    for (let i = 0; i < indirectObjects.length; i++) {
        const [ref, pdfObject] = indirectObjects[i];
        
        if (pdfObject && typeof pdfObject.getContents === 'function' && pdfObject.dict) {
            const dict = pdfObject.dict;
            const type = dict.get(PDFName.of('Type'));
            const subtype = dict.get(PDFName.of('Subtype'));
            
            if (type === PDFName.of('Font') || subtype === PDFName.of('Image') || type === PDFName.of('Halftone')) {
                continue;
            }
            
            try {
                const rawData = decodePDFRawStream(pdfObject).decode();
                const text = Array.from(rawData, byte => String.fromCharCode(byte)).join('');
                const modifiedText = text.replace(/re(\s+)([fFbB]\*?)(?=\s|$)/g, 're$1n');
                
                if (text !== modifiedText) {
                    const modifiedData = new Uint8Array(modifiedText.length);
                    for (let k = 0; k < modifiedText.length; k++) {
                        modifiedData[k] = modifiedText.charCodeAt(k) & 0xff;
                    }
                    
                    const newStreamObj = context.flateStream(modifiedData);
                    const keys = dict.keys();
                    for (let k = 0; k < keys.length; k++) {
                        const key = keys[k];
                        if (key !== PDFName.of('Filter') && key !== PDFName.of('Length')) {
                            newStreamObj.dict.set(key, dict.get(key));
                        }
                    }
                    context.assign(ref, newStreamObj);
                }
            } catch (err) {
                continue;
            }
        }
    }
    return await pdfDocInstance.save();
}
```
</details>

---

## ⚖️ ANTI-CENSORSHIP GUARANTEE (SECURITY.md)

Any legal warnings, DMCA takedown requests, or hostile actions initiated by Taylor Wessing LLP, Valve Corporation, or their attorneys to censor this repository **will be treated as public, undeniable proof of attempting to hide their own technical and professional incompetence**.

Such actions will trigger immediate, automated mirroring across decentralized filesystems and escalation of complaints directly to the European Data Protection Board (EDPB).

---

> [!NOTE]
> ### 🔒 ZERO-KNOWLEDGE PRIVACY GUARANTEE
> This tool runs **100% in your local sandbox** (either inside your browser or via local Python execution). 
> * No telemetry or tracking scripts.
> * Zero network requests are initiated during PDF parsing or sanitization.
> * Your sensitive files never leave your computer.
