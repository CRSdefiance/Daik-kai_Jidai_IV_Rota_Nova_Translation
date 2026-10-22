# V485 movie playback controls and unresolved fixture incompatibility

Production remains V484, SHA-256
`f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c`.
No production ROM, patch, progression flag, inventory or canonical base is changed.

## Purpose

M28 uses20 progressive name textures27-46. V336 verified only the fully revealed
Hodram Joakim Bergstrom plane46. The new test aimed to cover every intermediate
plane, with every-frame captures2800-4300. It produced no new rendering clearance:
the current file-substitution fixture stopped on an empty upper movie screen.

An initial run used mouse pointer mode instead of the historical touch mode.
Its result is excluded from matched controls. The corrected run uses identical
core DLL/options, input schedule and cold boot; it still does not display the name.

## Matched boundary controls

Each normal control replaces only M20 with exact M28 bytes. No scripts, code,
save/unlock flags or loaded state change. All reports terminate normally and all
captured hashes are verified. All copies use the same current source movie,
SHA-256 `f5558e31683fe488b5cd29db4e449ee99e93bb51dac76b960b07dae915d15ce1`.

| Parent | Frame3700 result |
| --- | --- |
| V326 | All3047 Hodram name/shadow pixels match. |
| V342 | All3047 Hodram name/shadow pixels match. |
| V360 | Name plane does not appear; upper screen black. |
| V474 | Same substitution does not display the name. |
| V484 | Same substitution does not display the name. |

The registered V342/V360 profiles have identical batches; the sole additional
stage is `commodity_ui_release`, config `commodity_ui_release_v3.json`.
This ties the observed substitution incompatibility to that integration boundary.
The movie engine range FD000-100E90 remains byte-identical across all controls.
The exact mechanism and normal M28 playback behavior remain unproven.

## Caller setup investigation

Original scalar dispatch executes for all33 movie IDs:20-27 pass1 to D2DB0 and
M28 passes0. The1 path loads/draws a dialogue background; these caller contexts
must not be treated as equivalent merely because the file contents are swapped.

A separately labeled fixture substitutes the same movie and changes only the
four-byte instruction D2BC4 to pass0. It does not establish successful current
M28 playback. A subsequent observed A-confirmation attempt also does not produce
the name card. These are research inputs, not a shipped fix, normal caller or
ending-unlock credit. Read-only CPU/TCM/VRAM exports are diagnostic observations,
not proof of the stop's cause. No savestate is loaded.

## Artifacts and next work

Proof: `work/analysis/m28_planes_v485/control_proof.json`.
Original mode dispatch: `original_mode_domain.json` in the same folder.
Verifier: `scripts/verify_m28_fixture_controls_v485.py`.
Fixture preparation: `scripts/prepare_m28_planes_v485.py`.
Source/current fixture manifests and terminal capture reports are retained.
Selected diagnostic images are copied to E under
`Screenshots/Diagnostics/movie-playback-v485`, outside the guide archive.

Next, inspect the commodity stage's data ownership, allocations and renderer
interactions, and reproduce through the original M28 caller when available.
Do not infer a normal ending failure from the substitution fixture, restore old
Japanese labels as a production workaround, or count these stopped fixtures as
current GPU evidence. The20-phase coverage remains open.

All22 historical requirements and18 incomplete plaques are retained. The graphics
goal remains active. Earlier V484 boot/shop/patch evidence keeps its documented
scope. At actual completion, revisit older record-based checks.
