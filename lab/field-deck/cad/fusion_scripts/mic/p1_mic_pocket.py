# p1 - THE MIC'S POCKET IN THE FRONT'S CHIN, built in Fusion (owner: "ok. so do it.", 2026-10-11; on the picture "looks good",
# and asked about the wires' reach: "Not tried - cut it anyway", 2026-10-12 - the reach is checked before the front prints). The shared "Front (armoured)" (r7's item uses it too) is NOT touched: its solid is copied into a NEW
# component in the r8 item (a base feature), the shared one is hidden IN THE r8 ITEM ONLY, and the pocket is cut into the
# copy step by step, each step checked against the cloud's trial (cad-src/mk1_mic_pocket_r8.py r2, the same numbers):
#   fill the chin's three old bolt marks (y -77): d6.62 x 1.95 from the face
#   cut three new marks at y -75: round d6.6 x 0.9, hex 3.81 across flats x 1.95 (corners along x, as mk1_front cuts them)
#   bore dia mic_bore_dia (named number; 14.6 until the test piece says otherwise) from the back plane z 0 down to z -7.0
#   recess dia 11.6, z -7.0 .. -8.6; two slots 1.6 wide, 5.08 centre to centre, along y at x +-3.81, z -8.6 .. -9.8;
#   pinhole dia 2 from z -8.6 through to the face.
# Guarded: if the new component is there it says ALREADY THERE and changes nothing; if the state is not the one expected
# (one shared front in the r8 item, unmoved, 130.545864 cm3) it stops before changing anything; a step whose volume differs
# from the cloud's by more than 0.03 mm3 stops the script, and everything this run made is taken back (the new component is
# removed, the shared front shown again), so a second run starts clean.
import adsk.core, adsk.fusion, math, traceback

ITEM = 'BUILT IN FUSION'
SHARED = 'Front (armoured)'
COMP_NAME = 'Front r8 - mic pocket (built in Fusion)'
BODY = 'Front r8 with the mic pocket (print this)'
PARAM = 'mic_bore_dia'
PARAM_NOTE = ('Diameter of the mic pocket in the front (the INMP441 board is 13.94 at its widest). '
              'Set from the test piece: 1 = 14.3, 2 = 14.6, 3 = 15.0.')
D0 = 14.6
MX, MY = 0.0, -75.0
FACE, SEAT, RFLOOR, SLOTF = -11.6, -7.0, -8.6, -9.8
OLD_Y, NEW_Y, CHIN_X = -77.0, -75.0, (-52.0, 0.0, 52.0)
PT_D, PT_DEEP, HEX_AF, HEX_DEEP, FILL_D = 6.6, 0.9, 3.81, 1.95, 6.62
RECESS_D, HOLE_D, SLOT_W, ROW_X, PITCH = 11.6, 2.0, 1.6, 3.81, 2.54
SRC_CM3 = 130.545864
WANT = dict(start=130545.8640, fills=130677.8359, rounds=130585.4637, hexes=130545.8640, bore=129373.9557, recess=129204.8627,
            slots=129180.5300, pinhole=129177.2313)
VI = adsk.core.ValueInput.createByString
P = lambda x, y, z: adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)


def identity(m):
    a = m.asArray()
    return all(abs(a[i] - (1.0 if i in (0, 5, 10, 15) else 0.0)) < 1e-9 for i in range(16))


