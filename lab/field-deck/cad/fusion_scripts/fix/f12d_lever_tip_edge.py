# f12d (= f12b, the step found by name, inside the timeline group). MK-I r8 draft - THE POWER LEVER (f12), one step added (2026-10-08): r7's 45 degree edge on the tip, toward the body's mouth.
# f12 left it out on a wrong test: the cloud check intersected the FINISHED lever (edge already cut) with the edge's region and
# found nothing. Measured properly it takes nothing for a gap of 0.9 or more, but 0.07 mm3 at 0.8, 0.55 at 0.5, 1.14 at 0.3,
# 2.44 at 0 - found when the named number was tried at 0.5 (Fusion 815.161, r7 814.599).
# It goes INTO the tip cutter (joined to it), not as a cut of its own: for gaps of 0.9 and more it takes nothing, and a cut
# that takes nothing is a failed step in Fusion. The join is right for every gap: the edge's region lies inside the cutter's box.
# Also: the two ends of the construction line that holds the tip end's corner at y -61.8 are fixed (the sketches read
# "not fully tied down" for those two points only).
import adsk.core, adsk.fusion, math, traceback

ITEM = 'BUILT IN FUSION'
COMP = 'Power lever r8 - tip set to the true switch place (built in Fusion)'
BODY = 'Power lever (print this - PETG)'
PARAM = 'button_lever_gap'
TIP_X, NOSE_CH, ZF, Y0, HEAD_Y1, X_FAR = -27.6, 4.5, 25.5, -69.7, -61.8, -24.0
C1 = 'Lever - tip cutter = the box less the ball'
NEW = "Lever - tip cutter + its 45 deg edge toward the body's mouth"
R7 = {'0.3 mm': 831.0942, '0.5 mm': 814.5986, '2 mm': 678.1816, '1 mm': 771.4070}     # mk1_body_r7.lever(), nose y -67.6, z 33.7
VI = adsk.core.ValueInput.createByString
P = lambda x, y, z: adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)


def all_items(tl):
    """every step of the timeline, with the steps inside groups (a group itself reads health 5)"""
    out = []
    for i in range(tl.count):
        it = tl.item(i)
        if it.isGroup:
            grp = adsk.fusion.TimelineGroup.cast(it)
            out += [grp.item(j) for j in range(grp.count)]
        else:
            out.append(it)
    return out


def run(context):
    try:
        go()
    except Exception:
        print('*** STOPPED:\n' + traceback.format_exc())


