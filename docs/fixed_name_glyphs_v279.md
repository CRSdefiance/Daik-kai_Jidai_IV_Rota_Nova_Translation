# Fixed naming migration: V279 research

V278 verified the76 short-slot catalog records with actual Rafael player macros
and complete native glyph pixels. This turn checks the remaining fixed records,
resolves formatter warnings and corrects a previously unmapped presentation byte.
The current playable candidate remains V275; no incomplete migration is released.

## Fixed slots and formatter warnings

The initial368 fixed records have current slots equal in length to their exact
canonical source slots. The existing balanced formatter resolves warnings on42
records without changing prose, controls, physical panel dimensions or slot sizes.
Every changed block length and NUL offset stays exact, and every unmodified
segment stays byte-identical. This is a proposal, not modified playable scripts.

## Actual four-route player contexts

Ordinary6000-frame Hodram and Lil boots supply real player RAM. The existing
Rafael6000-frame research boot is reused. Maria uses a clearly marked research
selection fixture: the original selection-limit instruction changes from3 to4
only when the native saved-flag predicate is zero. Save flags, original script/
graphics files and ARM7 are preserved. This is not a legitimate unlock or a
normal gameplay/handoff ROM. Every RAM export is hashed and read-only; no
savestate is loaded or name getter replaced.

| Player | FI | FA | FO | FU |
|---|---|---|---|---|
| Rafael | Rafael | Castor | Castor Co. | Rafael Castor |
| Hodram | Hodram | Bergstrom | Bergstrom Fleet | Hodram Joakim Bergstrom |
| Lil | Lil | Argot | Argot Co. | Lil Argot |
| Maria | Maria | Li | Li Clan | Maria Huamei Li |

The relevant compiled macro lengths match each route's actual defaults. Complete
native expansion preserves the512-byte output region, NUL, input guards, stack
and existing catalog payload. The fixed records retain their complete padding
in the font test. Independent ASCII/Shift-JIS foreground/shadow pixels, semantic
glyph order, nonoverlapping cells, first/final letters and216×64 bounds pass.

## Seven Charlotte presentation states corrected

Visual review revealed leading **P** in seven older drafts. The codepoint is
`0x50`, Charlotte's presentation state. Native caller02029B18..02029B2C extracts
that metadata byte as actor argument80 and passes the text pointer after it.
Selector0202434C returns80; ordinary table80 identifies Charlotte, clean Japanese
シャルロット. These original/current parser and selector instructions are exact.

The scoped source mapping applies only to seven exact SC0 records and their
canonical hashes. It converts the draft's leading literal P into `{SPEAKER:50}`
and calibrates the record profile accordingly. The stored actor byte remains
`0x50`; it is not removed from the script or turned into text. This corrects the
compiler's width/pair-phase model and the test's actual body selection. No global
rule interprets arbitrary English words beginning with P as controls.

One corrected record, **SC0 B67 R0148**, needs46 bytes in its45-byte slot. It joins
the catalog rather than losing words or guard bytes. The current split is now
**367 fixed records plus77 catalog records**, still444 route records overall.

The corrected367 fixed bodies pass native expansion/pixel checks, and all46
corrected sheets were viewed. Initial368-record pixel results that treated P as
text are superseded by this native parser/body correction; they do not approve
that earlier presentation model.

The77-record/133-key catalog compiles fully. All128,492 route segments and3,668
COMMON selections show no unintended/conflicting key matches. Native startup/
cache/ARM7/arena,2,128 lookup/caller/alignment cases,1,197 near-miss cases and396
literal copies pass. Total reserved payload is98,272 bytes. The enlarged
catalog's100 macro-bearing keys still need real-state expansion and final glyph
proof on that exact new artifact; the earlier76-record proof cannot approve the
new hash without revalidation.

## Source/editorial followups remain explicit

The visual review also records nine exact source-backed followups in
`editorial_followups.json`: terse artifact/greeting wording, another company-macro
double period, K-Camille stutters and inconsistent literal Claudio/Janus surnames.
These are identified review issues, not automatically approved substitutions.
Read their clean Japanese/neighbors and the source/glossary before correcting
them. Full source/context gates are not inherited from green font tests.

## Continuing integration

Next: resolve the nine source/editorial issues, revalidate the enlarged catalog
and complete the six native COMMON and two structured HELP consumers. Integrate
the fields, all444 route records, native texts and remaining name/art consistency
through one full inherited profile. Reproduce V275 and verify the full patch and
ordinary scene/transition samples before handoff.

All18 plaque/hint entries and variants remain incomplete. Low-resolution Online
images remain excluded from further translation. Other native/art, alternate
status/equipment and final whole-goal gates remain open. The goal is active and
incomplete; revisit older record-based checks at actual completion.

## Evidence

- `translations/charlotte_presentation_state_v279.json`
- `work/analysis/fixed_names_v279/charlotte_50_native_parser_proof.json`
- `work/analysis/fixed_names_v279/fixed_record_proposal.json`
- `work/analysis/fixed_names_v279/native_proof.json`
- `work/analysis/fixed_names_v279/editorial_followups.json`
- `work/analysis/name_catalog_v277/{preparation_and_scope,catalog_plan,native_lookup_proof,native_literal_copy_proof}.json`
- `scripts/prepare_fixed_name_records_v279.py`
- `scripts/verify_fixed_name_glyphs_v279.py`

The immediate native bitmap tests and captured player state do not prove every
original progressive scene, custom name, portrait transition or hardware setup.
