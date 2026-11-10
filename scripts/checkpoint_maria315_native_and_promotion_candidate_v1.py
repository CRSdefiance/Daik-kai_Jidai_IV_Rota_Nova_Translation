"""Save unfinished prose/native work and identify the fully qualified testing ROM."""
import ast
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Maria_B286_B302_clean_20261110')
PACKAGE = Path('releases/all_routes_editorial_20261110_maria349_candidate')


def main():
    releasepath = Path('work/maria349_B275_B285_release_v1/registered_release_verification.json')
    release = load(releasepath)
    prosepath = Path('translations/maria_B286_B302_contextual_review_v1.json')
    namespath = Path('translations/maria_B286_B302_scoped_names_v1.json')
    prose, names = map(load, [prosepath, namespath])
    expected = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
    assert len(prose['records']) == 315
    assert Counter(r['decision'] for r in prose['records']) == dict(revision=162, retention=153)
    assert len(names['records']) == 14
    assert all(r['review'] == expected for d in [prose, names] for r in d['records'])
    nativepath = ROOT / 'native_body_v1/compiled_native_pages.json'
    native = load(nativepath)
    assert (len(native['records']), native['pages'], native['fresh_compiled_alignments']) == (309, 309, 1236)
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and native['direct_visual_review_pending']
    selectionpath = ROOT / 'native_final_selection_v1/resume_selection.json'
    selection = load(selectionpath)
    assert selection['native_selection_complete'] and selection['reused_records'] == 309 and selection['remaining_records'] == 0
    oldplanpath = ROOT / 'plan_v3/automatic_plans.json'
    planpath = ROOT / 'plan_v4/automatic_plans.json'
    oldplan, plan = map(load, [oldplanpath, planpath])
    assert not plan['failures']
    assert [(r['id'], r['encoded_hex']) for r in oldplan['records']] == [(r['id'], r['encoded_hex']) for r in plan['records']]
    assert not any(i['severity'] in ['error', 'warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    stylespath = ROOT / 'compiled_styles_v1/compiled_style_objects.json'
    menupath = ROOT / 'menu_native_v1/group_verification.json'
    nameplanespath = ROOT / 'name_planes_v1/native_name_planes.json'
    styles, menus, planes = map(load, [stylespath, menupath, nameplanespath])
    assert (len(styles['objects']), styles['physical_alternatives'], styles['native_target_slot_cases']) == (17, 113, 136)
    assert sum(len(n['rejected']) for n in styles['compiler_negatives']) == 153
    assert (menus['menus'], menus['captions'], menus['native_provider_alignments'],
            menus['bridged_modal_returns'], menus['current_andtarget_normal_highlight_planes'],
            menus['compiler_negatives']) == (3, 6, 18, 54, 24, 21)
    assert (planes['actors'], planes['distinct_current_strings'],
            planes['fresh_native_name_strings'], planes['reused_native_name_strings']) == (14, 18, 12, 6)
    report = Path('work/promotion_candidate_repository_qa_v2/pytest.xml')
    tests = ET.parse(report).getroot()[0]
    assert (tests.attrib['tests'], tests.attrib['errors'], tests.attrib['failures']) == ('27', '0', '0')
    producers = sorted(Path('scripts').glob('*maria315*.py')) + [
        Path('scripts/plan_scoped_clean_editorial_v4.py'),
        Path('scripts/prepare_promotion_candidate_maria349_v1.py')]
    for path in producers:
        ast.parse(path.read_bytes(), filename=str(path))
    promotionpath = PACKAGE / 'verification/promotion_reconstruction.json'
    promotion = load(promotionpath)
    assert digest(promotion['candidate']) == release['candidate_sha256'] == promotion['candidate_sha256']
    assert promotion['exact_registered_candidate_reconstructed_from_clean_input'] and not promotion['main_promoted']
    qa = PACKAGE / 'verification/promotion_repository_checks.json'
    assert not qa.exists()
    save(qa, dict(tests=27, passed=27, errors=0, failures=0, terminal_exit_code=0,
                 report=str(report), report_sha256=digest(report),
                 first_attempt='work/promotion_candidate_repository_qa_v1/pytest.xml',
                 first_attempt_result='25 passed; two temporary-directory setup errors before test bodies; parent created for fresh v2 run',
                 producers_parsed={str(p): digest(p) for p in producers},
                 pending_Maria315_not_in_test_ROM=True))
    note = PACKAGE / 'PROMOTION_CANDIDATE.md'
    assert not note.exists()
    note.write_text('''# Promotion-ready testing copy — November 10, 2026

Use `out/promotion_ready_20261110_maria349_v1/Translation_DS_Maria349_promotion_candidate.nds` and its adjacent manifest. This is a fresh clean-input reconstruction of the registered Maria349 release, byte-identical to the previously qualified candidate; it adds no unapproved text. ROM SHA256: `fd825d4d7b0ae27192da6ad193117d5759685416e41e9a0802ec5f45484fd6f0`.

The existing `translation.xdelta` reconstructs this same ROM from the clean Japanese input identified in README.md. All 724 manifest entries, 114 accepted layers and 59 release checks are preserved, including Rafael/tutorial work, the Market Trade-screen correction and ASCII right bounds. Fresh repository verification passes 27 tests. Existing startup, protected-name and representative gameplay proofs apply to these exact bytes; this packaging step claims no new gameplay. Main remains V4701 until explicit acceptance after cold-boot testing.

The separate Maria315 B286–B302 batch is saved in Git with 162 proposed revisions, 153 justified retentions and 14 scoped name reviews. First four prose gates pass. Native checks pass 309 bodies/309 pages/1,236 alignments, 17 complete style objects, six captions and 18 name strings. Direct visual review, storage/gameplay checks, fifth gates and registered integration remain pending. These edits are not included in this ROM and add no completion credit. Resume from the current editorial handoff; preserve the full goal and all historical evidence.
''', encoding='utf-8', newline='\n')
    save(PACKAGE / 'checksums.json', {
        str(p.relative_to(PACKAGE)).replace('\\', '/'): digest(p)
        for p in PACKAGE.rglob('*') if p.is_file() and p.name != 'checksums.json'
    })
    paths = [prosepath, namespath, ROOT/'prose_gates_v1.json', ROOT/'scoped_terms_reference_v1.json',
             ROOT/'scoped_names_reference_v2.json', ROOT/'dynamic_roles_current_v1.json',
             nativepath, oldplanpath, planpath, selectionpath, stylespath, menupath, nameplanespath,
             ROOT/'planner_actor0_executed_v2_snapshot.py', releasepath, promotionpath, qa, note,
             Path('scripts/plan_scoped_clean_editorial_v2.py'), *producers]
    evidence = {str(p): digest(p) for p in paths}
    summary = ('Maria315 B286–B302 has315 contextual comparisons:162 proposed revisions,153 justified retentions and14 scoped names;'
        'allfirst four prose gates pass. Fresh native checks pass309 bodies/309 pages/1236 alignments,17 styles/136 slots,6 captions and18 name strings. '
        'Direct visual,stored/gameplay,fifth gates andintegration remain pending. A fresh clean-input reconstruction ofthe fully registered Maria349 candidate '
        'isready for user testing;724 entries/114 layers/59 checks and27 fresh repository tests pass. Main awaits acceptance;23778 integrated,full goal active,no worker live.')
    document = 'docs/editorial_Maria315_native_and_promotion_candidate_20261110.md'
    text = f'''# Maria315 native checkpoint and promotion candidate — November 10, 2026

{summary}

Testing ROM: [Translation DS Maria349 promotion candidate](../out/promotion_ready_20261110_maria349_v1/Translation_DS_Maria349_promotion_candidate.nds). SHA256: `{release['candidate_sha256']}`. Adjacent manifest is an exact copy of the registered manifest, whose paths retain their original provenance. The standalone GitHub package is [here](../releases/all_routes_editorial_20261110_maria349_candidate/PROMOTION_CANDIDATE.md). The fresh copy was decoded from the existing registered patch and clean input and compared byte for byte to the qualified release. This is a reconstructed testing copy of Maria349, not a newly integrated Maria315 build. Startup, all24 protected getters, actual191-body/193-page samples andall59 release checks are reused only because the ROM is identical. No new gameplay orhardware claim. Main remains V4701 pending explicit user acceptance after cold-boot testing.

The user requested a build to promote andcommit/push our work. Pending edits are checkpointed separately rather than granting premature release approval. The previous GitHub release commit `c3bf64e6e2bb7717f781cef7fb6f8469b1989f32` is preserved. The upcoming commit saves this complete checkpoint, package proofs andthe unfinished prose manuscripts; Git publication is verified separately after committing.

Continue from the prior [clean binding checkpoint](editorial_Maria315_B286_B302_clean_bindings_20261110.md); its completed source/draft/current bindings remain valid. All315 records in17 whole exchanges were contextually compared against the clean Japanese and sealed independent drafts. Individual exact source/current references, findings and162 revisions/153 justified retentions are in `translations/maria_B286_B302_contextual_review_v1.json`. All14 scoped names have justified retentions in `translations/maria_B286_B302_scoped_names_v1.json`; first four gates are true andevery formatting gate stays false. Actor156 is explicitly supplemented:28 original name getters,18 distinct strings. Four item titles,five commodities,three places andthe full Proof of Conquest convention are exactly bound in `scoped_terms_reference_v1.json`. No invented kinship,rank orbiography is introduced.

The review corrects third-person self-reference,unsupported claims,reported uncertainty, the guardian's reversed discovery andthe reversed Sextant handover. Charles mentioned the monk's Alchemy Book; he did not write it. Keep the source mineral-poison/medicine/sacrifice progression without inventing a toxin ormedical training. Preserve allsource actors,including Rafael0 in B286 andLil2 in B302,independently ofcurrent captain Maria3. B295R4's full-width Latin I andtwo full-width question reactions are corrected as text/glyph issues. Existing natural short reactions and Xiexie remain for individual documented reasons. All full exchange detail remains in the manuscripts rather than repeated here.

Final plan `plan_v4/automatic_plans.json` has309 bodies/309 pages,zero errors/warnings/failures andsix separate captions. B298R49's complete warning/question now fits one page rather than stranding “into their hands?” on a second page; prose is unchanged. The actor0 planner requires exactly the two source-qualified records and complete original preambles. Repository review found that the earlier continuation had reused historical helper filename v2; its exact executed bytes are preserved in `planner_actor0_executed_v2_snapshot.py`,historical v2 is restored byte for byte from Git,andthe new helper is separately versioned as `scripts/plan_scoped_clean_editorial_v4.py`. Fresh v4 planning reproduces every encoded byte ofthe completed native run. `native_final_selection_v1/resume_selection.json` binds all309 durable receipts without repeating native rendering. Earlier failed/superseded plans andproducers remain historical evidence.

Native body session34165 finished terminal0:309 records,309 pages,1236 alignment cases,complete first/internal/final glyphs,canaries,bounds,consumption andpagination. Seventeen whole style objects pass136 slots and153 compiler negatives. Three two-choice menus passsix captions,18 alignments,54 modal returns,24 normal/highlight planes and21 negatives. Names pass12 fresh/six exact reused strings across14 actors. These are offline checks: no newly generated body,caption orname sheet has yet been directly viewed in this batch. All fifth gates stay false. No Maria315 ROM,storage check,actual scene observation,release registration orcompletion credit is claimed.

Next directly view every generated body page via readable contact sheets plus allname/caption sheets,then save visual approval. Bind styles to final plan_v4 using exact same bytes; reuse compatible completed native receipts. Complete stored reconstruction,allocation/branches/lookups andrepresentative initialized gameplay,including originalactor0/Lil headers,B295 glyph/FA,13FE returns,the reclaimed question page andallthree menus. Register the cumulative successor andexact clean-input patch only after necessary checks,then credit315 once. Do not restart clean drafts,prose comparisons orcompleted native rendering.

Fresh repository QA passes27/27 tests,terminal0. Initial v1 had25 passing andtwo temporary-directory setup errors before those test bodies; the fresh v2 run after creating its parent passes all27. The first reconstruction attempt was denied access to the generated-output junction before output; the authorized elevated retry passes. No auto-review rejection occurred. No running batch job remains.

Integrated counts remain23,778=14,181 revisions+9,597 retentions;historicalsource/prose/draft count23,781. Native story remainder2,120=Maria315+Lil1,805 includes this entire uncredited batch. Shared/shop/town/random/player-facing scope andthe broader207-name review remain separate. Preserve every earlier translation,retention,ROM,draft,proof andfailed producer. Fullstory scope,earlyRafael/tutorial priority,wraps andglyph consistency remain active. No guide photos. Deferred graphics artwork andthe later older-record technical re-audit remain separate.
'''
    checkpoint(mutation=ROOT/'native_promotion_progress_checkpoint_v1',
        batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Maria315 prose/native checked; visual/storage/gameplay/release pending.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, proposed_revisions=162, justified_retentions=153,
            native_job_live=False, native_sessions=[], stored_job_live=False, stored_sessions=[],
            registered_build_live=False, registered_cumulative_build_live=False, no_batch_worker_live=True,
            current_batch_evidence=evidence, guide_photos=False,
            previous_goal_turn_classification='progress', current_goal_turn_classification='progress',
            next_action='Directly view allMaria315 native body/name/caption pages;stored andrepresentative gameplay then registered integration.'),
        additional_updates={'Maria_SC3_B286_B302_clean_20261110': dict(new_credit=0,
            contextual_comparison_pending=False, names_terms_consumers_pending=False,
            proposed_revisions=162, justified_retentions=153, current_scoped_actors_bound=14, current_name_getters_bound=28,
            first_four_individual_gates_pass=True, all_five_review_gates_pending=False, all_fifth_gates_pending=True,
            offline_native_body_records=309, offline_native_pages=309, offline_native_alignment_cases=1236,
            direct_visual_review_pending=True, stored_checks_pending=True, gameplay_pending=True,
            registered_integration_pending=True, no_batch_worker_live=True, evidence=evidence, full_goal_complete=False)},
        summary=summary, document=document, document_text=text, completed=23778,
        protected={'translations/release_stack.json': release['registry_sha256'],
            release['candidate']: release['candidate_sha256'], release['manifest']: release['manifest_sha256'],
            release['patch']: release['patch_sha256'], release['canonical_base']: release['canonical_sha256']})
    save(ROOT/'native_promotion_checkpoint.json', dict(document=document, evidence=evidence,
        native_terminal_exit_code=0, all_fifth_gates_pending=True, new_credit=0, full_goal_complete=False))
    print('PASS checkpoint:315 prose decisions/native checked;no new credit;Maria349 testing candidate ready.')


if __name__ == '__main__':
    main()
