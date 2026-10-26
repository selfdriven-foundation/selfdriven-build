import adsk.core, adsk.fusion

NAME = 'Back plate r8 - mark + words (built in Fusion)'

def run(context):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct)
    doc = app.activeDocument
    print('doc', doc.name, 'modified', doc.isModified, 'version', doc.dataFile.versionNumber, 'timeline', des.timeline.count)
    root = des.rootComponent
    occ27 = [o for o in root.occurrences if 'BUILT IN FUSION' in o.component.name][0]
    comp27 = occ27.component
    print('r8 item parts:', comp27.occurrences.count, '| shared plate still in it:', [o.name for o in comp27.occurrences if o.component.name.startswith('Back plate (screwed on)')])
    cov = [o for o in comp27.occurrences if o.component.name.startswith('Speaker cover (PROVISIONAL')][0].component
    print('cover: volume %.6f, steps %s' % (cov.bRepBodies.item(0).volume, [f.name for f in cov.features][-2:]))
    pl = [o for o in comp27.occurrences if o.component.name == NAME]
    if not pl:
        print('plate copy: NOT there'); return
    comp = pl[0].component
    print('plate copy: volume %.6f; steps: %s' % (comp.bRepBodies.item(0).volume, [f.name for f in comp.features]))
    old = [f for f in comp.features if f.name.startswith('Back ')]
    old.sort(key=lambda f: -f.timelineObject.index)
    for f in old:
        n = f.name
        f.deleteMe()
        print('  removed step', n)
    for s in [s for s in comp.sketches if s.name.startswith('Back ')]:
        n = s.name
        s.deleteMe()
        print('  removed sketch', n)
    b = comp.bRepBodies.item(0)
    print('plate copy now: volume %.6f (plain copy of r7 is 24.044619), faces %d' % (b.volume, b.faces.count))
    tl = des.timeline
    bad = []
    for i in range(tl.count):
        try:
            hs = tl.item(i).healthState
        except Exception:
            hs = -1
        if hs not in (0, 5):
            bad.append((i, tl.item(i).name, hs))
    print('timeline', tl.count, 'items; not healthy:', bad)
