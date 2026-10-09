# Tribute direction and complete-source repair

## Verified defect in V142

Native messages 76–82 report a payment offered to the player. V142 English includes
“Pay now” and “Please pay,” reversing that direction. Other variants omit monthly
timing or gold-coin units. Message 83, a packed neighbor, omits the exclusive-contract
relationship. The complete source owners are B0 R58–R62, containing IDs 76–83.

`translations/common_tribute_repairs_manuscript_v2.json` now contains eight fresh,
natural American English translations. Their source/context/localization/naturalness
reviews are complete; **runtime formatting remains false**. Requests consistently
ask the recipient to accept tribute. Neutral variants stay statements, and the
hesitant/older variants retain their tone. The separate town notice preserves the
contract-holder/amount argument order and exclusive-contract relationship.

## Native transfer evidence

At 0202DE3C–0202DE6C the actual code obtains the payer treasury from owner+0C,
computes one percent using UMULL with 51EB851F and LSR #5, subtracts that amount
from the payer through 0203CC80, and credits the player through the same native
setter. It then obtains the payer's representative, converts the amount through
ABF50, and selects table 021189C0 at call 0202DE94. No payment request to the player
is implied by this path.

`probe_common_tribute_transfer.py` executes the actual transfer/getter/setter bodies,
with no substitute bookkeeping. Twenty-seven cases cover zero-amount skipping,
one-percent boundaries, ordinary cap 99,999,999, receiver saturation and a raw
uint32 source-field boundary. Ordinary maximum tribute is 999,999; even the raw
uint32 boundary yields only 42,949,672. Guarded adjacent object fields remain exact.
Source eligibility, full caller, actor selection, numeric conversion and presentation
are outside this transfer probe.

Twenty-three focused tests pass. Native-code mutations that reverse the payer debit,
double the amount or read an adjacent field fail. Changed reciprocal/cap literals
and out-of-range fields also fail. Ruff passes. Evidence:
`work/analysis/common_tribute_transfer_proof.json`.

## Layout and integration state

All eight literal-format previews have zero layout blockers and were visually
reviewed, including first/final glyphs. They still show `%s` rather than actual
substitutions, so they do not approve runtime formatting. The provisional V143
repacking plan fits all eight full paragraphs without shortening: 22 changed records
(five authored owners and seventeen padding donors), 83 native uint16 offsets,
all 3,668 selected texts compared, original cache sizes/NUL identities preserved.
This is a research plan, **not a registered or built V143 ROM**. V142 remains latest.

## Native expanded text and town producer

The actual message 83 caller is 020B25A8 through wrapper 020546B8. It assigns ID
83 at 020B253C. At 020B259C the first argument is the faction-name pointer; the
second argument at 020B25A0 is ABF50's converted money. Notification is conditional
on the beneficiary being the current route's faction (020B2564–020B256C). The
virtual name getter therefore selects the player-defined faction name. Its native
editor capacity is eighteen bytes, with nineteen bytes including NUL in serialized
storage; this is the existing player-name proof, not a new guessed width.

The income array at stack+490 starts with faction indices 0–19 (020B2450–020B2470).
The next loop has at most ninety contributions. Getter 020B3FD4 loads a uint16
income field; 020B24CC–020B24E0 divides it by ten. Status 3 multiplies by three and
halves; status 4 halves. The maximum contribution is 9,829, and the conservative
array sum bound is 19 + 90 × 9,829 = 884,629. This bound preserves the unusual
nonzero initial array values rather than silently treating them as zero. The
eligibility and owner-index contracts still need review in the full caller.

