# Darkens the fixed mirror's base color so it fits the darker pieces.
# Grey parts (low saturation) go to a dark steel grey; the yellow hazard stripes stay as they are.
# Input: T_MirrorFixed_basecolor_original.png (exported from Unreal), output: T_MirrorFixed_basecolor.png.
# Run: python recolor.py
import os

import numpy as np
from PIL import Image

DARKEN = 0.42                         # brightness kept on grey parts
TINT = np.array([0.93, 0.98, 1.08])   # slight steel blue cast
SAT_FULL, SAT_NONE = 0.25, 0.45       # saturation below SAT_FULL is fully recolored, above SAT_NONE not at all

here = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(here, "T_MirrorFixed_basecolor_original.png")).convert("RGBA")
rgba = np.asarray(src).astype(np.float32) / 255.0
rgb, alpha = rgba[..., :3], rgba[..., 3:]

mx, mn = rgb.max(axis=2), rgb.min(axis=2)
sat = np.where(mx > 1e-4, (mx - mn) / np.maximum(mx, 1e-4), 0.0)
weight = np.clip((SAT_NONE - sat) / (SAT_NONE - SAT_FULL), 0.0, 1.0)[..., None]

dark = np.clip(rgb * DARKEN * TINT, 0.0, 1.0)
out = rgb * (1.0 - weight) + dark * weight
img = Image.fromarray((np.concatenate([out, alpha], axis=2) * 255.0 + 0.5).astype(np.uint8), "RGBA")
img.save(os.path.join(here, "T_MirrorFixed_basecolor.png"))
print("saved")
