# V547 native legacy descriptor provenance

V546 is unchanged. This is an evidence checkpoint, not a new ROM candidate.
The previous goal turn made progress by correcting source bevels. This turn
captures fresh ordinary New Game chooser RAM and executes original descriptor
setup to distinguish native workspace storage from unresolved raw archive art.

## Verified current state

The sole captured synthetic header is at02192E34, in controller02192500 at+934.
Its words are8,52,136,000E6B04,00112940. Original constructor instructions
0209ED40-0209ED94 reproduce all20 bytes using the actual current parent/globals;
all other main RAM bytes remain unchanged. The controlled fragment preserves
captured valid format flags: the code updates the low byte/100 bit and does not
initialize every reserved high bit. Poisoning the whole flags word was an invalid
contract and is excluded from proof.

The palette pointer is02279938. Every one of its256 lower15 BGR555 colors matches
the native flat GRP/CMMNIMG.000 prefix.227 complete words differ in their high bit.
No alpha behavior is inferred solely from lower15 normalization. This palette
is not equivalent to the legacy ILNK CMMNIMG.DK4 block0 palette.

The pixels pointer is022A5774. The complete original initializer at 0x0210DC24 sets indexed8 and direct16 headers at022A554C
and022A5560 to share that pixel storage. The complete native call returns with
its stack/saved-register ABI and adjacent header canaries intact. Indexed8 has
word width128,height192; direct16 has width256,height192. Original face-strip
header setup0210D5A8-0210D5E8 reproduces the captured56x512 indexed descriptor
at02279894 before subsequent resource/UI initialization. That fragment is not
credited as a complete initializer or ABI test.

Raw SLACK17 is byte-exact in02233040 after the four raw portrait reads. That
address differs from the synthetic header's pixel pointer, and the workspace
prefix is not the raw block. Existing V202/V479 loose portrait display/binding
proofs remain separate. Do not decode raw14-17 with this descriptor's palette
or infer that it displays raw19 comics.

## Scope and remaining work

The exact relevant instructions match the clean ROM. The current run cold boots
through ordinary New Game with no battery save, savestate, cheat or RAM fixture.
The original snippets execute on an isolated copy of the captured RAM. The full
UI constructor, other users, indirect/file-ID readers, raw archive color mapping,
comic19 display and global non-use remain unproved. Continue tracing the actual
raw-buffer users/other archive readers and source artwork review. Preserve all
22 original requirements and18 incomplete plaque/hint entries.

Proof:work/analysis/legacy_descriptor_v547/descriptor_proof.json.
Verifier:scripts/trace_legacy_descriptor_v547.py;Ruff passes.
No new ROM/patch or canonical promotion. Revisit older record-based checks only
when the full graphics goal has actually completed.
