"""Preserve clean B199 progress and paired-label context without integration credit."""
import argparse
import gzip
import json
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B199_and_names_checkpoint_v5776')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5777')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5762/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
KEY='Lil_B199_clean_source_and_couple_names_context_v5776'
SCOPE='unfinished_editorial_scope_v5776'
PREVIOUS='previous_latest_checkpoint_before_B199_and_names_v5776'
OLD_SCOPE='unfinished_editorial_scope_v5761'
COUNTERS=dict(records_editorially_completed=6232,records_with_source_and_prose_pass=6235,
              records_revised_and_integrated=3917,retained_wordings_editorially_completed=2315)
PACKET=Path('work/analysis/lil_B199_source_v5767/all31_clean_current_complete_context.json')
GLOSS=Path('work/analysis/lil_B199_clean_context_v5765/all31_clean_portrait_chase_found_book_and_misunderstood_gift_glosses.json')
CONTEXT=Path('work/analysis/couple_context_review_v5775/five_whole_source_contexts_paired_label_draft_and_B199_name_fields.json')
CENSUS=Path('work/analysis/couple_speaker_uses_v5773b/all_four_routes_direct_role_speech_census_and_complete_native_exchanges.json')
GETTERS=Path('work/analysis/couple_name_consumers_v5774/four_current_native_role_getters_and_exact_staged_owners.json')
SUMMARY=(
 'V5776 records a fresh clean-Japanese whole-exchange pass for31 uncredited Lil SC2B199 speeches before earlier English prose. '
 'The portrait identification and qualified reputation lead into Lil\'s impatient summons,Samwell\'s explicit body-size taunt,'
 'cartoon chase and four FE impact beats,Camille\'s FI-addressed complaint,tidying and discovery of an apparently old book,'
 'then Lil\'s return and the mistaken-present exchange. Preserve two attempted corrections,her appreciation and his final '
 'private uncertainty. Parentheses at70/115 stay private;the book is not an intended romantic present and remains untitled. '
 'Do not invent kinship from adult-man address,ownership,author,era,injury,rank,romance or item powers. '
 'Source1168 stored/1166 logical bytes plus two tailzeros has47 commands/31 speeches:30 progressive/one FE,'
 'selectors2/9/22/FE,one FI,no FA/FO,no typed choices/style objects,relative sites or C200. One2000 pause,'
 'two distinct picture commands,four resource controls,two short47xx,one A000 and the complete ending require '
 'their own source-bound control review. Do not transfer B198\'s predicates,style or FE voice. '
 'All31 clean/current command shapes and preambles match;31 are disjoint from6232 completed objects. '
 'Fresh current207-name/eight-voice resolution binds Lil2 voice3,Camille9 voice2 and Samwell22 voice2. '
 'Pass62 source/current dispatches including two FE cases and original FI expansion,one original event199/action200 '
 'getter with no explicit dependency prefix,and a fresh zero-relative-site census. '
 'Six guarded original progressive/full-catalogue name consumers preserve actor models and unowned4MiB. '
 'Clean fields bind Lil Argot,Camille\'s Marinus/Overijssel fields and Samwell\'s middle ダ;the existing untranslated '
 'Samwell full-catalogue field stays open without silent Romanization or new retention credit. '
 'Portrait subject ロッコ＝アレムケル is not found in the207 clean name entries;approved Latin spelling remains pending. '
 'Current English speech is stored only as structural hex,not used as a translation source or approved prose. '
 'The requested retrospective proper-name and speaker-role localization continues. The screenshot tea request is '
 'actor165 in SC0B196R22/SC1B188R22/SC2B184R22/SC3B157R21,not COMMON. '
 'Clean164/165 labels are カップル男/カップル女. A literal full-preamble census of1307 stored storyline blocks '
 'finds96 direct role speeches in17 blocks and581 stored contextual speeches,grouped into five identical role sequences. '
 '1312 event actions must not be confused with1307 stored blocks;the initial failed producer is preserved. '
 'Five complete representative exchanges comprising212 speeches and27 distinct role utterances were manually read: '
 'Ian tavern observers,Fernando\'s distant breakup,tea,cold/fur,and Mikhail\'s conversation without this woman\'s partner. '
 'Do not claim all581 manually reread or that differing route surroundings are identical. '
 'Propose natural nameplates Man/Woman in place of Man in a Couple/Woman in a Couple,with exact source/current '
 'references and individual reasons. Preserve relationship facts in dialogue;do not add marriage,age or grandfather kinship. '
 'Four current read-only progressive/full-catalogue native getters agree;each staged label has one ARM9 literal '
 'pointer and sole owner across all207 primary/secondary/middle table fields,with no table-interior alias. '
 'This literal census does not exclude dynamic consumers. Target label display,runtime substitutions,other relevant '
 'consumer review and registered integration remain pending. Earlier label rationale and207-entry queue remain intact. '
 'No new ROM,emulator run,source/prose completion or duplicate shared-dialogue credit is added. '
 'Counts remain6232 completed/6235 source-prose/3917 integrated revisions/2315 justified retentions/SC24347/SC396/'
 'routes4633/4633,zero pending credited route drafts. Registered experimental V5756 and its exact clean-input patch '
 'remain unchanged;main V4701 remains promoted. Preserve all ROMs,translations,drafts,proofs,failures and history. '
 'The full four-storyline,earlier translated dialogue,shared town/shop,random,Help and remaining-prose objective '
 'continues,including retrospective early wrapping and proper-name/role-label localization. '
 'Graphics/all18 plaques and later older-record technical re-audit remain separate/open.'
)
NEXT=(
 'Continue Lil SC2B199 from31 clean-first glosses5765,source packet5767,native dispatch/entry/relative/name '
 'proofs5769-5772 and clean name fields5775. Bind the one2000 pause/resume,two source picture layouts,'
 'four resource commands,two short47xx,A000 and poisoned complete ending/tailzeros before approving their semantics. '
 'Keep the portrait subject spelling pending until a source-bound project naming decision;do not guess from catalog absence. '
 'Then compare previous English as a whole exchange and prepare individually justified revisions/retentions,validated '
 'native display,representative content gameplay and registered cumulative release with exact clean patch. '
 'No B199 integration credit yet. Continue paired164/165 proposed Man/Woman from five clean whole-context reasons5775 '
 'and four native current consumers5774. Bind remaining relevant substitution/consumer paths,verify complete proposed '
 'nameplate/catalog display and representative distinct behavior before registered integration. Do not globally replace '
 'all Man/Woman labels or double-credit previously integrated dialogue. Preserve207-name queue,Samwell middle-field '
 'finding and other alias leads. Do not repeat sealed B198/Stockholm checks without a concrete new risk. '
 'Keep the entire four-storyline/earlier-dialogue/shared town/shop/random/Help/prose and early-wrap goal active. '
 'Graphics/all18 plaques and later older-record technical re-audit remain separate. No promotion,pruning,commit or '
 'push is part of this checkpoint.'
)

