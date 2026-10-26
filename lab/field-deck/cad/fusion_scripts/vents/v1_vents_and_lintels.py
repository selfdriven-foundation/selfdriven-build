# v1 - AIR SLOTS ON THE HANDLE SIDE + FLAT LINTELS OVER THE TWO WINDOWS, built in Fusion (owner: "Yes, add vents
# (Recommended)", 2026-10-12; blind review P: the two window lintels start as a hair-thin line - MUST FIX). It changes the r8
# item's OWN body (r8's copy of r7's body; r7's item is not touched): three new steps at the end of the timeline, each checked
# against the cloud's trial (cad-src/mk1_vents_r8.py, ALL CHECKS PASS), all in case coordinates (the item's own frame):
#   1 three slots through the handle-side wall (x 73.2 .. 75.7), sketched at z 38.0 and cut down to z 12.6:
#     y -64.875 .. -61.875 (armour plate 1), -54.45 .. -51.05 (the groove between the plates), -43.625 .. -40.625 (plate 2)
#   2 the side window's lintel flat underneath: x 72.8 .. 76.2, y -28.5 .. 28.0, from z 38.6 down to z 35.5
#   3 the top opening's lintel flat underneath: x -5.6 .. 46.0, y 30 .. 38, from z 46.6 down to z 43.0
# Guarded: if its first sketch is there it says ALREADY THERE and changes nothing; if the body is not the one read back
# (117.633533 cm3, 1156 faces) it stops before changing anything; a step whose volume change differs from the cloud's by more
# than 0.03 mm3, or a step that is not healthy, stops the script and everything this run made is taken back (newest first),
# so a second run starts clean. It never saves.
import adsk.core, adsk.fusion, traceback

ITEM = 'BUILT IN FUSION'
BODY_PREFIX = 'Body (copy of r7)'
V0_CM3, FACES0 = 117.633533, 1156
SLOTS = [(-64.875, -61.875), (-54.45, -51.05), (-43.625, -40.625)]
SX0, SX1, SZ0, SZ1 = 72.5, 76.5, 12.6, 38.0
SIDE = (72.8, 76.2, -28.5, 28.0, 35.5, 38.6)
TOP = (-5.6, 46.0, 30.0, 38.0, 43.0, 46.6)
TAKES = dict(slots=533.0474, side=191.0927, top=388.5480)       # mm3 each step takes (the cloud's trial)
SK1 = 'Vents - three slots in the handle-side wall (sketch at z 38.0)'
GROUP = 'Body r8 - air slots on the handle side + flat lintels (built in Fusion)'
VI = adsk.core.ValueInput.createByString
P = lambda x, y, z: adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)
# (what, point, 0 = solid / 2 = empty after this script) - every one checked on the cloud's trial and on the body before
PROBES = [('slot 1 middle', (74.45, -63.375, 25.0), 2), ('slot 2 middle', (74.45, -52.75, 25.0), 2), ('slot 3 middle', (74.45, -42.125, 25.0), 2),
          ('wall between slots 1 and 2', (74.45, -58.1, 25.0), 0), ('wall between slots 2 and 3', (74.45, -47.4, 25.0), 0),
          ('under slot 1', (74.45, -63.375, 12.4), 0), ('over slot 1', (74.45, -63.375, 38.2), 0),
          ('side window, the old chamfer', (74.45, 0.0, 37.5), 2), ('side lintel above the flat', (74.45, 0.0, 38.8), 0),
          ("side window's corner piece, kept", (73.6, 29.0, 38.0), 0), ("screw post's tip, gone", (73.1, 19.1, 38.5), 2),
          ('screw post above it', (72.5, 19.1, 39.5), 0), ('top opening, the old V', (20.0, 34.0, 45.0), 2),
          ('top lintel above the flat', (20.0, 34.0, 46.8), 0), ("top opening's D jamb wall", (-7.0, 35.0, 45.0), 0),
          ("top opening's C end, inner part", (47.0, 34.0, 44.5), 0)]


