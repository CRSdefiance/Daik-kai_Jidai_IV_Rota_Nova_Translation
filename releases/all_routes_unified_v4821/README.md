# Translation DS cumulative editorial build V4821

Status: experimental, verified editorial checkpoint. V4701 remains the promoted main build. The full editorial goal remains active.

This build adds the complete B180 fragrance conversation: eleven contextual reviews, five revisions and six individually justified retentions. It restores the shared-impression question, removes unsupported third-person gender, preserves the speakers' courteous curiosity and comic urgency, and corrects the prospective Lisbon category from Spices to Scents. Every earlier translation, font fix and shop657 wrapping correction is included.

## Files and reconstruction

| Artifact | Repository path | SHA-256 |
|---|---|---|
| Candidate | `out/all_routes_combined_v4821_candidate.nds` | `7732a1a8431ca60c192b0f59000949b40e6ece56a6276f51a8ed81ecccc2b51b` |
| Manifest | `out/all_routes_combined_v4821_candidate.manifest.json` | Recorded in the registered release verification |
| Clean-input patch | `out/all_routes_combined_v4821_candidate.xdelta` | `d2deaf5c070fd55a5eacca35d6bd2f282413aa01e320d712c661c6de14982ad2` |
| Required clean Japanese input | `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Canonical construction baseline | `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Prior cumulative comparison | `out/all_routes_combined_v4766_candidate.nds` | `c3a9a133f7d149995a5d0feae824da32bc6741603f023ba7cda1cefb79ff4503` |

Apply the xdelta patch to the required clean Japanese input. The tested reconstruction equals the candidate byte for byte. The candidate was built through `scripts/build_integrated_release.py` using registered profile `all-routes-unified-v4821`, beginning with the canonical baseline and the complete registered stack. The manifest lists all 562 batches and all required accepted layers; 114 accepted layers are preserved. The new B180 layer remains experimental.

Only `/data/SC2.DK4` block180 changes relative to V4766. Every other internal file, font, graphic, story, ARM9/ARM7 component and runtime byte remains exact. All28 source commands, ten relative spans, two original random predicates, three alternative effects, C200 and the single end remain intact. The relocation is independently reversible.

## Verification and limits

- All18 cumulative release checks, 78 release/dialogue regressions and52 atomic rejection cases pass.
- All eleven complete current-font text planes and final stored alignment cases pass, including leading/final letters, bounds and pagination.
- Paired Japanese/English scene-entry fixtures display all eleven panels and the normal return. Two focused repeat boots account for the different original random effects and the exact one-byte town-state difference. Random outcomes were never forced. Four scene/focus cold boots total30004 frames.
- Current New Game and inherited-battery town/Refit cold boots match31 framebuffers and five actor/captain controls against the prior build with the same font. One fresh parent town control was needed. These startup/control boots add38803 frames.
- The scene fixtures enter B180 content through original B22 initialization. They do not establish natural event180 eligibility, earned fashion state, the earlier conversation's location, future-world equality, a full route playthrough or hardware verification. The inherited town battery is disclosed test context.

For playtesting, cold boot the title/New Game flow, Lil's opening, town shops and Refit, and report any missing letters, premature wraps, extra pages or transition problems. Natural encounters with the reviewed scene remain useful additional coverage.

Coverage is5923 completed contextual rereads and5926 source/prose reviews, including3753 revisions and2170 justified retentions. The next B181 ruby-necklace exchange has ten clean-source glosses and zero review credit. All other storylines, shared town/shop dialogue, random scenes, Help and player-facing prose remain in scope. Graphics and the later older-record technical re-audit remain separate and open.

Authoritative evidence: `translations/lil_B180_contextual_final_review_v1.json`, `work/analysis/lil_B180_release_v4822/registered_release_verification.json`, `work/analysis/editorial_handoff_verification_v4828/verified_handoff.json`, and `docs/editorial_handoff_current.md`.
