"""MK-I BODY r7 = r5 + THE POWER BUTTON as a LEVER (M1).

The owner, 2026-10-03, shown where the X1201's own switch sits: "Push pin in the wall (Recommended)".
The switch is a right-angle tact switch at the X1201's bottom corner on the side WITHOUT the handle; its
plunger points sideways at that wall and ends about 12 mm short of it (mk1_m1_est.py).

r6 answered that with a loose pin sliding in a bore, held by a cap and a screw. It passed its own 292
checks and FAILED the fresh-eyes review (2026-10-04) on the one thing the checks had only asserted:
a loose pin has no rest position. Left pushed in - and driving its screw pushes it in - it stands in the
plunger's way when the body is lowered over the electronics, its flat faces the plunger, and with a
3.4 mm guide and 9 mm of overhang it binds instead of sliding back. r6 was never shown or printed.

r7: the pin is the end of a LEVER - one printed part, a 1.0 mm leaf with the push pin (the "post") at
its free end - held from OUTSIDE by one M3x8.
  - The leaf is the spring: let go, the post is back out. Nothing is loose, nothing rattles.
  - The lever goes in LAST, from outside, through a window in the wall, with the body already on the
    deck - and comes off FIRST. Nothing of the button is in the plunger's way while the body moves.
  - It comes out the same way: one screw. So the post's length is fitted with the body ON the deck, and
    before any lever exists the plunger can be seen and MEASURED through the window.
  - It is printed lying on its side: the leaf bends along its filaments, not across its layers.
  - If it ever breaks, a gram and a half is printed again, not the body.

Six fresh-eyes reviews (2026-10-04 / 05) shaped it. None found a blocker in r7's geometry; what they found is in here.
 Review 2, on r7's first form:
  - a thumb could push the lever further than the nose's 45 deg edge covered -> the lever is 2 mm taller
    toward the mouth and that edge is 4.5 deep (what that covers is MEASURED in mk1_check_r7.py, 17 f);
  - the window's ceiling was one 19.5 mm bridge -> a MULLION stands across the window, behind the leaf:
    two bridges of 12.0 and 5.5 mm, and the wall above the window is tied to the wall below it;
  - the screw's thread is only in the boss (clearance through the thin web), and the boss is 1 mm wider
    on either side, so the pilot has 3.0 mm of plastic beside it, not 2.0.
 Review 3, on the second form (which set the lever's angle with a REST under the leaf, 10 mm from the screw):
  - that rest was a rubbing contact on the MOVING leaf: a lever left pressed against it by the screw's drag
    would not come back all the way -> the rest is gone. The lever's fixed end has a LEG that lies in a
    CHANNEL down the strip. It sets the angle both ways, 14 mm from the screw, on a part that does not move;
  - a caliper had almost nothing to stand on beside the window -> a GAUGE: it sits where the lever sits,
    with the lever's own screw, and gives the caliper a flat face and the depth rod an opening (gauge());
  - the leaf twists a little when pressed off its middle, and the plunger sits above the leaf's middle -> the
    nose is a piece of a SPHERE, not of a cylinder: it meets the plunger at the same spot however the leaf's
    end turns or twists. The press pad is on the plunger's height, not on the leaf's middle;
  - the nose's head is 2 mm wider toward the screw: it covers the plunger's face over the whole estimate, and with
    0.7 of float against it all but 0.13 mm of it along the wall (the fifth review's measure; at the extremes
    the nose meets the plunger's rim and still works it); lever() takes the nose's place along the wall and its
    height as well as its length;
  - the gap at the leaf's free end is 0.8, not 0.5.
 Review 4, on the third form:
  - THE ONE BLOCKER, in the measuring step, not in the geometry: a depth rod that misses the plunger reads 3 .. 4 mm
    long, and final_x_nose() would have made a lever that holds the switch down -> final_x_nose() takes at least
    three readings, uses the smallest, and refuses what the plunger's tip cannot give;
  - with the screw hole's play the lever can turn about its LEG'S END, twice as far as about the screw: 0.12 mm was
    left at the free end -> the lever's hole is 3.2 (the web's stays 3.4), the free end has 1.1 mm above and below,
    the leg's root is filleted;
  - the play of the lever made to a reading is 1.0, not 0.7;
  - the gauge gave 0.12 .. 0.20 mm per N under the caliper and its leg stood alone on the printer's bed -> its tongue,
    leg and neck are 2.5 thick with a counterbore for the screw's head, and the leg is tied to the bar.
 Review 5, on the fourth form (no blocker; all of it in the measuring step):
  - the guard on the readings leaned on the estimate it guards -> final_x_nose() also takes ONE reading beside the
    plunger and the gauge's own measured thickness: the tip must stand 2.0 .. 5.0 proud of the face beside it;
  - offered a little askew, the leg could come to lie ON a wall of its channel and snap under the screw -> the
    channel's two walls have a lead-in (RAIL_CH). A change of the BODY: two bevels, 8 mm long;
  - the gauge has a land where its own thickness can be measured (its neck runs on to the mullion);
  - lever A is the lever AS DRAWN (nose at the far end of the estimate). It is not printed before the readings:
    the lever that is printed is made by lever(x_nose=final_x_nose(...)).
 Review 6, two reviewers on the fifth form (no blocker; body, test piece and gauge "can be printed as they are"):
  - hanging on its screw the lever sits low by the hole's play and droops: the leg's end had 0.05 .. 0.15 mm left
    before it met the wall under the channel's closed end -> the LEVER's leg ends 0.9 short of that end and its end
    is bevelled. The body and the gauge are NOT touched: the gauge keeps the numbers it was reviewed with;
  - printed on its side the leaf's lower edge fell between two layers (10.5 mm) -> 10.4 at the tongue, 10.2 at the
    free end, the pad 6.8: all on the 0.2 mm grid. The tongue gets 0.9 instead of 0.8 over the sill;
  - three readings on the switch's metal face and a fourth on something deeper passed the "proud" test -> the
    readings now include one that only the button can give: pushed until it CLICKS, the rod goes 0.1 .. 0.5 further.
    And the caliper's zero is read before and after, on glass: a zero key touched in between would have gone
    straight into the nose;
  - the nose's height stays 2 mm or more from the face that lies on the printer's bed (a first-layer bulge must
    not become the touching point).

What r7 changes in the body against r5 - and nothing else:
  WINDOW  through the wall without the handle, y -70.5 .. -51, z 24.4 .. 36.8, in two parts either side
          of the mullion. It takes in the upper part of the second air slot (the lever crosses that slot).
  MULLION a bar across the window at y -58.5 .. -56.5, 1.0 behind the leaf, thickened inside by a rib
          with a 45 deg corbel; its head leans forward to carry the ceiling.
  SEAT    a groove 1.2 deep across the solid strip between the second and the third air slot: the
          lever's fixed end lies in it, 0.2 under the wall's face (its screw's head stands 1.45 proud).
          The window's long edges are bevelled 45 deg.
  CHANNEL the same depth, 4.4 wide, down the middle of that strip from the seat to z 16.2: the lever's leg.
          Its two walls have a lead-in at the wall's face, 0.5 wide and 0.4 deep.
  BOSS    behind that strip, inside: 6.5 mm of depth for the screw's thread; 45 deg corbel under it
          (the body prints mouth-down); 1 mm wider than the strip on either side.
  GIVEN UP FOR IT: the lowest of the nine air slots (y -63.5 .. -60.5). The window's lower edge needs the
          wall under it in one piece: with that slot left in, the strip between it and the next slot would
          stand free. Eight slots are left; the second is 1.2 mm shorter at its top, and the boss stands
          1 mm into the inner mouths of the second and third.
"""
from build123d import *
import math
import r3_params as R
from r3_params import WALL, PILOT_D, CLEAR_D
import mk1_body_r3 as B3
import mk1_body_r5 as B5
from mk1_body_r5 import Geo, VARIANTS, CHOSEN, dprofile, dbox, report