def bodies_of(comp):
    return [b for b in comp.bRepBodies if b.name.startswith(BODY_PREFIX)]


def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    items = [o for o in des.rootComponent.occurrences if ITEM in o.component.name]
    if len(items) != 1:
        print('STOPPED: %d items named ...%s...' % (len(items), ITEM)); return
    comp = items[0].component
    bs = bodies_of(comp)
    if [s for s in comp.sketches if s.name == SK1]:
        print('ALREADY THERE: %s | body %s | modified %s' % (SK1, [(b.name, round(b.volume * 1000, 4), b.faces.count) for b in bs], app.activeDocument.isModified)); return
    if len(bs) != 1 or abs(bs[0].volume - V0_CM3) > 5e-6 or bs[0].faces.count != FACES0:
        print('STOPPED, not the body read back: %s' % [(b.name, round(b.volume, 6), b.faces.count) for b in bs]); return
    b = bs[0]
    pc = lambda q: b.pointContainment(P(*q))
    before = [(nm, pc(q)) for nm, q, want in PROBES if pc(q) != 0]
    print('before: %r %.6f cm3, %d faces | probes not solid before (must be none): %s | modified %s' % (b.name, b.volume, b.faces.count, before, app.activeDocument.isModified))
    if before:
        print('STOPPED: a probe point is not solid in the body before the cuts'); return
    made = []
    try:
        build(des, comp, made)
    except Exception:
        print('*** STOPPED:\n' + traceback.format_exc())
        print('made before it stopped: %s' % [m.name for m in made])
        try:
            for m in reversed(made):
                m.deleteMe()
            nb = bodies_of(comp)[0]
            print('ROLLED BACK: %d things removed; body %.6f cm3 (before %.6f), %d faces' % (len(made), nb.volume, V0_CM3, nb.faces.count))
        except Exception:
            print('*** ROLL-BACK FAILED - Fusion needs a look:\n' + traceback.format_exc())


