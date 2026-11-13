# V586: every equipment name on the native wooden hint

Production remains experimental V581. This batch changes testing tools and
audit records, not ROM artwork/code, patch, release profile or canonical base.

## Actual display coverage

One fresh14,360-frame DeSmuME cold boot uses a byte-exact isolated copy of the
existing Maria save. Ordinary navigation opens the original Sailor Info screen.
Twenty-eight explicitly labeled equipment fixtures then cover the complete
current native catalogue:28 weapons,26 armor items and49 accessories,103 unique
equipment IDs in total. Source names/categories are obtained through the original
item getters, not inferred from a filename or a manually abbreviated list.

Each set puts a weapon in slot0, armor in slot1 and accessories in slots2-4.
The original ownership descriptor/transfer routines perform the assignments in
isolated live RAM. Explicit slot assignment is a display fixture: normal item
acquisition, eligibility and earned progression are not claimed. The fixture
retains strict V581 ARM9/captain/category/ID guards and rejects changes outside
the affected item records, acquisition-history bits and crew equipment bytes.

The ordinary B/A navigation rebuilds Sailor Info for each set; Left selects the
five hints. Every fixture is replayed independently from its captured before-RAM
snapshot, and its exact changed bytes/metadata match the live report. Complete
captured equipment vectors, native category/name/owner getters and screenshots
bind each item to its actual displayed slot. Getter verification leaves each
exported4 MiB RAM image unchanged.

## Verified pixels

- All103 unique equipment names pass the full original game-font masks, including
  leading/trailing letters and blank cells. These are actual emulator captures,
  not just separately executed font/painter routines.
- All103 original32x32 item icons pass105,472 pixel comparisons. The complete
  current item atlas is byte-identical to clean source.
- All140 hint appearances pass205,088 whole-paper pixel comparisons:103 occupied
  names and37 empty hints. The expected wood/frame pixels are independently
  derived from the original Japanese town-info wood strip with the V581 source
  mapping. The resident tile matches that original-source mapping. Complete
  borders, margins, background and visible repeat joins are included.
- Empty cases in this run cover Armor and the three accessory positions. Slot0
  always contains a weapon; this batch adds no new empty-Weapon appearance. The
  existing V581 empty-Weapon check remains separate evidence.

Seven unmodified full screenshots were visually reviewed: Alexander's Campaigns,
Self-Sharpening Plane, Aristarchus Telescope, Red-Haired Pirate Sword, Saladin's
Silver Armor, Giant Red Spear and an empty Equipped Items hint. The reviewed
names are complete and readable, with no new clipping, missing first/final
letters or conspicuous repeat seam identified in those views. All140 captures
receive the automated full-paper checks; human-style visual inspection is not
claimed for every individual screenshot. Hidden original grain remains inferred
as documented in the V581 repair, not exact recovery of concealed source pixels.

## Preservation and artifact location

ROM remains `out/all_routes_combined_v581_candidate.nds`, SHA256
`542c2faf58bde6f408c873a930e29cdb215ef4940375aeffb650644c26d41e68`.
Its existing patch remains SHA256
`e411c4f24e4669309f262493320b08708c9f376da2b9bd80631a002d2f34e415`.
All470 batches/114 accepted layers and the V581 integration proof retain scope;
no new release or canonical promotion occurs.

The original Maria save, historical source copy and current test source copy
remain SHA256`fbae21aa2c5a695bde0eddfc10a3bbeb80d01478bd6a9ed743d824595dc3096e`.
The emulator uses its own separate save directory. No gameplay Save command is
sent. These source-copy invariants are checked separately from screenshot output.

- `scripts/native_equipment_fixture_v586.py`: original transfer/descriptor fixture
  with exact RAM write bounds and explicit category-correct slot assignments.
- `scripts/headless_desmume_v193.py`: optional `equipment_items` pause command,
  gated by the existing explicit `--allow-inventory-fixtures` flag and recorded
  under `synthetic_equipment_display_fixtures`. Other navigation commands retain
  their existing behavior.
- `scripts/verify_equipment_catalogue_v586.py`: full catalogue/native captured
  state, fixture replay, font/wood/icon/source-save checks.
- `work/analysis/equipment_catalogue_v586/native_catalogue_proof.json`: final
  evidence. Input sets, preflight and navigation prefix are alongside it on E
  through the existing analysis junction.
- Full unmodified captures/reports/RAM snapshots remain under
  `E:/Rota Nova translations/Generated/work/emulation_v193/equipment_catalogue_v586_live`.
- All140 selected full screenshots, proofs, command journal and hashed provenance
  are under `E:/Rota Nova translations/Screenshots/Test fixtures/V586 All equipment hints`.
  They are synthetic fixtures, not ordinary guide/publication candidates.

The first launch without an interactive terminal stopped with EOF at frame5400,
before applying an equipment fixture. Its output is retained separately as
`equipment_catalogue_v586`; it has no completed report and earns no passing test
credit. The fresh `_live` run above is terminal-successful and is the only run
used for the catalogue claims.

## Remaining scope

This closes the individual-name display gap for all103 catalogue equipment IDs
on Maria in the recorded condition. It does not prove every character/condition
combination, normal acquisition/eligibility, all related menu states or physical
hardware behavior. All18 original plaque/hint audit entries remain incomplete
under the user's instruction, and all22 historical requirement objects remain
deep-identical. The marker/miniature/Confirm/legacy/logo/movie-context work and
other graphics gates stay open. The graphics goal remains active and incomplete.

The marker investigation preceding this run found three alternate descriptor
constructor sites selecting the common indexed table02115EFC, outside the small
header source rows in the entries inspected. It supplied no new ordinary marker
caption-parent proof; no completion credit is assigned to that diagnostic.
