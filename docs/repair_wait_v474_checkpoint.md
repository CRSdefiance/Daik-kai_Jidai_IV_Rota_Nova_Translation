# V474 repair dialogue word boundaries

The actual Genoa Yard repair message801 previously split wait as wa/it. Its clean
Japanese says to wait one day until repairs finish. The existing English remains
unchanged: Repairs will take one day. Please wait until they're finished.

The original portrait caller02054014 now routes only801 into the established
portrait word wrapper. One dispatch instruction and20 bytes of existing empty
ITCM space change. The SDK bank remains4096 bytes. All other ARM9 bytes,COMMON
prose and directory,HELP,route files,PXL/FLS art,palettes,dimensions and borders
remain identical to V468. This is a scoped fix,not a claim that every native
dialogue caller throughout the game has received word wrapping.

## Verification

Native execution compares all3668 IDs in the original and alternate parent:
7336 dispatch comparisons. Only801 in the intended parent is added. All42 complete
old rumor,clue,equipment,Guild and neighbor wrapper cases remain exact. The native
renderer retains every glyph and every word on one row;source/output guards and
saved-register ABI pass through the inherited harness.

Matched cold boots of the genuine Valencia save replay the normal Genoa voyage
and repair in V468 and V474. All130 captured frames before the repair match.
The actual corrected screen has611 complete glyph pixels:333 on the first line,
278 on the second. Both lines begin at x22,y296/312. Every pixel outside the
repair-text rectangle remains exact. The original donor remains unchanged.

Fourteen earlier Rafael sailor-column frames and56 fresh-game title,character,
story,town and Help-entry frames match. All470 inherited batches and every V468
stage remain registered. The exact patch reconstructs the candidate from clean.
Targeted DeSmuME evidence does not prove hardware or full-game completion.

## Combined candidate

- Profile: all-routes-unified-v474,experimental.
- Base: out/raphael_natural_v2_accepted_base.nds,
  SHA256 3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
- Candidate: out/all_routes_combined_v474_candidate.nds,
  SHA256 1d513b81762499f0fd6a2edeeabb182a69c334756fc9261f70c07a0110984b9e.
- Patch SHA256 2ad890f698830dc528aaf48d9cdf4423c3f58dd03b8194bd95e855740a8d497c.
- Relative to V468,only /__arm9__.bin changes.
- Native verifier: scripts/verify_repair_wait_native_v474.py.
- Release verifier: scripts/verify_repair_wait_release_v474.py;Ruff passes.
- Proof: work/analysis/repair_wait_v474/release_proof.json.

ROM,patch,manifest and the finalized native repair screenshot are saved on E.
No canonical promotion. Human cold-boot acceptance remains required;test title,
New Game and the Yard repair message before accepting the candidate.

The repaired/rested Genoa save remains reusable. Occupied Weapon,other equipment
conditions,and the full legacy/environment/Gallery/ending graphics requirements
remain open. All22 historical requirements and all18 incomplete plaques retained.
Revisit older record-based checks at actual full-goal completion.
