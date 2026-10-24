#!/usr/bin/env python3
"""urunler.json çiçek kataloğunu doğrular (CI ve elle). Çiçek SAYISI denetlenmez (üst sınır yoktur).
Denetlenenler: benzersiz/boş olmayan kimlik, ad, geçerli fiyat, renk biçimi, yinelenen (çizim + ad) kayıt ve
eski fotoğraf alanı (`photo`) kalıntısı. Tanınmayan çizim türü hata değildir: yönetim paneli ve site gül çizimiyle gösterir."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "urunler.json").read_text(encoding="utf-8"))
errs, seen, sigs = [], set(), set()
flowers = d.get("flowers", [])
if not isinstance(flowers, list): errs.append("flowers liste olmalı"); flowers = []
HEX = re.compile(r"#[0-9a-fA-F]{6}")
norm = lambda x: re.sub(r"\s+", " ", str(x or "").lower().replace("ı", "i")).strip()
for f in flowers:
    fid = f.get("id")
    if not fid or fid in seen: errs.append(f"Boş/yinelenen id: {fid!r}")
    seen.add(fid)
    if not str(f.get("name", "")).strip(): errs.append(f"{fid}: ad boş")
    sig = (f.get("shape"), norm(f.get("name")), norm(f.get("variety")), (f.get("color") or "").lower())
    if sig in sigs: errs.append(f"{fid}: aynı çizim/ad/çeşit/renkte yinelenen kayıt")
    sigs.add(sig)
    try:
        if float(f.get("price")) < 0: raise ValueError
    except (TypeError, ValueError): errs.append(f"{fid}: geçersiz fiyat {f.get('price')!r}")
    for k in ("color", "center"):
        if f.get(k) and not HEX.fullmatch(f[k]): errs.append(f"{fid}: geçersiz {k} {f[k]!r}")
    if "photo" in f: errs.append(f"{fid}: eski 'photo' alanı kaldırılmalı (çiçekler çizimle gösterilir)")
if not (d.get("flowerCatalog") or {}).get("initialized"): errs.append("flowerCatalog.initialized işareti yok (admin ilk girişte kurulumu yapar)")
print(f"{len(flowers)} çiçek")
if errs:
    print("HATA:\n - " + "\n - ".join(errs)); sys.exit(1)
print("Katalog geçerli.")