PX, PY = B3.PX, B3.PY
X0 = PX[0]                                   # the wall's OUTER face on the side without the handle: -38.2
X_IN = X0 + WALL                             # its inner face: -35.7

# ---- where the plunger is (mk1_m1_est.py: SW_Y_MID, Z_AXIS_MID, X_TIP) - ESTIMATES ----
BTN_Y, BTN_Z = -65.7, 33.4

# ---- the air slots round the lever ----
VW = B3.VENT["w"]                            # 3.0
VZ = B3.VENT["z"]                            # (12, 38)
SLOT_GONE = B3.VENT["ys"][0]                 # -62.0  the slot that makes way
SLOT_A = B3.VENT["ys"][1]                    # -52.5  the slot the lever crosses; the window takes its upper part
SLOT_B = B3.VENT["ys"][2]                    # -43.0  the slot the seat ends in
STRIP_Y = (SLOT_A + VW / 2, SLOT_B - VW / 2) # (-51.0, -44.5): the solid strip the lever is screwed to
VENT = dict(B3.VENT, ys=[y for y in B3.VENT["ys"] if y not in (SLOT_GONE, SLOT_A)])   # r5's body cuts these seven; slot A is cut here

# ---- window, seat, channel, mullion, boss ----
WIN_Z = (24.4, 36.8)                         # on the 0.2 mm layer grid. The lug column's corbel starts at z 38.3
WIN_Y0 = -70.5                               # 0.75 inside the grille plate's flat top (it starts at y -71.25)
SEAT = 1.2                                   # the groove's depth: leaf 1.0 + 0.2, so the leaf lies 0.2 under the wall's face
X_SEAT = X0 + SEAT                           # -37.0
BEVEL = SEAT                                 # 45 deg on the window's long edges, as deep as the seat: z 36.8 -> 38.0 and 24.4 -> 23.2
MULL_Y = (-58.5, -56.5)                      # the mullion; the plunger's face is at y -68.9 .. -62.5, the screw at -47.75
MULL_BACK = 1.0                              # its face lies this far behind the seat's plane: the leaf bends in front of it
X_MULL = X_SEAT + MULL_BACK                  # -36.0
MULL_IN = 4.7                                # its inner face, in from the wall's outer face (x -33.5): 0.3 of wall + 2.2 of rib
X_MULL_IN = X0 + MULL_IN
MULL_Z1 = 38.0                               # the rib's flat top, 1.2 above the window's ceiling
MULL_Z0 = WIN_Z[0] - (MULL_IN - WALL)        # 22.2: where the rib's 45 deg corbel leaves the wall
SCREW_Y = (STRIP_Y[0] + STRIP_Y[1]) / 2      # -47.75
LEG_W = 4.0                                  # the lever's leg, along the wall
LEG_FIT = 0.2                                # ... and its clearance in the channel, on either side (a printed fit: less would not drop in)
CHAN_Y = (SCREW_Y - LEG_W / 2 - LEG_FIT, SCREW_Y + LEG_W / 2 + LEG_FIT)     # (-49.95, -45.55): 1.05 mm of strip left on either side
CHAN_Z0 = 16.2                               # the channel's lower end (on the layer grid); the boss's corbel starts behind the strip at 17.7
RAIL_CH = (0.5, 0.4)                         # lead-in on the channel's two walls, at the wall's face: this wide along the wall, this deep
                                             # (fifth review: offered a little askew, the leg could come to lie ON a wall instead of between
                                             # them - and snap when the screw is driven). 0.8 of each wall stays square; the leg's sides bear
                                             # on 0.5 of that (the leg's own bevel takes 0.3 at the channel's floor)
BOSS_IN = 9.0                                # the boss's inner face, in from the wall's outer face (x -29.2)
X_BOSS = X0 + BOSS_IN
BOSS_WING = 1.0                              # the boss is this much wider than the strip, on either side
BOSS_Z = (24.2, 37.0)                        # it backs the whole seat
BOSS_Z0 = BOSS_Z[0] - (BOSS_IN - WALL)       # 17.7: where its 45 deg corbel leaves the wall

# ---- the lever ----
LEAF_T = 1.0
X_AXIS = X_SEAT - LEAF_T / 2                 # -37.5: the leaf's middle plane
LEAF_Z = (25.3, 35.7)                        # 0.9 over the sill, 1.1 under the ceiling (the ceiling is a printed bridge and may sag).
                                             # The lever is printed lying on the face at z 35.7: its heights count from there, and they are
                                             # on the 0.2 mm layer grid - tongue 10.4, free end 10.2, pad 6.8, leg's end 18.6 (sixth review)
LEAF_Y = (-69.7, -44.8)                      # 0.8 from the window's end; 0.3 short of slot B
SCREW_Z = 30.6                               # a number of the BODY (the hole in web and boss): it does not follow the leaf
FREE_Y = -60.0                               # beyond this the leaf, the post and the pad are the lever's FREE end ...
FREE_Z0 = 25.5                               # ... and their lower edge is one layer higher than the tongue's: 1.1 mm to the sill and 1.1 to the ceiling there
LEVER_HOLE = 3.2                             # the hole in the LEVER (web: 3.4). 0.1 of play: the lever cannot turn far about its leg's end
LEG_R = 0.6                                  # fillets where the leg leaves the tongue
FLOAT = 0.7                                  # assembly float across the wall and along it: the display in its frame 0.4 + the body on the frame 0.3
LEG_Z0 = CHAN_Z0 + 0.9                       # 17.1: the leg's end, 13.5 mm from the screw and 0.9 short of the channel's closed end (sixth
                                             # review: with 0.3 a lever hanging low on its screw could set its leg's end on the wall below)