def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    items = [o for o in des.rootComponent.occurrences if ITEM in o.component.name]
    if len(items) != 1:
        print('STOPPED: %d items named ...%s...' % (len(items), ITEM)); return
    item = items[0].component
    old = [o for o in item.occurrences if o.component.name == COMP_NAME]
    if old:
        print('ALREADY THERE: %s | bodies %s | modified %s' % (COMP_NAME, [(b.name, round(b.volume * 1000, 4)) for b in old[0].component.bRepBodies],
                                                               app.activeDocument.isModified)); return
    sh = [o for o in item.occurrences if SHARED in o.component.name]
    if len(sh) != 1:
        print('STOPPED: %d occurrences of the shared front in the r8 item: %s' % (len(sh), [o.name for o in sh])); return
    so = sh[0]
    bodies = [b for b in so.component.bRepBodies]
    if not identity(so.transform2) or len(bodies) != 1 or abs(bodies[0].volume - SRC_CM3) > 2e-6:
        print('STOPPED, not the state expected: moved %s, bodies %s' % (not identity(so.transform2), [(b.name, round(b.volume, 6)) for b in bodies])); return
    print('before: shared front %s (%s), body %r %.6f cm3, visible %s | modified %s' % (so.name, so.component.name, bodies[0].name, bodies[0].volume,
                                                                                      so.isLightBulbOn, app.activeDocument.isModified))
    made, ctx = [], {}
    try:
        build(des, item, so, bodies[0], made, ctx)
    except Exception:
        print('*** STOPPED:\n' + traceback.format_exc())
        print('timeline items made before it stopped: %s' % made)
        try:                                   # take back what this run made (all of it lives in the new component), show the shared front again
            if ctx.get('occ') is not None:
                ctx['occ'].deleteMe()
            so.isLightBulbOn = True
            des.activateRootComponent()
            print('ROLLED BACK: the new component removed (%s), the shared front shown again (%s); the named number %s stays' % (
                not any(o.component.name == COMP_NAME for o in item.occurrences), so.isLightBulbOn, PARAM))
        except Exception:
            print('*** ROLL-BACK FAILED - Fusion needs a look:\n' + traceback.format_exc())


