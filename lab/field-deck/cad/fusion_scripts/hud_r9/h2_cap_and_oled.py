# h2 - THE NEW HUD CAP + THE REAL OLED BOARD AS A REFERENCE, in the r8 item (after h1; owner: "Yes, build it (Recommended)",
# 2026-10-12). Nothing shared is changed:
#   - a NEW component "HUD cap r9 - for the real OLED (built in Fusion)" with the cloud trial's cap (cad-src/mk1_hud_r9.py:
#     r4's cap with the dummy fourth bolt, 1.0 longer at its upper edge, to the brow's 38.2; the three screws where they were),
#     read from its STEP (case coordinates) into a base feature; the old "HUD cap (4)" occurrence is hidden IN THE r8 ITEM
#     ONLY (r7's item keeps it; its three screws stay - they are where the new cap's screws are);
#   - a NEW component "OLED board - real (IMG_2095), header up (reference)": PCB 27.3 x 27.6, glass, the flex, the four
#     solder joints and the four plugs as allowances, where the trial puts them; the old "OLED board (reference) - copy"
#     (R3's caliper size) and "HUD red filter (film, reference) - copy" (R3's window; this OLED is yellow / blue) are hidden.
# Guarded: if the new cap is there it says ALREADY THERE and changes nothing; if h1 has not run (the body is not at the volume
# h1 leaves) it stops before changing anything; a file whose md5, solids, volume or box differ from the cloud's stops the
# script, and everything this run made is taken back (the new components removed, the hidden ones shown again). It never saves.
import adsk.core, adsk.fusion, traceback, hashlib

DIR = '/path/to/Field Deck/7 - Next Case/cad-src/fusion_scripts/hud_r9/tools/'
ITEM = 'BUILT IN FUSION'
BODY_PREFIX = 'Body (copy of r7)'
V_AFTER_H1 = 115.715268          # cm3: the body after h1 (Fusion's start 116.520846 + the cloud's eight changes)
CAP_COMP = 'HUD cap r9 - for the real OLED (built in Fusion)'
CAP_BODY = 'HUD cap r9 (print this - PETG)'
CAP_FILE, CAP_MD5, CAP_V, CAP_BOX = '9_hudcap_r9.step', '31348888b6746c139864798e12b21af0', 3782.2976, [60.0, 37.5131, 15.282, 93.0, 71.4223, 52.6107]
OLED_COMP = 'OLED board - real (IMG_2095), header up (reference)'
OLED_FILE, OLED_MD5 = '10_oled_real_ref.step', 'f3d0e6ca24b1138b0358bb7ea6bdf2c2'
OLED = [(1250.7768, 'PCB 27.3 x 27.6 x 1.66 (IMG_2095)'),
         (754.1682, 'Glass 26.7 x 19.48 x 1.45'),
         (33.1200, 'Display flex round the lower edge (allowance)'),
         (48.9600, 'Four solder joints on the front (allowance 2.0 high)'),
         (505.0836, 'Four plugs on the header (allowance, 20 from the PCB front)')]
HIDE = ['HUD cap (4):', 'OLED board (reference) - copy:', 'HUD red filter (film, reference) - copy:']
GROUP = 'HUD r9 - the new cap + the real OLED as a reference (built in Fusion)'


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
    have = [o for o in item.occurrences if o.component.name in (CAP_COMP, OLED_COMP)]
    if have:
        print('ALREADY THERE: %s | modified %s' % ([(o.name, [(b.name, round(b.volume * 1000, 4)) for b in o.component.bRepBodies]) for o in have],
                                                   app.activeDocument.isModified)); return
    bs = [b for b in item.bRepBodies if b.name.startswith(BODY_PREFIX)]
    if len(bs) != 1 or abs(bs[0].volume - V_AFTER_H1) > 5e-5:
        print('STOPPED: the body is not where h1 leaves it: %s (want %.6f)' % ([(b.name, round(b.volume, 6)) for b in bs], V_AFTER_H1)); return
    hide = []
    for pre in HIDE:
        m = [o for o in item.occurrences if o.name.startswith(pre)]
        if len(m) != 1 or not identity(m[0].transform2):
            print('STOPPED: %d occurrences named %s... in the r8 item' % (len(m), pre)); return
        hide.append(m[0])
    for f, md in ((CAP_FILE, CAP_MD5), (OLED_FILE, OLED_MD5)):
        h = hashlib.md5(open(DIR + f, 'rb').read()).hexdigest()
        if h != md:
            print('STOPPED: %s has md5 %s, the cloud wrote %s' % (f, h, md)); return
    print('before: body %.6f cm3 | to hide: %s | timeline %d | modified %s' % (bs[0].volume, [(o.name, o.isLightBulbOn) for o in hide], des.timeline.count, app.activeDocument.isModified))
    made, was = [], [(o, o.isLightBulbOn) for o in hide]
    try:
        build(app, des, item, hide, made)
    except Exception:
        print('*** STOPPED:\n' + traceback.format_exc())
        try:
            for m in reversed(made):
                if m.isValid:
                    m.deleteMe()
            for o, w in was:
                o.isLightBulbOn = w
            des.activateRootComponent()
            print('ROLLED BACK: %d things removed, the hidden ones shown again: %s' % (len(made), [(o.name, o.isLightBulbOn) for o, w in was]))
        except Exception:
            print('*** ROLL-BACK FAILED - Fusion needs a look:\n' + traceback.format_exc())


