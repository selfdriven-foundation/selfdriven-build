# MK-I r8 draft - RECORD (2026-10-08), NOT TO BE RUN AGAIN: the short scripts that were run straight in Fusion (no file, no
# loader) right after f10b. Kept so that what ran is on file. Each block below is one run, in order; the text is as it ran,
# with only this header and the block titles added.
#
# What happened: f10b moved the relief's outline correctly (all four corners 0.000000 mm from where they were meant to be;
# body 117.640554 cm3 = the cloud's trial), but the LAST step, "Fix 3 - notches with sloped tops ...", showed a warning:
# "No target body! Compute Failed". The body still had the notches. Rolling the timeline back and forward, setting the cut's
# target body again, and changing its distance 6 -> 6.5 -> 6 mm did NOT clear it. Suppressing the notch cut changed nothing
# (the relief step seemed to give the notches by itself - Fusion's stored results were out of step). What cleared it:
# switching the RELIEF cut off and on again (block 1). After that the two steps gave exactly what they should (block 2):
# relief alone 117.668217 cm3 with no notches, with the notch cut 117.640554; every step healthy. Then the named number was
# tried (block 3). Lesson: after moving fixed points in a sketch that a cut uses, check EVERY step's health and check each
# cut's own share by switching it off - not only the final volume.

# ---- block 1: the repair (the relief cut off and on; the notch cut was also switched off and on first, for the diagnosis)
BLOCK_1 = r'''
import adsk.core, adsk.fusion
def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    tl = des.timeline
    names = {0: 'inside', 1: 'on', 2: 'AIR', 3: 'unknown'}
    def state(tag):
        b = [x for x in comp.bRepBodies if x.name == 'Body (copy of r7) + sound posts + slot'][0]
        pr = [names[b.pointContainment(adsk.core.Point3D.create(x / 10.0, -7.7722, 4.7396))] for x in (-20.1, 37.9, -14.0, 32.0)]
        f = [e for e in comp.features.extrudeFeatures if e.name.startswith('Fix 3 - notches')][0]
        print('%-28s body %.6f cm3, faces %d | notch probes %s | notch cut suppressed %s health %d' % (tag, b.volume, b.faces.count, pr, f.timelineObject.isSuppressed, f.healthState))
    state('now')
    f = [e for e in comp.features.extrudeFeatures if e.name.startswith('Fix 3 - notches')][0]
    f.timelineObject.isSuppressed = True
    adsk.doEvents()
    state('notch cut SUPPRESSED')
    f = [e for e in comp.features.extrudeFeatures if e.name.startswith('Fix 3 - notches')][0]
    f.timelineObject.isSuppressed = False
    adsk.doEvents()
    state('notch cut back on')
    r = [e for e in comp.features.extrudeFeatures if e.name.startswith('Fix 3 - relief inside')][0]
    r.timelineObject.isSuppressed = True
    adsk.doEvents()
    state('RELIEF cut suppressed')
    r = [e for e in comp.features.extrudeFeatures if e.name.startswith('Fix 3 - relief inside')][0]
    r.timelineObject.isSuppressed = False
    adsk.doEvents()
    state('relief cut back on')
    bad = [(tl.item(i).name[:40], tl.item(i).healthState) for i in range(tl.count) if not tl.item(i).isGroup and tl.item(i).healthState != 0]
    print('not healthy now:', bad)
'''
# printed: now 117.640554 / AIR AIR / health 1 - notch cut SUPPRESSED 117.640554 / AIR AIR (!) - back on: the same -
# RELIEF cut suppressed 119.270319, notch cut health 0 - relief cut back on 117.640554, notch cut health 0 - not healthy: []

# ---- block 2: each cut's own share, by switching the notch cut off and on
BLOCK_2 = r'''
    (same set-up as block 1)
    state('now')
    n.timelineObject.isSuppressed = True;  state('notch cut suppressed (want 117.668216, probes inside)')
    n.timelineObject.isSuppressed = False; state('notch cut back on (want 117.640554, AIR)')
'''
# printed: now 117.640554, faces 1156, AIR AIR inside inside, all healthy - notch cut suppressed 117.668217, faces 1152,
# inside x4 - back on 117.640554, faces 1156, AIR AIR inside inside, relief health 0, notch cut health 0, not healthy: []

# ---- block 3: the named number tried, and set back
BLOCK_3 = r'''
import adsk.core, adsk.fusion
def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    comp = [o for o in des.rootComponent.occurrences if 'BUILT IN FUSION' in o.component.name][0].component
    tl = des.timeline
    par = des.userParameters.itemByName('stand_wall_relief_depth')
    want = {'1.0 mm': 118.013869, '1.5 mm': 117.397528, '1.3 mm': 117.640554}
    for e in ('1.0 mm', '1.5 mm', '1.3 mm'):
        par.expression = e
        adsk.doEvents()
        b = [x for x in comp.bRepBodies if x.name == 'Body (copy of r7) + sound posts + slot'][0]
        bad = [(tl.item(i).name[:40], tl.item(i).healthState) for i in range(tl.count) if not tl.item(i).isGroup and tl.item(i).healthState != 0]
        print('relief depth %s: body %.6f cm3 (the cloud: %.6f, difference %+.6f) | faces %d | bodies %d | not healthy %s' % (e, b.volume, want[e], b.volume - want[e], b.faces.count, comp.bRepBodies.count, bad))
    print('parameter now', par.expression)
'''
# printed: 1.0 mm 118.013869 (+0.000000) - 1.5 mm 117.397527 (-0.000001) - 1.3 mm 117.640554 (-0.000000); faces 1156,
# 1 body, not healthy [] each time; parameter now 1.3 mm