`probe_common_tribute_printf.py` executes the actual ABF50 number converter and
D7720 sprintf plus reached helpers for all eight draft messages. Seventy cases
cover zero, digit transitions, monthly normal/raw treasury maxima, the signed
integer maximum, and one/eighteen-byte ASCII or eighteen-byte CP932 names. Exact
expanded bytes, terminating NUL, surrounding output guards, return length and
balanced stack pass. Twenty-four actual town contribution arithmetic cases pass.
Five focused tests include a deliberately wrong native divisor, which is rejected;
Ruff passes. ABF50 uses signed division: arbitrary uint32 maximum is not a valid
positive formatting argument, and the probe explicitly rejects it.

Evidence: `work/analysis/common_tribute_printf_proof.json`, with exact V142 ARM9
and relevant native span hashes. These are native substitution proofs, not native
window-raster approval. Expanded row widths, real presentation and first-glyph
behavior remain pending; formatting review gates remain false. V142 remains the
latest built combined candidate.

## Expanded diagnostic previews and aggregate correction

The town notice draft now says “Towns under %s's exclusive contracts paid %s gold
coins in tribute.” This restores the aggregate meaning demonstrated by the native
ninety-town contribution loop and one notice per beneficiary. The Japanese noun
does not impose a singular town. The corrected full paragraph repacks without
shortening: still 22 changed records and 83 offsets; eight literal previews have
zero blockers. The provisional V143 plan was regenerated after this prose change.

`preview_common_tribute_expansions.py` generates 61 native-sprintf-expanded
diagnostic previews using the shared 216-pixel/four-row profile and exact ROM font
assets. Monthly cases include every digit transition through the raw treasury
maximum; town cases include the conservative 884,629 total and one/eighteen-byte
ASCII or eighteen-byte CP932 faction names. All fit the model, and comparison
preserves every non-whitespace glyph. The ten boundary panels were visually
reviewed: first/final characters and full numbers are visible. Two short final
lines remain: message 81 at 999,999 ends with “it.”, and message 83 with one-byte
name at 884,629 ends with “tribute.” These are unresolved review items.

Runtime-produced names are modeled as literal text, including ASCII F/I; they are
not passed back through authored-macro validation. This does not prove how the
actual COMMON window handles those bytes after substitution. Likewise, profile
word wrapping and font previews do not execute the native progressive window or
prove its pair batching, physical composition or line transitions. Do not approve
the formatting gates from these diagnostics alone. Evidence and reviewed sheet:
`work/qa/common_tribute_expanded/report.json` and `boundary_sheet.png`.

## Actual preprocessing reveals a release blocker

`probe_common_tribute_preprocessing.py` executes the actual 02054774 modal path
through 0205479C, including **CE898** (the COMMON varargs formatter) and **53914**
(the following macro expander). Earlier D7720 sprintf evidence proves a formatter
primitive only; it does not approve this complete display preparation path.

Five native cases use the real V142 formatted/expanded buffers 0228E474/0228E5A8,
bounded independently to avoid overlapping diagnostic guards. Actual CE898 output
preserves the full name, complete text and NUL in every case. The subsequent macro
expander corrupts three names: `Fleet` becomes `leet`, `Indigo` becomes `僕digo`,
and `ABCDEFGHIJKLMNOPQR` becomes `ABCDEGH僕KLMNOPQR`. One-byte `A` and nine CP932
`あ` glyphs survive. Adjacent buffers and stack writes stay within bounds.

At 5397C the expander treats uppercase F as a macro prefix even when its following
byte is unrecognized; the F disappears. At 53A44 uppercase I enters pronoun
expansion and advances two input bytes. The Japanese pronoun introduced into
`Indigo` is not evidence of an untranslated source: it is an incorrect runtime
interpretation of a player-defined name. Both macro paths still exist in V142.

This is a **release blocker for dynamic faction names**, not an acceptable preview
waiver. The repair must preserve source macros while protecting substituted name
bytes, and must pass this actual native preparation path before formatting gates
are approved. Five focused evidence tests pass, explicitly reproducing the pinned
V142 defect rather than calling it a passing release. Evidence:
`work/analysis/common_tribute_preprocessing_proof.json`. Native widgets/window
wrapping/physical display remain outside this probe.

