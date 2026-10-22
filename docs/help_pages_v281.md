# Complete structured HELP articles: V281 research

The previous turn corrected nine source/name issues and verified all444 prepared
route text bodies. This turn maps the native HELP consumer and prepares complete
Rafael/Military Investment articles without shortening their facts or links.
V275 remains the playable candidate. The HELP proposal is not integrated yet.

## Native format and limits

The original HELP article consumer is0207CE1C. It loads an ILNK topic into the
shared02233040 buffer and parses characters, newlines and inline topic links.
The renderer uses42 six-pixel cells,12-pixel source rows and a ten-row table.
Plain English is processed in two-byte runs. A newline or opening brace in the
second byte would not be parsed as its intended structural control.

Links are `{label:<one-byte topic ID>}`. They are not ordinary translated text.
Original references are retained:

| Article | Link | Topic ID |
|---|---|---:|
| Rafael | Military investment |37|
| Rafael | Influence |184|
| Military Investment | Market share |150|
| Military Investment | At war |187|

The byte150 followed by `}` can decode as a Japanese glyph; that decoded string
does not describe the actual link syntax. Source parsing skips complete Shift-JIS
characters before recognizing braces, so a trail byte that happens to equal `{`
is also not mistaken for a link.

## Complete continuation pages

The reviewed biography and investment article are longer than their old fixed
slots and ten-row display. The proposal uses native topic navigation:

- Rafael: topics7 and202.
- Military Investment: topics37,204 and205.
- Topic203 remains empty because203 is the native history's unused-slot sentinel.

The archive grows from202 to206 blocks. All200 unrelated original blocks remain
byte-identical. The formatter keeps semantic sections and whole paragraphs on
pages where possible, with Continue reading and Back to article start links.
Every word of the reviewed sections is mechanically compared with the generated
content, including both benefits, Lisbon/Mediterranean, doubled Influence,
Palace/Governor's Office,1–20 units,50/40-percent cost, both market-share
conditions, surrender resistance and better ships/cannons.

No manual alignment or shortened substitute is authored. The compiler moves an
existing boundary space into a link label where necessary to keep plain runs
even; it adds only invisible end-of-line pair padding. Visible text retains
ordinary word spacing. Link labels remain atomic and preserve their IDs.
Content targets41 cells plus a possible blank guard within the native42 cells.
Every page uses at most ten rows; the largest new page is304 bytes.

## Native proof and visual review

All five pages execute the original parsing loop and native ASCII painter.
Complete independent font pixels, every first/final letter, semantic glyph order,
exact line coordinates, link request IDs/rows/widths and input/header/pixel guards
match. The complete native page sheet was viewed with readable full prose and
distinct link styling. The parser's link-child creation is an observed contract;
this does not prove the final clickable UI child or a mouse/touch interaction.

The actual ILNK reader opens and loads all206 selected blocks using the exact
HELP caller's zero requested-size/full-block contract. Every block, terminal
NUL and adjacent guard is exact. The largest loaded block is388 bytes, below the
preceding archive's396-byte maximum. The only host bridge supplies SDK file I/O;
native ILNK header, offset, selection and copying execute.

Eight cases execute the original topic-history updater for original links and
all continuation IDs. The requested slot and unused203 sentinels remain exact.
Actual clicked Back/Forward and whole widget/display construction remain open.

The test harness initially reused a view address inside its larger pixel buffer.
Relocating that harness object resolves the extra unrelated pixels; no game code
or article wording changed. A finite page-size-based instruction budget allows
the complete parser/font loop to finish, with completion checked explicitly.
Targeted Ruff passes.

## Remaining work

Verify complete native clickable child construction and ordinary HELP navigation/
screen composition, then integrate these blocks with the complete name/text/art
migration through one registered inherited profile. The six native COMMON final
expansion/display gates and remaining broader editorial/name-art work also stay
open. Reproduce the preceding ROM and verify the full clean-ROM patch plus
ordinary changed-screen/scene samples before handoff.

All18 plaque/hint entries and variants remain incomplete. Low-resolution Online
images remain excluded from translation. Other native/art, alternate status/
equipment and final whole-goal requirements remain open. The goal is active and
incomplete; revisit older record-based checks at actual completion. Include raw
HELP link-token identity in that older-check review, rather than trusting a
CP932-decoded pseudo-glyph for a binary topic ID.

## Evidence

- `work/analysis/help_consumers_v281/page_proposal.json`
- `work/analysis/help_consumers_v281/native_parser_proof.json`
- `work/analysis/help_consumers_v281/native_archive_history_proof.json`
- `work/analysis/help_consumers_v281/native_help_pages.png`
- `scripts/prepare_help_pages_v281.py`
- `scripts/verify_help_parser_v281.py`
- `scripts/verify_help_archive_v281.py`

These are native loader/parser/pixel tests with controlled font/UI inputs, not
full gameplay navigation or hardware verification.
