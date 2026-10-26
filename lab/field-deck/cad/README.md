# CAD — how the MK-I case was made

**To print, use the STL files in [`../print/MK1-r9/`](../print/MK1-r9/MK1-r9_HOW-TO-PRINT.md).** This folder is the design
behind them.

| | |
|---|---|
| `MK1-r9_design_public_NOT-FOR-PRINT.step` | The whole r9 design as read back from Fusion 360 version 12, with the two first names on the body filled in ([this public copy](#this-public-copy)). For reference and CAD exchange: open it in any CAD program. The print files were cut from this design |
| `fusion_scripts/` | The Fusion 360 API scripts that built r8 and r9 as steps in the Fusion timeline |
| `build123d/` | The code models (build123d, Python) the case started from, and the scripts that checked the Fusion results and cut the print files |
| `checks/` | The reports the final design and the print files passed |
| `fonts/` | Orbitron Bold, the lettering font (SIL Open Font License, included) |

## The method

1. **Code first.** The style was picked from six mock-ups ("machine skeleton"). Revisions r1–r7 were built as build123d
   code and imported into the owner's Fusion file as STEP.
2. **Measured from the maker's drawing.** Raspberry Pi's Touch Display 2 drawing (RP-010429-MM-3), confirmed on a photo,
   placed the stack — the earlier caliper sheet turned out to be 2.6–4.4 mm short (errata E36). The OLED was measured from
   a flat photo by its own pixel pitch.
3. **Then Fusion steps.** From 7 October each change was built directly in Fusion by a script, with named parameters,
   and the code model was kept as the checked reference. In the order they were applied: the `back_r8_*` files at the
   top level (the back plate's mark and words) → `text/` (the words as real Fusion text) →
   `orbitron/` (the lettering redone in Orbitron Bold) → `fix/` (the corrections for the stack's real place, and the
   power lever) → `mic/` (the microphone pocket in the chin) → `vents/` → `hud_r9/`
   (the HUD redrawn around the real OLED). `final/` only makes pictures of the top opening.
4. **Read back and checked.** After each step the Fusion solid was exported and checked against the code trial: every
   layer printable, nothing floating, supports surveyed, the body's whole path onto the stack, the screws at their real
   lengths. Two independent reviews before printing.
5. **Print files.** `build123d/mk1_print_files_r9.py` cut the six parts from the version-12 read-back and laid each one
   the way up it prints (`checks/MK1_r9_print_files_checks.txt`, all pass).

## The checks

| Report | What it checked |
|---|---|
| `MK1_final_r9_checks.txt` | The whole final design: printability, attachment, clearances (all pass) |
| `MK1_final_r8v_checks.txt` | The r8 design with the vents, before the HUD redraw |
| `MK1_r9_hud_trial_checks.txt`, `MK1_check_r9_hud_fusion_readback.txt` | The redrawn HUD: the code trial, then Fusion's own solid |
| `MK1_r9_print_files_checks.txt` | The six print files against the design, each lying the right way up |
| `MK1_r9_screw_real_length_checks.txt` | Every screw joint with a real M3 × 8: thread engaged, hole depth left (all pass) |
| `MK1_r9_grip_screws_checks.txt` | The grip's four screws in detail |

## Coordinates and sides

- Sides: **A** = bottom, **B** = top, **C** = the grip side (Ethernet and USB; the user's left facing the screen),
  **D** = the side without the grip.
- Case coordinates: x+ toward the C side, y+ up (B), z+ toward the back. Fusion is Z-up: (X, Y, Z) in Fusion =
  (−x, z, y) in case coordinates. Details in `build123d/README-cad-src.md`.

## Running the scripts

- **Fusion scripts** run from Fusion's *Scripts and Add-Ins*; each defines `run()`. They are a record of steps already in
  the design — don't run them on the finished design (they would apply twice). Files marked `RECORD_do_not_run` were
  never meant to be run.
- **build123d scripts** need Python with `build123d`, `numpy`, `trimesh`, `shapely`, `matplotlib` and `Pillow`. They were
  run in a temporary cloud workspace, so paths inside them (`readback/…`, `out/…`, `/home/claude/…`,
  `/mnt/user-data/…`) point there — point them at your copies before running. Run the check scripts directly rather than
  importing them into other code: several do their work as soon as they are imported.

## This public copy

The printed deck's body has two first names cut 0.4 mm into the bottom corners of its flat back. This copy leaves them
out:

- **The body.** `build123d/public_namefree.py` fills each name with a block from the letters' floor up to the face, so
  that face is plain; nothing else changes (`checks/public_namefree_checks.txt`: the rest of the body is identical, and the
  new `MK1-r9-Body_PRINT-THIS.stl` lies exactly like the printed one). The STEP above carries this body; Fusion's part
  names are kept. The other five print files are the ones that were printed.
- **The scripts.** The Fusion steps that cut the names (the two `back_r8_step_<name>.py` files, `names35/`,
  `orbitron/o2_names_to_orbitron.py`, `orbitron/o4_export_and_pictures.py`, `text/s5_names_on_body.py` and
  `text/s7_test_strip.py`) are not here, the names' outlines are taken out of `fusion_scripts/back_r8_data.json`, and the
  measuring scripts in `orbitron/` and `text/` measure "NAME1" and "NAME2" instead.
- **Paths.** The Fusion scripts export to `/path/to/Field Deck/…`: set `DIR` to a folder of your own before running one.

The check reports in `checks/` are the originals, made on the printed design (with the names); the print-file report
lists the printed body's checksum.