LEG_END_CH = 0.3                             # 45 deg on the leg's end, on the edge that goes in first
PAD_H = 0.7                                  # the press pad: 0.5 proud of the wall's face
PAD_Y = (-68.6, -63.6)
PAD_Z0 = 28.9                                # the pad runs from here to the leaf's upper edge: its middle (z 32.3) is near the plunger's height
POST_Y = (LEAF_Y[0], -63.8)                  # the post where it stands on the leaf: flush with the leaf's free end; its other side is where the leaf starts to bend
HEAD_Y1 = -61.8                              # the nose's head is wider than the post's root, toward the screw: y -69.7 .. -61.8 (the ball rounds its two ends by 0.05 .. 0.2)
NOSE_Y = BTN_Y - 0.1                         # the nose's foremost point, along the wall: 0.1 beyond the plunger's estimated axis (it creeps the other way)
NOSE_Z = BTN_Z                               # ... and in height: the plunger's estimated axis
NOSE_CH = 4.5                                # 45 deg on the nose's edge toward the body's mouth
ROOT_R = 1.5                                 # fillet where the post meets the leaf
BED_CH = 0.2                                 # 45 deg round the face that lies on the printer's bed (elephant's foot)
PLAY = 0.8                                   # lever A: nose this far from the plunger's OUTERMOST estimated place
X_NOSE_A = -24.2 - PLAY                      # -25.0
SCREW_SHANK = 7.35                           # the M3x8 on hand (measured 2026-09-18); head d 5.7 x 1.65

# ---- the gauge ----
GAUGE_T = 5.5                                # from the seat's plane out to its flat face
X_GAUGE = X_SEAT - GAUGE_T                   # -42.5: the face the caliper's end rests on
GAUGE_OFF = 0.3                              # its bar stands this far off the wall's face
GAUGE_Y0 = -74.0                             # the bar's far end, 3.5 mm past the window's end
GAUGE_LEAF_Z0 = 25.2                         # the GAUGE keeps the numbers it was reviewed with (sixth review: "can be printed as it is"):
GAUGE_LEG_Z0 = 16.5                          # its tongue's lower edge and its leg's end do not follow the lever's
GAUGE_Z = (GAUGE_LEG_Z0, 38.0)               # the bar's height: from the leg's end (the face it is printed on) to 1.2 above the window
GAUGE_NECK = 5.0                             # past the seat's edge its full depth runs on this far inside the window, to 0.5 mm short of the
                                             # mullion. Between y -56 and -54 the gauge is GAUGE_T thick from seat face to flat face: the LAND
                                             # where the caliper's jaws measure the gauge itself (its real thickness, and the caliper's zero)
NOTCH_Y = (-69.9, -61.5)                     # the opening for the depth rod: the plunger's face, every estimate + 0.7 of float, is y -69.55 .. -61.85
NOTCH_Z = (29.6, 36.8)                       # ... and z 31.1 .. 35.9 (the estimate; float does not act in height); the opening's top is a bridge when printed and may sag
HEAD_RELIEF = 0.6                            # room round the screw's head
GAUGE_TONGUE = 2.5                           # its tongue, leg and neck are this thick (the lever's leaf: 1.0): the screw's head sits in a
                                             # counterbore on a 1.0 mm floor, the rest stands proud of the wall and makes the root stiff
PLAY_FINAL = 1.0                             # the play the lever made to readings gets (fourth review: 0.7 left no margin; sixth: "the right
                                             # centre"). What can eat it: the caliper tilted 0.1, the nose printed fat 0.2, gauge and lever seated
                                             # differently 0.2, the body refitted on the frame 0.25 - all at once 0.75. (The plunger giving under
                                             # the rod and a fat gauge are measured out: the click reading, gauge_t.) Holding the switch takes
                                             # 2 mm of error and more; and a play of 2.2 would still click (the leaf reaches the mullion at 3.1)
TIP_PROUD = (2.0, 6.0)                       # how far the plunger's tip may stand out of the switch's metal face for the readings to be believed
                                             # (photos: 3 .. 4, a second reader 3.2 .. 4.8; the estimate's extremes 2.5 .. 4.4).
                                             # A rod that was never on the tip gives 0 here
CLICK_GIVE = (0.10, 0.50)                    # pushed until the button clicks, the rod goes this much further than when it only touches (a tact
                                             # switch's stroke is about 0.25). Nothing else in there gives: a metal face reads the same again
SPREAD = 0.45                                # the three smallest tip readings agree within this (a miss is 3 mm off; a reading taken pushed 0.3)
ZERO_TOL = 0.05                              # the caliper's zero, rod on glass, before and after the readings
GAUGE_TOL = 0.2                              # the gauge's measured thickness against GAUGE_T
EXPECT_TOL = 1.3                             # a second set of readings (on the body) against the first (on the test piece)
PLAY_LIMITS = (0.5, 1.5)

# Why the nose is a piece of a sphere. The leaf bends between the strip's edge (y -51) and the post; pressed, its
# end TURNS (about 5.8 deg for every mm the nose goes in) and the nose swings toward the screw. A flat nose would
# meet the plunger with its leading corner. A ball of radius R touches a flat face at the point straight ahead of
# its centre, however it is turned. With R = the nose's distance from the leaf's middle plane the centre lies IN
# that plane, and the turn then moves the centre straight in, hardly along the wall: the touching point stays
# where NOSE_Y, NOSE_Z put it. The same holds for a TWIST of the leaf about its length (a finger off the pad's
# middle, or the plunger above the leaf's middle - it is, by 2.8 mm): the centre lies in the leaf's plane, so a
# twist moves it straight in too. A cylinder (the second form) took care of the turn only.
# mk1_check_r7.py measures both on the turned and on the twisted solid.


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def xcyl(x0, x1, r, y, z):
    """cylinder along x"""
    return Pos((x0 + x1) / 2, y, z) * Rot(Y=90) * Cylinder(r, x1 - x0)


def yprism(pts, y0, y1):
    """an (x, z) profile extruded along y from y0 to y1 (explicit direction: r3's extrude trap)"""
    face = make_face(Plane.XZ * Polyline(*pts, close=True))
    return Pos(0, y0, 0) * extrude(face, y1 - y0, dir=(0, 1, 0))


