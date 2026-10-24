#!/usr/bin/env python3
"""Hazır çizimli çiçekleri (admin.html → FLOWER_LIB) urunler.json kataloğuna aktarır. Tekrarlanabilir ve güvenlidir.
  python3 tools/import-flower-models.py            -> yalnızca ne ekleyeceğini gösterir
  python3 tools/import-flower-models.py --apply    -> yazar
Yalnızca katalogda OLMAYAN çiçekler eklenir (aynı kimlik, ya da aynı çizim + aynı ad = zaten var). Var olan kayıtlara, siparişlere ve
diğer anahtarlara dokunulmaz. Aynı komutu tekrar çalıştırmak kopya üretmez. Admin paneldeki “⤓ Eksik hazır çiçekleri aktar” ile aynı kurallar."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
def norm(x): return re.sub(r"\s+", " ", str(x or "").lower().replace("ı", "i")).strip()
adm = (ROOT / "admin.html").read_text(encoding="utf-8")
consts = dict(re.findall(r"\b([GPLDXY]) = '([^']+)'", re.search(r"var G = .*?;\n", adm).group(0)))
block = adm[adm.index("var FLOWER_LIB = ["):]; block = block[:block.index("\n  ];")]
lib = []
for m in re.finditer(r"\['((?:[^'\\]|\\.)*)','(\w+)','(#[0-9A-Fa-f]{6})','(#[0-9A-Fa-f]{6})',([GPLDXY]),(\d+),'([\w\-]+)'\]", block):
    name, shape, color, center, cat, price, fid = m.groups()
    lib.append({"id": fid, "name": name.replace("\\'", "'"), "variety": "", "price": int(price), "color": color, "center": center, "shape": shape, "cat": consts[cat]})
path = ROOT / "urunler.json"
d = json.loads(path.read_text(encoding="utf-8"))
fl = d.setdefault("flowers", [])
ids = {f.get("id") for f in fl}; sig = {(f.get("shape"), norm(f.get("name"))) for f in fl}
added = []
for f in lib:
    if f["id"] in ids or (f["shape"], norm(f["name"])) in sig: continue
    fl.append(f); ids.add(f["id"]); sig.add((f["shape"], norm(f["name"]))); added.append(f["name"])
print(f"Hazır çiçek kütüphanesi: {len(lib)}; katalogda: {len(fl) - len(added)} -> {len(fl)} çiçek; eklenecek: {len(added)}")
for n in added: print("  +", n)
if "--apply" not in sys.argv: print("Değişiklik YAPILMADI. Uygulamak için --apply ekleyin."); sys.exit(0)
fc = d.setdefault("flowerCatalog", {"initialized": True, "version": 1}); fc["modelsImport"] = 1
tmp = path.with_suffix(".json.tmp"); tmp.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); tmp.replace(path)
print("Tamam: urunler.json güncellendi.")
