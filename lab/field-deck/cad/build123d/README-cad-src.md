# CAD source (build123d) — copied from Claude's cloud workspace 2026-10-01

These scripts generate every case part from code. They lived only in a temporary cloud
workspace until now; this folder is the durable copy.

- `c1_params.py`, `r3_params.py` — single sources of truth for dimensions (case coords:
  x+ = ports = user's LEFT, y+ = top, z = 0 at the display back, z+ = toward the case back).
- `build_c1_frame.py` (FaceFrame + RetainerRing), `build_r3.py` (R3 shell + back panel),
  `build_concepts.py` (2026-10-01 next-case concepts A/B/C, massing only).
- Gates: `slice_scan.py` (erosion), `attach_scan.py` (attachment); `verify_*.py` fit checks.
- `icon_loops.npy` (selfdriven icon outline), `GreatVibes-Regular.ttf` (script font).

Fusion orientation used for the shared Fusion file (Z-up): (X, Y, Z)_fusion = (-x, z, y)_case.
Fusion's Front view shows the screen; the grip shows on the viewer's right.