def lever_boss(g):
    """the boss behind the strip, as wide as the strip. Starts 1 mm inside the wall so the two are one piece
    (R3: a boss that only touches does not fuse); its sides run on from the slots' sides."""
    pts = [(WALL - 1.0, BOSS_Z0), (WALL, BOSS_Z0), (BOSS_IN, BOSS_Z[0]), (BOSS_IN, BOSS_Z[1]), (WALL - 1.0, BOSS_Z[1])]
    return dprofile(g, "D", pts, STRIP_Y[0], STRIP_Y[1])


def boss_wings(g):
    """1 mm more boss on either side of the strip, from the wall's inner face inward: they stand in the inner mouths
    of slots A and B. Same 45 deg underside. Added AFTER the window and the slots are cut."""
    pts = [(WALL, BOSS_Z0), (BOSS_IN, BOSS_Z[0]), (BOSS_IN, BOSS_Z[1]), (WALL, BOSS_Z[1])]
    return dprofile(g, "D", pts, STRIP_Y[0] - BOSS_WING, STRIP_Y[0]) + dprofile(g, "D", pts, STRIP_Y[1], STRIP_Y[1] + BOSS_WING)


def mullion_rib(g):
    """what the mullion adds on the wall's inside: a rib with a 45 deg corbel under it and a flat top"""
    pts = [(WALL - 1.0, MULL_Z0), (WALL, MULL_Z0), (MULL_IN, WIN_Z[0]), (MULL_IN, MULL_Z1), (WALL - 1.0, MULL_Z1)]
    return dprofile(g, "D", pts, MULL_Y[0], MULL_Y[1])


def mullion_capital():
    """the mullion's head: from its face it leans 45 deg forward to the seat's plane, so that it carries the window's
    ceiling over the ceiling's whole depth - without it the bridges' outer lines would pass in front of the mullion,
    unsupported, 19.5 mm long. Added AFTER the window is cut; it overlaps mullion and ceiling by 0.2 so they are one."""
    z1 = WIN_Z[1]
    return yprism([(X_MULL, z1 - MULL_BACK), (X_SEAT, z1), (X_SEAT, z1 + 0.2), (X_MULL + 0.2, z1 + 0.2), (X_MULL + 0.2, z1 - MULL_BACK)], MULL_Y[0], MULL_Y[1])


def lever_cut():
    """the two parts of the window + the room in front of the mullion + slot A's lower part + the seat + the channel
    + the bevels + the screw's hole, as ONE cutter. Every piece runs past the faces it opens through."""
    z0, z1 = WIN_Z
    c = box(X0 - 1.0, X_IN + 1.0, WIN_Y0, MULL_Y[0], z0, z1)                                # window, free-end part
    c += box(X0 - 1.0, X_IN + 1.0, MULL_Y[1], STRIP_Y[0], z0, z1)                           # window, between mullion and strip
    c += box(X0 - 1.0, X_MULL, MULL_Y[0] - 0.5, MULL_Y[1] + 0.5, z0, z1)                    # in front of the mullion: the leaf's room
    c += box(X0 - 1.5, X_IN + 1.5, SLOT_A - VW / 2, SLOT_A + VW / 2, VZ[0], z0 + 0.5)       # slot A below the window (r5's cut)
    c += box(X0 - 1.0, X_SEAT, STRIP_Y[0] - 0.5, STRIP_Y[1] + 0.5, z0, z1)                  # the seat, from slot A to slot B
    c += box(X0 - 1.0, X_SEAT, CHAN_Y[0], CHAN_Y[1], CHAN_Z0, z0 + 0.5)                     # the channel for the leg, down the strip
    rw, rd = RAIL_CH
    for yw, sg in ((CHAN_Y[0], -1), (CHAN_Y[1], 1)):                                        # ... and the lead-in on its two walls
        tri = [(X0 - 0.5, yw + sg * (rw + 0.5 * rw / rd)), (X0 - 0.5, yw - sg * 0.1), (X0 + rd, yw - sg * 0.1), (X0 + rd, yw), (X0, yw + sg * rw)]
        c += Pos(0, 0, CHAN_Z0) * extrude(make_face(Polyline(*tri, close=True)), z0 + 0.5 - CHAN_Z0, dir=(0, 0, 1))
    up = [(X0 - 0.5, z1 - 0.3), (X_SEAT, z1 - 0.3), (X_SEAT, z1), (X0, z1 + BEVEL), (X0 - 0.5, z1 + BEVEL + 0.5)]
    lo = [(X0 - 0.5, z0 + 0.3), (X_SEAT, z0 + 0.3), (X_SEAT, z0), (X0, z0 - BEVEL), (X0 - 0.5, z0 - BEVEL - 0.5)]
    c += yprism(up, WIN_Y0, STRIP_Y[1] + 0.5)                                               # upper bevel, all along
    c += yprism(lo, WIN_Y0, SLOT_A)                                                         # lower bevel: along the window's sill; it ends in slot A's air.
    c += xcyl(X_SEAT - 0.5, X_IN, CLEAR_D / 2, SCREW_Y, SCREW_Z)                            #   (on the strip the sill is square: the channel's two walls end in it)
    c += xcyl(X_IN - 0.5, X_BOSS + 0.5, PILOT_D / 2, SCREW_Y, SCREW_Z)                      # pilot through the boss
    return c


def body(g):
    """r5's body with seven of its air slots, the boss, the mullion and the lever's cuts"""
    old = B5.VENT
    B5.VENT = VENT                                           # r5's body() cuts whatever slots this list names
    try:
        p = B5.body(g)
    finally:
        B5.VENT = old
    p += lever_boss(g)
    p += mullion_rib(g)
    p -= lever_cut()
    p += boss_wings(g)
    p += mullion_capital()
    return p


# ------------------------------------------------------------------ the lever, in place
def bend(push, y_load=None, nose_y=None):
    """the leaf's bending, for a nose travel `push` (mm): returns (turn of its end in radians, the point on the leaf's
    axis about which the stiff end can be said to turn). Beam: clamped at the strip's edge, flexible up to the post,
    stiff beyond; load at y_load (default: the middle of the pad). "Clamped" is the stiff extreme: the screw's head
    ends 0.4 mm from that edge. Were the leaf only pinned there and held 3.25 mm further back, it would be a fifth
    softer and turn less per mm. The fillet at the post's root shortens the flexible part a little: the strain per mm
    is some 2 % higher than this model says (second and third review, by their own beams)."""
    nose_y = NOSE_Y if nose_y is None else nose_y
    lf = STRIP_Y[0] - POST_Y[1]                                # flexible length
    a = (STRIP_Y[0] - (sum(PAD_Y) / 2 if y_load is None else y_load)) - lf      # the load, beyond the flexible part
    u, th = lf**3 / 3 + a * lf**2 / 2, lf**2 / 2 + a * lf      # end deflection and end turn, both times P/EI
    sa = (STRIP_Y[0] - nose_y) - lf                            # the nose's foremost point, beyond the flexible part
    turn = push * th / (u + th * sa)
    return turn, (X_AXIS, POST_Y[1] + u / th)


