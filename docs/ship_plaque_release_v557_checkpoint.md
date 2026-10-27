# V557 integrated Ships plaque texture correction

The previous turn identified all11 additional ship plaques with coarse horizontal
bands and prepared a source-based correction. V557 integrates and verifies it.

## Release identity

- Experimental ROM: `out/all_routes_combined_v557_candidate.nds`.
- Actual location: `E:/Rota Nova translations/Generated/out/all_routes_combined_v557_candidate.nds`.
- Candidate SHA256: `c7e5ed2ef8f75fadb686993fbe41ae2fd01ca988f76d09b159604b66d2d62cb2`.
- Canonical build base: `out/raphael_natural_v2_accepted_base.nds`.
- Base SHA256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile: `all-routes-unified-v557`;114 accepted layers and470 inherited batches.
- Added stage: `translations/ship_plaque_texture_v1.json`.
- Manifest: `out/all_routes_combined_v557_candidate.manifest.json`.
- Patch: `out/all_routes_combined_v557_candidate.xdelta`.
- Patch SHA256: `90d922c32dd047612771607a37f0667edb4fd95626a689472a91464192f16653`.
- Patch input: `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- No canonical promotion or human acceptance is claimed.

Only `/_pxl/shipinfo.pxl` changes from V555. The eleven faces receive fine clean
source grain and original native bevels. Overlapping erase remnants are restored
before all face passes. Every accepted English term and glyph position remains
exact. Headers, palettes, dimensions, unrelated pixels and all code remain exact
to V555. The inherited921-entry graphics preservation scope is retained.

## Static and actual display evidence

- Registered builder completes from the immutable canonical base.
- `scripts/verify_ship_plaque_release_v557.py --static-only` and full verifier pass.
- Eleven independent complete native-font masks pass, including first/final letters.
- Six actual Ships scenes match all98304 pixels of both screens,589824 total,
  without excluded points. All66 label appearances remain visible and complete.
- Back returns to the unchanged Info menu, and corrected navigation reopens Ships.
-56 unique startup regression frames remain exact to V555;57 capture records
  include the duplicate final frame. Inputs and core options are identical.
- Exact clean-ROM xdelta reconstruction matches the entire candidate.
- Ruff passes for the new release module and verifier.

The Ships runs cold-boot an unchanged isolated copied gameplay save whose source
SHA256 remains958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb.
There is no savestate load or temporary inventory/location/condition fixture.
Startup regression uses New Game without a preloaded save. These are targeted
DeSmuME emulator checks, not a complete route or hardware verification.

## Cargo source binding and the coincident-colour point

One cargo-border point175,79 initially fails an empirical composition that
classifies foreground by colour difference from the old background. It happens
to share the old plaque's colour. It is not excluded or silently accepted.

The actual native views0218E164/0218E1D8 bind owner02313BB4, source0,1440,
extent16x16 and palette0. Complete original resource resolver020D4170 returns
the actual resident `/_pxl/itemtrade16.pxl` at02361660 without a bridge or supplied
binding. The entire resident file remains exact to clean. Both native views are
rechecked in every credited RAM snapshot.

A straight16-row source crop is disproved by104 lower-half mismatches per icon.
A7-bit index interpretation is also rejected. Complete source search instead
identifies top8 rows at1440 and bottom8 at1447: the observed row map is
[0,1,2,3,4,5,6,7,7,8,9,10,11,12,13,14]. All512 icon pixels then match independently
in control and candidate, including the coincident border point. The full screen
composition explicitly includes both whole source icons. The original cause of
the repeated source row remains untraced; this is observed correspondence, not
proof of all icon rendering states. Cannon/sail/numeric foreground preservation
is checked against the same-input control, without claiming new source bindings.

## Diagnostic attempts retained

An initial non-PTY interactive control terminates at frame4000 on input EOF and
gets no completion credit. The next two runs complete, but A after Back opens
Sailors because the Info selection resets. They do not receive Ships re-entry
credit. The final `_control_r2` and `_actual_r2` schedules use Down then A, complete
5000 frames exit0 and provide all six credited Ships frames. All prior folders
remain diagnostics. The final fresh run completes21200 frames exit0.

## Artifacts and remaining scope

- `work/analysis/ship_plaque_release_v557/release_proof.json` and static/stage proofs.
- Config, navigation schedules, build log, source-save provenance and reconstructed ROM.
- `E:/Rota Nova translations/Generated/work/emulation_v193/ship_texture_v557_control_r2`.
- Corresponding `_actual_r2` and `_fresh` folders.
- Reviewed screenshot and provenance receipt:
  `E:/Rota Nova translations/Screenshots/Guide candidates/V557 Ships`.

User review areas: title menu/New Game, an established story/town screen, Ships
with occupied cargo and cannon/sail icons, ship selection and Back. The targeted
replay verifies this saved ship, not every ship/loadout. Broader ship terminology
consistency, other materials/embedded aliases, source row-repeat cause and wider
graphics consumers remain open. All22 historical requirements retain exact scope;
all18 original plaque/hint entries remain incomplete. The global texture issue
and full graphics goal remain active. Guide publication is not approved.
