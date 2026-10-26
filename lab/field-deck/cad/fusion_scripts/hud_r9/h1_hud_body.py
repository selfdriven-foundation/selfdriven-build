# h1 - THE HUD POD FOR THE REAL OLED BOARD, built in Fusion (owner: "Yes, build it (Recommended)", 2026-10-12, on the picture
# mk1/shots/MK1_r9_hud_proposal.png). It changes the r8 item's OWN body (r8's copy of r7's body; r7's item is not touched):
# eight steps at the end of the timeline. Each step is a tool solid from the cloud's trial (cad-src/mk1_hud_r9.py, ALL CHECKS
# PASS; cad-src/mk1_hud_r9_fusion_inputs.py wrote them), read from its STEP file (case coordinates, mm), copied into a base
# feature of the item (the imported component is removed again) and combined with the body:
#   1 join  the pod's outline 2.4 longer at the top (facet top 33.7) and the brow 1.0 higher (38.2)            [2 solids]
#   2 cut   the tube x 62.1 .. 90.9, along 1.2 .. 31.2 (R3: 62.5 .. 90.5, 1.2 .. 28.8)
#   3 join  the facet wall filled over R3's window, glass pocket and pilots (x 63 .. 90, along 3.5 .. 26.5, deep 0 .. 2.5)
#   4 join  four posts r 3 at the real holes (x 76.5 -+ 11.68, along 16.52 -+ 11.9); the two lower ones down to the floor  [4]
#   5 cut   the glass pocket 27.9 x 20.68 (deep 1.0 .. 4.2) + the relief over the four solder joints (x 70.8 .. 82.2)
#   6 cut   the window x 64.7 .. 88.3, along 12.0 .. 24.93 (over the lit screen)
#   7 cut   the window's top edge flat at z 19.2 (blind review P: "the chin" began as a 0.08 mm thread)
#   8 cut   four pilots d1.3 for the M1.6x4 screws, deep 1.0 .. 4.3                                              [4]
# Guarded: if one of its steps is there it says ALREADY THERE and changes nothing; if the body is not the one read back
# (116.520846 cm3, 1171 faces) or a probe point is not as the cloud has it before, it stops before changing anything; a tool
# that is not what the cloud wrote (its file's md5, number of solids, volumes, box), a step that is not healthy, or a step whose
# volume change differs from the cloud's by more than 0.03 mm3 stops the script, and everything this run made is taken back
# (newest first), so a second run starts clean. It never saves.
import adsk.core, adsk.fusion, traceback, hashlib

DIR = '/path/to/Field Deck/7 - Next Case/cad-src/fusion_scripts/hud_r9/tools/'
ITEM = 'BUILT IN FUSION'
BODY_PREFIX = 'Body (copy of r7)'
V0_CM3, FACES0 = 116.520846, 1171
TAG = 'HUD r9 - '
GROUP = 'Body r9 - the HUD for the real OLED board (built in Fusion)'
# (file, name, join/cut, solids, tool volume mm3, box (case mm), each solid's volume, the body's change mm3, md5 of the file)
STEPS = [('1_outer_join.step', 'outer', 'join', 2, 2301.6000, [60.0, 70.7532, 21.4026, 93.0, 92.3769, 51.4731], [297.0, 2004.6], 2301.6000, '08456e8f9231408e9c2b842dc3218c3d'),
         ('2_tube_cut.step', 'tube', 'cut', 1, 30240.0000, [62.1, 44.435, 2.5646, 90.9, 90.519, 48.2785], [30240.0], -3067.9024, '132c88658d9bc3e9a91f1b14be6d0ba8'),
         ('3_fill_join.step', 'fill', 'join', 1, 1552.5000, [63.0, 71.9841, 2.601, 90.0, 89.232, 21.3662], [1552.5], 1059.0251, 'cd357900d3a0938e006b9ce64adeb1ff'),
         ('4_posts_join.step', 'posts', 'join', 4, 278.2186, [61.82, 69.1483, 2.1929, 91.18, 91.0378, 26.16], [62.2035, 62.2035, 76.9058, 76.9058], 207.1437, 'b21ac1d7fdc6a91a4c51b51c711485b7'),
         ('5_pocket_cut.step', 'pocket', 'cut', 1, 1942.2984, [62.55, 72.601, 5.3584, 90.45, 91.6337, 25.1935], [1942.2984], -972.5456, '4ec6fc6e80551dcbe5335cd407ccd032'),
         ('6_window_cut.step', 'window', 'cut', 1, 762.8700, [64.7, 78.4149, 8.2486, 88.3, 88.9246, 19.5303], [762.87], -305.1484, '75a873bd2e14a1fb6d9d755ee24b4285'),
         ('7_chin_cut.step', 'chin', 'cut', 1, 27.7972, [64.7, 87.4186, 18.1177, 88.3, 89.5951, 19.2], [27.7972], -10.7603, '13df0eadbabea4379558d5ede9ed16ce'),
         ('8_pilots_cut.step', 'pilots', 'cut', 4, 17.5207, [64.17, 70.9609, 3.6194, 88.83, 90.2085, 24.4805], [4.3802, 4.3802, 4.3802, 4.3802], -16.9901, '43d1a3310b76db6217a52b5b157305c9')]
