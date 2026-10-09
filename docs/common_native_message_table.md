# COMMON native message table

The clean ARM9 loader at runtime `0x020534F4` selects a COMMON block with
`0x02053628`, loads it into one of two 4,096-byte cache slots, and copies a
message to the buffer at handle + `0x2030`. These are native message boundaries,
independent of the NUL-record inventory used by older translation batches.

## Verified evidence

ARM9 file offsets (runtime load address `0x02000000`):

| Range | Meaning |
| --- | --- |
| `0x534F4..0x535E0` | Loader, including literal pool |
| `0x53628..0x53660` | Block selector, including directory pointer |
| `0x14186C..0x141910` | 41 pairs of uint16 first global ID and block size |
| `0x141910..0x1435BA` | 3,668 uint16 message offsets plus zero sentinel |
| `0x1435BC` | `COMMON/MESFILE.DK4` pathname |

The selector searches the directory's first IDs. The loader reads adjacent
global offsets. Copy length is next offset minus start; when the next offset
is smaller (a block transition), length is block size minus start. It copies
that span and writes an additional NUL terminator in its output buffer.
The displayed text can end at an earlier NUL inside the copy span.

`dk4tool/script/common_message_table.py` locks both functions, the directory,
the clean offset table and clean COMMON with SHA-256. It validates every source
span against its owning NUL record and its block's cache allocation. Candidate
mode retains the code/directory locks but reads the candidate's own offsets.
The accepted BGM layer changes 19 offsets, including ten odd byte offsets;
byte-based copying supports these. Clean offsets are all even.

## Current inventory

Combined V99 contains 829 Japanese-bearing native entries across 438
Japanese-bearing NUL records. These counts describe different boundaries and
must not be added. All 151 item descriptions are English at their native starts.
Player visibility and resource identifiers still require classification. Mapping
a string proves its boundaries, not that it is displayed in gameplay.

The same inventory finds **691 leading-prefix cases** in older translated text:
printable English appears before a native pointer where the clean prefix has
only alignment spaces. The loader selects `thing` from `Nothing` in message 824,
and `ould` from `Could` in 3033. These require repair/review before release.
This check is intentionally narrow (first local offsets one or two); packed
interior entries and endings still require a full source/translation comparison.
The 151 native item entries have their separate exact-text verification.

V100/V101 repair 687 findings. V100 restores clean alignment using unused
padding for 627 messages; V101 points 60 starts directly to existing English.
Saved checks compare all 3,668 spans and preserve all unrelated selected text.
V101's four remaining findings are packed records with merged/missing messages,
requiring a fresh eight-entry translation rather than a pointer-only fix.

V103 resolves those four records plus B33 and restores four additional messages
in B11 R0039. Native prefix findings are now zero. The inventory additionally
compares each clean message with its actual current selection and reports
**117 blank messages with Japanese source**, alongside 826 Japanese-bearing
entries. Blank messages can hide in English-marked NUL records. Both categories
require completion review; neither a percentage nor absence of Japanese proves
all engine-selected messages are translated.

`common_native_repack.py` reallocates authored records inside the original cache
block using terminal spaces from mapped, nonempty single-entry donors. It retains
LF guard bytes, every NUL/global ID and exact block sizes, recalculates all affected
offsets, and compares every selected message. The materializer uses canonical
source locks, clean editorial source, reviewed previews and cloned profile layers.

V104/V105 restore 38 B0/B1 entries and reduce blank selections to 97. New authored
packed entries need no artificial separator: the loader copies the exact native
span and writes its own NUL to the output buffer. Adding a padding space after a
four-line description can create a blank-page risk. Repack QA uses the exact
authored allocation, and a regression verifies adjacent entries remain complete
without separators. Historical candidates retain their source-locked layouts.

V106 restores twenty-one B2/B3 commodity descriptions and reduces missing native
selections to 87. The saved comparison covers all 3,668 entries, preserves every
unrelated message and all original cache allocations, and confirms thirteen changed
records and 68 updated offsets. Japanese-bearing entries remain 826; source-based
fidelity and runtime review are still required beyond structural verification.

V107/V108 restore fifty-two B4-B6 messages, retaining every source argument and
distinct warning voice. Missing native selections fall to 61. All saved entries
are compared with each parent; only COMMON and ARM9 change, preserving every
block/cache allocation. Fresh clean-source extraction of missing owning groups
and all native neighbors is available with `extract_common_blank_native_sources.py`.