def bring(app, comp, f, made):
    """import a STEP into comp (a new sub-component), copy its solids out (temporary bodies), remove the import"""
    im = app.importManager
    before = set(o.name for o in comp.occurrences)
    ok = im.importToTarget(im.createSTEPImportOptions(DIR + f), comp)
    new = [o for o in comp.occurrences if o.name not in before]
    for o in new:
        made.append(o)
    if not ok or len(new) != 1 or not identity(new[0].transform2):
        raise RuntimeError('%s: import gave %s, %d new occurrences' % (f, ok, len(new)))
    src = list(new[0].component.bRepBodies)
    for so in new[0].component.allOccurrences:
        if not identity(so.transform2):
            raise RuntimeError('%s: a sub-occurrence is moved' % f)
        src += list(so.component.bRepBodies)
    temps = [adsk.fusion.TemporaryBRepManager.get().copy(x) for x in src]
    new[0].deleteMe()
    made.remove(new[0])
    return temps


def box_of(b):
    q = b.boundingBox
    return [q.minPoint.x * 10, q.minPoint.y * 10, q.minPoint.z * 10, q.maxPoint.x * 10, q.maxPoint.y * 10, q.maxPoint.z * 10]


def build(app, des, item, hide, made):
    tl = des.timeline
    t_start = tl.count
    # ---- the cap
    occ = item.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    made.append(occ)
    comp = occ.component
    comp.name = CAP_COMP
    temps = bring(app, comp, CAP_FILE, made)
    if len(temps) != 1 or abs(temps[0].volume * 1000 - CAP_V) > 0.01 or max(abs(a - c) for a, c in zip(box_of(temps[0]), CAP_BOX)) > 0.002:
        raise RuntimeError('cap: %d solids, %s mm3, box %s - the cloud wrote %.4f, %s' % (len(temps), [round(t.volume * 1000, 4) for t in temps], [round(v, 4) for v in box_of(temps[0])], CAP_V, CAP_BOX))
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    comp.bRepBodies.add(temps[0], bf)
    bf.finishEdit()
    bf.name = 'HUD cap r9 - from the cloud trial (mk1_hud_r9.py)'
    comp.bRepBodies.item(0).name = CAP_BODY
    cb = comp.bRepBodies.item(0)
    print('   the new cap: %r %.4f mm3 (the cloud %.4f), %d faces, box %s' % (cb.name, cb.volume * 1000, CAP_V, cb.faces.count, [round(v, 3) for v in box_of(cb)]))
    # ---- the real OLED as a reference
    occ2 = item.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    made.append(occ2)
    comp2 = occ2.component
    comp2.name = OLED_COMP
    temps = bring(app, comp2, OLED_FILE, made)
    vols = sorted(round(t.volume * 1000, 3) for t in temps)
    if len(temps) != len(OLED) or any(abs(a - c) > 0.01 for a, c in zip(vols, sorted(v for v, n in OLED))):
        raise RuntimeError('OLED reference: %s mm3 - the cloud wrote %s' % (vols, sorted(v for v, n in OLED)))
    bf2 = comp2.features.baseFeatures.add()
    bf2.startEdit()
    for t in temps:
        comp2.bRepBodies.add(t, bf2)
    bf2.finishEdit()
    bf2.name = 'OLED board - real, header up (reference, from the cloud trial)'
    for b in comp2.bRepBodies:
        nm = [n for v, n in OLED if abs(v - b.volume * 1000) < 0.01]
        b.name = nm[0] if len(nm) == 1 else 'UNNAMED'
    print('   the real OLED reference: %s' % [(b.name, round(b.volume * 1000, 4)) for b in comp2.bRepBodies])
    # ---- hide R3's cap, R3's board, the red film (in the r8 item only)
    for o in hide:
        o.isLightBulbOn = False
    print('   hidden in the r8 item: %s' % [(o.name, o.isLightBulbOn) for o in hide])
    badsteps = [(tl.item(i).name, tl.item(i).healthState) for i in range(t_start, tl.count) if not tl.item(i).isGroup and tl.item(i).healthState != 0]
    print('timeline: %d new steps (%d .. %d); not healthy: %s' % (tl.count - t_start, t_start, tl.count - 1, badsteps))
    if badsteps:
        raise RuntimeError('steps not healthy: %s' % badsteps)
    if tl.count - t_start > 1:
        try:
            g = tl.timelineGroups.add(t_start, tl.count - 1)
            g.name = GROUP
            print('grouped as: %s' % g.name)
        except Exception as ex:
            print('(not grouped: %s)' % ex)
    des.activateRootComponent()
    print('active component: %s | modified %s' % (des.activeComponent.name, adsk.core.Application.get().activeDocument.isModified))
