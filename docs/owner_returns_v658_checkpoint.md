# V658: source-bound helper return paths for unresolved controls

The previous goal turn made progress through V657's three ordinary crew policies,
complete plaque/field comparisons and saved audit evidence. This checkpoint
investigates another specific gap in the unresolved miniature/Confirm resource
search. No ROM or graphics changes are made.

## Why the earlier search was insufficient

V619's bounded ARM flow analysis propagates constants across branches and
callee-saved registers. It deliberately forgets r0–r3 and ip across opaque calls.
A helper could therefore return a calculated owner address which that analysis
would lose. Repeating literal searches or the same gameplay inputs would not
answer this question.

The separate V658 implementation preserves the V619 source unchanged and adds
return expressions for a narrowly defined, source-bound helper class. It does
not guess the behavior of opaque calls.

## Admitted helpers and native verification

The source units include every declared main section, the real runtime pool
copy and the declared ARM9 overlay. Among 6,073 direct ARM BL target candidates,
64 helpers meet the complete contract: at most eight instructions, straight-line
AL integer operations or PC-relative literal loads, ending in bx lr. They have
no calls, tail branches, predication, stack accesses, input-memory reads, stores
or saved-register writes. Other functions remain opaque.

All 64 complete bodies and every consumed literal are byte-exact to the clean
Japanese ROM. Two independent original native executions per helper check the
return expression, overflow behavior, saved-register/stack ABI and absence of
memory writes: 128 cases. This is a finite set of native witnesses plus explicit
instruction modeling, not an exhaustive test of every possible argument.

The six existing flow-analysis controls still pass. An additional positive
control calls the actual original two-instruction member helper 0201DB64 with
a deliberately supplied argument; it returns argument+0x94. The extended analysis
retains the calculated Confirm address, while unknown-input and opaque-call
controls correctly retain uncertainty. Four native caller-prefix witnesses
independently check the positive/unknown-input cases. These are isolated analysis
controls, not original gameplay consumers.

## Complete result of this bounded expansion

The flow model reaches a fixed point across 256,458 decoded source instruction
positions. It resolves return values at 1,991 source call contexts. A second
verifier executes the complete original callee for every relevant finite input
combination at each resolved context: 1,991 native context witnesses, with exact
returns, ABI and no memory writes. Unknown unused arguments are filled with zero
only in those isolated witnesses. Caller reachability, runtime arguments and
conditional-call execution are not thereby observed.

There are still seven Frame/Confirm owner candidates, with no new candidate
introduced by a pure helper return:

- Six are the original initializer's owner field stores. The complete original
  initializer is executed in clean/current machines; all 315 owners, filenames,
  writes and executed instruction bytes match.
- The remaining Frame register-copy candidate belongs to the previously bound
  view setter at 02085470. Its original source rectangle is [80,216,8,8], outside
  every miniature caption cell. The current source code remains clean-exact.

This closes the specific loss of these 64 pure return expressions. It does not
find an ordinary parent for Done, Rank, Cancel, Pick Cargo, Pick Ship or the
separate Confirm graphic. Future work should not repeat direct literals, fixed
styles or this pure-helper class. Input-memory/stack aliases, non-pure callees,
Thumb, unresolved switches, indirect paths and other runtime readers remain
outside this analysis. Initial source-table bytes are not a claim of immutable
runtime contents. No global unused-art claim follows from the negative result.

## Evidence and preservation

- Analysis: `scripts/trace_owner_returns_v658.py`.
- Independent native follow-up: `scripts/verify_owner_returns_v658.py`.
- Proof: `work/analysis/owner_returns_v658/proof.json`; subordinate source-unit,
  flow, helper, input-combination and control records are retained beside it.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V658 Owner returns`.
- Targeted Ruff and the complete native follow-up pass.
- Current ROM remains `out/all_routes_combined_v653_candidate.nds`, SHA256
  `c4e9c4faf18c212e5b6572d61e6b2821493f38bbc1dc89d601b37b16058b3ade`.

There is no new emulator run, screenshot, GPU/display, guide or ordinary control
coverage in this checkpoint. ROM, patch, manifest, registry, canonical and release
pointers remain exact. All 18 original plaque/hint entries remain incomplete and
all 22 historical scope objects remain unchanged. Other material, equipment,
card/legacy/art, transition, gameplay and final acceptance requirements remain
open. The low-resolution Online exclusions and brown-mark preservation remain
in force; older record-based checks are still due at full-goal completion.