def leg():
    """the fixed end's LEG: 4 mm wide, in the leaf's own plane, from the leaf's lower edge down the strip. It lies in
    the channel with LEG_FIT on either side; its end is 13.5 mm from the screw. That is what sets the lever's angle -
    both ways, and on the part of the lever that does not move: +-0.85 deg about the screw, +-1.3 deg with the play
    of the lever's 3.2 mm hole used up as well (the lever then turns about the leg's end; +-1.6 deg if the screw's
    thread is 2.85 and not 3.00). The two edges that go in first are bevelled, and so is its end; the channel's
    walls have their own lead-in (RAIL_CH). The end stops 0.9 short of the channel's closed end."""
    xl = X_SEAT - LEAF_T
    ya, yb, c = SCREW_Y - LEG_W / 2, SCREW_Y + LEG_W / 2, 0.3
    f = make_face(Polyline((xl, ya), (X_SEAT - c, ya), (X_SEAT, ya + c), (X_SEAT, yb - c), (X_SEAT - c, yb), (xl, yb), close=True))
    s = Pos(0, 0, LEG_Z0) * extrude(f, LEAF_Z[0] - LEG_Z0 + 0.01, dir=(0, 0, 1))
    e = LEG_END_CH
    return s - yprism([(X_SEAT - e - 0.01, LEG_Z0 - 0.01), (X_SEAT + 0.01, LEG_Z0 - 0.01), (X_SEAT + 0.01, LEG_Z0 + e + 0.01)], ya - 0.1, yb + 0.1)


def leg_fillets():
    """R LEG_R where the leg leaves the tongue (fourth review: printed on its side the leg is loaded ACROSS its layers
    when the screw's head drags the lever round; a sharp inside corner is where it would start to tear)"""
    xl, zt = X_SEAT - LEAF_T, LEAF_Z[0]
    out = None
    for ys, sg in ((SCREW_Y - LEG_W / 2, -1), (SCREW_Y + LEG_W / 2, 1)):
        blk = box(xl, X_SEAT, min(ys, ys + sg * LEG_R), max(ys, ys + sg * LEG_R), zt - LEG_R, zt + 0.01)
        blk -= xcyl(xl - 0.5, X_SEAT + 0.5, LEG_R, ys + sg * LEG_R, zt - LEG_R)
        out = blk if out is None else out + blk
    return out


def xprism(pts, x0, x1):
    """a (y, z) profile extruded along x from x0 to x1"""
    face = make_face(Plane.YZ * Polyline(*pts, close=True))
    return Pos(x0, 0, 0) * extrude(face, x1 - x0, dir=(1, 0, 0))


def lever(x_nose=X_NOSE_A, push=0.0, spin=0.0, nose_y=NOSE_Y, nose_z=NOSE_Z, twist=0.0):
    """the lever in place. x_nose, nose_y, nose_z = where the nose's foremost point is (case coordinates): lever A's
    are the defaults; the lever made to a reading gets its own (final_x_nose()).
    push > 0 shows it pressed: the stiff end is where the bent leaf puts it (turned about the point bend() gives);
    the leaf between that point and the screw is drawn turned too, which it is not - use a pushed lever for its
    post and nose only. twist (degrees) turns it about the leaf's length (for the checks; same caveat).
    spin (degrees) turns the whole lever about its screw's axis: positive is the way tightening drags it.
    nose_z may not come nearer than 2 mm to the face that lies on the printer's bed (z LEAF_Z[1]): nearer, the ball's
    edge there is less than 0.1 behind its foremost point and a first-layer bulge would do the touching. It need not
    follow the plunger's axis exactly: the ball meets the plunger's flat face wherever its foremost point is."""
    if nose_z > LEAF_Z[1] - 2.0 + 1e-9:
        raise ValueError("nose_z %.2f is nearer than 2 mm to the lever's bed face (z %.1f): keep it at %.1f or lower" % (nose_z, LEAF_Z[1], LEAF_Z[1] - 2.0))
    xl = X_SEAT - LEAF_T                                     # the leaf's outer face: -38.0
    y0, y1 = LEAF_Y
    r = x_nose - X_AXIS                                      # the ball's radius: its centre lies in the leaf's middle plane
    xe = x_nose + 0.5                                        # the post is drawn 0.5 too long, square-ended; the ball then cuts the nose

    def profile(pad):
        pts = [(xe, HEAD_Y1), (X_SEAT, POST_Y[1]), (X_SEAT, y1), (xl, y1)]
        if pad:
            pts += [(xl, PAD_Y[1] + PAD_H), (xl - PAD_H, PAD_Y[1]), (xl - PAD_H, PAD_Y[0]), (xl, PAD_Y[0] - PAD_H)]
        pts += [(xl, y0), (xe, y0)]
        f = make_face(Polyline(*pts, close=True))
        v = [q for q in f.vertices() if abs(q.X - X_SEAT) < 1e-6 and abs(q.Y - POST_Y[1]) < 1e-6]
        assert len(v) == 1, "lever profile: the post's root corner was not found"
        return fillet(v, ROOT_R)

    fp, fq = profile(False), profile(True)
    z0, z1 = LEAF_Z
    s = Pos(0, 0, z0) * extrude(fp, PAD_Z0 - z0 + 0.001, dir=(0, 0, 1))                    # below the pad
    s += Pos(0, 0, PAD_Z0) * extrude(fq, z1 - BED_CH - PAD_Z0, dir=(0, 0, 1))              # with the pad
    s += Pos(0, 0, z1 - BED_CH - 0.001) * extrude(fq, BED_CH + 0.001, dir=(0, 0, 1), taper=45)   # the face at z LEAF_Z[1] lies on the bed
    # the nose: what of the post's last 7 mm lies outside the ball is taken off. Two traps, both met on 2026-10-04:
    #  - the post must NOT end in a cylinder of the ball's own radius about the ball's centre (the second form's crown):
    #    ball and cylinder then touch along a circle, and a cut near that circle's plane came back EMPTY, without an
    #    error - the owner's picture lost the lever that way. Hence the square end, which the ball cuts cleanly;
    #  - the ball is built TILTED, so that its seam and poles lie in no plane a later cut or probe is likely to use.
    s -= box(x_nose - 7.0, xe + 0.5, y0 - 1.0, HEAD_Y1 + 1.0, z0 - 1.0, z1 + 1.0) - Pos(X_AXIS, nose_y, nose_z) * Rot(X=31, Y=17) * Sphere(r)
    zf = FREE_Z0                                             # the free end's lower edge: 0.3 higher than the tongue's
    s -= box(xl - PAD_H - 1.0, xe + 1.0, y0 - 1.0, FREE_Y, z0 - 1.0, zf)
    s -= yprism([(x_nose - NOSE_CH, zf - 0.8), (xe + 0.5, zf - 0.8), (xe + 0.5, zf + NOSE_CH + (xe + 0.5 - x_nose)), (x_nose - NOSE_CH, zf)], y0 - 0.5, HEAD_Y1 + 0.5)   # the edge toward the mouth: 45 deg
    s += leg()
    s += leg_fillets()
    s -= xcyl(xl - 2.0, X_SEAT + 1.0, LEVER_HOLE / 2, SCREW_Y, SCREW_Z)
    if twist:
        s = s.rotate(Axis((X_AXIS, 0, SCREW_Z), (0, 1, 0)), twist)
    if push:
        turn, (px, py) = bend(push, nose_y=nose_y)
        s = s.rotate(Axis((px, py, 0), (0, 0, 1)), math.degrees(turn))
    if spin:
        s = s.rotate(Axis((0, SCREW_Y, SCREW_Z), (1, 0, 0)), spin)
    return s