## Display-only ARM escape prototype

`probe_common_display_name_escape.py` executes a new 128-byte ARM copy helper in
diagnostic RAM, then executes the actual COMMON CE898/53914 preparation path. It
copies CP932 pairs intact and replaces only standalone ASCII F/I with the existing
safe full-width Ｆ/Ｉ glyphs. The original name field is untouched; eighteen stored
bytes require at most thirty-six display bytes plus NUL. Bounded output guards,
input immutability, return pointer and stack are checked.

All fourteen prototype cases pass, including Fleet, Indigo, FI/IC/FO/FU/FA,
eighteen repeated F/I letters, an eighteen-byte ordinary ASCII name, nine Japanese
glyphs, and valid CP932 characters with trail bytes 46/49. Forty-one focused tests
cover each of eighteen ASCII letter positions, maximum display extent and invalid
stored names. The native macro expander is unchanged by this prototype.

This prototype is **not installed in a ROM**. A production hook/code location,
buffer allocation and lifetime, all live registers and complete enlarged-glyph
layout still require proof. Display F/I width increases from six to twelve pixels;
do not reuse the earlier all-ASCII name layout proof for escaped names. This
protects the town notice argument only in the diagnostic pipeline and does not
resolve every dynamic-name consumer in the project. Evidence:
`work/analysis/common_display_name_escape_proof.json`.

## Maximum display width and native temporary ring

The fourteen protected-name outputs now have exact-font diagnostic previews in
`work/qa/common_display_names`. Every case fits the shared four-row model; eighteen
repeated F or I letters use four rows and split the long name across a modeled
continuation. All fourteen panels were visually reviewed, including complete
first/final glyphs and six-digit money. This does not prove native progressive
wrapping or line-boundary behavior for those split names.

`probe_common_display_name_ring.py` executes actual AC000 allocation, the research
ARM escape helper and actual ABF50 conversion in **one machine**. Across all 32
starting indices and four eighteen-byte names (128 cases), the escaped name and
the amount occupy distinct 128-byte slots, including index 31 wrapping to zero.
The index advances twice; all other ring bytes and the original input remain exact.
Thirty-four focused ring tests pass. The reference comparison preserves original
CP932 extension alias bytes rather than canonicalizing them by decode/re-encode.

Evidence: `work/analysis/common_display_name_ring_proof.json` and
`work/qa/common_display_names/report.json`. A production call-site hook, executable
code placement, intervening COMMON-loader allocations and physical window display
remain pending; no profile or playable ROM has been changed.

## Serialized ARM9 caller-hook research

`probe_common_display_name_hook.py` extends the actual resident ITCM autoload
section from 01FF8000–01FF9B20 by 168 bytes (128-byte copy helper plus 40-byte
allocator wrapper). The wrapper obtains a native ring slot, protects the display
name and restores the caller's live r4/LR while setting sl to the output pointer.
The original `mov sl,r0` at 020B2590 becomes a BL to 01FF9BA0. Actual subsequent
caller instructions convert the amount and prepare ID 83/name/amount arguments.

The serialized section ends at 01FF9BC8, before the overlay load start 01FFA000.
All previous resident bytes and the complete DTCM section are exact after saving
and reparsing. In the static section, only the one hook instruction and autoload
table start/end fields change; the table moves by 168 bytes. The implicit static
section extent and all other code-settings fields are preserved. No runtime-owned
zero-filled static tail is used as a cave.

One hundred sixty cases execute the saved/reparsed ARM9 hook with five names at
every native ring index. The name, complete amount, ID 83, live amount/registers
and caller stack survive. This remains **research ARM9**, stored at
`work/analysis/common_display_name_hook_arm9.bin`; it is not a playable ROM or
registered release. Evidence: `common_display_name_hook_proof.json`. The static
reference audit, actual startup/overlay loading, intervening COMMON-loader ring
lifetime and native progressive window remain pending. Metadata non-overlap alone
does not approve those runtime contracts.

