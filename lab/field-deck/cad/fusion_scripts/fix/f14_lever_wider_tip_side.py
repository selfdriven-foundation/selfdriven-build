# f14 - MK-I r8 draft - THE POWER LEVER (f12 + f12e): the blind review's SHOULD FIX, 2026-10-08.
# Pressed, the post turns and the point that touches the button runs round the rounded tip toward the free end (-y). The tip's
# centre was only 2.1 from the post's -y side: the ball ran out at 13.65 deg (2.80 mm of travel), short of the 2.90 the deepest
# switch place asks. Now, BEYOND THE WALL only (from x -34.0, by a 45 deg step), the post's -y side is 0.5 further out, at
# y -70.2: the ball runs out at 16.99 deg (3.49 mm), 0.59 to spare (r7's rule 0.3). Inside the wall's thickness nothing
# changes (the leaf's end stays 0.8 from the window's end). Tried first in the cloud: mk1_lever_r8fix2.py + its check.
# What this script does, in this order:
#   A. the 45 deg edge toward the body's mouth (f12e) starts at y -70.6, not -70.2 (its plane moved, its length 8.9 -> 9.3):
#      at -70.2 it would lie ON the new face. With the lever as it is this changes nothing (checked: the volume stays).
#   B. with the marker just after the bed-face edge (f12), a block for the wider side is added - a sketch on the plane
#      z 25.3, extruded to z 35.5, and its last 0.2 at 45 deg like the rest of the bed face - BEFORE the tip is cut, so the
#      rounded tip, its 45 deg edge and the free end's lower edge all shape it as they shape the rest.
#   C. back to the end; every step healthy; volume against the cloud for the gap at 1.0, 0.3, 0.5, 2.0 (then back to 1.0).
# Safe to run twice: it stops with ALREADY THERE. It does not save the file (the owner saves).
import adsk.core, adsk.fusion, math, traceback

ITEM = 'BUILT IN FUSION'
COMP = 'Power lever r8 - tip set to the true switch place (built in Fusion)'
BODY = 'Power lever (print this - PETG)'
PARAM = 'button_lever_gap'
BED_STEP = "Lever - 45 deg edge round the face that lies on the printer's bed"
Z_PLANE = "Lever - plane z 25.3 (the leaf's lower edge)"
EDGE_PLANE = "Lever - plane at the tip's far side (y -70.2)"
EDGE_PLANE_NEW = "Lever - plane at the tip's far side (y -70.6, clear of the wider side's face)"
EDGE_EXT = "Lever - 45 deg edge of the tip (helper)"
SK_NAME = "Lever - the post's side toward the free end, 0.5 further out beyond the wall (sketch)"
EX_NAME = "Lever - the post's side toward the free end, 0.5 further out beyond the wall (blind review)"
TP_NAME = "Lever - 45 deg edge round the bed face, on the wider side"
Z0, Z1, BED = 25.3, 35.7, 0.2
Y0, FACE_Y, STEP_X, EXT_X1, EXT_Y1 = -69.7, -70.2, -34.0, -26.0, -69.2
HEAD_Y1 = -61.8
EDGE_Y_OLD, EDGE_Y_NEW = -70.2, -70.6
VOL_NOW = 771.4188                              # Fusion's lever after f12 + f12e, gap 1.0
VOL_BED = 931.604                               # f12's WANT just after the bed-face edge
D_EXT, D_TAPER = 50.2350, 0.8864                # what the two new steps add there (the cloud)
WANT = {'1 mm': 789.5291, '0.3 mm': 853.5709, '0.5 mm': 835.8230, '2 mm': 690.6873}    # mk1_lever_r8fix2.lever2() for each gap
FIRST = {'1 mm': 771.4070, '0.3 mm': 831.0942, '0.5 mm': 814.5986, '2 mm': 678.1816}   # ... and without the wider side (f12e's)
AREA = 7.8750                                   # mm2, the block's outline
VI = adsk.core.ValueInput.createByString
P = lambda x, y, z: adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)