def lever_screw():
    """reference: the M3x8 button head on the leaf, into the boss"""
    xl = X_SEAT - LEAF_T
    return xcyl(xl - 1.65, xl, 2.85, SCREW_Y, SCREW_Z) + xcyl(xl - 0.01, xl + SCREW_SHANK, 1.5, SCREW_Y, SCREW_Z)


def lever_for_print(s):
    """lying on its side, the edge that faces the body's mouth UP (so the nose's 45 deg edge and the leg are on top)"""
    q = Rot(X=180) * s
    bb = q.bounding_box()
    return Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z) * q


# ------------------------------------------------------------------ the gauge, in place
def gauge():
    """a GAUGE for the readings the lever's length is made to. It lies on the lever's seat, its leg in the lever's
    channel, held by the lever's screw - so its flat face stands where the seat puts it, as the lever's nose will.
    Its tongue, leg and neck are GAUGE_TONGUE thick (the lever's leaf is 1.0): the screw's head sits in a counterbore
    on a 1.0 mm floor, so the same screw reaches the same thread, and the root does not give under the caliper
    (fourth review: with a 1.0 mm tongue the face gave 0.12 .. 0.20 mm per N).
    From the seat's edge it rises (45 deg) to a BAR that stands outside the wall, GAUGE_OFF off its face, from the
    leg's end up to above the window and 3.5 mm past the window's end. The bar's outer face is flat and 21.5 mm
    tall: the caliper's end rests on it whichever way up it is held, on both sides of an opening; the depth rod
    goes through the opening to the plunger. Reading R = flat face to the plunger's tip; the tip is at
    x = X_GAUGE + R. Printed standing, like the body (z up): bar, tie and leg are ONE foot on the bed."""
    xl, xt = X_SEAT - LEAF_T, X_SEAT - GAUGE_TONGUE
    y1, yb = LEAF_Y[1], STRIP_Y[0]
    ya, yc, c = SCREW_Y - LEG_W / 2, SCREW_Y + LEG_W / 2, 0.3        # the leg's two sides; its lead-in bevels
    xo = X0 - GAUGE_OFF
    yn = yb - GAUGE_NECK
    yr = yb - (xt - X_GAUGE)                                          # where the 45 deg rise reaches the flat face
    z0, z1 = GAUGE_LEAF_Z0, LEAF_Z[1]                                 # its own lower edge: the gauge is as it was reviewed
    gz0, gz1 = GAUGE_Z
    # at the leg's height: bar + tie + leg, one outline (the tie passes OUTSIDE the wall, over the channel's wall)
    pl = [(xo, GAUGE_Y0), (X_GAUGE, GAUGE_Y0), (X_GAUGE, yr), (xt, yb), (xt, yc), (X_SEAT - c, yc), (X_SEAT, yc - c),
          (X_SEAT, ya + c), (X_SEAT - c, ya), (xo, ya)]
    # at the tongue's height: tongue + neck (inside the window, slot A's place) + rise + bar
    pa = [(X_SEAT, y1), (xt, y1), (xt, yb), (X_GAUGE, yr), (X_GAUGE, GAUGE_Y0), (xo, GAUGE_Y0), (xo, yn), (X_SEAT, yn)]
    # above the tongue: the bar alone
    pb = [(xo, yb), (xt, yb), (X_GAUGE, yr), (X_GAUGE, GAUGE_Y0), (xo, GAUGE_Y0)]
    fl = make_face(Polyline(*pl, close=True))
    s = Pos(0, 0, gz0 + BED_CH) * extrude(fl, z0 - gz0 - BED_CH + 0.001, dir=(0, 0, 1))
    s += Pos(0, 0, gz0 + BED_CH + 0.001) * extrude(fl, BED_CH + 0.001, dir=(0, 0, -1), taper=45)     # the foot on the bed, bevelled
    s += Pos(0, 0, z0) * extrude(make_face(Polyline(*pa, close=True)), z1 - z0, dir=(0, 0, 1))
    s += Pos(0, 0, z1 - 0.001) * extrude(make_face(Polyline(*pb, close=True)), gz1 - z1 + 0.001, dir=(0, 0, 1))
    # printed z up, nothing may start in mid-air: three undersides are 45 deg
    s -= yprism([(xo - 0.01, z0 - 0.01), (X_SEAT + 0.01, z0 - 0.01), (X_SEAT + 0.01, z0 + (X_SEAT - xo) + 0.01)], yn - 0.01, yb)   # the neck, inside the window
    s -= xprism([(ya, z0 - 0.01), (yb - 0.01, z0 - 0.01), (yb - 0.01, z0 + (ya - yb) + 0.01)], xo, X_SEAT + 0.01)                  # the tongue's corner toward slot A (the tie carries its proud part)
    s -= xprism([(yc, z0 - 0.01), (y1 + 0.01, z0 - 0.01), (y1 + 0.01, z0 + (y1 - yc) + 0.01)], xt - 0.01, X_SEAT + 0.01)            # the tongue's corner toward slot B
    s -= box(X_GAUGE - 1.0, xo + 1.0, NOTCH_Y[0], NOTCH_Y[1], NOTCH_Z[0], NOTCH_Z[1])              # the opening for the depth rod
    # counterbore: the head sits on a 1.0 mm floor. The circle runs out through the tongue's end and leaves two thin
    # edges there (fifth review: cosmetic). Opening it to the end with a square slot was tried and taken back: the
    # slot's flat roof is a 3 x 1.5 mm overhang right over the screw's head (the print gate found it).
    s -= xcyl(X_GAUGE - 1.0, xl, 2.85 + HEAD_RELIEF, SCREW_Y, SCREW_Z)
    s -= xcyl(xl - 2.0, X_SEAT + 1.0, CLEAR_D / 2, SCREW_Y, SCREW_Z)
    return s