## Native startup copying and complete warm-cache preparation

`probe_common_display_name_autoload.py` executes the actual 020009E0 startup
directory iteration and section load/store instructions for original V142 and
the serialized extended ARM9. Both resident and DTCM sections arrive byte-exact;
the extended helper is copied by the native loader. Overlay destinations and the
unused DTCM tail remain untouched. Forty-two additional word stores account for
the 168-byte extension. Three CP15 cache-maintenance instructions are skipped as
an explicit hardware contract; this is not a complete cold-boot claim. Two focused
tests include a removed native store, which is rejected.

`probe_common_tribute_loaded_copy.py` repacks all eight corrected paragraphs into
research COMMON/ARM9 bytes in memory, then executes the actual hooked town path,
546B8/5528C/534F4 cache lookup and CEC74 copy, followed by real CE898 formatting and
53914 macro expansion in one machine. Twenty cases cover Fleet/Indigo, eighteen
F/I letters and nine CP932 glyphs at ring indices 0/1/30/31. Source first/final
characters, expanded corrected notice, full amount and NUL remain exact. The
native ring is allocated exactly twice; no intervening allocation occurs in this
**warm-cache** path. The manuscript source is checked against clean Japanese.

Evidence: `work/analysis/common_display_name_autoload_proof.json` and
`work/analysis/common_tribute_loaded_copy_proof.json`. Cold-cache filesystem I/O,
static gap references, physical cache coherency, full startup/overlay loading,
widgets and native progressive display remain pending. No playable V143 ROM or
release profile is registered; formatting gates remain false.

## Actual town-modal pixels reveal word/number wrapping defects

`probe_common_tribute_modal_pixels.py` connects corrected preparation output to
the unchanged native 548A8 modal pipeline, D5404 text drawing and actual ITCM
CP932 painter with the exact ROM font. Ten cases (five protected names, both pixel
formats) preserve every nonblank source glyph in order and match an independent
full-buffer font/pixel decoder. The first T and final period survive. Actual
mode-zero bounds are 256×96; the longest names render within three native rows.
The source renderer bytes and ITCM painter are unchanged by the research hook.

However, native automatic wrapping is character-based: the reviewed panels split
`paid` across rows for Fleet and split `884629` as `8846`/`29` for eighteen repeated
F/I names. Long names can also split. The earlier word-wrapped diagnostic profile
did **not** predict these native rows. Complete glyph/pixel preservation therefore
does not approve formatting. A guarded word-wrap repair must keep words and money
values together; do not shorten prose or declare these splits acceptable.

Evidence and readable ink visualization: `work/qa/common_tribute_native_modal/`
contains `report.json`, per-name PNGs and `native_sheet.png`. The ink view maps
the initialized placeholder background to white; raw native pixel hashes are
preserved. Physical parent color/routing/origin and input dismissal remain runtime
contracts. This modal result does not approve the separate portrait-bearing
monthly actor windows. Formatting gates remain false, and no V143 ROM is built.

## Guarded runtime word-wrap reference resolves the native split cases

`probe_common_tribute_guarded_wrap.py` wraps **expanded runtime text**, keeping the
authored manuscript paragraphs unchanged. The reference plans whole words within
234 pixels on the first row and 228 on continuations, and emits two protective
ASCII spaces after each generated LF. This leaves space for the real pair renderer
inside the native 256-pixel mode-zero bitmap. Complete eighteen-full-width-letter
names with possessive suffixes fit as single words. Oversized words, authored
controls, more than four rows and unexpected repeated whitespace fail closed.
Repeated whitespace in player-defined names is a remaining reference limitation;
the production implementation must preserve it rather than normalize the name.