# (what, point (case mm), before, after: 0 = solid, 2 = empty) - each one checked on the cloud's solids
PROBES = [('window, through the skin', (76.50000, 83.50734, 14.08274), 2, 2),
          ('glass pocket', (76.50000, 82.76420, 14.75188), 2, 2),
          ('lip over the window', (76.50000, 88.72656, 19.87927), 0, 0),
          ("the chin's flat cut", (76.50000, 88.20606, 19.00230), 0, 2),
          ('solder-joint relief', (76.50000, 89.41850, 22.88946), 0, 2),
          ('skin over the relief', (76.50000, 91.20235, 22.62891), 2, 0),
          ('new tube, top end', (76.50000, 84.74469, 29.65448), 0, 2),
          ('new tube top wall', (76.50000, 85.81530, 30.84351), 2, 0),
          ('brow, the new 1.0', (76.50000, 74.43188, 48.09048), 2, 0),
          ('old window, filled', (76.50000, 77.15060, 7.02287), 2, 0),
          ('old pilot, filled', (66.00000, 73.39637, 4.34785), 2, 0),
          ('new pilot, lower inner', (64.82000, 72.73352, 5.10616), 0, 2),
          ('new pilot, upper handle side', (88.18000, 88.28726, 23.12757), 2, 2),
          ('new post, lower inner', (65.82000, 71.99038, 5.77529), 2, 0),
          ('new post, upper handle side', (87.18000, 87.91568, 23.46213), 0, 0),
          ("lower post's foot", (64.82000, 70.23725, 3.82825), 0, 0),
          ('tube 0.4 wider', (62.30000, 74.10551, 17.83848), 0, 2),
          ('side wall', (61.90000, 74.10551, 17.83848), 0, 0),
          ('tube middle', (76.50000, 74.10551, 17.83848), 2, 2),
          ('facet wall below the window', (76.50000, 73.28475, 3.77554), 0, 0)]
P = lambda x, y, z: adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)


def identity(m):
    a = m.asArray()
    return all(abs(a[i] - (1.0 if i in (0, 5, 10, 15) else 0.0)) < 1e-9 for i in range(16))


def bodies_of(comp):
    return [b for b in comp.bRepBodies if b.name.startswith(BODY_PREFIX)]


def mine(comp):
    out = []
    for coll in (comp.features.baseFeatures, comp.features.combineFeatures):
        out += [f.name for f in coll if f.name.startswith(TAG)]
    return out


def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    items = [o for o in des.rootComponent.occurrences if ITEM in o.component.name]
    if len(items) != 1:
        print('STOPPED: %d items named ...%s...' % (len(items), ITEM)); return
    comp = items[0].component
    bs = bodies_of(comp)
    if mine(comp):
        print('ALREADY THERE: %s | body %s | modified %s' % (mine(comp), [(b.name, round(b.volume * 1000, 4), b.faces.count) for b in bs], app.activeDocument.isModified)); return
    if len(bs) != 1 or abs(bs[0].volume - V0_CM3) > 5e-6 or bs[0].faces.count != FACES0:
        print('STOPPED, not the body read back: %s' % [(b.name, round(b.volume, 6), b.faces.count) for b in bs]); return
    b = bs[0]
    bad = [(nm, b.pointContainment(P(*q))) for nm, q, before, after in PROBES if b.pointContainment(P(*q)) != before]
    print('before: %r %.6f cm3, %d faces | probes not as the cloud has them before (must be none): %s | timeline %d | modified %s' % (
        b.name, b.volume, b.faces.count, bad, des.timeline.count, app.activeDocument.isModified))
    if bad:
        print('STOPPED: the body is not in the state the cloud expects'); return
    for f, nm, op, ns, tv, box, svs, ch, md in STEPS:
        h = hashlib.md5(open(DIR + f, 'rb').read()).hexdigest()
        if h != md:
            print('STOPPED: %s has md5 %s, the cloud wrote %s' % (f, h, md)); return
    print('the eight tool files: md5 as the cloud wrote them')
    made = []
    try:
        build(app, des, comp, made)
    except Exception:
        print('*** STOPPED:\n' + traceback.format_exc())
        print('made before it stopped: %s' % [m.name for m in made if m.isValid])
        try:
            for m in reversed(made):
                if m.isValid:
                    m.deleteMe()
            nb = bodies_of(comp)[0]
            print('ROLLED BACK: %d things removed; body %.6f cm3 (before %.6f), %d faces; bodies in the item %d; timeline %d' % (
                len(made), nb.volume, V0_CM3, nb.faces.count, comp.bRepBodies.count, des.timeline.count))
        except Exception:
            print('*** ROLL-BACK FAILED - Fusion needs a look:\n' + traceback.format_exc())


