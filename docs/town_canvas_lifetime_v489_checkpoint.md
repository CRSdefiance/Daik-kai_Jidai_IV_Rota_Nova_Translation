# V487-V489 town bitmap lifetime research; V488 revoked

Production remains verified V484, SHA-256
`f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c`.
The graphics goal is active; no new candidate is distributed or promoted.

## Progress and failed release gate

A private town bitmap preserves the original shared numeric header and VRAM
pixels. Native create/release/recreate, pointer clearing, allocation reuse,
canaries and saved-register/stack checks pass under explicit allocator contracts.
The normal town display retains all translated commodity names and full shop
captions. The ordinary Istanbul5900 difference is a different valid shop response
(Bulk trade rather than Business),not a shifted glyph or border change.

Releasing the town buffer before original movie heap setup restores the complete
M28 Hodram name plane in the V487 rendering fixture. Registered V488 retains all
470 batches and114 accepted layers, changes only ARM9 relative to V484 and passes
all921 graphics preservation checks. Its candidate SHA-256 is
`dc8682abbe7702026d0749c571092a51e2ad645afe8f9b89b31cec6a037eba5b`.

However, the full21200-frame fresh-game test fails at the later help interval.
Frames through14800 match;15200 differs, and subsequent frames fail completely.
The core logs an undefined instruction. Terminal PC is E58D0210. This rejects
V488 despite native tests and successful substituted movie rendering.

## Code-storage and lifecycle controls

V488 constructor code was placed in zero bytes C828-C8F4,with its pointer at C8FC.
Runtime export shows writes changing that region;initial zero contents alone did
not prove exclusive code ownership. A V489 research variant repacks the entire
constructor/cleanup/pointer into C504-C600,leaving C828-C900 untouched. All new
code bytes remain intact at the failure, but the same help crash persists.
Therefore storage relocation alone is not a valid fix or established crash cause.

The actual indirect call fails at20C8F14,return20C8F18,through an object at22CF784
whose vtable field is zero. This is stronger diagnostic evidence than interpreting
a black frame,but does not establish why the object was invalidated.

- Repacked private bitmap **without cleanup**:all56 fresh reference captures
  match exactly;terminal PC is the normal1FF9568 path.
- Repacked cleanup before movie heap setup:same16 failed frames15200-21200.
- Cleanup moved earlier,before movie display-context setup:same16 failed frames.

The SDK allocator/free APIs both use arena0 and the current heap when given-1.
Captured SDK heap descriptors show one current heap0. Wrong-heap release,
allocation identity,retained view references and exact object-lifetime corruption
remain investigation leads,not proven explanations.

## Evidence and next step

V488 native evidence:`work/analysis/town_canvas_lifetime_v488/native_proof.json`.
V488 reports:`town_lifetime_v488`, `town_lifetime_fresh_v488` and
`town_lifetime_movie_v488` under `work/emulation_v193`.
V489 manifests and research sources:`work/analysis/town_canvas_lifetime_v489`.
Full fresh/no-cleanup/earlier-cleanup reports and read-only exports are retained.

Next,resolve real allocator and UI-object lifetime safety before registering
another playable repair. A smaller/transient surface or proven safe ownership
could address the allocation interaction;do not weaken the help regression gate
or restore Japanese commodity labels as a workaround. Rejected prototypes are
not parents or release artifacts. Original ending caller/unlock and20 progressive
M28 name planes remain open. All22 historical requirements and18 incomplete
plaques remain;revisit older record-based checks at actual goal completion.
