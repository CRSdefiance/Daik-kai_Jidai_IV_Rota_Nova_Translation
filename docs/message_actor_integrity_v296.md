# Native actor integrity repair V296

The previous turn resolved the four held naming preambles and found378 current
speaker-byte mismatches. V296 repairs all378 in the complete inherited release.

## High-level rule and lossless repair

A native0xFFFF4000 message object stores actor state in the metadata high byte,
not as visible text. The old formatting sometimes dropped a printable actor or
encoded actor0A as a protected leading newline. That made the first English byte
become actor state and shifted the actual body pointer.

262 actor0A records remove only the synthetic space/LF/guard prefix, restore0A
and move the freed bytes into trailing padding.114 other records use one existing
trailing padding byte to restore the actor. Two full records, SC3B62R0053 and
B139R0177, consume their existing zero native alignment byte. The following native
command addresses and all block/archive extents are exact. Every word, punctuation
mark and macro is retained. No new RAM, renderer or font change is needed.

The two consumed alignment bytes remove an empty NUL-only artifact from each
block. Later NUL-entry ordinal IDs in those blocks are therefore not stable
post-repair identifiers. Use original source IDs plus native object byte offsets;
all native command addresses remain unchanged. The release report declares the
exact two cases. This is why NUL-only record checks cannot substitute for native
object and VM-cursor verification.

## Verification

All378 repaired objects execute the original actor parser, complete body scan and
native VM cursor rounding. Original actor values and all body words/macros pass,
and all378 cursors equal their prior next-command positions. The external display
call is an explicit bridge in this isolated cursor test.

The integrated transformation now enforces original actor preservation across
all19254 native message objects using stable byte positions. FullV275 reproduces
byte-for-byte after the shared-builder change. All467 accepted/experimental batches
and required layers remain in the candidate manifest. Changed files versusV275
are only SC0/SC1/SC2/SC3; all ARM9/ARM7/overlay/font/art bytes are exact.

A production Rafael6000-frame cold boot reaches title/New Game/selection/opening.
A separate Maria fixture changes the established one-byte selection limit only;
it is not a legitimate unlock or a playable handoff. Its6000-frame ordinary input
run displays repaired Xien Yan dialogues SC3B33R0086/R0103. All933 and660 black
native glyph pixels, first/internal/final letters and bounds match independently.
No savestate is loaded; all capture hashes and empty callback errors pass. Both
processes exited. These are targeted emulator tests, not complete route/device tests.
The clean-base xdelta reconstructs exactly. Ruff passes.

## Registered artifacts

| Item | Identity |
|---|---|
| Profile | all-routes-unified-v296 |
| Candidate | out/all_routes_combined_v296_candidate.nds |
| ROM SHA256 | 6096fb457d460c53964f1fe3c7aac33e152ac7eef28fefe6309e202760497833 |
| Patch | out/all_routes_combined_v296_candidate.xdelta |
| Patch SHA256 | 37ebba3db532d866a9da304f3d29d9c61ae1432f98f618cce4d517de7e7b5a7d |
| Canonical base | out/raphael_natural_v2_accepted_base.nds |
| Canonical SHA256 | 3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe |
| Clean patch input | work/clean.nds |
| Clean SHA256 | f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d |

Evidence is under `work/analysis/message_actor_integrity_v296`: native proof,
transform proof, full_actor_gate.json, actual_display_proof.json, preceding exact
reproduction and reconstructed ROM. The manifest declares all inherited stages
and repaired source IDs/native offsets. The stage is source/target/census locked.

## Remaining goal work

Experimental; explicit user cold-boot acceptance remains pending. The canonical
base is unchanged. Test new games and ordinary dialogue on the user's emulator,
particularly Xien and generic NPC names, full first letters and page continuation.

The newly reviewed444 naming-source corrections, shared name fields, COMMON/HELP
and artwork captions still need combined integration and current allocation/copy/
glyph checks. Broader embedded/native context gates and all18 plaques plus Armor/
Weapon variants remain incomplete. Online-image translation exemption is retained.
The graphics goal is active and incomplete. Revisit older record-based checks at
actual completion, including NUL-ordinal and native metadata assumptions.
