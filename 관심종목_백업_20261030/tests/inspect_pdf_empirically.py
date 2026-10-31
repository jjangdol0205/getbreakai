import os
import sys
import fitz  # PyMuPDF
import json

def inspect_pdf(pdf_path):
    print(f"\n=======================================================")
    print(f"Inspecting PDF: {pdf_path}")
    print(f"=======================================================")
    assert os.path.exists(pdf_path), f"File not found: {pdf_path}"
    
    # 1. File Size Check
    file_size = os.path.getsize(pdf_path)
    file_size_kb = file_size / 1024.0
    print(f"[1] File size: {file_size:,} bytes ({file_size_kb:.2f} KB)")
    assert file_size > 50 * 1024, f"File size {file_size_kb:.2f} KB <= 50 KB"
    print("    -> PASS: File size > 50 KB")

    # 2. Page Count Check
    doc = fitz.open(pdf_path)
    page_count = len(doc)
    print(f"[2] Page count: {page_count}")
    assert page_count == 3, f"Strict 3-page constraint violated: got {page_count} pages"
    print("    -> PASS: Exactly 3 pages (len(doc) == 3)")

    # 3. Page Geometry and Text Bounding Box Clipping Check (y1 <= 838.0 pt)
    print(f"[3] Page Geometry & Bottom Margin Clipping Check (Max y1 <= 838.0 pt):")
    all_fonts = set()
    for page_idx in range(page_count):
        page = doc[page_idx]
        rect = page.rect
        print(f"    Page {page_idx + 1} dimensions: {rect.width:.2f} x {rect.height:.2f} pt (A4 standard: 595.28 x 841.89 pt)")
        assert abs(rect.width - 595.28) <= 5.0, f"Page {page_idx + 1} width mismatch: {rect.width}"
        assert abs(rect.height - 841.89) <= 5.0, f"Page {page_idx + 1} height mismatch: {rect.height}"

        blocks = page.get_text("blocks")
        max_y1 = 0.0
        lowest_block = None
        for b in blocks:
            x0, y0, x1, y1, text, block_no, block_type = b
            if block_type == 0:  # text block
                if y1 > max_y1:
                    max_y1 = y1
                    lowest_block = (x0, y0, x1, y1, text.strip().replace('\n', ' '))
                assert y1 <= 838.0, f"Clipping detected on Page {page_idx + 1}: block y1={y1:.2f} > 838.0 pt! Text: {text[:50]}"
        
        print(f"    Page {page_idx + 1} Max y1: {max_y1:.2f} pt (Margin to 838.0 pt: {838.0 - max_y1:.2f} pt, Margin to page end: {rect.height - max_y1:.2f} pt)")
        if lowest_block:
            print(f"    Page {page_idx + 1} Lowest block snippet: [{lowest_block[4][:60]}...]")
        print(f"    -> PASS: Page {page_idx + 1} zero clipping verified.")

    # 4. Font Inspection
    print(f"\n[4] Font Inspection across all pages:")
    for page_idx in range(page_count):
        page = doc[page_idx]
        page_fonts = page.get_fonts(full=True)
        print(f"    Page {page_idx + 1} embedded fonts count: {len(page_fonts)}")
        for f in page_fonts:
            # f: (xref, ext, type, basefont, name, encoding, ...)
            all_fonts.add((f[2], f[3]))
            print(f"       - Font type: {f[2]}, name: {f[3]}")
            
        # Also inspect fonts in text spans
        text_dict = page.get_text("dict")
        span_fonts = set()
        for block in text_dict.get("blocks", []):
            if block.get("type") == 0:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        f_name = span.get("font", "")
                        if f_name:
                            span_fonts.add(f_name)
        print(f"    Page {page_idx + 1} span fonts: {sorted(list(span_fonts))}")

    # 5. Non-inline Text Overlap Inspection
    print(f"\n[5] Non-inline Text Overlap Inspection:")
    for page_idx in range(page_count):
        page = doc[page_idx]
        text_dict = page.get_text("dict")
        # Gather all text spans with their bbox and text
        spans = []
        for block in text_dict.get("blocks", []):
            if block.get("type") == 0:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if text:
                            spans.append({
                                "bbox": span["bbox"],
                                "text": text,
                                "size": span.get("size", 0),
                                "flags": span.get("flags", 0)
                            })
        
        # Check span overlaps
        overlaps = []
        for i in range(len(spans)):
            b1 = spans[i]["bbox"]
            for j in range(i + 1, len(spans)):
                b2 = spans[j]["bbox"]
                # Calculate intersection
                ix0 = max(b1[0], b2[0])
                iy0 = max(b1[1], b2[1])
                ix1 = min(b1[2], b2[2])
                iy1 = min(b1[3], b2[3])
                
                # Check if there is a significant intersection (not just touching edges)
                if ix1 - ix0 > 2.0 and iy1 - iy0 > 2.0:
                    area = (ix1 - ix0) * (iy1 - iy0)
                    overlaps.append((spans[i], spans[j], area))
                    
        print(f"    Page {page_idx + 1}: Total text spans = {len(spans)}, Significant overlaps = {len(overlaps)}")
        if overlaps:
            print(f"    WARNING: Overlaps found on Page {page_idx + 1}:")
            for s1, s2, area in overlaps[:5]:
                print(f"       Overlap area {area:.2f}: '{s1['text']}' @ {s1['bbox']} vs '{s2['text']}' @ {s2['bbox']}")
        else:
            print(f"    -> PASS: Zero text span overlaps on Page {page_idx + 1}!")

    # 6. Render pages to PNG at 150 DPI
    print(f"\n[6] Rendering pages to PNG at 150 DPI:")
    zoom = 150.0 / 72.0  # 150 DPI
    mat = fitz.Matrix(zoom, zoom)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_pngs = []
    for page_idx in range(page_count):
        page = doc[page_idx]
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_png = os.path.join(os.path.dirname(pdf_path), f"{base_name}_page_{page_idx + 1}_150dpi.png")
        pix.save(out_png)
        print(f"    Saved: {out_png} ({pix.width}x{pix.height} px, {os.path.getsize(out_png):,} bytes)")
        output_pngs.append(out_png)

    doc.close()
    return {
        "file_size": file_size,
        "page_count": page_count,
        "output_pngs": output_pngs
    }

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p1 = os.path.join(base_dir, "daily_pdf", "Latest_Morning_Alpha_Briefing.pdf")
    p2 = os.path.join(base_dir, "daily_pdf", "2026-10-16_Morning_Alpha_Briefing.pdf")
    
    res1 = inspect_pdf(p1)
    res2 = inspect_pdf(p2)
    print("\nALL PDF INSPECTIONS COMPLETED SUCCESSFULLY!")
