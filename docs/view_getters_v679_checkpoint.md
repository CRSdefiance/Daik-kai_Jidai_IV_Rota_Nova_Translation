# V679: actual owner-backed and cached-direct name-editor views

## Purpose and new source path

V678 completed the two wedding-dialogue corrections, registered/compiled the full
combined ROM and patch, verified three cold boots and archived387 files. This
goal turn returns to unresolved graphics consumers. It changes no ROM, art,
translation, patch, registry, source assets or release pointer.

Earlier V668 observed resource requests; V669/V670/V673 observed three pixel
primitives. The original generic image-view getter020D4170 has another relevant
distinction: type4 asks the view's resource owner through its virtual getter;
other types return the cached header at view+16 directly. A resource-request
trace cannot stand for those cached branches. This checkpoint records actual
complete48-byte view fields at that getter's entry.

The entire original52-byte getter is byte-identical between clean and current
ROMs. A private host-only interpreter-slot filter records its actual input CPU
prefix, eight stack words, all12 view words, and either the type4 owner/name or
the actual cached20-byte header. Original host registers, flags and stack are
preserved; the unchanged original handler executes once. No emulated CPU, RAM,
VRAM, source graphic or input is written by the observer. The host pointer is
restored before freeing the filter; the pinned DLL remains unchanged.

## Runs and exact evidence

Three ordinary7900-frame name-editor cold boots finish normally: initial
observer, unmodified-core baseline and cached-header observer. They have no
battery save, savestate, unlock or gameplay fixture. They exercise the existing
New Game name editor, Latin selection, insertion/deletion, page controls and
returns. The Japanese character-entry choices are functional keyboard content,
not an untranslated instruction or new graphic defect.

Both observed versions match all24 distinct complete two-screen baseline
captures and full terminal4MiB RAM. All50656 actual entry records repeat in
order, including CPU parameters, complete view fields, owner filenames and
zero bounded-read flags. The second observer adds only the cached-header fields
that the initial version did not record. Each filter version passes16 native
host scratch/ABI cases: full files versus last-byte corruption, the Frame/Marker
shared-header collision, owner/cached paths, invalid pointers, disabled/full
buffer and wrong-PC/instruction behavior. These are instrument controls, not
additional gameplay screens.

| Actual input branch | Entries | Source evidence |
| --- | ---: | --- |
| Owner-backed type4 |18211|Seven actual owner/filename pairs recorded|
| Cached-direct type5 |32445|Ten complete native header layouts,35 complete view field combinations|

The seven actual owner names are charselect, charselectinfo, personbustup00,
turq_sankaku, title03, title04 and Marker. None names Frame or Confirm in this
schedule. All ten original caller return addresses bind to clean-identical
direct BL instructions calling020D4170.

## Relocated descriptors and the limit of whole-file matching

The ten cached header layouts all use format4 and signed/wrapping relative
palette offsets resolving exactly to02125A20, the original text palette. The
complete32-byte palette is source-exact. Pixel offsets resolve to six addresses within02000000..02400000,
plus0601A000 and027E0000; these addresses are retained with their
complete header words. Different header sizes can share a pixel base. They are
not silently interpreted as independent fully loaded loose files.

No cached descriptor equals a whole loose Frame, Confirm or Marker file. This
does **not** prove its pixel content cannot contain a copied/converted graphic:
relative header fields and shared working canvases can differ from a file's
layout. Actual pixel content provenance and every drawing path remain separate
questions. The new evidence prevents assigning a filename to these descriptors
from a later RAM snapshot or from a partial header match.

All35 actual cached view combinations execute the complete original getter in
both clean/current isolated native machines:70 cases. They return the recorded
cached pointer, preserve view fields, saved registers and SP, make no owner
lookup and write only the saved LR on the scratch call stack. These supplied
input replays verify the complete branch, not observed live return values or
individual completed paints.

## Visual review and remaining work

Actual editor/return captures, the Japanese input page and the Latin letter page
were opened and inspected. No new lost letters, damaged graphic or unexpected
page behavior was identified in those views. The four-frame derived review
sheet is an inspection aid; all24 unmodified full captures per run are archived.
These are targeted automated emulator tests, not full-route or hardware tests.

The six small controls remain open. This resolves an instrumentation gap in
the name editor; it is not global unused-art evidence or a reason to repeat the
same filename/request or software-blitter search. Further work needs actual
cached-pixel producers, other renderers or new game contexts. All18 plaque/hint
entries remain incomplete, all22 historical requirement objects remain exact,
and eight village cards, legacy/comic/restoration contexts, older record checks
and final acceptance stay in the active graphics goal. User Online exclusions
and preservation of brown comic marks remain in force.

## Evidence

- Candidate remains experimental V678:
  `out/all_routes_combined_v678_candidate.nds`.
- SHA256: `d1aaf37bcb7dec218d200a5fa72a6c58e0fb50ab85a8bcb7766d4e749903e341`.
- Prepare/observer/controls/run/verify scripts use the `view_getters_v679` name.
- Proof, complete source contract, controls and first observer sources:
  `work/analysis/view_getters_v679/`.
- Reports, PNGs, raw traces and terminal RAM:
  `E:/Rota Nova translations/Generated/work/emulation_v193/view_getters_v679_*`.
- Archive:
  `E:/Rota Nova translations/Screenshots/Test fixtures/V679 Cached image views`.
- Focused Ruff, paired-screen/native verification and final archive checks pass.

No new playable ROM is needed. No fixture/guide publication, canonical promotion,
commit or push is performed by this checkpoint.
