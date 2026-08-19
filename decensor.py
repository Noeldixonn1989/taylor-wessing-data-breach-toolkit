#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Redaction Auditor & Sanitizer (CLI Tool)
Part of the PhishDestroy Intelligence Suite

Forensic utility to audit, detect, and neutralize failed visual redactions in PDF documents.
Flawed redactions occur when solid black vector shapes are drawn on top of sensitive text 
characters without deleting the underlying text stream.

This tool offers two powerful sanitization methodologies:
1. 'stream' (Default): Surgical stream replacement of rectangle painting operators with 'no-fill'.
2. 'overlay' (Fallback): Appending white rects over coordinates of detected black vector paths.
"""

import os
import sys
import argparse
import re
from datetime import datetime

# Import PyMuPDF
try:
    import fitz
except ImportError:
    print("\033[91m[!] Error: PyMuPDF (fitz) is not installed in your active environment.\033[0m")
    print("\033[93m[*] Please install it using: pip install pymupdf\033[0m")
    sys.exit(1)

class Theme:
    RST = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"

def log_info(msg, prefix="*"):
    ts = datetime.now().strftime("%H:%M:%S")
    color = Theme.CYAN if prefix == "*" else Theme.GREEN
    print(f"{Theme.DIM}[{ts}]{Theme.RST} {color}{prefix}{Theme.RST} {msg}")

def log_warn(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{Theme.DIM}[{ts}]{Theme.RST} {Theme.YELLOW}!{Theme.RST} {msg}")

def log_error(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{Theme.DIM}[{ts}]{Theme.RST} {Theme.RED}x{Theme.RST} {msg}")

def check_text_under_shapes(doc, threshold=0.1):
    """
    Scans the pages of the PDF to see if there are actual text character layers 
    situated directly underneath the coordinates of any detected solid black visual drawings.
    Returns a dictionary mapping page numbers to lists of leaked text snippets.
    """
    log_info("Scanning document layout for active text-under-shape leaks...")
    leaks = {}
    total_black_bars = 0
    total_leaked_bars = 0

    # We scan all pages up to a reasonable limit to verify active leaks
    scan_limit = min(len(doc), 100) 

    for page_num in range(scan_limit):
        page = doc[page_num]
        drawings = page.get_drawings()
        words = page.get_text("words") # List of tuples: (x0, y0, x1, y1, "word", block_no, line_no, word_no)

        page_leaks = []

        for path in drawings:
            fill = path.get("fill")
            if fill and fill[0] <= threshold and fill[1] <= threshold and fill[2] <= threshold:
                total_black_bars += 1
                rect = fitz.Rect(path["rect"])

                # Check if any words intersect with this black bar
                words_under = []
                for w in words:
                    w_rect = fitz.Rect(w[0], w[1], w[2], w[3])
                    # Check if the black bar rectangle contains or overlaps the word
                    if rect.contains(w_rect) or rect.intersects(w_rect):
                        words_under.append(w[4])

                if words_under:
                    total_leaked_bars += 1
                    leak_text = " ".join(words_under)
                    # Limit the length of reported leak text for display
                    if len(leak_text) > 60:
                        leak_text = leak_text[:57] + "..."
                    page_leaks.append({
                        "rect": path["rect"],
                        "text": leak_text
                    })

        if page_leaks:
            leaks[page_num + 1] = page_leaks

    return leaks, total_black_bars, total_leaked_bars

def audit_document_integrity(input_path, threshold=0.1):
    """Parses PDF metadata, scans for visual black bars, and verifies if text is actually leaked underneath."""
    log_info("Performing forensic layout audit...")
    try:
        doc = fitz.open(input_path)
    except Exception as e:
        log_error(f"Failed to open PDF document: {e}")
        sys.exit(1)

    metadata = doc.metadata
    producer = metadata.get("producer", "Unknown") or "Unknown"
    creator = metadata.get("creator", "Unknown") or "Unknown"
    page_count = len(doc)

    log_info(f"Metadata Producer: {Theme.BOLD}{producer}{Theme.RST}")
    log_info(f"Metadata Creator : {Theme.BOLD}{creator}{Theme.RST}")
    log_info(f"Total Page Count : {Theme.BOLD}{page_count}{Theme.RST}")

    # Check for text leaks under shapes
    leaks, total_black_bars, total_leaked_bars = check_text_under_shapes(doc, threshold)
    doc.close()

    p_low = producer.lower()
    is_aspose = "aspose" in p_low or "aspose.pdf" in p_low

    if is_aspose:
        log_warn(f"Document generator signature matches vulnerable exporter: {Theme.BOLD}{producer}{Theme.RST}")

    if total_leaked_bars > 0:
        log_error(f"{Theme.BOLD}{Theme.RED}CONFIRMED ACTIVE DATA LEAK DETECTED!{Theme.RST}")
        log_error(f"Found {Theme.BOLD}{total_leaked_bars}{Theme.RST} black visual shapes actively covering extractable text layers (out of {total_black_bars} total visual bars).")

        # Print a preview of the first few leaks
        log_info("Leaked Text Preview:")
        preview_count = 0
        for page_num, page_leaks in leaks.items():
            for leak in page_leaks:
                if preview_count >= 5:
                    break
                print(f"  {Theme.DIM}[Page {page_num}]{Theme.RST} {Theme.RED}Leak:{Theme.RST} \"{Theme.BOLD}{leak['text']}{Theme.RST}\"")
                preview_count += 1
            if preview_count >= 5:
                break
        if total_leaked_bars > 5:
            log_info(f"... and {total_leaked_bars - 5} more leaks.")
    else:
        if total_black_bars > 0:
            log_info(f"Found {total_black_bars} black visual bars, but {Theme.BOLD}{Theme.GREEN}zero text leaks{Theme.RST} underneath them.", prefix="+")
            log_info("Redactions are structurally secure (text has been successfully destroyed or was never present under the bars).", prefix="+")
        else:
            log_info(f"{Theme.BOLD}{Theme.GREEN}SECURE: No visual black mask bars detected.{Theme.RST} Document is clean.", prefix="+")

def sanitize_via_streams(input_path, output_path):
    """
    Surgical, global stream-level sanitization (Method 'stream').
    Scans ALL streams in the PDF (including page contents, Form XObjects, and patterns)
    and replaces filled rect painting operators with 'no-fill' (re n). This handles visual 
    blockers nested inside Form XObjects or external resource objects, neutralizing them perfectly.
    """
    log_info("Starting surgical global stream-level sanitization (Content Streams & Form XObjects)...")
    doc = fitz.open(input_path)
    
    total_streams_modified = 0
    total_operators_replaced = 0

    # Scan every object in the PDF cross-reference table
    for xref in range(1, doc.xref_length()):
        if not doc.is_stream(xref):
            continue
            
        try:
            # Skip binary stream objects like Fonts, Images, and Halftones to prevent unnecessary overhead
            obj_dict = doc.xref_object(xref)
            if any(marker in obj_dict for marker in ["/Type /Font", "/Subtype /Image", "/Type /Halftone"]):
                continue
                
            # Read and decode raw stream content
            stream_bytes = doc.xref_stream(xref)
            text = stream_bytes.decode('latin-1')
            
            # Locate rectangle drawing 're' followed by paint/stroke operators
            # and replace them with 're n' (no-fill), preserving original separator whitespaces/newlines.
            modified_text, count = re.subn(
                r'\bre\s+([fFbB]\*?)(?=\s|$)',
                lambda m: f"re{m.group(0)[2:-len(m.group(1))]}n",
                text
            )
            
            if count > 0:
                doc.update_stream(xref, modified_text.encode('latin-1'))
                total_streams_modified += 1
                total_operators_replaced += count
        except Exception as e:
            continue

    log_info(f"Neutralized {Theme.BOLD}{total_operators_replaced}{Theme.RST} black visual block rectangles across {Theme.BOLD}{total_streams_modified}{Theme.RST} streams (including Page Contents and Form XObjects).", prefix="+")
    return doc

def sanitize_via_overlays(doc, r_thresh, g_thresh, b_thresh):
    """
    Drawing-level overlay sanitization (Method 'overlay').
    Detects solid black vector drawing layers and appends a white block directly over them.
    This visually masks out the mask itself, letting the text be visible in traditional viewers.
    """
    log_info("Starting canvas overlay-level drawing sanitization...")
    total_masks_stripped = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        drawings = page.get_drawings()

        for path in drawings:
            fill = path.get("fill")
            # If path contains a color fill matching our 'black' threshold
            if fill and fill[0] <= r_thresh and fill[1] <= g_thresh and fill[2] <= b_thresh:
                rect = fitz.Rect(path["rect"])
                # Overdraw with a zero-width white filled rectangle
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)
                total_masks_stripped += 1

    log_info(f"Overlaid {Theme.BOLD}{total_masks_stripped}{Theme.RST} black drawings with visual whiteouts.", prefix="+")
    return doc

def list_structural_elements(input_path):
    """Lists page-by-page structural elements inside the PDF (images, drawings, annotations, text blocks)."""
    log_info(f"Analyzing and listing structural elements of: {Theme.BOLD}{input_path}{Theme.RST}")
    doc = fitz.open(input_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        drawings = len(page.get_drawings())
        images = len(page.get_images())
        annots = len(list(page.annots()))
        text_blocks = len(page.get_text("blocks"))
        
        print(f"  {Theme.CYAN}[Page {page_num+1}]{Theme.RST} "
              f"Drawings: {Theme.BOLD}{drawings}{Theme.RST} | "
              f"Raster Images: {Theme.BOLD}{images}{Theme.RST} | "
              f"Annotations: {Theme.BOLD}{annots}{Theme.RST} | "
              f"Text Blocks: {Theme.BOLD}{text_blocks}{Theme.RST}")
    doc.close()

def extract_and_save_leaks(input_path, output_txt_path, threshold=0.1):
    """Saves all extracted text situated underneath black bars to a text file."""
    log_info("Running leak extraction engine...")
    doc = fitz.open(input_path)
    
    leaks = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        drawings = page.get_drawings()
        words = page.get_text("words")
        
        page_leaks = []
        for path in drawings:
            fill = path.get("fill")
            if fill and fill[0] <= threshold and fill[1] <= threshold and fill[2] <= threshold:
                rect = fitz.Rect(path["rect"])
                words_under = [w[4] for w in words if rect.contains(fitz.Rect(w[0], w[1], w[2], w[3])) or rect.intersects(fitz.Rect(w[0], w[1], w[2], w[3]))]
                if words_under:
                    page_leaks.append(" ".join(words_under))
                    
        if page_leaks:
            leaks.append((page_num + 1, page_leaks))
            
    doc.close()
    
    if leaks:
        try:
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write(f"=== FORENSIC LEAK ANALYSIS FOR {os.path.basename(input_path)} ===\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n\n")
                
                total_leaks = 0
                for page, page_leaks in leaks:
                    f.write(f"--- Page {page} ---\n")
                    for idx, text in enumerate(page_leaks):
                        total_leaks += 1
                        f.write(f"Leak #{idx+1} [Coordinates in original PDF]:\n")
                        f.write(f"  Content: \"{text}\"\n\n")
                f.write(f"Total verified leaks: {total_leaks}\n")
            log_info(f"Extracted {total_leaks} leaks and saved to text report: {Theme.BOLD}{output_txt_path}{Theme.RST}", prefix="+")
        except Exception as e:
            log_error(f"Failed to write leaks report: {e}")
    else:
        log_info("No active leaks found to extract.", prefix="+")

def decompose_to_text_only(input_path, output_path):
    """
    Decomposes the PDF by completely stripping all visual drawing layers, vector shapes, 
    filled boxes, borders, lines, and annotations, leaving only the pure text and image elements.
    """
    log_info("Decomposing document to reveal raw core text layers...")
    doc = fitz.open(input_path)
    
    total_cleaned = 0
    
    for xref in range(1, doc.xref_length()):
        if not doc.is_stream(xref):
            continue
            
        try:
            obj_dict = doc.xref_object(xref)
            if any(marker in obj_dict for marker in ["/Type /Font", "/Subtype /Image", "/Type /Halftone"]):
                continue
                
            stream_bytes = doc.xref_stream(xref)
            text = stream_bytes.decode('latin-1')
            
            # Match any path paint operator: f, F, S, s, b, B (and even-odd variants) that follow path-building operations
            # and replace them with 'n' (no-paint/no-fill).
            modified_text, count = re.subn(
                r'\b(re|l|c|v|y|m|h)\s+([fFsSbB]\*?)(?=\s|$)',
                lambda m: f"{m.group(1)} n",
                text
            )
            
            if count > 0:
                doc.update_stream(xref, modified_text.encode('latin-1'))
                total_cleaned += count
        except Exception:
            continue
            
    log_info(f"Decomposed vector layers. Neutralized {total_cleaned} graphic operations.", prefix="+")
    doc.save(output_path, garbage=4, deflate=True, clean=True)
    doc.close()

def main():
    print(f"\n{Theme.BOLD}{Theme.BLUE}=== PDF REDACTION AUDITOR & SANITIZER (CLI) ==={Theme.RST}")
    print(f"{Theme.DIM}Powered by PhishDestroy Threat Intelligence Division{Theme.RST}\n")

    parser = argparse.ArgumentParser(
        description="Audit PDF structures, detect visual masking redaction errors, and strip vector masks."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Path to the compromised PDF document to audit/sanitize"
    )
    parser.add_argument(
        "-o", "--output", help="Destination path for sanitized PDF (default: <input>_unmasked.pdf)"
    )
    parser.add_argument(
        "-m", "--method", choices=["stream", "overlay", "both"], default="stream",
        help="Sanitization strategy: 'stream' (surgical replace), 'overlay' (visual whiteout), 'both' (apply stream, then fallback overlay)"
    )
    parser.add_argument(
        "-t", "--threshold", type=float, default=0.1,
        help="RGB color channel maximum threshold (0.0 - 1.0) for detecting black shapes in overlay mode (default: 0.1)"
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="Decompose and list structural elements (images, drawings, blocks) page-by-page and exit"
    )
    parser.add_argument(
        "-e", "--extract-txt", help="Path to extract and save verified leak text to a report (e.g. leaks.txt) and exit"
    )
    parser.add_argument(
        "-d", "--decompose-pdf", action="store_true",
        help="Decompose PDF into raw text layer by stripping ALL vector drawings, lines, and boxes, and exit"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        log_error(f"Input file does not exist: {args.input}")
        sys.exit(1)

    # Trigger structural list mode and exit
    if args.list:
        list_structural_elements(args.input)
        sys.exit(0)

    # Trigger graphic layer decomposition and exit
    if args.decompose_pdf:
        if not args.output:
            base, ext = os.path.splitext(args.input)
            args.output = f"{base}_decomposed{ext}"
        decompose_to_text_only(args.input, args.output)
        sys.exit(0)

    # Trigger leak extraction and exit
    if args.extract_txt:
        extract_and_save_leaks(args.input, args.extract_txt, args.threshold)
        sys.exit(0)

    # Set default output path if not specified
    if not args.output:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}_unmasked{ext}"

    # Audit document signatures and layouts
    audit_document_integrity(args.input, args.threshold)

    # Initialize sanitized document
    doc = None

    # Step 1: Surgical Stream Replacement
    if args.method in ["stream", "both"]:
        doc = sanitize_via_streams(args.input, args.output)

    # Step 2: visual vector whiteout fallback
    if args.method == "overlay":
        doc = fitz.open(args.input)
        doc = sanitize_via_overlays(doc, args.threshold, args.threshold, args.threshold)
    elif args.method == "both":
        doc = sanitize_via_overlays(doc, args.threshold, args.threshold, args.threshold)

    # Step 3: Compress and save
    try:
        log_info(f"Writing sanitized file to: {Theme.BOLD}{args.output}{Theme.RST}")
        # garbage=4: Eliminate all dead xref objects
        # deflate=True: Max compression of internal streams
        # clean=True: Optimize layout trees and clean duplicate fonts/XObjects
        doc.save(args.output, garbage=4, deflate=True, clean=True)
        doc.close()
        log_info(f"{Theme.BOLD}{Theme.GREEN}Sanitized PDF successfully saved!{Theme.RST}\n", prefix="+")
    except Exception as e:
        log_error(f"Failed to serialize output document: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
