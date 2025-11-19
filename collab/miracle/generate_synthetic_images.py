"""
Generate simple synthetic PNG visualizations for the sample medical cases.

This creates a small PNG for each `patient_id` in `MEDICAL_CASES` (from
`ingest_medical_data.py`) and saves them into `collab/miracle/generated_images/`.

Run:
    python generate_synthetic_images.py

"""
import os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import ast


# Safely extract MEDICAL_CASES from ingest_medical_data.py without importing
def load_medical_cases():
    src = Path(__file__).parent / "ingest_medical_data.py"
    text = src.read_text(encoding="utf-8")
    # Find the start of MEDICAL_CASES = [ and the matching closing bracket
    marker = "MEDICAL_CASES"
    idx = text.find(marker)
    if idx == -1:
        raise RuntimeError("Could not find MEDICAL_CASES in ingest_medical_data.py")

    # Find the '=' after marker and parse the following literal using ast
    eq_idx = text.find("=", idx)
    literal = text[eq_idx + 1 :]

    # Attempt to parse the first top-level literal (list/dict)
    try:
        node = ast.parse(literal, mode="eval")
        data = ast.literal_eval(node)
        return data
    except Exception:
        # Fallback: find the bracketed section manually
        start = text.find("[", eq_idx)
        if start == -1:
            raise
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


MEDICAL_CASES = load_medical_cases()


OUT_DIR = Path(__file__).parent / "generated_images"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def pattern_to_image(pattern: str, seed: int, size: int = 256) -> Image.Image:
    """Create a simple grayscale image representing the given pathology pattern.

    This is a visual placeholder — NOT a real clinical image. It uses blobs,
    radial gradients and noise to differentiate patterns.
    """
    rng = np.random.default_rng(seed)

    # Base canvas: gradient
    y = np.linspace(0, 1, size).reshape(size, 1)
    x = np.linspace(0, 1, size).reshape(1, size)
    canvas = 0.3 + 0.4 * (0.5 * (np.sin((x + y) * 6.0) + 1.0))

    # pattern-specific modifications
    if pattern == "normal":
        canvas += 0.05 * rng.normal(size=(size, size))
    elif pattern == "pneumonia":
        # bright diffuse patch on lower-right
        rr, cc = np.ogrid[:size, :size]
        mask = ((rr - size * 0.7) ** 2 + (cc - size * 0.65) ** 2) < (size * 0.32) ** 2
        canvas[mask] += 0.35 * rng.uniform(0.8, 1.0)
        canvas += 0.03 * rng.normal(size=(size, size))
    elif pattern == "fracture":
        # sharp high-contrast line
        for i in range(3):
            x0 = int(size * (0.2 + 0.6 * rng.random()))
            y0 = int(size * (0.1 + 0.8 * rng.random()))
            thickness = rng.integers(1, 4)
            rr = np.arange(size)
            cc = (x0 + (rr - y0) * rng.uniform(-0.05, 0.05)).astype(int)
            cc = np.clip(cc, 0, size - 1)
            canvas[rr, cc] += 0.6
    elif pattern == "tumor":
        # localized bright nodule with halo
        rr, cc = np.ogrid[:size, :size]
        cy = int(size * (0.45 + 0.1 * rng.random()))
        cx = int(size * (0.5 + 0.1 * rng.random()))
        r = int(size * 0.12)
        dist = ((rr - cy) ** 2 + (cc - cx) ** 2) ** 0.5
        canvas += 0.5 * np.exp(-(dist / r) ** 2)
    elif pattern == "edema":
        # diffuse mild brightening
        canvas += 0.15 * rng.uniform(0.8, 1.1)
    elif pattern == "effusion":
        # crescent bright area
        rr, cc = np.ogrid[:size, :size]
        mask = (cc > size * 0.55) & (rr > size * 0.5)
        canvas[mask] += 0.25
    elif pattern == "arthritis":
        # small high-frequency speckle
        canvas += 0.2 * rng.normal(scale=0.2, size=(size, size))
    else:
        canvas += 0.05 * rng.normal(size=(size, size))

    # Add global noise and clip
    canvas += 0.03 * rng.normal(size=(size, size))
    canvas = np.clip(canvas, 0.0, 1.0)

    # Convert to 8-bit image
    arr = (canvas * 255).astype(np.uint8)
    img = Image.fromarray(arr, mode="L")

    # Slight blur for realism
    img = img.filter(ImageFilter.GaussianBlur(radius=1.0))

    return img


def main():
    print("Generating synthetic images...")

    created = []
    for idx, case in enumerate(MEDICAL_CASES):
        pid = case.get("patient_id")
        pattern = case.get("pattern", "normal")
        filename = f"{pid}_{case['body_part'].lower()}.png"
        out_path = OUT_DIR / filename

        img = pattern_to_image(pattern=pattern, seed=1000 + idx, size=256)
        img.save(out_path)
        created.append(out_path)
        print(f"  ✓ {out_path.relative_to(Path.cwd())}")

    print(f"\nSaved {len(created)} images to: {OUT_DIR}")
    # Write a simple index file
    with open(OUT_DIR / "index.txt", "w", encoding="utf-8") as fh:
        for p in created:
            fh.write(str(p.name) + "\n")


if __name__ == "__main__":
    main()
