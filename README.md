# PDF Redaction Auditor & Sanitizer Suite
### Powered by PhishDestroy Threat Intelligence Division

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Local Sandbox Only](https://img.shields.io/badge/Privacy-100%25_Local-green.svg)](#privacy--zero-knowledge-guarantee)
[![Offline Ready](https://img.shields.io/badge/Offline-Enabled-success.svg)](#running-completely-offline)

A professional, zero-knowledge, client-side cybersecurity utility designed to audit PDF document structures, analyze metadata signatures, detect insecure "visual-only" redactions, and safely sanitize compromised documents.

---

## 🔍 Core Context: The Valve Investigation & The Tragic "DIY" Redaction Comedy

This suite is a core forensic component of the larger **PhishDestroy Threat Intelligence Investigation** into Valve Corporation's systemic profiteering from cybercrime. We officially contacted Dr. Patrick (DPO/Partner) at Taylor Wessing LLP regarding this catastrophic leak. Their response confirmed that the firm is completely inadequate and has absolutely no intention of notifying affected data subjects or warning the public. Therefore, the global community must proactively audit and sanitize their own files immediately. We highly advise against contacting or doing business with these clowns who are systematically unable to redact basic PDFs.

### 📚 Official Investigative Writeups & Writeups:
* **📖 Full Investigation:** [Valve Profits from Stolen Accounts](https://phishdestroy.io/valve-profits-from-stolen-accounts)
* **📖 Part 1 (Medium):** [My Dog vs. Elite GDPR Lawyers: The Valve Data Breach Nobody is Talking About](https://phishdestroy.medium.com/my-dog-vs-elite-gdpr-lawyers-the-valve-data-breach-nobody-is-talking-about-f6f7683d813d)
* **📖 Part 2 (Medium):** [My Dog vs. Elite Lawyers Part 2: The 5-Year PDF Vulnerability Exposing Global Corporations](https://phishdestroy.medium.com/my-dog-vs-elite-lawyers-part-2-the-5-year-pdf-vulnerability-exposing-global-corporations-81cdad269253)

### The Incompetence Timeline
In an attempt to comply with EU GDPR Article 15 Subject Access Requests regarding stolen user account data, Valve Corporation's elite, high-priced external counsel—**Taylor Wessing LLP**—systematically leaked thousands of private records belonging to third-party Steam users.

This catastrophic, massive data breach did not happen due to an external hack, but due to severe technical incompetence and corporate "DIY" software engineering:
* **"DIY" Software Hubris:** Rather than purchasing standard, industry-certified, secure PDF redaction software (such as Adobe Acrobat Pro Redaction Tools), Taylor Wessing LLP's developers and lawyers decided to build their own custom, automated, in-house script using *Aspose.PDF for .NET*.
* **Visual Cover-ups Only:** Their "DIY" tool made a hilarious, amateur blunder: it merely programmatically searched the coordinates of sensitive fields and drew a **solid black vector rectangle** (using PDF's `re` and `f`/`F`/`b`/`B` operators) right on top of the text, thinking that visually covering the text was equivalent to deleting it.
* **The Tragic Trifle:** They completely forgot that visual overlays do **not** destroy the underlying character streams in the PDF's content. As a result, 100% of the redacted Personally Identifiable Information (PII) remained copyable and extractable.

---

## 🛠️ Features

- **Smart Offline-First Web GUI (`index.html`)**: Beautiful, responsive, dark-themed dashboard. Dual loading system searches for local library files (`lib/`) to enable 100% internet-free offline auditing, falling back to secure CDNs if not found.
- **Precision Text Overlay**: Automatically extracts text coordinates and aligns searchable transparent text nodes exactly over the PDF canvas, allowing instant visual verification of what lies underneath visual shapes.
- **Local Python CLI Tool (`decensor.py`)**: Robust forensic script utilizing PyMuPDF with interactive colorful logs and advanced optimization capabilities.
- **Dual Sanitization Strategies**:
  1. **Content Stream Operation Swap (`stream` method)**: Surgical search-and-replace that swaps rectangular visual fill operators (`re f`, `re F`, `re b`, `re B`, etc.) with no-fill operators (`re n`). Exposes text visually while maintaining perfect structural alignment.
  2. **Whiteout Cover-up (`overlay` method)**: Fallback method that identifies visual "black" vector paths and draws white vector blocks on top of them.
- **GDPR Breach Notification Generator**: Generates formal data breach notification drafts addressed to data controller DPOs (such as Taylor Wessing LLP) and regulatory authorities (such as the HmbBfDI).

---

## 📁 Repository Structure

```text
├── lib/                             # Vendored offline JS libraries
│   ├── pdf.min.js                   # PDF.js core library
│   ├── pdf.worker.min.js            # PDF.js worker script
│   └── pdf-lib.min.js               # Client-side PDF modification library
├── decensor.py                      # Forensic Python CLI Auditor & Sanitizer
├── index.html                       # Fully responsive, standalone Web GUI dashboard
├── LICENSE                          # MIT License
└── README.md                        # Documentation and code walkthrough
```

---

## 🚀 Running Completely Offline

This suite is engineered for complete privacy. You can audit and sanitize extremely sensitive PDFs **without an internet connection**:

1. **Clone or Download** this repository.
2. Ensure the `lib/` directory is present containing the vendored JS assets.
3. Open `index.html` directly in any web browser by double-clicking it (or running `python -m http.server 8000` inside the directory).
4. Since the loader is offline-first, it will load `pdf.min.js` and `pdf-lib.min.js` from the local `./lib/` folder. No remote connections will be established, guaranteeing absolute privacy.

---

## 🌐 Deployment to GitHub Pages (Hosting)

This application is 100% static and ready to be hosted as a **GitHub Page** with zero build configuration:

1. Push this repository to your public or private GitHub repository.
2. Navigate to your repository's **Settings** -> **Pages**.
3. Under **Build and deployment**, set **Source** to `Deploy from a branch`.
4. Select your branch (e.g., `main`) and folder (`/` root), then click **Save**.
5. GitHub will instantly build and host your audit suite. Because the `./lib/` folder is committed to the repository, your GitHub Page will execute all PDF processing and decensoring completely on the user's local browser sandbox with **zero server interaction**.

---

## 💻 Python CLI Tool (`decensor.py`)

### Requirements
- Python 3.x
- PyMuPDF library (`pip install pymupdf`)

### Usage

```bash
# Display help and options
python decensor.py --help

# Sanitize a PDF using the default surgical content stream method
python decensor.py -i compromised.pdf -o unmasked.pdf

# Sanitize using drawing-level overlays (visual cover-up fallback)
python decensor.py -i compromised.pdf -o unmasked.pdf -m overlay

# Apply BOTH stream-level neutralization and overlay-level cover-up
python decensor.py -i compromised.pdf -o unmasked.pdf -m both
```

### Key Arguments
* `-i`, `--input`: **[Required]** Path to the compromised PDF.
* `-o`, `--output`: Destination path for sanitized PDF (Defaults to `<input>_unmasked.pdf`).
* `-m`, `--method`: Sanitization method, choose from:
  * `stream` (Default): Swap raw fill operators in decompressed streams with `n` (no-fill).
  * `overlay`: Overdraw detected black vector lines with white vector rectangles.
  * `both`: Run stream replacement first, then overlay coverups.
* `-t`, `--threshold`: RGB channel upper threshold (0.0 to 1.0) to classify "black" paths in overlay mode (Default: `0.1`).

---
⚠️ Why This Tool Exists: The Taylor Wessing / Valve Case Study
To understand the devastating scale of this vulnerability, look no further than elite corporate law firms.

In October 2023, the IT-law division of Taylor Wessing LLP, acting for Valve Corporation (Steam), responded to a GDPR Article 15 request. Instead of properly sanitizing the document, they used outdated software (Aspose.PDF 20.8) to apply visual black boxes over 830 pages of highly sensitive PII. Thousands of de-anonymized Steam logins, emails, and third-party chat logs of minors were fully exposed.

The Catalyst for This Release:
When the PhishDestroy Intelligence Division formally notified Taylor Wessing of this catastrophic data breach (complete with forensic metadata and evidence of their technical failure), their lead lawyer, Dr. Patrick Zurheide, chose a deeply concerning response strategy.

Instead of an adequate, professional acknowledgment or immediate GDPR containment, Dr. Zurheide decided to play arrogant legal word games. He feigned ignorance, attempted to dismiss the technical reality as "entertaining," and implicitly threatened the researchers.

This response made one thing crystal clear: Taylor Wessing and its IT-law "Doctors" operate under the delusion that they are the law, the judge, and the jury. They have consciously chosen to ignore a massive technical vulnerability in favor of corporate cover-ups and intimidation tactics.

Because we do not intend to waste time communicating with inadequate legal clowns who prioritize their egos over the safety of minor EU citizens, we are releasing this tool to the public.

There is a high probability that Taylor Wessing has been dispatching similarly compromised documents for years across their entire corporate client portfolio. Since they refuse to audit themselves, we are giving the public the power to audit them.

If elite lawyers billing hundreds of euros an hour can make this mistake, anyone can. This tool was built to ensure journalists, regulators, and individuals can audit the files they receive—or files they intend to send—to prevent similar data disasters.

---
⚠️ The Hypocrisy of "Elite IT Law" (Why We Chose GitHub)
Everywhere you look, Taylor Wessing LLP loudly markets itself as a pioneer in "IT Law" and a premier cybersecurity counsel for global tech mega-corporations.

Yet, behind this elite and highly expensive facade, the reality is deeply alarming. They are cutting corners and cheaping out on basic IT infrastructure, relying on severely outdated, flawed software (Aspose.PDF 20.8 from October 2025?) to process highly sensitive GDPR data.

When the PhishDestroy Intelligence Division confronted their lead IT-lawyer, Dr. Patrick Zurheide, with undeniable forensic proof that their cheap software caused a massive data breach—leaking the de-anonymized Steam logins and chat logs of minors—he didn't initiate a security protocol. Instead, he chose to play arrogant word games and literally mocked the situation as "entertaining".

We find this combination of extreme technical negligence and arrogant dismissal of a data breach deeply disturbing.

Because Taylor Wessing’s primary clients—and their legal opponents—operate directly in the tech and IT spheres, we believe GitHub is the absolute most appropriate place to host this open-source multi-tool.

We are deploying this auditing utility directly to the global IT community. If a law firm claiming to specialize in "IT Law" thinks data breaches are a joke, then every developer, tech company, and security researcher must have the tools to independently audit the "elite" documents they receive from them.

---
## 📝 Core Implementation Walkthrough

### 1. Python Stream-Level Operator Swapping
The core script uses PyMuPDF's low-level stream reading interfaces. It parses the decompressed cross-reference (`xref`) stream of each page, applies a whitespace-preserving regular expression to swap visual fill operators with a non-painting operator, and reconstructs the PDF stream with full garbage collection and stream deflation.

```python
import re, fitz

def strip_black_bars(input_path, output_path):
    # Open the compromised document offline
    doc = fitz.open(input_path)
    
    for page in doc:
        # Iterate through each drawing content stream on the page
        for stream_id in page.get_contents():
            stream_data = doc.xref_stream(stream_id)
            # Decode in Latin-1 to safely preserve any binary stream markers
            text = stream_data.decode('latin-1')
            
            # Locate rect drawing "re" followed by fill/stroke operator (f/F/b/B)
            # and swap with "n" (new path / no-fill). Preserves exact spacing/newlines!
            modified_text, count = re.subn(
                r'\bre\s+([fFbB]\*?)(?=\s|$)',
                lambda m: f"re{m.group(0)[2:-len(m.group(1))]}n",
                text
            )
            
            if count > 0:
                doc.update_stream(stream_id, modified_text.encode('latin-1'))
                
    # Save output with stream deflation and structural optimization
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()
```

### 2. Browser Client-Side JS Operator Swapping
The Web GUI performs the identical structural modifications in-memory using `pdf-lib`. It parses the local file into a byte array, traverses page content streams, performs the regex swap, and serializes the modified PDF, triggering a download for the sanitized file instantly.

```javascript
async function sanitizePdfClientSide(rawPdfBytes) {
    // Load document from local byte array into pdf-lib
    const { PDFDocument } = PDFLib;
    const pdfDocInstance = await PDFDocument.load(rawPdfBytes);
    const pages = pdfDocInstance.getPages();
    
    for (let page of pages) {
        const contentStreams = page.getContentStreams();
        
        for (let contentStream of contentStreams) {
            const rawData = contentStream.getContents();
            // Decompress and decode stream to UTF-8 text
            const text = new TextDecoder('utf-8').decode(rawData);
            
            // Match "re" drawing rect followed by fill/stroke operator (f/F/b/B)
            // and swap with "n" (no-fill), preserving original spacing/newlines
            const modifiedText = text.replace(/re(\s+)([fFbB]\*?)(?=\s|$)/g, 're$1n');
            
            if (text !== modifiedText) {
                const modifiedData = new TextEncoder('utf-8').encode(modifiedText);
                contentStream.setContents(modifiedData);
            }
        }
    }
    // Recompress stream structures and regenerate cross-reference offsets
    return await pdfDocInstance.save();
}
```

---

## 🔒 Privacy & Zero-Knowledge Guarantee

This tool operates on a **strict zero-knowledge privacy model**:
1. No telemetry or usage statistics are gathered.
2. No network requests are initiated during PDF parsing or sanitization.
3. Your documents are never uploaded to any remote endpoints. 
4. All client-side code is open-source and displayed right on the GUI welcome dashboard for immediate auditing.

---

## ⚖️ Legal & Compliance Advisory

Exposed Personally Identifiable Information (PII) of third parties contained within improperly redacted files is strictly protected under global data protection acts:
- **GDPR (European Union)**: Processing or exploiting unsecured text layers from redacted public documents violates the purpose limitation and data minimization principles.
- **Article 33 GDPR**: If you represent an organization that has accidentally distributed visually-only redacted PDFs, you must report the event as a Personal Data Breach to your competent supervisory authority within **72 hours** of detection.
- Use the built-in **Breach Notification Draft Generator** to immediately notify DPOs or file formal complaints with supervisory bodies.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
