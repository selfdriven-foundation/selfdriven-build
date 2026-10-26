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

NAME = 'Back plate r8 - mark + words (built in Fusion)'
BODY = 'Back plate (copy of r7) + mark + words'
PLANE = "Back - plane on the plate's outer face (z 53)"
SKETCH = 'Back 3 - SELFDRIVEN and 2026: real text + the diamond (sketch)'
OLD = 'Back 3 - the bottom line, cut'
FONT = 'Orbitron'
SPACING = 1.0               # percent: 0.05 mm more after every letter at 5.15 mm -> L and F stand 0.479 mm apart
CAP = '5.15 mm'             # the widest the long plate takes in this font (the line is 84.27 mm long, 3.55 mm from each end of the flat top)
XC, YC = 18.75, -67.61      # the long plate's flat top: its middle (case mm)
GAP, HALF = 2.9 / 5.3, 0.9 / 5.3   # word - diamond - year: the gap and the diamond's half diagonal per mm of letter height (as first drawn)

def ink(t):
    xs = []; ys = []
    for c in t.asCurves():
        ev = c.evaluator
        ok, p0, p1 = ev.getParameterExtents()
        ok, pts = ev.getPointsAtParameters([p0 + (p1 - p0) * k / 8.0 for k in range(9)])
        for p in pts:
            xs.append(p.x); ys.append(p.y)
    return min(xs) * 10, max(xs) * 10, min(ys) * 10, max(ys) * 10

def health(des):
    tl = des.timeline; bad = []
    for i in range(tl.count):
        try:
            hs = tl.item(i).healthState
        except Exception:
            hs = -1
        if hs not in (0, 5):
            bad.append((i, tl.item(i).name, hs))
    return tl.count, bad

def run(context):
    """o3 - the plate's line: the old cut and sketch removed, drawn again in Orbitron and centred from the MEASURED lengths"""
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    occ27 = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0]
    comp = [o for o in occ27.component.occurrences if o.component.name == NAME][0].component
    body = lambda: [x for x in comp.bRepBodies if x.name == BODY][0]
    for f in [x for x in comp.features if x.name == OLD]:
        f.deleteMe()
    for s in [x for x in comp.sketches if x.name == SKETCH]:
        s.deleteMe()
    p = des.userParameters.itemByName('line_letter_height')
    p.expression = CAP
    p.comment = 'height of the capitals of SELFDRIVEN and 2026 on the back plate (Orbitron Bold; 5.15 mm is the widest the long plate takes)'
    cap = p.value * 10
    plane = [x for x in comp.constructionPlanes if x.name == PLANE][0]
    sk = comp.sketches.add(plane); sk.name = SKETCH
    P = lambda x, y: sk.modelToSketchSpace(adsk.core.Point3D.create(x / 10.0, y / 10.0, 5.3))
    a = P(0, 0); b = P(10, 0); c = P(0, 10)
    if abs(b.x - a.x - 1.0) > 1e-6 or abs(c.y - a.y - 1.0) > 1e-6:
        print('*** this sketch is turned or mirrored against the case - stopped, nothing cut'); sk.deleteMe(); return
    H = adsk.core.HorizontalAlignments; V = adsk.core.VerticalAlignments
    base = YC - cap / 2.0
    def mk(word, x0, x1, al):
        inp = sk.sketchTexts.createInput3("'%s'" % word, adsk.core.ValueInput.createByString('line_letter_height'))
        inp.setAsMultiLine(P(x0, base), P(x1, base + 10.0), al, V.BottomVerticalAlignment, 0)
        inp.fontName = FONT
        inp.textStyle = adsk.fusion.TextStyles.TextStyleBold
        t = sk.sketchTexts.add(inp)
        adsk.fusion.MultiLineTextDefinition.cast(t.definition).characterSpacing = SPACING
        return t
    t1 = mk('SELFDRIVEN', -120.0, 0.0, H.RightHorizontalAlignment); i1 = ink(t1); w1 = i1[1] - i1[0]
    t2 = mk('2026', 0.0, 60.0, H.LeftHorizontalAlignment); i2 = ink(t2); w2 = i2[1] - i2[0]
    g = GAP * cap; hd = HALF * cap
    total = w1 + w2 + 2 * g + 2 * hd
    xl = XC - total / 2.0
    x_end = xl + w1; x_dia = x_end + g + hd; x_start = x_dia + hd + g
    t1.deleteMe(); t2.deleteMe()
    t1 = mk('SELFDRIVEN', x_end - 120.0, x_end, H.RightHorizontalAlignment)
    t2 = mk('2026', x_start, x_start + 60.0, H.LeftHorizontalAlignment)
    pts = [P(x_dia - hd, YC), P(x_dia, YC + hd), P(x_dia + hd, YC), P(x_dia, YC - hd)]
    lines = sk.sketchCurves.sketchLines
    for i in range(4):
        l = lines.addByTwoPoints(pts[i], pts[(i + 1) % 4]); l.isFixed = True
    ext = comp.features.extrudeFeatures
    for prof, nm in ((t1, 'Back 3 - SELFDRIVEN, cut'), (t2, 'Back 4 - 2026, cut'), (sk.profiles.item(0), 'Back 5 - the diamond between them, cut')):   # repair (c)
        einp = ext.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
        einp.setDistanceExtent(False, adsk.core.ValueInput.createByString('-engrave_depth'))
        einp.participantBodies = [body()]
        ext.add(einp).name = nm
    sk.isLightBulbOn = False
    for mp in des.allParameters:                                   # repair (b)
        if mp.objectType.endswith('ModelParameter') and 'Height' in mp.role:
            try:
                cb = mp.createdBy.name
            except Exception:
                cb = ''
            if cb == SKETCH:
                mp.expression = 'line_letter_height'
    des.computeAll()
    print('line %.3f long from x %.3f; SELFDRIVEN ends %.3f, diamond centre %.3f (half %.4f), 2026 starts %.3f' % (total, xl, x_end, x_dia, hd, x_start))
    print('plate %.6f cm3 (as built 23.686916), %d faces (563); timeline %s' % (body().volume, body().faces.count, health(des)))
    # as built: SELFDRIVEN ink x -23.385 .. 30.413 (53.798), 2026 x 37.798 .. 60.885 (23.087), line 84.270, diamond centre (34.105, -67.61) half 0.8745