def inverse(value):
    old=deepcopy(value)
    old['latest_checkpoint']=old.pop(PREVIOUS)
    old.pop(KEY);old.pop(SCOPE)
    return old

def check(plan,applied=False):
    for item in plan['files']:
        assert sha(Path(item['target']).read_bytes())==item['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(item['planned']).read_bytes())==item['planned_sha256']
        assert sha(gzip.decompress(Path(item['before']).read_bytes()))==item['before_sha256']
    for p,digest in plan['evidence'].items():assert sha(Path(p).read_bytes())==digest
    old=json.loads(gzip.decompress(Path(plan['files'][0]['before']).read_bytes()))
    new=read(plan['files'][0]['planned'])
    assert inverse(new)==old
    assert sha(encode_ledger(old))==plan['files'][0]['before_sha256']
    assert new['current_integrated_candidate']==old['current_integrated_candidate']
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items())
    assert new['goal_status']=='active' and not new['full_goal_complete']
    prior=read(PRIOR)
    assert prior['ledger_sha256']==plan['files'][0]['before_sha256']
    for key in ['candidate','patch']:
        assert sha(Path(prior[key]).read_bytes())==prior[key+'_sha256']
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    return new

def stage():
    assert not ROOT.exists() and not VERIFY.exists()
    before=LEDGER.read_bytes();old=json.loads(before);prior=read(PRIOR)
    assert sha(before)==prior['ledger_sha256']
    assert not any(k in old for k in [KEY,SCOPE,PREVIOUS])
    packet,gloss,context,census,getters=map(read,[PACKET,GLOSS,CONTEXT,CENSUS,GETTERS])
    rows=packet['blocks'][0]['records']
    assert len(rows)==len(gloss['records'])==31 and gloss['prior_English_speech_unread']
    known={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    assert len(known)==6232 and not known&{historical_key(r) for r in rows}
    assert packet['current_ROM_sha256']==prior['candidate_sha256']
    assert context['manual_review_scope']==dict(complete_representative_exchanges=5,complete_representative_speeches=212,
                                               distinct_role_utterances=27,all581_manually_reread=False)
    assert census['source_blocks_scanned']==1307 and len(census['selected_native_blocks'])==17
    assert len(getters['original_native_cases']['rows'])==4
    old_scope=Path(old[OLD_SCOPE]['path']);assert sha(old_scope.read_bytes())==old[OLD_SCOPE]['sha256']
    scope=deepcopy(read(old_scope));scope['next_focus']=NEXT
    scope['next_Lil_B199_clean_review_pending'].update(
        clean31_source_gloss_path=str(GLOSS),source_current_packet=str(PACKET),
        clean_first_glosses=31,new_completion_credit=0,English_manuscript_and_source_controls_and_scene_review_pending=True)
    scope['B199_and_paired_role_labels_clean_context_v5776']=dict(
        B199_speeches=31,all_uncredited=True,source_current_dispatches=62,original_name_consumers=6,
        actual_B199_scene_capture=False,paired_label_context=str(CONTEXT),pair_getters=str(GETTERS),
        draft_nameplates={'164':'Man','165':'Woman'},current_nameplates_unchanged=True,
        five_complete_representative_exchanges=5,manually_read_representative_speeches=212,
        remaining_name_consumer_display_and_registered_integration_pending=True,no_duplicate_dialogue_credit=True)
    assert 'speaker_names_and_role_labels_localization_review_v5708' in scope
    ROOT.mkdir(parents=True);scopepath=ROOT/'unfinished_editorial_scope_inventory.json';save(scopepath,scope)
    paths=[PRIOR,PACKET,GLOSS,CONTEXT,CENSUS,GETTERS,old_scope,scopepath,Path(__file__),
        Path('work/analysis/lil_B199_clean_inventory_v5764/all_clean_B199_speeches_before_predecessor_comparison.json'),
        Path('work/analysis/lil_B199_voices_v5768/current207_catalog_eight_voices_and_three_source_selectors.json'),
        Path('work/analysis/lil_B199_dispatches_v5769/all31_source_current_dispatches_one_FI_and16_control_leaves.json'),
        Path('work/analysis/lil_B199_entry_v5770/source_EV2_B199_action_dependency_and_native_getter_binding.json'),
        Path('work/analysis/lil_B199_branches_v5771/original_relative_skip_operand_proof.json'),
        Path('work/analysis/lil_B199_names_v5772/six_original_progressive_and_catalogue_name_consumers.json'),
        Path('work/analysis/couple_label_clean_context_v5766/four_complete_clean_route_exchanges_and_exact_couple_name_fields.json'),
        Path('scripts/census_couple_speaker_uses_v5773.py'),Path('scripts/census_couple_speaker_uses_v5773b.py'),
        Path('translations/ordinary_name_fidelity_manuscript_v1.json'),Path('translations/release_stack.json')]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    new=deepcopy(old);new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY+'\n\n'+NEXT
    new[KEY]=dict(summary=SUMMARY,next=NEXT,evidence=evidence,all31_B199_objects_uncredited=True,
        two_role_label_revisions_proposed_not_integrated=True,no_new_ROM_emulator_or_duplicate_credit=True,full_goal_complete=False)
    new[SCOPE]=dict(path=str(scopepath),sha256=sha(scopepath.read_bytes()),Lil_B199_uncredited_objects=31,
        proposed_role_label_revisions=2,retrospective207_name_queue_preserved=True,full_goal_complete=False)
    assert inverse(new)==old
    targets={LEDGER:encode_ledger(new)}
    assert len(targets[LEDGER])<100*1024*1024
    section='## V5776: B199 clean-first context and paired speaker-label localization draft\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name
        prefix=('# Current editorial handoff - V5776\n\n' if name=='editorial_handoff_current.md' else '')+section
        targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
    files=[]
    for i,(target,data) in enumerate(targets.items()):
        planned=ROOT/f'{i:02d}.after';backup=ROOT/f'{i:02d}.before.gz'
        planned.write_bytes(data);backup.write_bytes(gzip.compress(target.read_bytes(),mtime=0))
        files.append(dict(target=str(target.resolve()),planned=str(planned.resolve()),before=str(backup.resolve()),
            before_sha256=sha(target.read_bytes()),planned_sha256=sha(data)))
    save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True))
    print('Six targets staged;31 clean B199 objects and two proposed role-label changes remain uncredited.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['stage','audit','apply','verify']);phase=p.parse_args().phase
    if phase=='stage':stage()
    else:
        pp=ROOT/'staged_checkpoint.json';plan=read(pp)
        if phase=='audit':
            assert not (ROOT/'independent_preapplication_audit.json').exists();check(plan)
            save(ROOT/'independent_preapplication_audit.json',dict(plan_sha256=sha(pp.read_bytes()),
                all_before_planned_evidence_hashes_exact=True,deep_nested_inverse_and_exact_old_ledger_bytes_verified=True))
            print('Six-file preapplication and complete inverse audit pass.')
        elif phase=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'independent_preapplication_audit.json')['plan_sha256']==sha(pp.read_bytes());check(plan)
            for item in plan['files']:
                assert Path(item['target']).is_relative_to(Path.cwd().resolve())
                assert Path(item['planned']).is_relative_to(ROOT.resolve())
            for item in plan['files']:
                with Path(item['target']).open('r+b') as f:
                    f.write(Path(item['planned']).read_bytes());f.truncate();f.flush();os.fsync(f.fileno())
                assert sha(Path(item['target']).read_bytes())==item['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_exact=True,all_original_history_preserved=True))
            print('Six audited checkpoint targets applied with original history intact.')
        else:
            assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all_six_targets_exact']
            new=check(plan,True);prior=read(PRIOR)
            VERIFY.mkdir(parents=True)
            save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),
                candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],patch=prior['patch'],patch_sha256=prior['patch_sha256'],
                all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,**COUNTERS,
                completed=6232,source_prose=6235,revised=3917,retained=2315,SC2=4347,SC3=96,reviewed_routes=4633,completed_routes=4633,
                B199_uncredited_clean_glosses=31,B199_source_current_dispatches=62,B199_native_name_consumers=6,
                paired_labels_draft_only=True,paired_label_native_current_consumers=4,complete_source_representative_exchanges=5,
                complete_source_representative_speeches=212,distinct_role_utterances=27,all581_context_speeches_not_manually_reread=True,
                catalog_queue=207,no_new_ROM_or_emulator_run=True,no_promotion_commit_push_or_pruning=True,
                main_V4701_preserved=True,full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5777 verified: source progress saved;V5756/main/counters unchanged. Full goal active.')
