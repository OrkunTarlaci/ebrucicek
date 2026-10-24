#!/usr/bin/env python3
"""Bir çiçek fotoğrafını siteye ekler: kare kırpar, 480x480 WebP'ye çevirir,
image/flowers/ altına kaydeder, photos.json ve ATTRIBUTION.md dosyalarını günceller.

Kullanım:
  python3 tools/add-flower-photo.py f_lily_white indirilen.jpg \
      --credit "Ad Soyad" --license "Unsplash License" --source-url "https://..." \
      [--alt "Beyaz lilyum çiçeği yakın çekim"] [--focus-x 0.5 --focus-y 0.5]

Gerekli: pip install pillow
"""
import argparse, json, re, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "image" / "flowers"
SIZE = 480

def slug(fid: str) -> str:
    s = fid[2:] if fid.startswith("f_") else fid
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("flower_id")
    ap.add_argument("source")
    ap.add_argument("--credit", required=True, help="fotoğrafçı / kaynak")
    ap.add_argument("--license", required=True, dest="lic", help="örn. 'Unsplash License', 'CC0', 'Pexels License'")
    ap.add_argument("--source-url", required=True)
    ap.add_argument("--alt", default="")
    ap.add_argument("--focus-x", type=float, default=0.5)
    ap.add_argument("--focus-y", type=float, default=0.5)
    ap.add_argument("--quality", type=int, default=82)
    a = ap.parse_args()

    cat = json.loads((ROOT / "urunler.json").read_text(encoding="utf-8"))
    flowers = {f["id"]: f for f in cat.get("flowers", [])}
    if a.flower_id not in flowers:
        sys.exit(f"Bilinmeyen çiçek id: {a.flower_id} (urunler.json içinde yok)")
    name = flowers[a.flower_id]["name"]

    im = ImageOps.exif_transpose(Image.open(a.source)).convert("RGB")
    w, h = im.size
    side = min(w, h)
    left = round((w - side) * min(max(a.focus_x, 0), 1))
    top = round((h - side) * min(max(a.focus_y, 0), 1))
    im = im.crop((left, top, left + side, top + side)).resize((SIZE, SIZE), Image.LANCZOS)

    DIR.mkdir(parents=True, exist_ok=True)
    fname = slug(a.flower_id) + ".webp"
    im.save(DIR / fname, "WEBP", quality=a.quality, method=6)

    mf = DIR / "photos.json"
    data = json.loads(mf.read_text(encoding="utf-8")) if mf.exists() else {"photos": {}}
    data.setdefault("photos", {})[a.flower_id] = {
        "src": fname,
        "alt": a.alt or f"{name} çiçeği, yakın çekim fotoğraf",
        "credit": a.credit, "license": a.lic, "sourceUrl": a.source_url,
    }
    mf.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = ["# Çiçek fotoğrafları – kaynak ve lisans kaydı", "",
             "| Dosya | Çiçek | Fotoğrafçı / kaynak | Lisans | Bağlantı |", "|---|---|---|---|---|"]
    for fid, p in sorted(data["photos"].items()):
        lines.append(f"| {p['src']} | {flowers.get(fid, {}).get('name', fid)} | {p.get('credit','')} | {p.get('license','')} | {p.get('sourceUrl','')} |")
    (DIR / "ATTRIBUTION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: {name} -> image/flowers/{fname} ({(DIR / fname).stat().st_size // 1024} KB)")

if __name__ == "__main__":
    main()