Ten cases execute the actual modal renderer/ITCM painter with the generated text
and independently compare the complete pixels. All nonblank source characters
survive, and every complete word/money value occupies one native row. Five panels
were reviewed: the prior `paid` and `884629` splits are gone; longest F/I names stay
whole on one row. Seven focused tests cover odd/even ASCII phase at guarded LF,
leading L at x=6 in both formats, money retention and rejection of unsafe inputs.

Evidence: `work/qa/common_tribute_guarded_modal/report.json` and `native_sheet.png`.
This is a **Python wrapping reference plus actual native rendering**, not an
installed runtime formatter. A bounded native wrapper must be implemented and
connected to the research ARM9 before release approval. Source text has no manual
breaks and no shortening. Monthly portrait windows, cold-cache I/O, hardware
startup and physical input/placement remain pending; no playable ROM is changed.

## Bounded native ARM word-wrap implementation

`probe_common_native_word_wrap.py` now compiles and executes a 284-byte ARM leaf
wrapper in diagnostic RAM. It scans complete CP932 byte words, measures six pixels
per source byte (ASCII six, two-byte glyph twelve), preserves repeated separators,
and replaces exactly one inter-word space at a chosen break with LF plus two
machine guards. The original paragraph can be reconstructed exactly by replacing
each LF/guard sequence with one space, including repeated custom-name spaces.
The reference's previous repeated-whitespace restriction is removed.

Input is bounded to 224 bytes; output uses a guarded 240-byte buffer. The native
code enforces complete-word, output and four-row bounds, returns the output length,
preserves r4–r11 and stack, and leaves its complete input/adjacent bytes unchanged.
Twelve connected ARM-wrapper/native-modal cases preserve every word and complete
money value and match independent full-buffer glyph pixels. Six focused tests
cover long F/I names, repeated spaces and detection of a removed newline store.

Evidence: `work/analysis/common_native_word_wrap_proof.json`. This is executable
ARM code, but **no production macro-pass hook is installed**. Scoped connection,
temporary-output lifetime, startup copying of the enlarged payload and the full
message/renderer chain remain to verify before integration. Monthly actor windows
and physical/hardware contracts remain pending.

## Scoped word wrapping connected in serialized research ARM9

`probe_common_scoped_word_wrap_hook.py` installs the ARM word helper and a
post-macro wrapper in research ARM9. Total resident ITCM growth is 548 bytes,
ending at 01FF9D44 before the native overlay at 01FFA000. Serialization preserves
all earlier resident/DTCM content and only adds the expected static call hook and
autoload-directory relocation. The actual startup copier loads the full payload.

The modal call at 02054798 invokes the wrapper, which always runs original 53914
first. It wraps only when the original modal frame's saved parent LR is 020546E8
and the saved native ID is 83. These fields are above the wrapper's bounded scratch
frame; the wrapper reads them without modifying them. Successful output is copied
back with actual CEC74, including NUL. Rejected output is not partially committed.

Twenty-four cases execute the actual name hook, corrected COMMON warm-cache
loader, real formatting/macro expansion and scoped ARM word wrapping in one
machine, including ring wrap and repeated custom-name spaces. Twelve connected
native modal pixel cases preserve whole output. Eight scope probes show that other
IDs or parent wrappers bypass word wrapping and still execute original pronoun
expansion (`I?` → `僕`). Five focused scope/serialization tests pass.

Evidence: `work/analysis/common_scoped_word_wrap_proof.json` and research-only
`common_scoped_word_wrap_arm9.bin`. No playable V143 ROM/profile is registered.
Static gap reference audit, cold-cache disk loading, physical cache coherence/
routing/input and monthly portrait windows remain pending. Full formatting gates
remain false; this connected town-notice proof does not shrink the larger goal.

Research QA: `work/qa/common_tribute_repairs/report.json` and
`work/qa/common_native_repack_v143/repack_manifest.json`. Canonical promotion,
current ROM text and gameplay acceptance are unchanged.

