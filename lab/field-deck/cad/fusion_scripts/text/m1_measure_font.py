import adsk.core, adsk.fusion

def ink(t):
    xs = []; ys = []
    for c in t.asCurves():
        ev = c.evaluator
        ok, p0, p1 = ev.getParameterExtents()
        ok, pts = ev.getPointsAtParameters([p0 + (p1 - p0) * k / 8.0 for k in range(9)])
        for p in pts:
            xs.append(p.x); ys.append(p.y)
    return min(xs), max(xs), min(ys), max(ys), len(xs)

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    doc = app.activeDocument
    print('doc', doc.name, 'modified', doc.isModified, 'version', doc.dataFile.versionNumber, 'timeline', des.timeline.count)
    root = des.rootComponent
    sk = root.sketches.add(root.xYConstructionPlane); sk.name = 'font measure (scratch)'
    for font in ('Black Ops One', 'Arial'):
        for word in ('H', 'NAME2', 'NAME1', 'SELFDRIVEN', '2026', 'SELFDRIVEN · 2026'):
            inp = sk.sketchTexts.createInput3("'%s'" % word, adsk.core.ValueInput.createByString('10 mm'))
            inp.setAsMultiLine(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(40, 4, 0), adsk.core.HorizontalAlignments.LeftHorizontalAlignment, adsk.core.VerticalAlignments.BottomVerticalAlignment, 0)
            inp.fontName = font
            t = sk.sketchTexts.add(inp)
            x0, x1, y0, y1, n = ink(t)
            print('%-14s %-18s ink x %.4f..%.4f  y %.4f..%.4f  width %.4f height %.4f mm (text height 10 mm), points %d' % (font, word, x0 * 10, x1 * 10, y0 * 10, y1 * 10, (x1 - x0) * 10, (y1 - y0) * 10, n))
            t.deleteMe()
    sk.deleteMe()
    print('timeline', des.timeline.count)
