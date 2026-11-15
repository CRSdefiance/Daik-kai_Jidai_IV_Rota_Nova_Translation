"""Save all382 contextual prose reviews and provisional layouts without completion credit."""
import ast
import gzip
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Lil382_residual_A_clean_20261110')
ARCHIVE = Path('translations/editorial_checkpoints/Lil382_prose_20261110_v1')


def main():
    assert not ARCHIVE.exists()
    manuscript = Path('translations/lil_residual_A_382_contextual_review_v1.json')
    namespath = Path('translations/lil_residual_A_382_scoped_names_v1.json')
    prose, names = map(load,[manuscript,namespath])
    assert (prose['source_objects'],prose['complete_exchanges'],prose['proposed_revisions'],prose['justified_retentions'])==(382,30,257,125)
    assert names['scoped_actors']==34 and names['first_four_gates_pass']
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records']+names['records'])
    gates = load(ROOT/'prose_gates_v1.json')
    assert gates['structural_projection_pass'] and gates['all_fifth_gates_false']
    assert 'v2 requires per-record' in gates['unformatted_manuscript_rejected_by_release_gate']
    old = load(ROOT/'plan_v1/automatic_plans.json')
    planpath = ROOT/'plan_v4/automatic_plans.json'
    plan = load(planpath)
    diagnostics = load(ROOT/'plan_v4/diagnostics.json')
    assert len(plan['records'])==378 and sum(r['expected_native_pages'] for r in plan['records'])==386
    assert not plan['failures'] and not diagnostics['failures']
    assert not any(i['severity'] in ['error','warning'] for i in diagnostics['issues'])
    oldby = {r['id']:r for r in old['records']}
    changes = [dict(id=r['id'],old_pages=oldby[r['id']]['expected_native_pages'],new_pages=r['expected_native_pages'],
        before_lines=oldby[r['id']]['lines'],after_lines=r['lines']) for r in plan['records'] if r['encoded_hex']!=oldby[r['id']]['encoded_hex']]
    assert len(changes)==14 and sum(r['expected_native_pages'] for r in old['records'])==391
    assert sum(c['old_pages']-c['new_pages'] for c in changes)==5
    objects = load(ROOT/'current_objects_v1/current_objects.json')
    assert len(objects['style_records'])==14 and len(objects['choice_records'])==4 and objects['native_style_getter_cases']==16
    assert len(objects['credited_style_context_preserved_not_newly_reviewed'])==1
    assert len(objects['credited_style_context_preserved_not_newly_reviewed'][0]['source_records'])==5
    negatives = load(ROOT/'credited_context_negatives_v1/qualification.json')
    assert len(negatives['rejections'])==2 and all(r['rejected_before_output'] for r in negatives['rejections'])
    macros = load(ROOT/'formatting_v1/native_macro_measurements.json')
    assert macros['macro_ascii_lengths']==dict(FI=3,FA=5,FO=9,FU=9)
    assert sum(len(v['native']['cases']) for v in macros['defaults'].values())+len(macros['FE_FI_preflight']['cases'])==20
    assert load(ROOT/'mixed_static_selector_macro_preflight_v1.json')['alignment_cases']==12
    pending = ROOT/'provisional_layout_findings_v1.json'
    assert not pending.exists()
    save(pending,dict(changed_layouts=changes,initial_pages=391,provisional_pages=386,pages_reclaimed_offline_only=5,
        changes_preserve_all_logical_prose=True,body_objects=378,menus=2,captions=4,
        native_pixels_anddirect_visual_approval_pending=True,
        multipage_records=[r['id'] for r in plan['records'] if r['expected_native_pages']>1],
        short_internal_rows_from_page_clause_preferences_require_native_visual_review=True,
        no_fifth_gate_orcompletion_credit=True,new_credit=0))
    producers = [Path('scripts')/p for p in [
        'bind_editorial_current_credited_objects_v1.py','save_clean_editorial_comparisons_v3.py',
        'bind_lil382_terms_v1.py','finalize_clean_editorial_prose_v2.py','prepare_lil382_prose_v1.py',
        'prepare_captain_clean_formatting_v1.py','plan_captain_clean_editorial_v1.py',
        'refine_lil382_planned_pages_v1.py','qualify_lil382_credited_context_v1.py',Path(__file__).name]]
    for p in producers:
        ast.parse(p.read_bytes(),filename=str(p))
    ARCHIVE.mkdir(parents=True)
    artifacts = {}
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path.suffix not in ['.json','.txt']:
            continue
        target = ARCHIVE/path.relative_to(ROOT)
        target = target.with_suffix(target.suffix+'.gz')
        target.parent.mkdir(parents=True,exist_ok=True)
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
        assert gzip.decompress(target.read_bytes())==raw
        artifacts[str(path)]=dict(archive=str(target),source_sha256=digest(path),archive_sha256=digest(target))
    archive_manifest = ARCHIVE/'archive_manifest.json'
    save(archive_manifest,dict(artifacts=artifacts,all_historical_versions_preserved=True,
        raw_ROM_RAM_andcaptures_not_in_archive=True,records=382,first_four_gates_pass=True,formatting_pending=True,
        producers={str(p):digest(p) for p in producers},new_credit=0,full_goal_complete=False))
    releasepath = Path('work/maria315_B286_B302_release_v1/registered_release_verification.json')
    release = load(releasepath)
    protected = {'translations/release_stack.json':release['registry_sha256'],
        release['candidate']:release['candidate_sha256'],release['manifest']:release['manifest_sha256'],
        release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256'],
        str(manuscript):digest(manuscript),str(namespath):digest(namespath),
        'translations/promoted_build.json':digest('translations/promoted_build.json')}
    evidence = {str(p):digest(p) for p in [manuscript,namespath,archive_manifest,pending,
        ROOT/'prose_gates_v1.json',planpath,ROOT/'plan_v4/diagnostics.json',releasepath]}
    document = 'docs/editorial_Lil382_prose_layout_20261110.md'
    summary = ('Lil residual A has all 382 contextual prose decisions: 257 proposed revisions, 125 justified retentions and 34 scoped name reviews. '
        'All first four individual gates pass; fifth gates remain false. Fresh plans cover 378 bodies/386 pages plus four captions, '
        'with zero errors, warnings or failures; 14 layouts change and five pages are reclaimed offline. '
        'Native rendering, every-page visual review, storage, representative gameplay and registered integration remain pending. '
        'No new ROM or completion credit; 24,093 integrated. The registered Maria315 promotion candidate and main remain unchanged; the full goal stays active.')
    text = f'''# Lil residual A — contextual prose and provisional layouts, November 10, 2026

{summary}

The previous goal turn was progress: a fresh exact clean-input reconstruction of the registered Maria315 candidate was prepared, and the build handoff plus unfinished Lil drafts were committed and pushed as `acca7e229f9d424f8172912eabb5bbee38ecbe9b`. Local and GitHub heads matched and the working tree was clean at that handoff. This continuation adds substantive editorial work; it does not replace or promote the testing ROM. [Promotion build and provenance](editorial_promotion_Maria315_Lil382_checkpoint_20261110.md). Preserve all earlier ROMs and translations.

All 382 clean-first source objects in 30 complete groups now have exact source/current references, individual findings and reviewed English in [the contextual manuscript](../{manuscript.as_posix()}). The 257 revisions and 125 retentions are distinct from passing technical checks. Read all 391 source context objects, preserving nine already-credited B115 objects without duplicate credit. All clean meanings and independent drafts remain sealed and unchanged. The aggregate records 22 explicit contextual source-gloss/name corrections plus one improved retention explanation; it also supplies concise complete-exchange context for every group. The first four source/context/localization/naturalness gates pass on every record; the unformatted manuscript is correctly rejected by the v2 release gate. No formatting gate is inferred from prose approval.

Corrections include Gerhard’s personal refusal to lose; Angel’s movement to the enemy’s starboard quarter; source-accurate Yuris/Plett names; the specified enemy flagship; Miss FA rather than an invented noble Lady title; and distinct letter-announcement voices. The whole Aziza arc preserves the two-million demand/one-million agreement, her father’s accidental death and vanished Bloodstained Shamshir, her grief, voluntary retirement and recruitment. The keepsake does not earn money; it is not worthless. Al’s intervention adds no romance or ownership. Manuel’s mourning and sea/mother poem retain lyrical intent and reported linguistic similarity without inventing a real language example or a dead mother.

B115’s eligible Maria/Xien controls remain unchanged within SC2. Maria’s argument preserves slavery, pillage, the ruined village, indiscriminate-hatred warning, great-power partition and the Proofs of Conquest, with confidence rather than a guaranteed victory. Jam’s clean gambling opponent is Fernando: current Peres and independent-draft Emilio are both corrected. All actor20 contextual gloss labels are reconciled without rewriting the source-first seal. The bard-like arrow rumor uses the installed Demon-Piercing Arrow title; no cannon effect or treasure location is certified. Francisca’s explicit name replaces dear, her father’s birthday gift remains precious, and the barkeep is not invented as her father. Gabriel’s tab joke, glass swindle and escape remain; future handover is to the governor’s office. Twelve older mixed-width punctuation records have ASCII proposals. The source still distinguishes figurehead attempt/failure/success/refusal and FI Spirit +1.

The [34 scoped name decisions](../{namespath.as_posix()}) retain exact source/current identity and both native getter consumers, with individual reasons. Approved Lil/Maria/Camille forms remain. Janus, Cristina, Yuris, Fernando and the Jam Jack Ludwyan signature are reconciled in context. Angel, Snake and Dandy remain pirate nicknames. Barkeep, Port Worker, Priest and Bandit avoid invented kinship/rank. Sailor nameplates and existing catalogue subordinate aliases are retained only for these exact consumers; broader catalogue terminology and the full 207-name review remain separate. Full catalogue UI layout, fonts and newly rendered names are not approved by these prose gates.

The original style binder failed because B115 includes a complete already-credited context style object. Its guarded successor binds 14 selected physical style bodies/16 native slots and four captions, while preserving all five credited context alternatives explicitly. It verifies exact source bindings and current credit membership before exclusion. Two focused negatives reject falsely uncredited context or a missing exact source binding before output; originals and the ROM remain exact. An initial projection lacked the prepared per-block hash field and failed before output; the byte-identical complete-context prepared projection passes. The successful `current_objects_v2/current_objects.json` is preserved, with a verified byte-exact canonical alias under `current_objects_v1/`. No native guard or branch inventory was removed or repeated.

All 14 dynamic style references use selector208. Its original startup fallback is actor151/voice4, while the captain control207 resolves to Lil2. This proves no future conditional participation. Six item titles, Spirit and the exact previously approved Proofs of Conquest anchor are bound. Unnamed gloves, Gupta statue and figurehead stay descriptive where the source does not speak a catalogue title. Fresh original-ABI preflight passes 20 default/null-actor FE macro alignments and 12 additional Maria3/Aziza27/Escante43 cases. Defaults are FI Lil, FA Argot, FO Argot Co., FU Lil Argot; measured ASCII lengths are 3/5/9/9. These are macro/guard checks, not new gameplay or font approvals.

The fresh full-width formatter covers all 378 bodies and four separate menu captions. Initial `plan_v1` had one orphan final row in Aziza’s challenge; keeping me or together fixes it without changing prose. `plan_v2` passed with 391 pages. A focused boundary review found 13 paragraphs to revisit; nine full-paragraph one-page attempts and four clause preferences were tried. Four one-page attempts were rejected by unchanged constraints; one clause needed its exact comma and one weak determiner ending needed a phrase-pair preference. Failed `plan_v3` is preserved. The passing provisional `plan_v4/automatic_plans.json` has 378 bodies/386 pages, zero errors/warnings/failures, 14 changed layouts relative to v1 and five pages reclaimed. Text, controls, substitutions, physical widths (216 progressive/228 FE), fonts and runtime are unchanged. Every final plan still needs native pixels and direct visual approval. In particular, review all eight multipage paragraphs: some page-clause preferences produce short internal rows, and automated QA alone does not establish their readability. Refine those layouts from readable native contact sheets before the fifth gates.

All current JSON/TXT artifacts, including decisions, failed/superseded plans and original sealed drafts, are archived losslessly under [the durable checkpoint](../{archive_manifest.as_posix()}). The archived manifest records exact original and compressed hashes. Raw ROM, initialized RAM and captures remain local. No new 382-object gameplay was captured this turn; the existing 4,001-frame Lil runtime context is an opening snapshot only. Native body/caption/name rendering, every generated page’s visual review, stored-script allocation/relocation/pagination checks, representative distinct-behavior gameplay and registered cumulative integration/exact clean-input patch/own startup are the next work. Reuse completed source/prose and compatible renderer proofs; do not restart this review or the native census.

Integrated counts remain 24,093 = 14,343 revisions + 9,750 retentions. Native Maria census is 5,129/5,129; native Lil remainder is 1,805, including this still-uncredited 382. The registered candidate remains `{release['candidate_sha256']}`, with 725 entries/114 accepted layers/60 release checks; main stays V4701 pending acceptance. Full story/shared/shop/town/random/player-facing scope, earlier unfinished contextual passes, early Rafael/tutorial priority and the broader name review remain active. Keep deferred graphics artwork and the later older-record technical re-audit separate. No guide photos; no batch worker is live.
'''
    checkpoint(mutation=ROOT/'prose_layout_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Lil382 all contextual prose/name gates pass; provisional full-width plans checked; native/visual/storage/gameplay/release pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True,proposed_revisions=257,justified_retentions=125,
            current_batch_evidence=evidence,no_batch_worker_live=True,guide_photos=False,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            next_action='Render all378 Lil382 bodies/386 provisional pages andfour captions/34 scoped names; review every page andrefine multipage boundaries before stored/gameplay/release checks.'),
        additional_updates={'Lil_SC2_residual_A_382_clean_20261110':dict(new_credit=0,
            style_andchoice_binding_pending=False,current_styles_bound=14,current_captions_bound=4,
            contextual_comparison_pending=False,names_terms_consumers_pending=False,
            proposed_revisions=257,justified_retentions=125,current_scoped_actors_bound=34,current_name_getters_bound=68,
            first_four_individual_gates_pass=True,all_five_review_gates_pending=False,all_fifth_gates_pending=True,
            provisional_formatting_bodies=378,provisional_formatting_pages=386,offline_plan_layout_changes=14,offline_plan_pages_reclaimed=5,
            native_rendering_pending=True,direct_visual_review_pending=True,stored_checks_pending=True,gameplay_pending=True,
            registered_integration_pending=True,no_batch_worker_live=True,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=24093,protected=protected)
    for path,item in artifacts.items():
        assert digest(path)==item['source_sha256']
    print('PASS durable382-prose/provisional386-page checkpoint;zero new credit;registered candidate unchanged.')


if __name__=='__main__':
    main()
