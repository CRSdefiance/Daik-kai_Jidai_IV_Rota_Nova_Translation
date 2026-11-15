"""Package the verified cumulative checkpoint and its exact clean-input patch."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('releases/all_routes_unified_v5177')
if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v5183/verified_handoff.json')
    rp=Path('work/analysis/lil_B186_release_v5178/registered_release_verification.json')
    verified,release=read(vp),read(rp)
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    assert release['candidate_sha256']==verified['candidate_sha256'] and release['patch_sha256']==verified['patch_sha256']
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    manifest=read(release['manifest'])
    assert len(manifest['batches'])==570 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    text=f'''# Translation DS cumulative editorial checkpoint V5177

Experimental verified build. The full editorial goal remains active. Promoted main V4701 is preserved.

- ROM: {release['candidate']}
- ROM SHA-256: {release['candidate_sha256']}
- Clean-input patch: {release['patch']}
- Patch SHA-256: {release['patch_sha256']}
- Required clean Japanese input SHA-256: {release['clean_input_sha256']}
- Registered profile: {release['profile']}
- Immutable canonical construction baseline: {release['canonical_base']}
- Baseline SHA-256: {release['canonical_base_sha256']}
- Complete batch and check manifest: {release['manifest']}
- Previous cumulative build: out/all_routes_combined_v5122_candidate.nds

The patch reconstructs the complete ROM byte for byte from the exact clean Japanese input. The ROM also equals the reviewed one-block reference. All570 manuscript batches,114 accepted layers and the entire previous experimental stack remain included;all18 release checks pass. Only /data/SC2.DK4 block186 changes from V5122.

The twelve-object Owner/Cook sweetness exchange has seven revisions and five individually justified retentions. It preserves the missing-sweetness realization,the stretched repeated sweet emphasis,the Cook's hesitant question,the Owner's circular self-authority,the practical question and job retort,two perfunctory yeah-yeah replies,the confident prediction and stylized laugh. The separate Sweets/Alexandria notice stays tentative. No dish,recipe,ingredient,quantity,kinship,rank,nobility,price,profit or earlier scene location is invented. Sweets is broad source sweet things;it is not a new UI category or a proved single commodity.

One paragraph now flows across three rows instead of four,with every word unchanged. Two exact source/prose-bound ordinary soft wraps use the validated space;six mutation controls prevent transfer to another paragraph. All11 other targets/native planes remain exact. Font,width,guard,phase,pagination and source controls remain checked. Earlier translations remain subject to the broader contextual wrapping review.

All24 commands,12 complete preambles,one raw700 predicate,six relative operands,three alternative opaque effects,C200 and the four-byte end remain. Source652 stored/650 logical bytes becomes584 stored/582 logical bytes,with2 alignment zeros on each side. An exact inverse plus the original alignment zeros restores every predecessor byte. All335 other SC2 blocks,every other file,font,graphic,story,ARM9/ARM7 component and the123040-byte staged pool stay exact.

Offline verification covers complete native glyph order,bounds,one-page consumption,96 initial alignments,48 stored alignments,18 consumer/28 formatter negatives,30 skip cases and5 mapped structural paths. Twelve clean/current/relocated ownership cases preserve the original random generator and optional scratch write for the halfword-aligned relocated predicate. No emulator random seed or outcome is forced. Fresh336 target loads/672 parent modes pass;parent proof reuse requires exact whole-ROM equality to the already tested V5122 reference.

Two disclosed Japanese/English B22 content cold boots retain all24 source commands plus9 opening initializers. Each actual conditional execution visits27 commands and displays all12 speeches,one selected original effect,C200,end and normal return. All47 complete text holds and115 paired upper/portrait/name samples match. Both actual sheets and20 complete paired screens were viewed. Rolls297/592 both select source effect560;returns are5735/5737. Ten timing differences and four later original A-indicator differences remain unmasked and unretimed. Final RGB,five native state groups and whole actor/captain2 models agree;final random seeds1803218166/2467799992 differ. This establishes measured scope without causal random-state,future-world/full-RAM,natural event186 eligibility,earned fashion,earlier scene location,full-route or hardware claims.

Fresh V5177 New Game4001 and inherited-battery town17401 cold boots match V5122 across31 whole frames and five actor/captain checks. Source and disposable save copies remain unchanged. The six selected startup/town captures were viewed after image return. Four content/current boots total39404 frames across the review and integration work;all jobs are terminal and reaped. All110 release/dialogue pytest regressions and84 meaningful atomic rejection controls pass. An initial wrong unittest-runner attempt remains a diagnostic and is not counted as a passing run.

One Alexandria pointer alias at1223E4/storage15E4D0 remains Japanese;the separate1230B4 alias is English. Its caller/display fidelity remains an unresolved shared-text lead. The complete clean B186 exchange was glossed before old dialogue comparison;an incidental search exposed the old closing FE before formal comparison,and that narrow provenance caveat is retained.

Coverage is6,027 completed contextual rereads:3,818 revisions and2,209 justified retentions. Source/prose coverage is6,030,including three incomplete shared records. Counted route coverage is4,428 reviewed/completed records,a subset rather than a complete project denominator. B187 has16 fresh clean-only glosses and zero credit. Its cough/unnamed almond-containing remedy exchange still needs role/name bindings and full review. Preserve reported effectiveness and strong sales as character hearsay,the forgotten medicine name,the surprised memory trigger,the search intentions and the tentative Malacca notice.

All remaining storylines,shared town/shop exchanges,random scenes,Help,player prose and earlier wrapping remain in scope. Graphics and the later older-record technical re-audit stay separate. Every earlier ROM,translation,draft,executed producer,proof and diagnostic failure remains preserved. No promotion or pruning occurred.

For user smoke testing,check New Game,an existing town save and ordinary story transitions;observe the Owner/Cook scene if it occurs naturally. Automated content fixtures and naturally encountered gameplay remain distinguished.

Final review: translations/lil_B186_contextual_final_review_v1.json

Current handoff: docs/editorial_handoff_current.md

Verified handoff: {vp}
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    save(ROOT/'verification.json',dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],clean_input_sha256=release['clean_input_sha256'],
        canonical_base=release['canonical_base'],canonical_base_sha256=release['canonical_base_sha256'],
        manifest=release['manifest'],manifest_sha256=release['manifest_sha256'],changed_internal_files=release['file_changes'],
        changed_blocks={'/data/SC2.DK4':[186]},whole_clean_patch_and_reference_reconstruction_exact=True,
        all570_manifest_batches114_accepted18_checks_pass=True,completed=6027,source_prose=6030,revised=3818,retained=2209,
        main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,Path('translations/lil_B186_contextual_final_review_v1.json'),Path('docs/editorial_handoff_current.md')]},
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Packaged verified V5177 ROM/clean-input patch and exact coverage limits. Full editorial goal active.')