def gauge_for_print(s):
    """standing on the bar's foot and the leg's end, as modelled: z up"""
    bb = s.bounding_box()
    return Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z) * s


def reading_range():
    """the tip readings that are believable at all: every estimated place of the plunger's tip, +- FLOAT, and 1.5 mm
    more either way in case the estimate itself is off. This is only a sanity net - the tests that count are the
    click and the reading beside the plunger (final_x_nose)."""
    import mk1_m1_est as E
    return E.X_TIP[0] - FLOAT - 1.5 - X_GAUGE, E.X_TIP[1] + FLOAT + 1.5 - X_GAUGE


def final_x_nose(tips, *, click, felt_click, face, gauge_t, zero, play=PLAY_FINAL, expect_tip=None, proud=None, net=None):
    """where the nose goes, from what the owner measures with the gauge on (depth rod through its opening):
      tips     at least THREE readings, flat face to the plunger's TIP, the rod only TOUCHING it, lifted and set again;
      click    ONE reading on the tip with the rod pushed until the button CLICKS;
      felt_click  True only if the owner says he FELT (or heard) that click under the rod. A number alone does not
               prove it: a caliper rocked by a few degrees reads 0.1 .. 0.3 long on anything;
      face     ONE reading taken on purpose BESIDE the plunger, on the switch's metal face;
      gauge_t  the gauge's own thickness, the caliper's jaws across its land (drawn GAUGE_T);
      zero     (before, after): what the caliper shows with its end on glass and the rod pushed down onto the glass,
               once before the readings and once after them (0.00 on a sound caliper).
    Returns the nose's x: `play` short of the tip.
    GUARDED. The opening is six times the plunger's face: a rod poked in blind is on the tip one time in two or three
    (a blade more often), and a miss reads 3 .. 4 mm long - a lever made to that holds the switch down (fourth review,
    the one blocker). A range of believable readings does not settle it: it leans on the estimate (fifth review).
    Nor does "the tip stands proud of the face": three readings on the face and a fourth on something deeper pass
    that (sixth review). What only the button can do is GIVE and CLICK: pushed, the rod goes about 0.25 further and
    the click is felt. Every argument but the tip readings is given by NAME, so that none can be put in another's place.
      - every number finite; the caliper not set to inches;
      - zero: both within ZERO_TOL of 0.00 and of each other (a zero key touched between two readings shows here;
        a constant offset would cancel against gauge_t, a changed one goes straight into the nose);
      - gauge_t within GAUGE_TOL of GAUGE_T;
      - at least three tip readings; the SMALLEST counts; the three smallest agree within SPREAD;
      - click - smallest tip within CLICK_GIVE: less, and the tip readings were already pushed in or the rod was on
        something that does not give; more, and the rod slipped;
      - face - smallest tip within TIP_PROUD;
      - the smallest tip inside reading_range(); and, if expect_tip is given (the body after the test piece: the test
        piece's smallest tip + 0.3), within EXPECT_TOL of it;
      - play within PLAY_LIMITS.
    proud=(lo, hi) and net=(lo, hi) replace TIP_PROUD and reading_range() - ONLY with a photo on file that shows why
    (a plunger that really stands 6.5 proud; a switch that really sits 3 mm from where the photos put it).
    Anything else raises ValueError: measure again, do not make a lever."""
    try:
        rs = sorted(float(r) for r in tips)
    except TypeError:
        raise ValueError("tips must be at least three readings, not one number: a single reading cannot show that the rod was on the plunger")
    try:
        click, face, gauge_t, play = float(click), float(face), float(gauge_t), float(play)
        z0, z1 = (float(v) for v in zero)
    except (TypeError, ValueError):
        raise ValueError("click, face and gauge_t must each be ONE number, zero must be two (before, after)")
    if not all(math.isfinite(v) for v in rs + [click, face, gauge_t, z0, z1, play]):
        raise ValueError("every reading must be a number")
    if felt_click is not True:
        raise ValueError("no click was felt under the rod: the rod was not on the button. Look through the opening, set the rod on the nub, and take the readings again")
    if 0.15 < gauge_t < 0.30:
        raise ValueError("the gauge measures %.3f: the caliper is set to inches. Switch it to mm and take every reading again" % gauge_t)
    if abs(z0) > ZERO_TOL + 1e-9 or abs(z1) > ZERO_TOL + 1e-9 or abs(z1 - z0) > ZERO_TOL + 1e-9:
        raise ValueError("the caliper's zero (rod on glass) was %.2f before and %.2f after the readings; both must be within %.2f of 0.00 and of each other. "
                         "Zero it (jaws closed: 0.00) and take every reading again" % (z0, z1, ZERO_TOL))
    if abs(gauge_t - GAUGE_T) > GAUGE_TOL + 1e-9:
        raise ValueError("the gauge measures %.2f; it is drawn %.2f. Measure across its land again (jaws flat on both faces); if it stays, send a photo of the jaws on it" % (gauge_t, GAUGE_T))
    if len(rs) < 3:
        raise ValueError("give at least three tip readings (the rod lifted and set again between them); got %d" % len(rs))
    if rs[2] - rs[0] > SPREAD + 1e-9:
        raise ValueError("the three smallest tip readings (%.2f, %.2f, %.2f) differ by more than %.2f mm: the rod was not on the plunger's tip each time - measure again" % (*rs[:3], SPREAD))
    give = click - rs[0]
    if give < CLICK_GIVE[0] - 1e-9:
        raise ValueError("pushed until the click the rod went only %.2f mm further than the smallest tip reading (%.2f): either the tip readings were already pushed in "
                         "(take them again, the rod only touching), or the rod was not on the button - nothing else in there gives. Was a click felt?" % (give, rs[0]))
    if give > CLICK_GIVE[1] + 1e-9:
        raise ValueError("the click reading is %.2f mm longer than the smallest tip reading (%.2f); a button gives about 0.25. The rod slipped off the nub or the caliper rocked - measure again" % (give, rs[0]))
    lo_p, hi_p = TIP_PROUD if proud is None else proud
    stands = face - rs[0]
    if not lo_p - 1e-9 <= stands <= hi_p + 1e-9:
        raise ValueError("the reading beside the plunger (%.2f) is %.2f mm longer than the smallest tip reading (%.2f); the plunger should stand %.1f .. %.1f proud. "
                         "Look through the opening, measure again; if it stays, send a photo before a lever is made" % (face, stands, rs[0], lo_p, hi_p))
    lo, hi = reading_range() if net is None else net
    if not lo - 1e-9 <= rs[0] <= hi + 1e-9:
        raise ValueError("the smallest tip reading %.2f is outside %.1f .. %.1f: that is more than 1.5 mm from where the photos put the switch - send a photo through the opening before a lever is made" % (rs[0], lo, hi))
    if expect_tip is not None and abs(rs[0] - float(expect_tip)) > EXPECT_TOL + 1e-9:
        raise ValueError("the smallest tip reading %.2f is %.2f mm from the %.2f expected after the first set of readings: one of the two sets was not on the plunger's tip" % (rs[0], rs[0] - float(expect_tip), float(expect_tip)))
    if not PLAY_LIMITS[0] - 1e-9 <= play <= PLAY_LIMITS[1] + 1e-9:
        raise ValueError("play %.2f is outside %.1f .. %.1f" % (play, *PLAY_LIMITS))
    return X_SEAT - gauge_t + (rs[0] - (z0 + z1) / 2) - play


