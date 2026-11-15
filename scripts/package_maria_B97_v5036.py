"""Package verified V5030 with its exact clean-input patch and honest editorial scope."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('releases/all_routes_unified_v5030')
if __name__=='__main__':
    assert not ROOT.exists();verified=read('work/analysis/editorial_handoff_verification_v5035/verified_handoff.json');release=read('work/analysis/maria_B97_release_v5031/registered_release_verification.json');ledger=Path('translations/editorial_review_current_v1.json')
    assert sha(ledger.read_bytes())==verified['ledger_sha256'] and release['candidate_sha256']==verified['candidate_sha256'] and release['patch_sha256']==verified['patch_sha256']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    manifest=read(release['manifest']);assert len(manifest['batches'])==567 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    text=f'''# Translation DS cumulative editorial checkpoint V5030

Experimental cumulative build. The full editorial goal remains active; promoted main V4701 is preserved.

- ROM: `{release['candidate']}`
- ROM SHA-256: `{release['candidate_sha256']}`
- Clean-input patch: `{release['patch']}`
- Patch SHA-256: `{release['patch_sha256']}`
- Required clean Japanese input SHA-256: `{release['clean_input_sha256']}`
- Registered profile: `all-routes-unified-v5030`
- Immutable canonical build baseline: `{release['canonical_base']}`
- Canonical baseline SHA-256: `{release['canonical_base_sha256']}`
- Previous cumulative checkpoint: `out/all_routes_combined_v4987_candidate.nds`
- Manifest: `{release['manifest']}`

The patch applied to the exact clean input reconstructs this entire ROM byte for byte. The ROM also equals the reviewed B97-only research reference. The registered builder includes all 567 manifest batches and 114 accepted layers; all 18 release checks pass.

Only `/data/SC3.DK4` block 97 changes from V4987. Maria's complete 32-record exchange has 23 revisions and nine individually justified retentions. Preserve the village grievance,slave trading and plunder,argument against indiscriminate attacks,political alternative,voluntary invitation and uncertain tablet connection. Correct the earlier starvation implication and omitted reason the great powers seek the Proofs. All 40 original commands,eight non-speech leaves,complete speaker preambles,one faction substitution and original item display/hide remain. Every other file,story block,font,graphic,ARM9/ARM7 component and the 123040-byte staged pool is unchanged.

Maria's longer explanation uses the original A-button page advance. Both pages have complete verified glyphs;the continuation's first row keeps the original one-character guard indent. No prose was shortened or font/window widened to force one page.

Two disclosed Japanese/English content tests place the complete B97 scene in the B33 New Game slot. They display all 32 speeches/33 pages and complete the original item display and scene exit. All 327 held text planes and paired upper/portrait/name samples match their corresponding evidence. This does not establish natural event97 eligibility or earned recruitment/tablet progression. The original acquisition caption remains part of the fixture. Timing,final sailing screens,actor hashes and random-state differences are recorded without claiming full-state equivalence.

Fresh cumulative New Game and ordinary-town battery tests match V4987 across 31 whole frames and five actor/captain controls. These are targeted emulator checks;they do not establish an exhaustive playthrough or hardware coverage. Seventy-eight release/dialogue regression tests and 56 atomic rejection controls pass.

Coverage is 5,998 completed contextual rereads:3,803 revisions and 2,195 justified retentions. Source/prose coverage is 6,001,including three still incomplete shared entries. Route coverage is 4,399 reviewed and completed records;this is a counted subset,not a complete project denominator. The next Lil B184 tea scene has nine clean-only uncredited glosses. All remaining storylines,earlier wrapping,shared town/shop dialogue,random scenes,Help and player prose stay in scope. Graphics and the later older-record technical re-audit remain separate.

Final review: `translations/maria_B97_contextual_final_review_v1.json`

Current handoff: `docs/editorial_handoff_current.md`

Verification receipt: `work/analysis/editorial_handoff_verification_v5035/verified_handoff.json`

All earlier ROMs,translations,executed producers,proofs and diagnostic failures remain preserved. No promotion or pruning occurred.
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],canonical_base=release['canonical_base'],canonical_base_sha256=release['canonical_base_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],changed_internal_files=release['file_changes'],changed_blocks={'/data/SC3.DK4':[97]},whole_clean_patch_and_reference_reconstruction_exact=True,all567_manifest_batches114_accepted18_checks_pass=True,completed=5998,source_prose=6001,main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,evidence={str(p):sha(Path(p).read_bytes()) for p in ['work/analysis/editorial_handoff_verification_v5035/verified_handoff.json','work/analysis/maria_B97_release_v5031/registered_release_verification.json','translations/maria_B97_contextual_final_review_v1.json','docs/editorial_handoff_current.md']},producer_sha256=sha(Path(__file__).read_bytes())))
    print('Packaged V5030 ROM/clean-input patch references and scope;full goal active.')