def build(des, item, so, src, made, ctx):
    tl = des.timeline
    t_start = tl.count
    par = des.userParameters.itemByName(PARAM)
    if not par:
        par = des.userParameters.add(PARAM, VI('%g mm' % D0), 'mm', PARAM_NOTE)
    print('named number %s = %s' % (PARAM, par.expression))
    occ = item.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    ctx['occ'] = occ
    comp = occ.component
    comp.name = COMP_NAME
    F = comp.features

    def note(obj, name):
        obj.name = name
        made.append(name)
        return obj

    def body():
        return [b for b in comp.bRepBodies if b.name == BODY][0]

    def check(key):
        v = body().volume * 1000.0
        ok = abs(v - WANT[key]) < 0.03
        print('   %-8s body %.4f mm3 (the cloud: %.4f) %s' % (key, v, WANT[key], 'ok' if ok else '*** DIFFERS'))
        if not ok:
            raise RuntimeError('step %s: %.4f against %.4f' % (key, v, WANT[key]))

    def plane(z, name):
        if abs(z) < 1e-9:
            return comp.xYConstructionPlane
        for sgn in (1, -1):
            pin = comp.constructionPlanes.createInput()
            pin.setByOffset(comp.xYConstructionPlane, VI('%g mm' % (sgn * z)))
            pl = comp.constructionPlanes.add(pin)
            if abs(pl.geometry.origin.z * 10.0 - z) < 1e-6:
                pl.isLightBulbOn = False
                return note(pl, name)
            pl.deleteMe()
        raise RuntimeError('plane z %g not made' % z)

    def profiles(sk, mm2, n, tol=0.005):
        got = [p for p in sk.profiles if abs(p.areaProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).area * 100.0 - mm2) < tol]
        if len(got) != n:
            raise RuntimeError('sketch %s: %d profiles of %.4f mm2, want %d (have %s)' % (sk.name, len(got), mm2, n, [round(p.areaProperties().area * 100, 4) for p in sk.profiles]))
        col = adsk.core.ObjectCollection.create()
        for p in got:
            col.add(p)
        return col

    def extrude(col, sk, dist_mm, along_z, op, name):
        n = sk.xDirection.crossProduct(sk.yDirection)
        sg = '' if n.z * along_z > 0 else '-'
        inp = F.extrudeFeatures.createInput(col, op)
        inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI('%s%g mm' % (sg, dist_mm))), adsk.fusion.ExtentDirections.PositiveExtentDirection)
        inp.participantBodies = [body()]
        return note(F.extrudeFeatures.add(inp), name)

    def sketch(pl, z, name):
        sk = note(comp.sketches.add(pl), name)
        return sk, (lambda x, y: sk.modelToSketchSpace(P(x, y, z)))

    def circle(sk, S, x, y, d_expr, d_mm):
        c = sk.sketchCurves.sketchCircles.addByCenterRadius(S(x, y), d_mm / 20.0)
        c.centerSketchPoint.isFixed = True
        sk.sketchDimensions.addDiameterDimension(c, S(x + d_mm, y + d_mm)).parameter.expression = d_expr
        return c

    # ---- 0 the copy of the shared front, in a base feature of the new component
    bf = F.baseFeatures.add()
    bf.startEdit()
    comp.bRepBodies.add(adsk.fusion.TemporaryBRepManager.get().copy(src), bf)
    bf.finishEdit()
    note(bf, 'Front r8 - copy of the shared front (r7 armour)')
    comp.bRepBodies.item(0).name = BODY
    check('start')
    so.isLightBulbOn = False
    print('   the shared front hidden in the r8 item (r7 item untouched): visible %s' % so.isLightBulbOn)
    pf = plane(FACE, 'Mic - plane on the front face (z -11.6)')
    # ---- 1 the chin's three old bolt marks filled
    sk, S = sketch(pf, FACE, 'Mic - old chin marks to fill (sketch)')
    for x in CHIN_X:
        circle(sk, S, x, OLD_Y, '%g mm' % FILL_D, FILL_D)
    extrude(profiles(sk, math.pi * (FILL_D / 2) ** 2, 3), sk, HEX_DEEP, 1, adsk.fusion.FeatureOperations.JoinFeatureOperation, 'Mic - the three old chin marks filled (y -77)')
    check('fills')
    # ---- 2 three new marks, 2 mm higher: round recess, then hex
    sk, S = sketch(pf, FACE, 'Mic - new chin marks, round (sketch)')
    for x in CHIN_X:
        circle(sk, S, x, NEW_Y, '%g mm' % PT_D, PT_D)
    extrude(profiles(sk, math.pi * (PT_D / 2) ** 2, 3), sk, PT_DEEP, 1, adsk.fusion.FeatureOperations.CutFeatureOperation, 'Mic - new chin marks at y -75, round 0.9 deep')
    check('rounds')
    sk, S = sketch(pf, FACE, 'Mic - new chin marks, hex (sketch)')
    R = HEX_AF / math.sqrt(3.0)
    for x in CHIN_X:
        pts = [S(x + R * math.cos(math.radians(60 * k)), NEW_Y + R * math.sin(math.radians(60 * k))) for k in range(6)]
        L = sk.sketchCurves.sketchLines
        first = prev = L.addByTwoPoints(pts[0], pts[1])
        for k in range(2, 6):
            prev = L.addByTwoPoints(prev.endSketchPoint, pts[k])
        L.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)
    for ln in sk.sketchCurves.sketchLines:
        ln.startSketchPoint.isFixed = True; ln.endSketchPoint.isFixed = True
    extrude(profiles(sk, math.sqrt(3) / 2 * HEX_AF ** 2, 3), sk, HEX_DEEP, 1, adsk.fusion.FeatureOperations.CutFeatureOperation, 'Mic - new chin marks at y -75, hex 1.95 deep')
    check('hexes')
    # ---- 3 the pocket from the back plane: bore (mic_bore_dia) to the seat
    sk, S = sketch(comp.xYConstructionPlane, 0.0, 'Mic - bore (sketch)')
    circle(sk, S, MX, MY, PARAM, par.value * 10.0)
    extrude(profiles(sk, math.pi * (par.value * 5.0) ** 2, 1), sk, -SEAT, -1, adsk.fusion.FeatureOperations.CutFeatureOperation, 'Mic - bore %s down to the seat (z -7.0)' % PARAM)
    if abs(par.value - D0 / 10.0) < 1e-9:
        check('bore')
    # ---- 4 the recess under the seat (the joints hang in it)
    ps = plane(SEAT, 'Mic - plane at the seat (z -7.0)')
    sk, S = sketch(ps, SEAT, 'Mic - recess (sketch)')
    circle(sk, S, MX, MY, '%g mm' % RECESS_D, RECESS_D)
    extrude(profiles(sk, math.pi * (RECESS_D / 2) ** 2, 1), sk, SEAT - RFLOOR, -1, adsk.fusion.FeatureOperations.CutFeatureOperation, 'Mic - recess 11.6 down to z -8.6')
    if abs(par.value - D0 / 10.0) < 1e-9:
        check('recess')
    # ---- 5 two slots for the pins' short ends
    pr = plane(RFLOOR, 'Mic - plane at the recess floor (z -8.6)')
    sk, S = sketch(pr, RFLOOR, "Mic - slots for the pins' short ends (sketch)")
    r = SLOT_W / 2.0
    for sx in (1, -1):
        cx = MX + sx * ROW_X
        y0, y1 = MY - PITCH, MY + PITCH
        L, A = sk.sketchCurves.sketchLines, sk.sketchCurves.sketchArcs
        a = L.addByTwoPoints(S(cx - r, y0), S(cx - r, y1))
        b = L.addByTwoPoints(S(cx + r, y1), S(cx + r, y0))
        A.addByThreePoints(a.endSketchPoint, S(cx, y1 + r), b.startSketchPoint)
        A.addByThreePoints(b.endSketchPoint, S(cx, y0 - r), a.startSketchPoint)
    for c in list(sk.sketchCurves.sketchLines) + list(sk.sketchCurves.sketchArcs):
        c.startSketchPoint.isFixed = True; c.endSketchPoint.isFixed = True
    for c in sk.sketchCurves.sketchArcs:
        c.centerSketchPoint.isFixed = True
    extrude(profiles(sk, SLOT_W * 2 * PITCH + math.pi * r * r, 2), sk, RFLOOR - SLOTF, -1, adsk.fusion.FeatureOperations.CutFeatureOperation, "Mic - two slots for the pins' short ends, to z -9.8")
    if abs(par.value - D0 / 10.0) < 1e-9:
        check('slots')
    # ---- 6 the pinhole through to the face
    sk, S = sketch(pr, RFLOOR, 'Mic - pinhole (sketch)')
    circle(sk, S, MX, MY, '%g mm' % HOLE_D, HOLE_D)
    extrude(profiles(sk, math.pi * (HOLE_D / 2) ** 2, 1), sk, RFLOOR - FACE + 0.5, -1, adsk.fusion.FeatureOperations.CutFeatureOperation, 'Mic - pinhole 2.0 through to the face')
    if abs(par.value - D0 / 10.0) < 1e-9:
        check('pinhole')
    # ---- the result
    b = body()
    pc = lambda x, y, z: b.pointContainment(P(x, y, z))
    probes = [('in the hex socket (0, -75, -10.5)', (0, -75, -10.5), 2), ('pinhole (0, -75, -9.0)', (0, -75, -9.0), 2), ('skin beside it (1.5, -75, -9.0)', (1.5, -75, -9.0), 0),
              ('slot (3.81, -75, -9.5)', (3.81, -75, -9.5), 2), ('under the slot (3.81, -75, -10.2)', (3.81, -75, -10.2), 0), ('bore (7.0, -75, -3)', (7.0, -75, -3.0), 2),
              ('beyond the 14.6 bore (7.6, -75, -3)', (7.6, -75, -3.0), 0), ('old mark filled (0, -79.5, -11.2)', (0, -79.5, -11.2), 0),
              ('old mark filled (-52, -79.5, -11.2)', (-52, -79.5, -11.2), 0), ('new round recess (-52, -72.2, -11.2)', (-52, -72.2, -11.2), 2)]
    bad = [(nm, pc(*q)) for nm, q, want in probes if pc(*q) != want]
    print('probes (0 = solid, 2 = empty): %d checked, wrong: %s' % (len(probes), bad))
    tb = b.boundingBox
    print('body %r: %.6f cm3, %d faces, x %.3f..%.3f y %.3f..%.3f z %.3f..%.3f' % (b.name, b.volume, b.faces.count, tb.minPoint.x * 10, tb.maxPoint.x * 10,
                                                                               tb.minPoint.y * 10, tb.maxPoint.y * 10, tb.minPoint.z * 10, tb.maxPoint.z * 10))
    badsteps = [(tl.item(i).name, tl.item(i).healthState) for i in range(t_start, tl.count) if not tl.item(i).isGroup and tl.item(i).healthState != 0]
    print('timeline: %d new steps (%d .. %d); not healthy: %s' % (tl.count - t_start, t_start, tl.count - 1, badsteps))
    try:
        g = tl.timelineGroups.add(t_start, tl.count - 1)
        g.name = 'Front r8 - mic pocket (built in Fusion; its size: %s)' % PARAM
        print('grouped as: %s' % g.name)
    except Exception as ex:
        print('(not grouped: %s)' % ex)
    des.activateRootComponent()
    print('active component: %s | modified %s' % (des.activeComponent.name, adsk.core.Application.get().activeDocument.isModified))