def pad_to_tip(x_nose):
    """the printed lever's length the owner can check with the caliper's jaws: from the press pad's face to the nose's
    foremost point (they are opposite each other). For a lever made by final_x_nose() with a true zero this is
    smallest tip reading - gauge_t + (LEAF_T + PAD_H - play): with the play of 1.0, tip - gauge + 0.7."""
    return x_nose - (X_SEAT - LEAF_T - PAD_H)


# ------------------------------------------------------------------ reference: the switch, as estimated
def switch_reference():
    """(board corner, switch body, plunger) at their best-estimate place - for pictures and for the checks.
    ESTIMATES (mk1_m1_est.py); none of this is a part."""
    import mk1_m1_est as E
    zb = E.Z_BACK_MID; xd = sum(E.X_D) / 2; zc = zb - E.BOARD["T"]
    board = Pos(xd + 20.0, sum(E.Y_A) / 2 + 22.0, zb - E.BOARD["T"] / 2) * Box(40.0, 44.0, E.BOARD["T"])
    sw = Pos(xd + 3.6, BTN_Y, zc - 3.5) * Box(7.2, 7.2, 7.0)
    plunger = xcyl(E.X_TIP_MID, xd + 0.01, E.PLUNGER_D / 2, BTN_Y, BTN_Z)
    return board, sw, plunger


if __name__ == "__main__":
    import time
    g = Geo(VARIANTS[CHOSEN])
    print("window y %.1f..%.1f z %.1f..%.1f | mullion y %.1f..%.1f, face x %.1f, rib to x %.1f | seat %.1f deep on the strip y %.1f..%.1f | channel y %.1f..%.1f down to z %.1f | bevels to z %.1f / %.1f" % (
        WIN_Y0, STRIP_Y[0], *WIN_Z, *MULL_Y, X_MULL, X_MULL_IN, SEAT, *STRIP_Y, *CHAN_Y, CHAN_Z0, WIN_Z[1] + BEVEL, WIN_Z[0] - BEVEL))
    print("boss to x %.1f, y %.1f..%.1f, z %.1f..%.1f, corbel from z %.1f | screw y %.2f z %.1f" % (X_BOSS, STRIP_Y[0] - BOSS_WING, STRIP_Y[1] + BOSS_WING, *BOSS_Z, BOSS_Z0, SCREW_Y, SCREW_Z))
    print("lever A: leaf %.1f thick, y %.1f..%.1f, z %.1f..%.1f, leg to z %.1f | post root y %.1f..%.1f, head to y %.1f, ball R %.1f about (%.1f, %.1f, %.1f), nose at x %.1f (post %.1f long) | air slots %d + slot A below the window" % (
        LEAF_T, *LEAF_Y, *LEAF_Z, LEG_Z0, *POST_Y, HEAD_Y1, X_NOSE_A - X_AXIS, X_AXIS, NOSE_Y, NOSE_Z, X_NOSE_A, X_NOSE_A - X_SEAT, len(VENT["ys"])))
    ok = dict(tips=[18.3, 18.35, 18.4], click=18.55, felt_click=True, face=21.9, gauge_t=GAUGE_T, zero=(0.0, 0.0))
    xn = final_x_nose(**ok)
    print("gauge: flat face at x %.1f (%.1f from the seat's plane), y %.1f..%.1f, z %.1f..%.1f; opening y %.1f..%.1f, z %.1f..%.1f; a tip reading of 18.3 puts the tip at x %.1f, the nose at x %.2f, and the lever measures %.2f from pad to tip" % (
        X_GAUGE, GAUGE_T, GAUGE_Y0, STRIP_Y[0] - (X_SEAT - GAUGE_TONGUE - X_GAUGE), *GAUGE_Z, *NOTCH_Y, *NOTCH_Z, X_GAUGE + 18.3, xn, pad_to_tip(xn)))
    print("tip readings believable at all: %.1f .. %.1f; the tip must stand %.1f .. %.1f proud of the face beside it and give %.2f .. %.2f at the click" % (*reading_range(), *TIP_PROUD, *CLICK_GIVE))
    for nm, ch in (("one tip reading", dict(tips=[18.3])), ("two tips and a miss", dict(tips=[18.3, 18.4, 21.9])), ("three on the metal face, the fourth deeper", dict(tips=[21.9, 21.9, 21.95], click=21.95, face=24.9)),
                   ("tips already pushed in", dict(tips=[18.55, 18.55, 18.6])), ("no click felt", dict(felt_click=False)), ("face not proud", dict(face=18.4)), ("gauge 6.2", dict(gauge_t=6.2)), ("inches", dict(gauge_t=0.2165)),
                   ("zero moved", dict(zero=(0.0, 0.8))), ("not a number", dict(click=float("nan"))), ("play -1", dict(play=-1.0)), ("second set 3 mm off the first", dict(expect_tip=21.4))):
        try:
            final_x_nose(**dict(ok, **ch)); print("  NOT refused:", nm)
        except ValueError as e:
            print("  refused (%s): %s" % (nm, str(e)[:110]))
    t = time.time(); b = body(g); report("body r7 (plain)", b); print("   built in %.0f s" % (time.time() - t))
    report("lever A", lever()); report("lever A pressed 1.0", lever(push=1.0)); report("lever A spun 0.5 deg", lever(spin=0.5)); report("lever A twisted 3 deg", lever(twist=3.0))
    report("gauge", gauge())
    report("a lever made to a reading (nose at x -23.6, 0.6 along the wall, 0.3 up)", lever(x_nose=-23.6, nose_y=NOSE_Y + 0.6, nose_z=NOSE_Z + 0.3))
    print("turn per mm %.2f deg, pivot %s" % (math.degrees(bend(1.0)[0]), bend(1.0)[1]))