## Research ITCM arena reservation

The static placement scan found an existing pointer at `020E45E4` to
`01FF9B20`, the previous resident end. Native SDK getter `020E450C` uses it
as arena 3's initial lower boundary. Earlier research extensions therefore
occupied allocatable memory and must not be used for release integration.

Both research serializers now update that initializer literal. The name-only
extension reserves through aligned boundary `01FF9BE0`; the combined 548-byte
extension ends at `01FF9D44` and reserves through `01FF9D60`. Native initial
low/high getters execute and confirm these bounds while retaining `02000000`
as the upper boundary. Both extensions remain before overlay start `01FFA000`.
Two focused tests include restoring the unsafe old boundary and verifying rejection.

The reserved combined research passes 24 warm-cache and 12 cold-cache native
ILNK cases, twelve connected native pixel cases, eight scope checks and native
startup section copying. Cold-cache open/read operations use explicit host file
contracts; physical SDK filesystem behavior is not proven. Full allocator
initialization, computed writes, cache hardware, monthly portrait windows and
playable integration remain pending. Evidence:
`work/analysis/common_itcm_arena_reservation_proof.json` and refreshed
`work/analysis/common_scoped_word_wrap_proof.json`. V142 remains unchanged.

## Native initialization and monthly portrait preparation

The complete native arena-bound initializer at `020E47C8` now executes with
diagnostic RAM globals, including native getters/setters and the initialization
flag. Original, name-only and combined research versions store their expected
arena 3 boundaries; every other low/high entry is unchanged. A repeated call
preserves established bounds. Three tests pass. This strengthens the earlier
getter-only evidence; heap allocation, later computed writes and physical startup
remain outside the proof.

Monthly messages use the separate portrait path at `02054058`. Its actual
formatting segment `02054144`–`02054164` calls CE898 then 53914 with the actor in
r10. Seventy cases across IDs 76–82, five amounts and two nonzero diagnostic actor
IDs preserve full prose, digits, leading characters, output guards and stack.
The amount range includes zero, digit transitions, normal monthly maximum and
raw uint32-treasury maximum. Actor selection/lookup, widget construction and
portrait-window raster/layout remain unproven. Evidence:
`work/analysis/common_monthly_tribute_preparation_proof.json`. Formatting review
remains false until the complete window path is checked.

## Monthly portrait geometry and raster

Native geometry segments `0205408C`–`020540C8` and
`02054174`–`0205419C` produce the lower-screen viewport `[0,96,256,192]`.
Actual constructor `02054DB0` initializes fields +40 through +4C to
`[8,16,0,0]`. The resulting client is 256×96 and uses shared text renderer
`020548A8`; the renderer passes +40 to native D4DA0, whose body is a no-op.
The research raster now supports these portrait constructor fields explicitly.

All seven drafts at normal and raw-treasury maximum amounts pass both pixel
formats: 28 actual raster cases preserve every nonblank glyph and match independent
font decoding. Eighteen cases split words or amounts. The same paragraphs executed
through the ARM word helper then rendered with guarded continuation rows produce
28 further cases with no split words/amounts. Twenty-nine existing renderer and
guarded-wrapping tests pass. No wording was shortened or manually line-broken.

Evidence: `work/analysis/common_monthly_tribute_pixels_proof.json`. These connected
separate invocations retain explicit parent bitmap/client setup contracts. Monthly
runtime hook connection, visual review, portrait composition, input, physical
routing and gameplay remain pending; formatting approval remains false.

## Scoped monthly runtime wrapping research