V109/V110 restore fifty-nine B9-B12 messages, reducing blank native selections
to 31. All 3,668 saved selections are compared with each immediate parent.
Only COMMON and ARM9 change, preserving unrelated text and original cache sizes.
Printf order is source-locked; the live affiliation/title values in message 871
and broker hierarchy in 978 still require semantic and layout confirmation.

V111/V112 restore the remaining blank-owned B13-B16 groups and freshly repair
lateen-sail message 1285. All 66 previews are reviewed; every saved native selection
is compared with its parent. V112 reports zero blank messages and zero prefix
findings, but 826 Japanese-bearing selections remain. Older packed translations
still require full fidelity review and live macro/layout sampling.

V113 translates all twenty-nine Japanese-bearing B20 selections plus their symbolic
outburst neighbor. Thirty reviewed previews and all 3,668 saved selections pass.
Native inventory now reports 797 Japanese-bearing selections, zero blank messages
and zero prefix findings. The initial unsafe-percent outburst was corrected to an
asterisk and the rebuilt candidate passes integrity. Live layout remains pending.

V114 completes the 38 remaining B21 battle selections. V115 maps all COMMON IC
occurrences as first-person pronouns from locked ARM9 code/literals and repairs
21 occurrences plus eight neighbors. All 67 previews are reviewed and all saved
selections compared. Native inventory now reports 740 Japanese-bearing selections,
zero blanks and zero prefix findings. The pronoun audit found older single-entry
English with unrelated meaning; full older-native fidelity remains required. See
`common_IC_pronoun_mapping.md`. Live paired fleet-label expansions remain pending.

V116/V117 translate 76 B22/B23 messages with all previews reviewed and saved
selections compared. The current inventory has 665 Japanese-bearing selections,
zero blanks and zero narrow prefix findings. A broader source/current native
argument-shape audit nevertheless finds 78 older-English mismatches in 70 owners
(93 entries with neighbors). Missing counts, placeholders and merged/split text
require repair; all older English also needs semantic review. Active native
integrity comparisons now use global source identity rather than old clean byte
positions, preserving and testing intentional punctuation-only pauses.

V118/V119 repair 67 older-native messages with all previews and saved selections
checked. Full printf-shape triage leaves 24 mismatches in B12; its 26-message
draft lacks 197 terminal padding bytes and remains unregistered. Full older
English fidelity review includes argument-count matches. V119 inventory remains
665 Japanese selections, zero blanks and zero narrow prefix findings. See the
current campaign checkpoint for allocation and runtime work.

V120 now integrates all 77 B12 messages with whole-record reblocking and two
B6 repairs. The original argument-shape queue has zero mismatches. All 3,668
saved selections compare exactly; all 151 relocated items and 43 tests pass.
Clean directory/code locks remain exact; current mode accepts only the explicitly
verified relocated directory. Source contexts and item verification use global
IDs; old physical block/record coordinates intentionally change. The expanded
inventory detects erased punctuation as well as Japanese; source question 469
is restored. Runtime remains pending; 665 Japanese selections still remain.

Generate the full current inventory:

```text
python scripts/inventory_common_native_messages.py --candidate out/all_routes_combined_v120_candidate.nds --out work/analysis/common_native_v120.json
```

Any future repack must preserve global IDs and the native cache limit, update
the relevant ARM9 offsets, account for every copied entry, retain controls and
terminators, and verify unchanged entries from the saved ROM. The full table
alone does not authorize a relocation or establish runtime layout acceptance.

## V121 expedition-message extension

V121 extends the complete transform with 24 source-reviewed B24 messages and
all reviewed previews. All 3,668 saved selections match the full map; an
independent V120 comparison preserves every unrelated selected paragraph.
The exact directory hash is
`e00046fc75fe92f69ec5f484efe5307e6275cca9276def974bb15aeddddd5ee5`.
All cache limits, executable bytes and 151 item owners remain verified.
See `remaining_translation_checkpoint.md` for candidate hash, evidence and
remaining scope. Static shark argument classification is documented in
`common_shark_argument_mapping.md`; runtime expanded names remain pending.
