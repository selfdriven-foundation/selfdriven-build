# MK-I r8 draft - THE POWER BUTTON'S LEVER, built in Fusion (2026-10-08). The owner: "why cloud? why not fusion?".
# r7's lever (mk1_body_r7.lever(): six blind reviews) with its tip set to the switch's TRUE place - no gauge reading:
#   the tip's gap to the button at rest = the named number button_lever_gap (1.0 mm, r7's design value); the button's tip
#   by Raspberry Pi's drawing is at x -27.6, so the lever's tip is at x = -27.6 - gap. Smaller gap = the click comes sooner.
#   The tip's centre along the wall and in height: y -67.6, z 33.7 (the middle of the button's range; z as high as r7 allows).
# A NEW component inside the r8 item (r7's lever there is a copy shared with the r7 item: it is not touched).
# Every step is checked against the lever made in the cloud (mk1_lever_r8fix.py, the same numbers): 771.407 mm3 for a gap of 1.0.
# r7's 45 degree edge on the tip toward the body's mouth is NOT built: with this tip the rounded tip already lies inside it for
# every gap from 0 to 2.5 (measured in the cloud) - the cut would take nothing, and an empty cut is a failed step in Fusion.
import adsk.core, adsk.fusion, math, traceback

ITEM = 'BUILT IN FUSION'
COMP_NAME = 'Power lever r8 - tip set to the true switch place (built in Fusion)'
BODY = 'Power lever (print this - PETG)'
PARAM = 'button_lever_gap'
PARAM_NOTE = ("Gap between the power lever's tip and the button when nobody presses it (button by Raspberry Pi's drawing). "
              "Smaller = the click comes sooner. 1.0 is the design value; it works from about 0.3 to 2.0.")
TIP_X = -27.6
NOSE_Y, NOSE_Z = -67.6, 33.7
X_SEAT, X_AXIS, XL = -37.0, -37.5, -38.0
Z0, Z1, PAD_Z0, BED = 25.3, 35.7, 28.9, 0.2
Y0, Y1 = -69.7, -44.8
HEAD_Y1, POST_Y1 = -61.8, -63.8
PAD_Y, PAD_H = (-68.6, -63.6), 0.7
FREE_Y, ZF = -60.0, 25.5
ROOT_R = 1.5
SCREW_Y, SCREW_Z = -47.75, 30.6
LEG_W, LEG_Z0, LEG_C, LEG_END, LEG_R, HOLE_D = 4.0, 17.1, 0.3, 0.3, 0.6, 3.2
X_FAR = -24.0
GAP0 = 1.0
# the cloud's lever, step by step (mm3, gap 1.0): what the body must be after each step
WANT = dict(below_pad=313.581, pad=914.814, bed=931.604, tip=752.111, free=747.395, leg=779.295, fillets=779.4495, hole=771.407)
AREA = dict(nopad=87.1059, pad=91.0959)        # mm2, the two outlines

VI = adsk.core.ValueInput.createByString
P = lambda x, y, z: adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)


def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    item = [o for o in des.rootComponent.occurrences if ITEM in o.component.name][0].component
    tl = des.timeline
    old = [o for o in item.occurrences if o.component.name == COMP_NAME]
    if old:
        b = old[0].component.bRepBodies
        print('ALREADY THERE: %s | bodies %s' % (COMP_NAME, [(x.name, round(x.volume * 1000, 3)) for x in b])); return
    made = []
    try:
        build(des, item, tl, made)
    except Exception:
        print('*** STOPPED:\n' + traceback.format_exc())
        print('timeline items made before it stopped: %s' % made)