def go():
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    tl = des.timeline
    item = [o for o in des.rootComponent.occurrences if ITEM in o.component.name][0].component
    comp = [o for o in item.occurrences if o.component.name == COMP][0].component
    F = comp.features
    par = des.userParameters.itemByName(PARAM)
    if abs(par.value - 0.1) > 1e-9:
        print('*** %s is %s, not 1 mm - set it back first' % (PARAM, par.expression)); return
    if [f for f in F.combineFeatures if f.name == NEW]:
        print('ALREADY THERE:', NEW); return
    # fix the guide lines' end points
    nfix = 0
    for sk in comp.sketches:
        if sk.name.startswith('Lever - outline'):
            for ln in sk.sketchCurves.sketchLines:
                if ln.isConstruction:
                    for p in (ln.startSketchPoint, ln.endSketchPoint):
                        if not p.isFixed:
                            p.isFixed = True; nfix += 1
            print('   %s: fully tied down %s' % (sk.name, sk.isFullyConstrained))
    print('guide points fixed: %d' % nfix)
    found = []
    for i in range(tl.count):                           # the lever's steps sit inside a timeline GROUP: look inside groups too
        it = tl.item(i)
        if it.isGroup:
            grp = adsk.fusion.TimelineGroup.cast(it)
            for j in range(grp.count):
                if grp.item(j).name == C1:
                    found.append(grp.item(j))
        elif it.name == C1:
            found.append(it)
    if len(found) != 1:
        raise RuntimeError('timeline: %d steps named %r' % (len(found), C1))
    t_before = tl.count
    found[0].rollTo(False)                              # the marker just after the cutter is made (f12b: the feature's own
                                                        # timelineObject said "Associated feature is invalid"; f12c: not found at the top level)
    print('marker after "%s": %d' % (C1, tl.markerPosition))
    gap0 = 1.0
    xc = TIP_X - gap0 - NOSE_CH                         # where the 45 deg line leaves the free end's lower edge
    yp = Y0 - 0.5
    pl = None
    for sgn in (1, -1):
        pin = comp.constructionPlanes.createInput()
        pin.setByOffset(comp.xZConstructionPlane, VI('%g mm' % (sgn * yp)))
        cand = comp.constructionPlanes.add(pin)
        if abs(cand.geometry.origin.y * 10.0 - yp) < 1e-6:
            pl = cand; break
        cand.deleteMe()
    pl.name = "Lever - plane at the tip's far side (y -70.2)"; pl.isLightBulbOn = False
    sk = comp.sketches.add(pl); sk.name = "Lever - 45 deg edge of the tip toward the body's mouth (sketch)"
    S = lambda x, z: sk.modelToSketchSpace(P(x, yp, z))
    L = sk.sketchCurves.sketchLines
    q1, q2, q3, q4 = S(xc, ZF - 0.8), S(X_FAR, ZF - 0.8), S(X_FAR, ZF + (X_FAR - xc)), S(xc, ZF)
    bot = L.addByTwoPoints(q1, q2); rgt = L.addByTwoPoints(bot.endSketchPoint, q3)
    sla = L.addByTwoPoints(rgt.endSketchPoint, q4); lft = L.addByTwoPoints(sla.endSketchPoint, bot.startSketchPoint)
    bot.endSketchPoint.isFixed = True
    gc = sk.geometricConstraints
    gc.addHorizontal(bot); gc.addVertical(rgt); gc.addVertical(lft)
    D = sk.sketchDimensions; H, V = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
    D.addDistanceDimension(bot.startSketchPoint, bot.endSketchPoint, H, S((xc + X_FAR) / 2, ZF - 2.5)).parameter.expression = '%g mm + %s' % (X_FAR - (TIP_X - NOSE_CH), PARAM)
    D.addDistanceDimension(lft.endSketchPoint, lft.startSketchPoint, V, S(xc - 1.5, ZF - 0.4)).parameter.expression = '0.8 mm'
    D.addDistanceDimension(rgt.startSketchPoint, rgt.endSketchPoint, V, S(X_FAR + 1.5, ZF + 4.0)).parameter.expression = '%g mm + %s' % (0.8 + X_FAR - (TIP_X - NOSE_CH), PARAM)
    a_want = 0.8 * (X_FAR - xc) + (X_FAR - xc) ** 2 / 2.0
    prs = [p for p in sk.profiles if abs(p.areaProperties().area * 100 - a_want) < 0.02]
    print('   sketch: %d profile(s), %s mm2 (want %.4f), fully tied down %s' % (sk.profiles.count, [round(p.areaProperties().area * 100, 4) for p in sk.profiles], a_want, sk.isFullyConstrained))
    if len(prs) != 1:
        raise RuntimeError('the edge sketch is not what was meant')
    n = sk.xDirection.crossProduct(sk.yDirection)
    inp = F.extrudeFeatures.createInput(prs[0], adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI('%s%g mm' % ('' if n.y > 0 else '-', HEAD_Y1 + 0.5 - yp))), adsk.fusion.ExtentDirections.PositiveExtentDirection)
    ex = F.extrudeFeatures.add(inp); ex.name = "Lever - 45 deg edge of the tip (helper)"
    edge = ex.bodies.item(0); edge.name = 'tip edge (helper)'
    bb = edge.boundingBox
    print('   edge body y %.3f .. %.3f, x %.3f .. %.3f, z %.3f .. %.3f, %.4f mm3' % (bb.minPoint.y * 10, bb.maxPoint.y * 10, bb.minPoint.x * 10, bb.maxPoint.x * 10, bb.minPoint.z * 10, bb.maxPoint.z * 10, edge.volume * 1000))
    cutter = [b for b in comp.bRepBodies if b.name == 'tip cutter (helper)'][0]
    tools = adsk.core.ObjectCollection.create(); tools.add(edge)
    ci = F.combineFeatures.createInput(cutter, tools); ci.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation; ci.isKeepToolBodies = False
    cj = F.combineFeatures.add(ci); cj.name = NEW
    tl.moveToEnd()
    adsk.doEvents()
    lev = [b for b in comp.bRepBodies if b.name == BODY][0]
    bad = [(t.name, t.healthState) for t in all_items(tl) if t.healthState != 0]
    print('steps in the timeline (groups opened) %d; steps added %d; lever now %.4f mm3 (r7 %.4f); bodies %s; not healthy %s' % (len(all_items(tl)), tl.count - t_before, lev.volume * 1000, R7['1 mm'], [b.name for b in comp.bRepBodies], bad))
    for e in ('0.3 mm', '0.5 mm', '2 mm', '1 mm'):
        par.expression = e
        adsk.doEvents()
        lev = [b for b in comp.bRepBodies if b.name == BODY][0]
        bad = [(t.name[:40], t.healthState) for t in all_items(tl) if t.healthState != 0]
        print('   gap %-6s lever %.4f mm3, r7 %.4f, difference %+.4f | tip x %.3f | not healthy %s' % (e, lev.volume * 1000, R7[e], lev.volume * 1000 - R7[e], lev.boundingBox.maxPoint.x * 10, bad))
    print('parameter back to', par.expression)
