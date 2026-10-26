# MK-I r9 deck - how to print (12 Oct 2026)

Six files. Each one already lies the right way up - do not turn them in the slicer.
Picture: `MK1-r9_parts_as_they_lie.png` (orange = the part, beige = the plate).
They are cut from Fusion version 12 as you saved it, and every check passed on them
(`mk1/MK1_final_r9_checks.txt`, `mk1/MK1_r9_print_files_checks.txt`).

## Settings for every part (the same as your test prints)

Bambu Studio. Turn on "Advanced" at the top of the process settings, or some of these stay hidden.
Then save it as your own process preset (the save icon next to its name), so it does not reset again.

- Printer: Bambu Lab A1, 0.4 nozzle. Plate type: Textured PEI Plate.
- Filament: Bambu PETG HF (its own temperatures - do not change them). Dry the PETG first.
- Process: start from "0.20mm Standard @BBL A1", then:
  - Quality: layer height 0.2, initial layer height 0.2.
    Precision: X-Y hole compensation 0, X-Y contour compensation 0, elephant foot compensation 0.15.
  - Strength: wall loops 4, sparse infill density 20 % (pattern and top / bottom shells as they are).
  - Speed: as it is.
  - Support: see each part below (OFF for everything except the body).
  - Others: brim - see each part below (none except the body); skirt loops 0.

For the body only: Support ON - type normal (auto), threshold angle 30, "on build plate only" ticked,
"remove small overhangs" ticked, top Z distance 0.3. Others: brim type "Outer brim only", brim width 5 mm.

## In this order

1. **Body** - `MK1-r9-Body_PRINT-THIS.stl` - 147 g, 208 x 182 x 53 mm
   - Support ON: normal, "on build plate only", threshold 30 deg, "remove small overhangs" on.
     It holds up the flat roof inside the skirt; the support comes out through the open back.
   - Brim ON: outer, 5 mm. Only a thin rim touches the plate, and the corners can curl like the test corner did.
   - If the slicer also puts support under the two flat window tops (the HUD window and the top opening),
     leave it - it snaps out.
   - The deck in the photos has two first names cut into the bottom corners of the flat back. In this public copy
     they are filled in, so that face prints plain.

2. **Front** - `MK1-r9-Front_PRINT-THIS.stl` - 164 g, 208 x 164 x 30 mm
   - Support OFF. With support on, the slicer fills the marks and grooves in the face.
   - Brim type: "No-brim" (set it - "Auto" may add one).

3. **Handle** - `MK1-r9-Handle_PRINT-THIS.stl` - 123 g
   - Support OFF (the grip's grooves print as short bridges). Brim type "No-brim".

4. **Back plate** - `MK1-r9-BackPlate_PRINT-THIS.stl` - 30 g
   - Support OFF, brim type "No-brim".
   - In the preview, look at the words (SELFDRIVEN, 2026): every letter should show.

5. **HUD cap + speaker cover** - one plate together - 5 g + 14 g
   - `MK1-r9-HUD-Cap_PRINT-THIS.stl`, `MK1-r9-SpeakerCover_PRINT-THIS.stl`
   - Support OFF, brim type "No-brim". The cover's two screw ears start as short bridges (3.5 mm at most).

Not to print: the power lever (you have the r8fix2 levers from 9 Oct - keep a spare)
and the retainer ring (reuse the printed one).

## After printing

- HUD: nothing to do (the small screen is held with double-sided foam tape - see below).
- Front: poke the mic's pinhole clear with a needle or a straightened paper clip.
- Back plate: lay it on the table - it should not rock.

## Screws

- 18 x M3x8 button head (2 mm hex key): back plate 4, HUD cap 3, handle 4, body to front 4, speaker cover 2, power lever 1.
  They cut their own thread in the plastic - no drill (stiff the first time, that is normal). Snug, not tight.
- HUD screen board: no screws - double-sided foam tape: a 3 mm square over each of its 4 corner holes,
  on the screen side (not on the glass).

## When you put it together

- HUD screen board: the 4 pins (header) at the TOP. Tape on its 4 corners (screen side), peel the backing,
  slide it in from the back with the plugs on, press at the 4 corners onto the posts.
- HUD cap: tighten the two top screws gently - there is only 1.5 mm of plastic beside them.
- Body to front: snug only (0.8 mm of plastic under each head).
  The lower one on the handle side goes in BEFORE the handle.
- Handle (the grip): 4 x M3x8 through its 4 holes into the front.
  It goes on after the body is screwed to the front (it covers one of those screws).
- The power lever comes out before the body comes off or goes on.
- Foam (holds the screen forward): Moroday 12.7 x 25 mm garage weatherseal (Bunnings).
  Cut one 20 mm piece and stick it in the middle of the battery board's back, between its four screws.
  With the back plate on: the plate lies flat and the screen does not move.
- First run with the case closed: 30 min of load + charging. `vcgencmd get_throttled` should say `throttled=0x0`,
  and the cells should stay at or under 45 C.
