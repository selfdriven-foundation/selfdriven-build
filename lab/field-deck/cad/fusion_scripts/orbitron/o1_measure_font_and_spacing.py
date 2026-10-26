# MK-I r8 draft - THE SWITCH TO ORBITRON BOLD, in the owner's Fusion file "cyberdeck", 2026-10-07 (on top of his version 5).
# What was run, in the order it was run, WITH THE TWO REPAIRS FOLDED IN (the first runs needed them):
#   (a) changing a text's font / style / spacing through the API left its cut with a "Reference Failures" warning and the
#       old letters in the solid until design.computeAll() was called;
#   (b) the same change FLATTENED the text's height to a plain number (3.00 mm): the link to the named parameter had to
#       be put back by hand (ModelParameter with role 'Text1-Height' -> expression 'name_letter_height');
#   (c) one cut with a collection [text, text, sketch profile] cut only the profile once computeAll had run: each text
#       gets its own cut.
# Measured first, in his Fusion (o1): font name 'Orbitron' gives the Bold face (the only one installed) with or without
# the bold style - identical outlines, no fake bold; text height = capitals' height; no pair spacing; CHARACTER SPACING
# is UNIFORM: s percent adds s/100 x 0.96111 x text height after every letter (for this font), nothing after the last
# one - the ink still ends exactly on the box. Keep a script under about 8 kB; read the state back after each.
import adsk.core, adsk.fusion

def ink(t):
    xs = []; ys = []
    for c in t.asCurves():
        ev = c.evaluator
        ok, p0, p1 = ev.getParameterExtents()
        ok, pts = ev.getPointsAtParameters([p0 + (p1 - p0) * k / 8.0 for k in range(9)])
        for p in pts:
            xs.append(p.x); ys.append(p.y)
    return min(xs) * 10, max(xs) * 10, min(ys) * 10, max(ys) * 10

def run(context):
    """o1 - measure the font and the character spacing in a scratch sketch (made and removed again)"""
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    root = des.rootComponent
    sk = root.sketches.add(root.xYConstructionPlane); sk.name = 'font measure (scratch)'
    H = adsk.core.HorizontalAlignments; V = adsk.core.VerticalAlignments
    def make(word, bold=False, spacing=None, right=False, height='10 mm'):
        inp = sk.sketchTexts.createInput3("'%s'" % word, adsk.core.ValueInput.createByString(height))
        inp.setAsMultiLine(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(40, 4, 0),
                           H.RightHorizontalAlignment if right else H.LeftHorizontalAlignment, V.BottomVerticalAlignment, 0)
        inp.fontName = 'Orbitron'
        if bold:
            inp.textStyle = adsk.fusion.TextStyles.TextStyleBold
        t = sk.sketchTexts.add(inp)
        if spacing is not None:
            adsk.fusion.MultiLineTextDefinition.cast(t.definition).characterSpacing = spacing
        r = ink(t); t.deleteMe()
        return r
    for bold in (False, True):
        for word in ('H', 'I', 'NAME2', 'NAME1', 'SELFDRIVEN', '2026'):
            x0, x1, y0, y1 = make(word, bold)
            print('bold=%-5s %-10s width %.3f height %.3f' % (bold, word, x1 - x0, y1 - y0))
    # as measured: H 10.222 x 10.000, I 1.819, NAME2 79.125, NAME1 35.708, SELFDRIVEN 103.597 (10.014 tall), 2026 44.542 - both styles
    for word in ('IIII', 'IY', 'NAME2', 'NAME1'):
        for sp in (0, 10, 50, 100):
            a = make(word, False, sp, False); b = make(word, False, sp, True)
            print('%-8s spacing %3d: left %.3f..%.3f   right-aligned at 400: %.3f..%.3f' % (word, sp, a[0], a[1], b[0], b[1]))
    # as measured: every gap grows by 0.9611 mm per 10 percent at 10 mm text (IIII 10.736 / 13.619 / 25.153 / 39.569)
    sk.deleteMe()
