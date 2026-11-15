# Writes the bevel textures for the 3D look of the UI buttons and slider handles:
#   T_UI_ButtonBevel.png         raised: light top and left edge, dark bottom and right edge
#   T_UI_ButtonBevelPressed.png  pressed in: the same edges swapped
# Both are grey, so the button's tint colour sets the hue. They are drawn as 9-slice boxes
# with a 0.25 margin, so the 16 pixel border keeps its size on any button.
# Run: python make_button_bevel.py
import os

from PIL import Image, ImageDraw

SIZE, SCALE, RADIUS = 64, 4, 7  # texture size, supersampling, corner radius in pixels


def bevel(pressed):
    big = SIZE * SCALE
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    px = img.load()
    for y in range(big):
        t = y / (big - 1)
        # Face: lighter at the top when raised, lighter at the bottom when pressed.
        face = (0.86 - 0.14 * t) if not pressed else (0.70 + 0.12 * t)
        for x in range(big):
            px[x, y] = (0, 0, 0, 0)
            v = face
            e = 3 * SCALE  # edge width
            if y < e:
                v = 0.42 if pressed else 1.0
            elif y >= big - e:
                v = 0.98 if pressed else 0.40
            elif x < e:
                v = 0.55 if pressed else 0.95
            elif x >= big - e:
                v = 0.90 if pressed else 0.62
            g = int(round(v * 255))
            px[x, y] = (g, g, g, 255)
    # Rounded corners through an alpha mask, then scale down for smooth edges.
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, big - 1, big - 1), radius=RADIUS * SCALE, fill=255)
    img.putalpha(mask)
    return img.resize((SIZE, SIZE), Image.LANCZOS)


here = os.path.dirname(os.path.abspath(__file__))
bevel(False).save(os.path.join(here, "T_UI_ButtonBevel.png"))
bevel(True).save(os.path.join(here, "T_UI_ButtonBevelPressed.png"))
print("saved")
