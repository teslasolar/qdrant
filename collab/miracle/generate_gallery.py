"""
Generate a simple HTML gallery for the synthetic images and their metadata.

Run:
    python generate_gallery.py

This script reads `MEDICAL_CASES` from `ingest_medical_data.py` (safely),
and writes `generated_images/gallery.html` which shows thumbnails and metadata.
"""
from pathlib import Path
import html
import ast


ROOT = Path(__file__).parent
OUT_DIR = ROOT / "generated_images"
OUT_FILE = OUT_DIR / "gallery.html"


def load_medical_cases():
    src = ROOT / "ingest_medical_data.py"
    text = src.read_text(encoding="utf-8")
    marker = "MEDICAL_CASES"
    idx = text.find(marker)
    if idx == -1:
        raise RuntimeError("Could not find MEDICAL_CASES in ingest_medical_data.py")
    eq_idx = text.find("=", idx)
    literal = text[eq_idx + 1 :]
    try:
        node = ast.parse(literal, mode="eval")
        data = ast.literal_eval(node)
        return data
    except Exception:
        start = text.find("[", eq_idx)
        depth = 0
        end = start
        for i, ch in enumerate(text[start:], start):
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        literal = text[start:end]
        return ast.literal_eval(literal)


def make_gallery(cases):
    rows = []
    for case in cases:
        pid = case.get("patient_id")
        bp = case.get("body_part", "unknown").lower()
        png_name = f"{pid}_{bp}.png"
        img_path = png_name if (OUT_DIR / png_name).exists() else None

        meta_lines = []
        for k in ("diagnosis", "modality", "age", "sex", "notes"):
            if k in case:
                meta_lines.append(f"<strong>{html.escape(k)}:</strong> {html.escape(str(case[k]))}")

        meta_html = "<br>".join(meta_lines)

        if img_path:
            img_tag = f'<img src="{html.escape(img_path)}" alt="{pid}" width="240">'
        else:
            img_tag = '<div style="width:240px;height:180px;background:#ddd;display:flex;align-items:center;justify-content:center">No image</div>'

        rows.append(f"<div class=card>{img_tag}<div class=meta><h3>{html.escape(pid)}</h3>{meta_html}</div></div>")

    html_doc = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Medical Images - Gallery</title>
  <style>
    body{font-family:Arial;background:#f6f6f6;padding:20px}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
    .card{background:#fff;padding:8px;border-radius:6px;box-shadow:0 1px 3px rgba(0,0,0,0.08)}
    .card img{display:block;margin:0 auto}
    .meta{padding:6px 4px}
    .meta h3{margin:0 0 6px 0;font-size:16px}
  </style>
</head>
<body>
  <h1>Medical Images (Synthetic)</h1>
  <p>These images are generated placeholders mapped to the sample cases.</p>
  <div class="grid">
    %s
  </div>
</body>
</html>
""" % ("\n    ".join(rows))

    OUT_FILE.write_text(html_doc, encoding="utf-8")
    print(f"Wrote gallery: {OUT_FILE}")


if __name__ == "__main__":
    cases = load_medical_cases()
    make_gallery(cases)
