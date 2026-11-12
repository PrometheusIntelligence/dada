#!/usr/bin/env python3
"""Contact sheet of a model from every facing:  python3 iso_preview.py [module.]function out.png [facings] [scale]   e.g. iso_models_b.heavy_tank"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
import kit, iso, iso_models
from build import render

name, out = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 16
sc = int(sys.argv[4]) if len(sys.argv) > 4 else 4
import importlib
mod, _, fn = name.rpartition(".")
m = getattr(importlib.import_module(mod) if mod else iso_models, fn)()
if len(sys.argv) > 3 and sys.argv[3] == "8": pass
fr = iso.facings(m, n)
cols = 8 if n >= 8 else n
rowsn = (n + cols - 1) // cols
pad = 4
sheet = Image.new("RGBA", (pad + cols * (m.w * sc + pad), pad + rowsn * (m.h * sc + pad)), (96, 120, 72, 255))
for k, baked in enumerate(fr):
    img = render(kit.rows(baked, m.w, m.h), ("#3a6fd0", "#1f3f7a"), sc)
    sheet.alpha_composite(img, (pad + (k % cols) * (m.w * sc + pad), pad + (k // cols) * (m.h * sc + pad)))
sheet.save(out)
print("wrote", out)