def build(app, des, comp, made):
    tl = des.timeline
    t_start = tl.count
    F = comp.features
    body = lambda: bodies_of(comp)[0]
    last = [body().volume * 1000.0]
    tbm = adsk.fusion.TemporaryBRepManager.get()
    im = app.importManager

    for k, (f, nm, op, ns, tv, box, svs, ch, md) in enumerate(STEPS):
        # ---- the tool: import its STEP into the item (a new component), check it, copy its solids out, remove the import
        before = set(o.name for o in comp.occurrences)
        ok = im.importToTarget(im.createSTEPImportOptions(DIR + f), comp)
        new = [o for o in comp.occurrences if o.name not in before]
        for o in new:
            made.append(o)
        if not ok or len(new) != 1:
            raise RuntimeError('%s: import gave %s, %d new occurrences' % (f, ok, len(new)))
        occ = new[0]
        src = list(occ.component.bRepBodies)
        for so in occ.component.allOccurrences:
            if not identity(so.transform2):
                raise RuntimeError('%s: a sub-occurrence is moved' % f)
            src += list(so.component.bRepBodies)
        if not identity(occ.transform2):
            raise RuntimeError('%s: the imported occurrence is moved' % f)
        temps = [tbm.copy(x) for x in src]
        vols = sorted(round(t.volume * 1000.0, 3) for t in temps)
        bb = None
        for t in temps:
            q = t.boundingBox
            lo, hi = [q.minPoint.x * 10, q.minPoint.y * 10, q.minPoint.z * 10], [q.maxPoint.x * 10, q.maxPoint.y * 10, q.maxPoint.z * 10]
            bb = lo + hi if bb is None else [min(bb[i], lo[i]) for i in range(3)] + [max(bb[3 + i], hi[i]) for i in range(3)]
        if len(temps) != ns or any(abs(a - c) > 0.01 for a, c in zip(vols, svs)) or any(abs(a - c) > 0.002 for a, c in zip(bb, box)):
            raise RuntimeError('%s: %d solids %s box %s - the cloud wrote %d solids %s box %s' % (f, len(temps), vols, [round(v, 4) for v in bb], ns, svs, box))
        occ.deleteMe()
        made.remove(occ)
        # ---- into a base feature of the item, then combined with the body
        names0 = set(x.entityToken for x in comp.bRepBodies)
        bf = F.baseFeatures.add()
        made.append(bf)
        bf.startEdit()
        for t in temps:
            comp.bRepBodies.add(t, bf)
        bf.finishEdit()
        bf.name = '%s%d tool: %s (%s)' % (TAG, k + 1, nm, op)
        tools = [x for x in comp.bRepBodies if x.entityToken not in names0]
        if len(tools) != ns:
            raise RuntimeError('%s: %d new bodies in the item, want %d' % (f, len(tools), ns))
        for j, x in enumerate(tools):
            x.name = '%sstep %d tool %s %d' % (TAG, k + 1, nm, j + 1)
        col = adsk.core.ObjectCollection.create()
        for x in tools:
            col.add(x)
        ci = F.combineFeatures.createInput(body(), col)
        ci.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation if op == 'join' else adsk.fusion.FeatureOperations.CutFeatureOperation
        ci.isKeepToolBodies = False
        ci.isNewComponent = False
        cf = F.combineFeatures.add(ci)
        made.append(cf)
        cf.name = '%s%d %s %s' % (TAG, k + 1, op, nm)
        if cf.healthState != 0:
            raise RuntimeError('step %s not healthy: %s %s' % (nm, cf.healthState, cf.errorOrWarningMessage))
        now = body().volume * 1000.0
        d = now - last[0]
        good = abs(d - ch) < 0.03
        print('   %d %-6s %-4s %d solid(s), tool %.4f mm3: body %+.4f mm3 (the cloud: %+.4f) -> %.4f mm3, %d faces %s' % (
            k + 1, nm, op, ns, tv, d, ch, now, body().faces.count, 'ok' if good else '*** DIFFERS'))
        if not good:
            raise RuntimeError('step %s: %+.4f against %+.4f' % (nm, d, ch))
        left = [x.name for x in comp.bRepBodies if x.name.startswith(TAG)]
        if left:
            raise RuntimeError('tool bodies left after step %s: %s' % (nm, left))
        last[0] = now
    # ---- the result
    b = body()
    bad = [(nm, b.pointContainment(P(*q))) for nm, q, before, after in PROBES if b.pointContainment(P(*q)) != after]
    print('probes (0 = solid, 2 = empty): %d checked, wrong: %s' % (len(PROBES), bad))
    if bad:
        raise RuntimeError('probe points not as the cloud has them after: %s' % bad)
    tb = b.boundingBox
    print('body %r: %.6f cm3, %d faces, x %.3f..%.3f y %.3f..%.3f z %.3f..%.3f | bodies in the item: %d' % (b.name, b.volume, b.faces.count,
          tb.minPoint.x * 10, tb.maxPoint.x * 10, tb.minPoint.y * 10, tb.maxPoint.y * 10, tb.minPoint.z * 10, tb.maxPoint.z * 10, comp.bRepBodies.count))
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
