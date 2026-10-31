"""Convert Inter CFF fonts to TrueType so Chromium embeds them as TrueType (not Type 3)."""
import sys, os
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

def convert(src, dst):
    font = TTFont(src)
    gs = font.getGlyphSet()
    glyf = newTable("glyf"); glyf.glyphOrder = font.getGlyphOrder(); glyf.glyphs = {}
    for name in font.getGlyphOrder():
        pen = TTGlyphPen(gs)
        gs[name].draw(Cu2QuPen(pen, 1.0, reverse_direction=True))
        glyf[name] = pen.glyph()
    font["glyf"] = glyf
    font["loca"] = newTable("loca")
    del font["CFF "]
    if "VORG" in font: del font["VORG"]
    font["maxp"] = newTable("maxp"); m = font["maxp"]
    m.tableVersion = 0x00010000; m.maxZones = 1
    for a in ("maxTwilightPoints","maxStorage","maxFunctionDefs","maxInstructionDefs","maxStackElements","maxSizeOfInstructions"):
        setattr(m, a, 0)
    m.maxComponentElements = max(len(g.components) if hasattr(g, "components") else 0 for g in glyf.glyphs.values())
    font["head"].indexToLocFormat = 0
    font["head"].glyphDataFormat = 0
    font["post"].formatType = 2.0
    font["post"].extraNames = []; font["post"].mapping = {}
    font.sfntVersion = "\x00\x01\x00\x00"
    font.save(dst)

src_dir = "/usr/share/fonts/opentype/inter"
out = sys.argv[1]
for name in ["Regular", "Italic", "Medium", "SemiBold", "Bold", "ExtraBold"]:
    convert(os.path.join(src_dir, f"Inter-{name}.otf"), os.path.join(out, f"Inter-{name}.ttf"))
    print("ok", name)
