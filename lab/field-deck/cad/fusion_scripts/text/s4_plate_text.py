# AS BUILT in the owner's Fusion file "cyberdeck" on 2026-10-07 (unsaved work on top of his version 4).
# RECONSTRUCTED: the scripts were sent to Fusion step by step and edited on the way; the session's own record of them
# was lost when the cloud machine restarted. This file was rewritten afterwards so that it reproduces what Fusion
# reports (MK1_r8_text_fusion_asbuilt.txt: step names, texts, font, heights, alignments, where the ink lies). It has
# NOT been run again in this form. Fusion is the source for the words; this is the fallback if that work is lost.
# Facts it relies on (measured in his Fusion after the font was installed and Fusion restarted):
#   - font 'Black Ops One' (BlackOpsOne-Regular.ttf in ~/Library/Fonts); text height = height of the capitals, exactly
#   - Fusion does not use the font's pair spacing; non-ASCII characters in a text arrive garbled - ASCII only
#   - keep a script under about 8 kB and read the state back after each one
import adsk.core, adsk.fusion

NAME = 'Back plate r8 - mark + words (built in Fusion)'
BODY = 'Back plate (copy of r7) + mark + words'
PLANE = "Back - plane on the plate's outer face (z 53)"
SKETCH = 'Back 3 - SELFDRIVEN and 2026: real text + the diamond (sketch)'
FEATURE = 'Back 3 - the bottom line, cut'
FONT = 'Black Ops One'
BASE = -70.26                                 # the capitals stand on this y (case mm): 5.3 mm letters centred on the long plate (y -67.61)
X_END, X_DIA, X_START = 30.41, 34.21, 38.01   # SELFDRIVEN ends here / the diamond's centre / 2026 starts here: the whole line is centred on x 18.75
HALF = 0.9                                    # the diamond's half diagonal

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
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    occ27 = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0]
    comp = [o for o in occ27.component.occurrences if o.component.name == NAME][0].component
    if [s for s in comp.sketches if s.name == SKETCH]:
        print('ALREADY THERE:', SKETCH); return
    up = des.userParameters
    if not [p for p in up if p.name == 'engrave_depth']:
        up.add('engrave_depth', adsk.core.ValueInput.createByString('0.6 mm'), 'mm', 'how deep mark and words are cut into the back plate')
    if not [p for p in up if p.name == 'line_letter_height']:
        up.add('line_letter_height', adsk.core.ValueInput.createByString('5.3 mm'), 'mm', 'height of the capitals of SELFDRIVEN and 2026 on the back plate')
    plane = [p for p in comp.constructionPlanes if p.name == PLANE][0]
    body = [x for x in comp.bRepBodies if x.name == BODY][0]
    v0 = body.volume
    sk = comp.sketches.add(plane); sk.name = SKETCH
    P = lambda x, y: sk.modelToSketchSpace(adsk.core.Point3D.create(x / 10.0, y / 10.0, 5.3))
    a = P(0, 0); b = P(10, 0); c = P(0, 10)
    if abs(b.x - a.x - 1.0) > 1e-6 or abs(c.y - a.y - 1.0) > 1e-6:
        print('*** this sketch is turned or mirrored against the case - stopped, nothing cut'); sk.deleteMe(); return
    H = adsk.core.HorizontalAlignments; V = adsk.core.VerticalAlignments
    texts = []
    for word, p0, p1, al in (('SELFDRIVEN', P(X_END - 70.0, BASE), P(X_END, BASE + 10.0), H.RightHorizontalAlignment),
                             ('2026', P(X_START, BASE), P(X_START + 40.0, BASE + 10.0), H.LeftHorizontalAlignment)):
        inp = sk.sketchTexts.createInput3("'%s'" % word, adsk.core.ValueInput.createByString('line_letter_height'))
        inp.setAsMultiLine(p0, p1, al, V.BottomVerticalAlignment, 0)      # bottom alignment: the capitals stand on the box's lower edge
        inp.fontName = FONT
        t = sk.sketchTexts.add(inp); texts.append(t)
        print('%-10s font %r, ink x %.3f..%.3f y %.3f..%.3f mm (case)' % ((word, t.fontName) + ink(t)))
    yc = BASE + 5.3 / 2.0
    pts = [P(X_DIA - HALF, yc), P(X_DIA, yc + HALF), P(X_DIA + HALF, yc), P(X_DIA, yc - HALF)]
    lines = sk.sketchCurves.sketchLines
    for i in range(4):
        l = lines.addByTwoPoints(pts[i], pts[(i + 1) % 4]); l.isFixed = True
    coll = adsk.core.ObjectCollection.create()
    for t in texts:
        coll.add(t)
    coll.add(sk.profiles.item(0))                                          # the diamond is the sketch's only closed outline besides the texts
    ext = comp.features.extrudeFeatures
    einp = ext.createInput(coll, adsk.fusion.FeatureOperations.CutFeatureOperation)
    einp.setDistanceExtent(False, adsk.core.ValueInput.createByString('-engrave_depth'))
    einp.participantBodies = [body]
    f = ext.add(einp); f.name = FEATURE
    sk.isLightBulbOn = False
    body = [x for x in comp.bRepBodies if x.name == BODY][0]
    print('plate now: volume %.6f cm3 (change %.6f; as built -0.149068 -> 23.656033), faces %d' % (body.volume, body.volume - v0, body.faces.count))
