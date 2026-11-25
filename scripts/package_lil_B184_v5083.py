"""Package the verified cumulative ROM,clean-input patch and honest test scope."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('releases/all_routes_unified_v5076')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v5082/verified_handoff.json')
    rp=Path('work/analysis/lil_B184_release_v5077/registered_release_verification.json')
    verified,release=read(vp),read(rp)
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    assert release['candidate_sha256']==verified['candidate_sha256'] and release['patch_sha256']==verified['patch_sha256']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    manifest=read(release['manifest']);assert len(manifest['batches'])==568 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    text=f'''# Translation DS cumulative editorial checkpoint V5076

Experimental verified build. The full editorial goal remains active. Promoted main V4701 is preserved.

- ROM: `{release['candidate']}`
- ROM SHA-256: `{release['candidate_sha256']}`
- Clean-input patch: `{release['patch']}`
- Patch SHA-256: `{release['patch_sha256']}`
- Required clean Japanese input SHA-256: `{release['clean_input_sha256']}`
- Registered profile: `{release['profile']}`
- Immutable canonical build baseline: `{release['canonical_base']}`
- Canonical baseline SHA-256: `{release['canonical_base_sha256']}`
- Previous cumulative build: `out/all_routes_combined_v5030_candidate.nds`
- Full batch,changed-record and verification manifest: `{release['manifest']}`

The clean-input patch reconstructs this entire ROM byte for byte. It also equals the reviewed one-block reference. All 568 manifest batches,114 accepted layers and the complete prior experimental stack are retained;all 18 release checks pass. The newly added batch is `translations/lil_B184_editorial_manuscript_v5.json`.

Only `/data/SC2.DK4` block184 changes from V5030. This nine-record tea exchange contains four revisions and five individually justified retentions. It preserves the couple's enjoyment,household tea errand,relaxed calm and playful hyperbole,followed by the tentative Tea/Sofala notice. It invents no marriage,age,kinship,city shortage,price,profit or medical/gameplay effect.

The visual review also corrected premature wrapping in the delayed-popularity observation. It now uses two readable rows and keeps “catch on sooner” together,with every word unchanged. The exact source/prose-bound correction preserves all other targets,font,width,guards and controls. Earlier translations and retained wording remain subject to the broader wrapping review.

All 12 source commands,nine complete speaker preambles,A000,C200 and the four-byte end remain. The block shrinks from432 to416 stored/logical bytes with no trailing alignment bytes;an exact inverse recovers every predecessor byte. Every other story block,file,font,graphic,ARM9/ARM7 component and the123040-byte staged pool is unchanged.

Two disclosed Japanese/English B22 content fixtures displayed all nine panels and completed all21 commands,including the nine original opening initializers and normal town return. All35 held text planes and115 paired upper/portrait/name samples match. Both actual panel sheets and20 full screens were viewed. Eight command timings and four later original A-indicator differences remain recorded without masking or retiming. Final RGB,five measured native groups,whole actor/captain2 and the measured random seed agree;this does not prove full-state or future-world equivalence. These fixtures do not establish natural event184 eligibility or earned fashion progression.

Fresh current New Game and inherited-battery town cold boots match V5030 across31 whole frames and five actor/captain checks. The battery remains unchanged and does not represent newly earned progress. All four content/current runs total39404 frames. These are targeted emulator checks,not an exhaustive playthrough or hardware verification. Seventy-eight release/dialogue regressions and71 pre-mutation rejection controls pass. Native glyph,bounds,wrapping,pagination,loading,reference and control checks also pass.

Coverage is6,007 completed contextual rereads:3,807 revisions and2,200 justified retentions. Source/prose coverage is6,010,including three incomplete shared records. Counted route coverage is4,408 reviewed/completed records,a subset rather than the full project denominator. The next fur/cold-weather scene has eight fresh clean-only glosses and no review credit. Its explicitly reported sales and rising prices must be preserved,while its separate Stockholm fashion forecast stays tentative.

All remaining storylines,shared town/shop exchanges,random scenes,Help,player prose and earlier wrapping stay in scope. Graphics and the later older-record technical re-audit remain separate. All earlier ROMs,translations,executed producers,proofs and diagnostic failures remain preserved. No promotion or pruning occurred.

For user smoke testing,check New Game,an existing town save and ordinary story transitions;observe the tea conversation if it occurs naturally. Automated coverage and unvisited conditions remain distinguished in the records.

Final review: `translations/lil_B184_contextual_final_review_v1.json`

Current handoff: `docs/editorial_handoff_current.md`

Verified handoff: `{vp}`
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],canonical_base=release['canonical_base'],
        canonical_base_sha256=release['canonical_base_sha256'],manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],
        changed_internal_files=release['file_changes'],changed_blocks={'/data/SC2.DK4':[184]},whole_clean_patch_and_reference_reconstruction_exact=True,
        all568_manifest_batches114_accepted18_checks_pass=True,completed=6007,source_prose=6010,main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,Path('translations/lil_B184_contextual_final_review_v1.json'),Path('docs/editorial_handoff_current.md')]},
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Packaged verified V5076 ROM/clean-input patch references and exact coverage scope. Full goal active.')