def all_items(tl):
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
    lever = lambda: [b for b in comp.bRepBodies if b.name == BODY][0]
    if [f for f in F.extrudeFeatures if f.name == EX_NAME]:
        print('ALREADY THERE: %s | lever %.4f mm3 | %s = %s' % (EX_NAME, lever().volume * 1000, PARAM, par.expression)); return
    if abs(par.value - 0.1) > 1e-9:
        print('*** %s is %s, not 1 mm - set it back first' % (PARAM, par.expression)); return
    v0 = lever().volume * 1000
    if abs(v0 - VOL_NOW) > 0.03:
        print('*** the lever is %.4f mm3, not %.4f (f12 + f12e): not the state this script was made for - nothing done' % (v0, VOL_NOW)); return
    groups = []
    for i in range(tl.count):                           # steps inside a COLLAPSED group cannot be rolled to: open it first
        it = tl.item(i)
        if it.isGroup:
            g_ = adsk.fusion.TimelineGroup.cast(it)
            if g_.name.startswith('Power lever r8') and g_.isCollapsed:
                g_.isCollapsed = False; groups.append(g_)
    bad = [(t.name, t.healthState) for t in all_items(tl) if t.healthState != 0]
    print('start: lever %.4f mm3; groups opened %d; steps %d; not healthy %s' % (v0, len(groups), len(all_items(tl)), bad))
    if bad:
        raise RuntimeError('a step is not healthy before anything was done')

    # ---- A. the 45 deg edge's plane to y -70.6, its length to 9.3
    pls = [p for p in comp.constructionPlanes if p.name in (EDGE_PLANE, EDGE_PLANE_NEW)]
    exs = [f for f in F.extrudeFeatures if f.name == EDGE_EXT]
    if len(pls) != 1 or len(exs) != 1:
        raise RuntimeError('A: found %d planes named %r and %d steps named %r' % (len(pls), EDGE_PLANE, len(exs), EDGE_EXT))
    pl, ex = pls[0], exs[0]
    off = adsk.fusion.ConstructionPlaneOffsetDefinition.cast(pl.definition).offset
    dst = adsk.fusion.DistanceExtentDefinition.cast(ex.extentOne).distance
    y_now, len_now = pl.geometry.origin.y * 10, abs(dst.value * 10)
    print('A: plane offset %s (y %.3f) | edge length %s' % (off.expression, y_now, dst.expression))
    s_off = 1.0 if off.value > 0 else -1.0
    s_dst = 1.0 if dst.value > 0 else -1.0
    if abs(y_now - EDGE_Y_NEW) < 1e-6 and abs(len_now - (HEAD_Y1 + 0.5 - EDGE_Y_NEW)) < 1e-6:
        print('A: already done by a run before this one')        # a run that stopped after A (lesson 4: safe to run twice)
    elif abs(y_now - EDGE_Y_OLD) < 1e-6 and abs(len_now - (HEAD_Y1 + 0.5 - EDGE_Y_OLD)) < 1e-6:
        off.expression = '%g mm' % (s_off * abs(EDGE_Y_NEW))
        dst.expression = '%g mm' % (s_dst * (HEAD_Y1 + 0.5 - EDGE_Y_NEW))
        adsk.doEvents()
        if abs(pl.geometry.origin.y * 10 - EDGE_Y_NEW) > 1e-6:
            off.expression = '%g mm' % (s_off * abs(EDGE_Y_OLD)); dst.expression = '%g mm' % (s_dst * (HEAD_Y1 + 0.5 - EDGE_Y_OLD))
            raise RuntimeError('A: the plane went to y %.3f, not %.1f - put back' % (pl.geometry.origin.y * 10, EDGE_Y_NEW))
    else:
        raise RuntimeError('A: the plane or the length is neither what f12e made nor what this script makes')
    pl.name = EDGE_PLANE_NEW
    te = [t for t in all_items(tl) if t.name == EDGE_EXT]
    if len(te) != 1:
        raise RuntimeError('A: %d timeline steps named %r' % (len(te), EDGE_EXT))
    te[0].rollTo(False)                                 # look at the helper itself before it is joined (found as f12e found its step)
    hb = [b for b in comp.bRepBodies if b.name == 'tip edge (helper)']
    hbb = hb[0].boundingBox if hb else None
    tl.moveToEnd(); adsk.doEvents()
    v1 = lever().volume * 1000
    bad = [(t.name, t.healthState) for t in all_items(tl) if t.healthState != 0]
    print('A: plane at y %.3f; the helper spans y %s; lever %.4f mm3 (was %.4f); not healthy %s' % (
        pl.geometry.origin.y * 10, ('%.3f .. %.3f' % (hbb.minPoint.y * 10, hbb.maxPoint.y * 10)) if hbb else 'NOT FOUND', v1, v0, bad))
    if not hbb or abs(hbb.minPoint.y * 10 - EDGE_Y_NEW) > 1e-4 or abs(hbb.maxPoint.y * 10 - (HEAD_Y1 + 0.5)) > 1e-4 or abs(v1 - v0) > 0.005 or bad:
        raise RuntimeError('A: not as meant (see the line above)')

    # ---- B. the wider side, before the tip is cut
    found = [t for t in all_items(tl) if t.name == BED_STEP]
    if len(found) != 1:
        raise RuntimeError('B: %d steps named %r' % (len(found), BED_STEP))
    found[0].rollTo(False)
    vb = lever().volume * 1000
    print('B: marker after "%s" (%d); lever there %.4f mm3 (f12: %.3f)' % (BED_STEP, tl.markerPosition, vb, VOL_BED))
    if abs(vb - VOL_BED) > 0.03:
        tl.moveToEnd(); raise RuntimeError('B: the lever before the tip is cut is not what f12 made')
    zp = [p for p in comp.constructionPlanes if p.name == Z_PLANE]
    if len(zp) != 1:
        tl.moveToEnd(); raise RuntimeError('B: %d planes named %r' % (len(zp), Z_PLANE))
    sk = comp.sketches.add(zp[0]); sk.name = SK_NAME
    S = lambda x, y: sk.modelToSketchSpace(P(x, y, Z0))
    L = sk.sketchCurves.sketchLines
    q = [(STEP_X, EXT_Y1), (STEP_X, Y0), (STEP_X + (Y0 - FACE_Y), FACE_Y), (EXT_X1, FACE_Y), (EXT_X1, EXT_Y1)]
    first = prev = L.addByTwoPoints(S(*q[0]), S(*q[1]))
    for k in range(2, len(q)):
        prev = L.addByTwoPoints(prev.endSketchPoint, S(*q[k]))
    L.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)
    for ln in L:
        ln.startSketchPoint.isFixed = True; ln.endSketchPoint.isFixed = True
    prs = [p for p in sk.profiles if abs(p.areaProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).area * 100 - AREA) < 0.005]
    print('   sketch: %d profile(s) %s mm2 (want %.4f), fully tied down %s' % (sk.profiles.count, [round(p.areaProperties().area * 100, 4) for p in sk.profiles], AREA, sk.isFullyConstrained))
    if len(prs) != 1:
        tl.moveToEnd(); raise RuntimeError('B: the sketch is not what was meant')
    n = sk.xDirection.crossProduct(sk.yDirection)
    sg = '' if n.z > 0 else '-'
    inp = F.extrudeFeatures.createInput(prs[0], adsk.fusion.FeatureOperations.JoinFeatureOperation)
    inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI('%s%g mm' % (sg, Z1 - BED - Z0))), adsk.fusion.ExtentDirections.PositiveExtentDirection)
    inp.participantBodies = [lever()]
    e1 = F.extrudeFeatures.add(inp); e1.name = EX_NAME
    v2 = lever().volume * 1000
    print('   %s: +%.4f mm3 (the cloud: +%.4f)' % (EX_NAME, v2 - vb, D_EXT))
    if abs(v2 - vb - D_EXT) > 0.03:
        tl.moveToEnd(); raise RuntimeError('B: the block did not add what the cloud says')
    e2 = None
    for tap in ('-45 deg', '45 deg'):
        inp = F.extrudeFeatures.createInput(prs[0], adsk.fusion.FeatureOperations.JoinFeatureOperation)
        inp.startExtent = adsk.fusion.OffsetStartDefinition.create(VI('%s%g mm' % (sg, Z1 - BED - Z0)))
        inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(VI('%s%g mm' % (sg, BED))), adsk.fusion.ExtentDirections.PositiveExtentDirection, VI(tap))
        inp.participantBodies = [lever()]
        e2 = F.extrudeFeatures.add(inp); e2.name = TP_NAME
        v3 = lever().volume * 1000
        if abs(v3 - v2 - D_TAPER) < 0.03:
            break
        print('   taper %s added %.4f - the other way' % (tap, v3 - v2))
        e2.deleteMe(); e2 = None
    if e2 is None:
        tl.moveToEnd(); raise RuntimeError('B: the bed-face edge on the block did not come out')
    print('   %s: +%.4f mm3 (the cloud: +%.4f)' % (TP_NAME, v3 - v2, D_TAPER))

    # ---- C. to the end; check; the named number tried
    tl.moveToEnd(); adsk.doEvents()
    lb = lever()
    bb = lb.boundingBox
    bad = [(t.name, t.healthState) for t in all_items(tl) if t.healthState != 0]
    print('C: lever %.4f mm3 (the cloud %.4f; Fusion\'s first lever was 0.012 over the cloud\'s) | spans x %.3f .. %.3f, y %.3f .. %.3f, z %.3f .. %.3f | bodies %s | not healthy %s' % (
        lb.volume * 1000, WANT['1 mm'], bb.minPoint.x * 10, bb.maxPoint.x * 10, bb.minPoint.y * 10, bb.maxPoint.y * 10, bb.minPoint.z * 10, bb.maxPoint.z * 10,
        [b.name for b in comp.bRepBodies], bad))
    for e in ('0.3 mm', '0.5 mm', '2 mm', '1 mm'):
        par.expression = e
        adsk.doEvents()
        lb = lever()
        bad = [(t.name[:40], t.healthState) for t in all_items(tl) if t.healthState != 0]
        print('   gap %-6s lever %.4f mm3, the cloud %.4f, difference %+.4f (first lever %.4f) | tip x %.3f | lowest y %.3f | not healthy %s' % (
            e, lb.volume * 1000, WANT[e], lb.volume * 1000 - WANT[e], FIRST[e], lb.boundingBox.maxPoint.x * 10, lb.boundingBox.minPoint.y * 10, bad))
    print('parameter back to', par.expression)
    for g_ in groups:
        g_.isCollapsed = True
    print('group closed again: %d | steps in the timeline (groups opened) %d' % (len(groups), len(all_items(tl))))