Research ARM9 now hooks the native monthly macro call at `02054160`. Its wrapper
always executes original 53914, then wraps only when the original portrait frame's
saved parent LR is `02053F40` and the parent's original selector-table argument is
`021189C0`. Frame offsets are +264 and +274 relative to the macro segment's stack
pointer (+364/+374 after the helper wrapper's bounded scratch allocation).

Eight actual `02053F0C` caller executions through `0205408C` establish those fields
using the native selector and warm COMMON lookup. Actor-object resolution remains
an explicit contract. Every selected draft matches the repacked full paragraph;
selector index six retains native fallback to ID76. The separate actual formatter/
macro/hook segment passes 70 cases, three other caller/table combinations bypass
wrapping, and 28 connected portrait raster cases pass. Thirteen focused tests and
lint pass. The resident extension's arena reservation and native autoload pass.

Evidence: `work/analysis/common_monthly_word_wrap_hook_proof.json` and research-only
`common_monthly_word_wrap_arm9.bin`. Visual review, whole caller/widget/render
execution, physical composition/input and gameplay remain pending. No playable
V143 ROM/profile exists and formatting gates remain false.

## Monthly visual review and connected caller state

Both sheets in `work/qa/common_monthly_native_wrapped` were inspected: all fourteen
panels preserve leading characters, complete amounts, punctuation and readable
whole-word rows. The report records the reviewed image hashes. The white ink view
is diagnostic; physical palette and portrait composition are not reviewed here.

The expanded static scan covers the full 652-byte resident extension through
`01FF9DAC`, with arena lower boundary `01FF9DC0`. It finds only the known original
arena initializer reference and records its classification; no other candidate
references occur across the original static/resident/DTCM/overlay components.
Computed addresses and indirect writes remain outside the scan's proof scope.

Eight actual native monthly callers now continue from selection and warm COMMON
lookup into formatting, macros and the scoped wrapping hook without resetting
machine state. Initial widget construction between `0205408C` and `02054144` is
explicitly skipped; actor-object lookup remains a contract. Complete selected
paragraphs, amounts, NULs and output guards survive. Four focused scope/caller tests
pass, including native selector fallback. Full widget construction, physical
portrait composition/input and gameplay remain pending; this evidence does not
approve canonical promotion or register a playable candidate.

## Strict integration plan

`dk4tool/patch/common_tribute_release.py` now performs the reproducible runtime
component insertion and complete native repack. The tracked runtime component
contains the exact 652-byte reviewed research payload and the three source-locked
hooks plus arena reservation; serialization verifies every unrelated static,
resident and DTCM byte. `scripts/prepare_common_tribute_release.py` locks the final
COMMON/ARM9 outputs after all eight full paragraphs are repacked against exact
clean Japanese owner mappings. All 3,668 selections are compared; 22 records and
83 native offsets change.

`translations/common_tribute_release_v1.json` remains explicitly draft. Its release
entry point rejects incomplete review and changed dependencies/output bytes.
Complete widget proof, final formatting approval, both native paths checked after
the final repack, integrated profile/build/patch checks and gameplay remain pending.
No profile, playable ROM, canonical change or push is claimed.

## Experimental integration review superseding the draft gate

The exact final repack passes 192 warm town cases (six names across all 32 ring
positions), 12 cold town cases using host file contracts, eight monthly native
callers and 26 native pixel cases. Both native paths retain complete prose, names,
amounts, leading/interior/final glyphs, NULs and guards. Fourteen monthly panels
and the final six-name town sheet are visually inspected, including protected F/I
and repeated name spaces. Thirty-three focused regressions and lint pass.

The manuscript's formatting gates now approve this native text-layout scope for
an experimental candidate. The earlier draft requirement for complete widgets is
retained as physical/cold-boot validation, rather than described as completed by
offline text checks. The required distinction is explicit in tracked native review
`translations/common_tribute_native_review_v1.json`; canonical acceptance remains
false. Release config dependencies and output hashes lock that review. The full
435-batch V142 stack is inherited in registered profile `all-routes-unified-v143`,
with tribute repair last. Build, saved-ROM/patch verification, physical widget/
portrait composition, hardware cache/routing/input and cold-boot gameplay remain
pending until their actual results are recorded.