def build(des, item, tl, made):
    t_start = tl.count
    par = des.userParameters.itemByName(PARAM)
    if not par:
        par = des.userParameters.add(PARAM, VI('%g mm' % GAP0), 'mm', PARAM_NOTE)
    print('named number %s = %s' % (PARAM, par.expression))
    occ = item.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    comp = occ.component
    comp.name = COMP_NAME
    F = comp.features

    def note(obj, name):
        obj.name = name
        made.append(name)
        return obj

    def plane(base, axis, mm, name):
        for sgn in (1, -1):
            pin = comp.constructionPlanes.createInput()
            pin.setByOffset(base, VI('%g mm' % (sgn * mm)))
            pl = comp.constructionPlanes.add(pin)
            o = pl.geometry.origin
            if abs((o.x, o.y, o.z)[axis] * 10.0 - mm) < 1e-6:
                pl.isLightBulbOn = False
                return note(pl, name)
            pl.deleteMe()
        raise RuntimeError('plane %s = %g not made' % ('xyz'[axis], mm))

    def normal(sk):
        n = sk.xDirection.crossProduct(sk.yDirection)
        return (n.x, n.y, n.z)

    def profile_by_area(sk, mm2, tol=0.02):
        best = None
        for pr in sk.profiles:
            a = pr.areaProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).area * 100.0
            if abs(a - mm2) < tol and (best is None or abs(a - mm2) < best[0]):
                best = (abs(a - mm2), pr, a)
        if best is None:
            raise RuntimeError('sketch %s: no profile of %.4f mm2 (have %s)' % (sk.name, mm2, [round(p.areaProperties().area * 100, 4) for p in sk.profiles]))
        return best[1]

    def extrude(prof, dist_mm, along, op, bodies=None, start_mm=None, taper=None, name=None):
        n = normal(prof.parentSketch)
        d = n[0] * along[0] + n[1] * along[1] + n[2] * along[2]
        sg = '' if d > 0 else '-'
        inp = F.extrudeFeatures.createInput(prof, op)
        if start_mm is not None:
            inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI('%s%g mm' % (sg, start_mm)))
        ext = adsk.fusion.DistanceExtentDefinition.create(VI('%s%g mm' % (sg, dist_mm)))
        if taper is None:
            inp.setOneSideExtent(ext, adsk.fusion.ExtentDirections.PositiveExtentDirection)
        else:
            inp.setOneSideExtent(ext, adsk.fusion.ExtentDirections.PositiveExtentDirection, VI(taper))
        if bodies is not None:
            inp.participantBodies = bodies
        f = F.extrudeFeatures.add(inp)
        return note(f, name)

    def lever_body():
        return [b for b in comp.bRepBodies if b.name == BODY][0]

    def check(key, extra=''):
        v = lever_body().volume * 1000.0
        ok = abs(v - WANT[key]) < 0.03
        print('   %-10s body %.4f mm3 (the cloud: %.4f) %s %s' % (key, v, WANT[key], 'ok' if ok else '*** DIFFERS', extra))
        if not ok:
            raise RuntimeError('step %s: %.4f against %.4f' % (key, v, WANT[key]))

    def outline(pl, z, pad, name):
        sk = note(comp.sketches.add(pl), name)
        S = lambda x, y: sk.modelToSketchSpace(P(x, y, z))
        L = sk.sketchCurves.sketchLines
        gc = sk.geometricConstraints
        xe = TIP_X - GAP0 + 0.5
        pts = [(xe, HEAD_Y1), (X_SEAT, POST_Y1), (X_SEAT, Y1), (XL, Y1)]
        if pad:
            pts += [(XL, PAD_Y[1] + PAD_H), (XL - PAD_H, PAD_Y[1]), (XL - PAD_H, PAD_Y[0]), (XL, PAD_Y[0] - PAD_H)]
        pts += [(XL, Y0), (xe, Y0)]
        sp = [S(*p) for p in pts]
        lines = [L.addByTwoPoints(sp[0], sp[1])]
        for i in range(1, len(sp) - 1):
            lines.append(L.addByTwoPoints(lines[-1].endSketchPoint, sp[i + 1]))
        lines.append(L.addByTwoPoints(lines[-1].endSketchPoint, lines[0].startSketchPoint))
        slant, upright, bottom, front = lines[0], lines[1], lines[-2], lines[-1]
        for ln in lines[1:-2]:                     # every corner but the two at the tip end, and the post's root (it gets the fillet)
            ln.endSketchPoint.isFixed = True
        gc.addVertical(upright)
        gc.addHorizontal(bottom)
        gc.addVertical(front)
        root = sk.sketchPoints.add(S(X_SEAT, POST_Y1)); root.isFixed = True          # the post's root corner, before the fillet
        gc.addCoincident(root, slant)
        guide = L.addByTwoPoints(S(-40.0, HEAD_Y1), S(-20.0, HEAD_Y1)); guide.isConstruction = True; guide.isFixed = True
        gc.addCoincident(slant.startSketchPoint, guide)
        dim = sk.sketchDimensions.addDistanceDimension(root, slant.startSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, S(-33.0, HEAD_Y1 + 3.0))
        dim.parameter.expression = '%g mm - %s' % (TIP_X - X_SEAT + 0.5, PARAM)
        arc = sk.sketchCurves.sketchArcs.addFillet(slant, slant.endSketchPoint.geometry, upright, upright.startSketchPoint.geometry, ROOT_R / 10.0)
        rd = sk.sketchDimensions.addRadialDimension(arc, S(-35.0, POST_Y1 + 3.0))
        rd.parameter.expression = '%g mm' % ROOT_R
        pr = profile_by_area(sk, AREA['pad' if pad else 'nopad'])
        print('   sketch %s: %d profile(s), the outline %.4f mm2 (the cloud: %.4f), fully tied down %s, tip end at x %.3f' % (
            name, sk.profiles.count, pr.areaProperties().area * 100, AREA['pad' if pad else 'nopad'], sk.isFullyConstrained,
            sk.sketchToModelSpace(slant.startSketchPoint.geometry).x * 10))
        return sk, pr

    # ---- 1 the leaf and the pin, below the press pad (z 25.3 .. 28.9)
    p_z0 = plane(comp.xYConstructionPlane, 2, Z0, "Lever - plane z 25.3 (the leaf's lower edge)")
    s1, pr1 = outline(p_z0, Z0, False, 'Lever - outline below the press pad (sketch)')
    e1 = extrude(pr1, PAD_Z0 - Z0, (0, 0, 1), adsk.fusion.FeatureOperations.NewBodyFeatureOperation, name='Lever - leaf and pin, below the press pad')
    e1.bodies.item(0).name = BODY
    check('below_pad')
    # ---- 2 with the press pad (z 28.9 .. 35.5), and the last 0.2 at 45 deg (the face that lies on the printer's bed)
    p_pad = plane(comp.xYConstructionPlane, 2, PAD_Z0, "Lever - plane z 28.9 (the press pad's lower edge)")
    s2, pr2 = outline(p_pad, PAD_Z0, True, 'Lever - outline with the press pad (sketch)')
    extrude(pr2, Z1 - BED - PAD_Z0, (0, 0, 1), adsk.fusion.FeatureOperations.JoinFeatureOperation, bodies=[lever_body()], name='Lever - leaf, pin and press pad')
    check('pad')
    for tap in ('-45 deg', '45 deg'):
        eb = extrude(s2.profiles.item(0) if s2.profiles.count == 1 else profile_by_area(s2, AREA['pad']), BED, (0, 0, 1),
                     adsk.fusion.FeatureOperations.JoinFeatureOperation, bodies=[lever_body()], start_mm=Z1 - BED - PAD_Z0, taper=tap,
                     name="Lever - 45 deg edge round the face that lies on the printer's bed")
        v = lever_body().volume * 1000.0
        if abs(v - WANT['bed']) < 0.05:
            break
        print('   taper %s gave %.4f - the other way' % (tap, v))
        made.remove(eb.name); eb.deleteMe()
    check('bed')
    # ---- 3 the rounded tip: a ball about a point in the leaf's middle plane, radius = the tip's distance from that plane
    p_nz = plane(comp.xYConstructionPlane, 2, NOSE_Z, "Lever - plane at the height of the tip's centre")
    s3 = note(comp.sketches.add(p_nz), "Lever - ball for the rounded tip (sketch)")
    S3 = lambda x, y: s3.modelToSketchSpace(P(x, y, NOSE_Z))
    r0 = TIP_X - GAP0 - X_AXIS
    c3 = s3.sketchPoints.add(S3(X_AXIS, NOSE_Y)); c3.isFixed = True
    arc3 = s3.sketchCurves.sketchArcs.addByThreePoints(S3(X_AXIS - r0, NOSE_Y), S3(X_AXIS, NOSE_Y + r0), S3(X_AXIS + r0, NOSE_Y))
    ax3 = s3.sketchCurves.sketchLines.addByTwoPoints(arc3.startSketchPoint, arc3.endSketchPoint)
    g3 = s3.geometricConstraints
    g3.addCoincident(arc3.centerSketchPoint, c3)
    g3.addHorizontal(ax3)
    g3.addCoincident(c3, ax3)
    rd3 = s3.sketchDimensions.addRadialDimension(arc3, S3(X_AXIS, NOSE_Y + r0 + 2.0))
    rd3.parameter.expression = '%g mm - %s' % (TIP_X - X_AXIS, PARAM)
    pr3 = profile_by_area(s3, math.pi * r0 * r0 / 2.0, 0.05)
    rin = F.revolveFeatures.createInput(pr3, ax3, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    rin.setAngleExtent(False, VI('360 deg'))
    rv = note(F.revolveFeatures.add(rin), 'Lever - ball for the rounded tip (helper)')
    ball = rv.bodies.item(0); ball.name = 'tip ball (helper)'
    print('   ball: radius %.4f mm, volume %.4f mm3 (a sphere of %.2f: %.4f)' % (rd3.parameter.value * 10, ball.volume * 1000, r0, 4.0 / 3.0 * math.pi * r0 ** 3))
    # the box round the tip: from 7 mm behind the tip's front to beyond it
    p_low = plane(comp.xYConstructionPlane, 2, Z0 - 1.0, 'Lever - plane z 24.3 (under the leaf)')
    s4 = note(comp.sketches.add(p_low), 'Lever - box round the tip (sketch)')
    S4 = lambda x, y: s4.modelToSketchSpace(P(x, y, Z0 - 1.0))
    xb = TIP_X - GAP0 - 7.0
    rect = s4.sketchCurves.sketchLines.addTwoPointRectangle(S4(xb, Y0 - 1.0), S4(X_FAR, HEAD_Y1 + 1.0))
    far = [ln for ln in rect if abs(s4.sketchToModelSpace(ln.startSketchPoint.geometry).x * 10 - X_FAR) < 1e-6 and abs(s4.sketchToModelSpace(ln.endSketchPoint.geometry).x * 10 - X_FAR) < 1e-6][0]
    far.startSketchPoint.isFixed = True; far.endSketchPoint.isFixed = True
    near = [ln for ln in rect if abs(s4.sketchToModelSpace(ln.startSketchPoint.geometry).x * 10 - xb) < 1e-6 and abs(s4.sketchToModelSpace(ln.endSketchPoint.geometry).x * 10 - xb) < 1e-6][0]
    d4 = s4.sketchDimensions.addDistanceDimension(near.startSketchPoint, far.startSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, S4((xb + X_FAR) / 2, Y0 - 3.0))
    d4.parameter.expression = '%g mm + %s' % (X_FAR - (TIP_X - 7.0), PARAM)
    pr4 = profile_by_area(s4, (X_FAR - xb) * (HEAD_Y1 - Y0 + 2.0), 0.05)
    e4 = extrude(pr4, Z1 - Z0 + 2.0, (0, 0, 1), adsk.fusion.FeatureOperations.NewBodyFeatureOperation, name='Lever - box round the tip (helper)')
    cutter = e4.bodies.item(0); cutter.name = 'tip cutter (helper)'
    tools = adsk.core.ObjectCollection.create(); tools.add(ball)
    ci = F.combineFeatures.createInput(cutter, tools); ci.operation = adsk.fusion.FeatureOperations.CutFeatureOperation; ci.isKeepToolBodies = False
    note(F.combineFeatures.add(ci), 'Lever - tip cutter = the box less the ball')
    tools = adsk.core.ObjectCollection.create(); tools.add([b for b in comp.bRepBodies if b.name == 'tip cutter (helper)'][0])
    ci = F.combineFeatures.createInput(lever_body(), tools); ci.operation = adsk.fusion.FeatureOperations.CutFeatureOperation; ci.isKeepToolBodies = False
    note(F.combineFeatures.add(ci), 'Lever - rounded tip (its gap to the button: %s)' % PARAM)
    check('tip')
    # ---- 4 the free end's lower edge 0.2 higher than the tongue's (1.1 to the window's sill)
    s5 = note(comp.sketches.add(p_low), "Lever - free end's lower edge (sketch)")
    S5 = lambda x, y: s5.modelToSketchSpace(P(x, y, Z0 - 1.0))
    r5 = s5.sketchCurves.sketchLines.addTwoPointRectangle(S5(XL - PAD_H - 1.0, Y0 - 1.0), S5(X_FAR, FREE_Y))
    for ln in r5:
        ln.startSketchPoint.isFixed = True; ln.endSketchPoint.isFixed = True
    extrude(profile_by_area(s5, (X_FAR - (XL - PAD_H - 1.0)) * (FREE_Y - Y0 + 1.0), 0.05), ZF - (Z0 - 1.0), (0, 0, 1),
            adsk.fusion.FeatureOperations.CutFeatureOperation, bodies=[lever_body()], name='Lever - free end 0.2 higher (clear of the sill)')
    check('free')
    # ---- 5 the leg: it lies in the channel down the wall and sets the lever's angle; its two inner edges bevelled 0.3
    p_leg = plane(comp.xYConstructionPlane, 2, LEG_Z0, "Lever - plane z 17.1 (the leg's end)")
    s6 = note(comp.sketches.add(p_leg), 'Lever - leg (sketch)')
    S6 = lambda x, y: s6.modelToSketchSpace(P(x, y, LEG_Z0))
    ya, yb, c = SCREW_Y - LEG_W / 2, SCREW_Y + LEG_W / 2, LEG_C
    q = [(XL, ya), (X_SEAT - c, ya), (X_SEAT, ya + c), (X_SEAT, yb - c), (X_SEAT - c, yb), (XL, yb)]
    L6 = s6.sketchCurves.sketchLines
    prev = L6.addByTwoPoints(S6(*q[0]), S6(*q[1])); first = prev
    for k in range(2, len(q)):
        prev = L6.addByTwoPoints(prev.endSketchPoint, S6(*q[k]))
    L6.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)
    for ln in L6:
        ln.startSketchPoint.isFixed = True; ln.endSketchPoint.isFixed = True
    extrude(profile_by_area(s6, LEG_W * (X_SEAT - XL) - c * c, 0.005), Z0 - LEG_Z0 + 0.01, (0, 0, 1),
            adsk.fusion.FeatureOperations.JoinFeatureOperation, bodies=[lever_body()], name="Lever - leg (sets the lever's angle in its channel)")
    p_lb = plane(comp.xZConstructionPlane, 1, ya - 0.1, 'Lever - plane across the leg')
    s7 = note(comp.sketches.add(p_lb), "Lever - leg's end bevel (sketch)")
    S7 = lambda x, z: s7.modelToSketchSpace(P(x, ya - 0.1, z))
    e = LEG_END
    t7 = [(X_SEAT - e - 0.01, LEG_Z0 - 0.01), (X_SEAT + 0.01, LEG_Z0 - 0.01), (X_SEAT + 0.01, LEG_Z0 + e + 0.01)]
    L7 = s7.sketchCurves.sketchLines
    a7 = L7.addByTwoPoints(S7(*t7[0]), S7(*t7[1])); b7 = L7.addByTwoPoints(a7.endSketchPoint, S7(*t7[2])); L7.addByTwoPoints(b7.endSketchPoint, a7.startSketchPoint)
    for ln in L7:
        ln.startSketchPoint.isFixed = True; ln.endSketchPoint.isFixed = True
    extrude(profile_by_area(s7, (e + 0.02) ** 2 / 2.0, 0.002), LEG_W + 0.2, (0, 1, 0),
            adsk.fusion.FeatureOperations.CutFeatureOperation, bodies=[lever_body()], name="Lever - leg's end bevelled 0.3 (the edge that goes in first)")
    check('leg')
    # ---- 6 fillets R 0.6 where the leg leaves the tongue (printed on its side the leg is loaded across its layers)
    p_out = plane(comp.yZConstructionPlane, 0, XL, "Lever - plane on the leaf's outer face")
    s8 = note(comp.sketches.add(p_out), 'Lever - leg root fillets (sketch)')
    S8 = lambda y, z: s8.modelToSketchSpace(P(XL, y, z))
    L8 = s8.sketchCurves.sketchLines
    for ys, sg in ((ya, -1), (yb, 1)):
        r8 = L8.addTwoPointRectangle(S8(ys + sg * LEG_R, Z0 - LEG_R), S8(ys, Z0 + 0.01))
        for ln in r8:
            ln.startSketchPoint.isFixed = True; ln.endSketchPoint.isFixed = True
        cc = s8.sketchCurves.sketchCircles.addByCenterRadius(S8(ys + sg * LEG_R, Z0 - LEG_R), LEG_R / 10.0)
        cc.centerSketchPoint.isFixed = True
    fil = [pr for pr in s8.profiles if abs(pr.areaProperties().area * 100 - (LEG_R * (LEG_R + 0.01) - math.pi * LEG_R ** 2 / 4.0)) < 0.002]
    if len(fil) != 2:
        raise RuntimeError('leg fillets: %d profiles of the right size (want 2): %s' % (len(fil), [round(p.areaProperties().area * 100, 4) for p in s8.profiles]))
    col = adsk.core.ObjectCollection.create()
    for pr in fil:
        col.add(pr)
    n8 = normal(s8)
    inp8 = F.extrudeFeatures.createInput(col, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    inp8.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI('%s%g mm' % ('' if n8[0] > 0 else '-', X_SEAT - XL))), adsk.fusion.ExtentDirections.PositiveExtentDirection)
    inp8.participantBodies = [lever_body()]
    note(F.extrudeFeatures.add(inp8), "Lever - leg root fillets R 0.6")
    check('fillets')
    # ---- 7 the screw hole, 3.2 (0.1 of play round an M3)
    s9 = note(comp.sketches.add(p_out), 'Lever - screw hole (sketch)')
    S9 = lambda y, z: s9.modelToSketchSpace(P(XL, y, z))
    h9 = s9.sketchCurves.sketchCircles.addByCenterRadius(S9(SCREW_Y, SCREW_Z), HOLE_D / 20.0)
    h9.centerSketchPoint.isFixed = True
    s9.sketchDimensions.addDiameterDimension(h9, S9(SCREW_Y + 3.0, SCREW_Z + 3.0)).parameter.expression = '%g mm' % HOLE_D
    extrude(profile_by_area(s9, math.pi * (HOLE_D / 2) ** 2, 0.005), X_SEAT - XL + 1.0, (1, 0, 0),
            adsk.fusion.FeatureOperations.CutFeatureOperation, bodies=[lever_body()], name='Lever - screw hole 3.2')
    check('hole')
    # ---- tidy: helpers gone? one body; every step healthy; one group in the timeline
    bodies = [(b.name, round(b.volume * 1000, 4)) for b in comp.bRepBodies]
    bad = [(tl.item(i).name, tl.item(i).healthState) for i in range(t_start, tl.count) if not tl.item(i).isGroup and tl.item(i).healthState != 0]
    lb = lever_body().boundingBox
    print('bodies in the new component: %s' % bodies)
    print('lever spans x %.3f .. %.3f, y %.3f .. %.3f, z %.3f .. %.3f (tip at x %.3f = %.1f - gap)' % (
        lb.minPoint.x * 10, lb.maxPoint.x * 10, lb.minPoint.y * 10, lb.maxPoint.y * 10, lb.minPoint.z * 10, lb.maxPoint.z * 10, lb.maxPoint.x * 10, TIP_X))
    print('timeline: %d new steps (%d .. %d); not healthy: %s' % (tl.count - t_start, t_start, tl.count - 1, bad))
    try:
        g = tl.timelineGroups.add(t_start, tl.count - 1)
        g.name = 'Power lever r8 (built in Fusion; its gap to the button: %s)' % PARAM
        print('grouped as: %s' % g.name)
    except Exception as ex:
        print('(not grouped: %s)' % ex)
