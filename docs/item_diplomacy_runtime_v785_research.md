# V785: item-shop and diplomatic-letter runtime research

## Current release and editorial coverage

V783 remains the current registered, batch-verified experimental ROM and patch.
This checkpoint creates no playable ROM, changes no production COMMON text,
and grants no additional completed-entry or production-formatting approval.
The ledger remains **417 completed entries, 496 source/prose reviews and 79 drafts**.
The next batch is still COMMON 1070–1145: 63 proposed revisions and 13 retained
wordings. The separate graphics audit, including the original 18 plaques,
remains unfinished. The Online screenshot-body exclusion, preserved brown marks,
approved character names and older-record follow-up remain in force.

## Runtime progress

The extended selector fits its existing 128-byte table and 172-byte gate bank.
It uses an 11-bit start and 5-bit interval length, preserving exact memberships.
Role-table keys retain 32-byte alignment; the older queued tables retain
16-byte alignment. Pointer keys are biased away from numeric coordinate/status
IDs. This fixes a collision found during prototyping before any ROM was built.

Six guarded changes produce research ARM9 SHA-256
`288bcbfa29e2cbc6df81326bade9f074c156148cf2c2749ccabc0c570bbba4bf`.
The source ARM9 is V783's
`daa9686528955df3e88258c5c3fc1b63adb551b08669f2a33584e3bd9d674c02`.
No section, BSS, cache, startup, arena or 123,040-byte staged-payload geometry grows.
Every byte outside the six declared patches is restored and compared exactly.

| Evidence | Verified scope |
| --- | --- |
| 35,072 native selector cases | Exact old/new memberships, tested intervening/unaligned keys, wrong parents/high halves, registers, SP and LR |
| 140 status contracts | Complete 8 MiB guards, old UI names, all tested status sentences and ABI |
| Private reference census | Earlier external incoming contracts preserved, including the documented V772 bridge rebind |
| Instruction audit | Exact new code extents contain Thumb-1 and ARMv5 BL/BLX instructions |
| 40 original getter cases | Both type getters, all ten types, exact pointers/text, complete 8 MiB preservation and callee-saved ABI |
| COMMON 676/677 | Repaired native wrapping and complete text preserved in research bytes |

These are targeted native CPU tests. No new gameplay capture, complete playthrough,
hardware validation or new shop-scene activation is claimed. The V747 shop
framebuffer remains the actual scene reference for the user's formatting example.

## Storage conflict caught and corrected

The initial 0214C550–0214C564 lead is **rejected**. Although the Japanese label
table no longer points there, V626 already installs live strategist alignment
code in those bytes. An absence of absolute pointers was not ownership proof.
The source-byte guard stopped the prototype before a ROM could be produced.
V626's complete alignment/fallback bytes remain unchanged.

The moved `major economic boom` constant instead uses 20 bytes at
0216DEFC in the original Extras tie-in introduction's documented allocation.
Its complete translated prefix and terminating NUL remain exact. Absolute,
ARM/ADR, Thumb and crossing-string leads are inspected. Two apparent ARM
branches are words in the unchanged 0216215C–0216515C coordinate array:
its original base literal and consumer are pinned, and the original halfword
streaming instructions reproduce both coordinate pairs. These two cases are
qualified individually; there is no general data-range or unaligned-reference waiver.

## Six letter-type names

The V783 and research getters still return Japanese for types 0–5.
Types 6–9 remain exactly `Lure Fleet`, `Forge Papers`, `Bad Rumors` and `Bribe`.
The six proposed English document names are:

- goodwill letter
- pact proposal
- pact termination notice
- truce proposal
- declaration of war
- demand for submission

`Pact termination notice` is the revised nominal rendering of 協定破約.
It expresses the same complete notice and termination meaning as the earlier
`notice of pact termination` draft and reads naturally after `our` and `this`.
The original V784 plan and manuscript remain intact; the V2 proposal is separate.
The earlier prototype layouts using the old nominal phrase are not relabeled
as approval of the new getter output.

The six complete NUL-terminated names need 110 bytes. A nonoverlapping placement
fits within 132 source-bound bytes: three original scheme-label groups and two
retired village clues. Both complete active village replacements still match.
The two apparent village pointers span original MOV/BL instruction words;
both exact original instruction pairs are executed to their real callees with
argument, LR and whole-memory guards. All other current direct leads are the
six original type-table fields, which require an atomic registered redirect.
The intervening `7CScheme` RTTI name, adjacent code and all earlier text are preserved.

This is a **placement proposal**, not permission to overwrite the source labels.
Complete computed/virtual getter consumers, immutable-use/write closure and
display bounds/crops must be established first. Some consumers may require
context-specific nominal wording; the current 93D28/93D5C getter behavior is unchanged.

## Remaining batch work

1. Close original Guild constructor/NPC context, branch eligibility and arguments.
2. Map every relevant letter-name consumer, including virtual getters and crops;
   finish write exclusions and implement the six names through source guards.
3. Produce current native layouts and full font previews for every revised
   argument/output path, including the revised type-2 phrase.
4. Integrate all 76 paragraphs through natural-dialogue-v2 and the registered
   full release stack. Verify complete copies and exact clean-input patch.
5. Test representative actual buy/sell/bargain and diplomatic scenes, ordinary
   startup, scene transitions, bounds, pagination and complete letters.

Then continue COMMON 1146 onward, resolve 750–752 and review all routes and
remaining prose. No completion claim or canonical promotion is made.

## Evidence and reproduction

Research: `work/analysis/item_diplomacy_runtime_v785`.
Run `scripts/verify_item_runtime_v785.py`,
`scripts/audit_item_runtime_storage_v785.py`,
`scripts/research_item_type_storage_v785.py`, then
`scripts/record_item_runtime_v785.py` with the repository Python dependencies.
Research and producers are copied with SHA-256 receipts to
`E:/Rota Nova translations/Editorial review/V785 Item and diplomacy runtime research`.
No new guide screenshots, commit or GitHub push is produced.