def build(des, comp, made):
    tl = des.timeline
    t_start = tl.count
    F = comp.features
    body = lambda: bodies_of(comp)[0]
    last = [body().volume * 1000.0]

    def note(obj, name):
        obj.name = name
        made.append(obj)
        return obj

    def step(key, feat):
        if feat.healthState != 0:
            raise RuntimeError('step %s not healthy: %s %s' % (key, feat.healthState, feat.errorOrWarningMessage))
        now = body().volume * 1000.0
        took = last[0] - now
        ok = abs(took - TAKES[key]) < 0.03
        print('   %-6s took %.4f mm3 (the cloud: %.4f) -> body %.4f mm3 %s' % (key, took, TAKES[key], now, 'ok' if ok else '*** DIFFERS'))
        if not ok:
            raise RuntimeError('step %s took %.4f against %.4f' % (key, took, TAKES[key]))
        last[0] = now

    def plane(z, name):
        for sgn in (1, -1):
            pin = comp.constructionPlanes.createInput()
            pin.setByOffset(comp.xYConstructionPlane, VI('%g mm' % (sgn * z)))
            pl = comp.constructionPlanes.add(pin)
            if abs(pl.geometry.origin.z * 10.0 - z) < 1e-6 and abs(abs(pl.geometry.normal.z) - 1.0) < 1e-9:
                pl.isLightBulbOn = False
                return note(pl, name)
            pl.deleteMe()
        raise RuntimeError('plane z %g not made' % z)

    def rects(pl, z, name, boxes):
        sk = note(comp.sketches.add(pl), name)
        S = lambda x, y: sk.modelToSketchSpace(P(x, y, z))
        for x0, x1, y0, y1 in boxes:
            sk.sketchCurves.sketchLines.addTwoPointRectangle(S(x0, y0), S(x1, y1))
        for ln in sk.sketchCurves.sketchLines:
            ln.startSketchPoint.isFixed = True; ln.endSketchPoint.isFixed = True
        want = sorted((x1 - x0) * (y1 - y0) for x0, x1, y0, y1 in boxes)
        got = sorted(p.areaProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).area * 100.0 for p in sk.profiles)
        if len(got) != len(want) or any(abs(g - w) > 0.005 for g, w in zip(got, want)):
            raise RuntimeError('sketch %s: profiles %s mm2, want %s' % (name, [round(g, 4) for g in got], [round(w, 4) for w in want]))
        col = adsk.core.ObjectCollection.create()
        for p in sk.profiles:
            col.add(p)
        sk.isLightBulbOn = False
        return sk, col

    def cut_down(sk, col, depth, name):
        n = sk.xDirection.crossProduct(sk.yDirection)
        sg = '' if n.z < 0 else '-'                    # toward -z (down, into the part as it prints)
        inp = F.extrudeFeatures.createInput(col, adsk.fusion.FeatureOperations.CutFeatureOperation)
        inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI('%s%g mm' % (sg, depth))), adsk.fusion.ExtentDirections.PositiveExtentDirection)
        inp.participantBodies = [body()]
        return note(F.extrudeFeatures.add(inp), name)

    # ---- 1 the three slots
    pl = plane(SZ1, 'Vents - plane at z 38.0 (the slots\' roof)')
    sk, col = rects(pl, SZ1, SK1, [(SX0, SX1, y0, y1) for y0, y1 in SLOTS])
    step('slots', cut_down(sk, col, SZ1 - SZ0, 'Vents - three slots 3 / 3.4 / 3 x 25.4 in the handle-side wall (down to z 12.6)'))
    # ---- 2 the side window's lintel
    x0, x1, y0, y1, z0, z1 = SIDE
    pl = plane(z1, 'Lintels - plane at z 38.6 (side window, flat underneath)')
    sk, col = rects(pl, z1, 'Lintels - side window: the chamfer to take (sketch at z 38.6)', [(x0, x1, y0, y1)])
    step('side', cut_down(sk, col, z1 - z0, 'Lintels - side window flat underneath at z 38.6 (prints as a bridge)'))
    # ---- 3 the top opening's lintel
    x0, x1, y0, y1, z0, z1 = TOP
    pl = plane(z1, 'Lintels - plane at z 46.6 (top opening, flat underneath)')
    sk, col = rects(pl, z1, 'Lintels - top opening: the V to take (sketch at z 46.6)', [(x0, x1, y0, y1)])
    step('top', cut_down(sk, col, z1 - z0, 'Lintels - top opening flat underneath at z 46.6 (prints as a bridge)'))
    # ---- the result
    b = body()
    pc = lambda q: b.pointContainment(P(*q))
    bad = [(nm, pc(q)) for nm, q, want in PROBES if pc(q) != want]
    if bad:
        raise RuntimeError('probes wrong (0 = solid, 2 = empty): %s' % bad)
    print('probes: %d checked, all as the cloud has them' % len(PROBES))
    tb = b.boundingBox
    print('body %r: %.6f cm3 (took %.4f mm3 in all; the cloud: %.4f), %d faces, x %.3f..%.3f y %.3f..%.3f z %.3f..%.3f' % (
        b.name, b.volume, V0_CM3 * 1000.0 - b.volume * 1000.0, sum(TAKES.values()), b.faces.count, tb.minPoint.x * 10, tb.maxPoint.x * 10,
        tb.minPoint.y * 10, tb.maxPoint.y * 10, tb.minPoint.z * 10, tb.maxPoint.z * 10))
    badsteps = [(tl.item(i).name, tl.item(i).healthState) for i in range(t_start, tl.count) if not tl.item(i).isGroup and tl.item(i).healthState != 0]
    print('timeline: %d new steps (%d .. %d); not healthy: %s' % (tl.count - t_start, t_start, tl.count - 1, badsteps))
    try:
        g = tl.timelineGroups.add(t_start, tl.count - 1)
        g.name = GROUP
        print('grouped as: %s' % g.name)
    except Exception as ex:
        print('(not grouped: %s)' % ex)
    des.activateRootComponent()
    print('active component: %s | modified %s' % (des.activeComponent.name, adsk.core.Application.get().activeDocument.isModified))
