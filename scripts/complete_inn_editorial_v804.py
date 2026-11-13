"""Close Inn23 only after exact source/native/release and actual-family audit."""

from copy import deepcopy
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import inn_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_inn_integration_v803 import copy_exact
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/inn_history_v804')
DOC=Path('docs/inn_editorial_v804_completion.md')
MANUSCRIPT=Path('translations/inn_editorial_manuscript_v4.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V804 Inn family completion')
GUIDE=Path('E:/Rota Nova translations/Strategy Guide/Screenshots/V804 Inn complete')


def main():
    assert not DOC.exists() and not MANUSCRIPT.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    release=read(owned.ROOT/'registered_verification.json')
    stay=read(owned.ROOT/'stay_gameplay_verification.json');news=read(owned.ROOT/'news_report_refusal_gameplay.json')
    startup=read(owned.ROOT/'newgame_regression.json');history=read(ROOT/'history_gameplay_verification.json')
    departure=read(ROOT/'departure_gameplay_verification.json')
    rom_path=Path(release['candidate']);rom=NdsImage.open(rom_path)
    assert sha(rom_path.read_bytes())==release['candidate_sha256']=='7c6c8bb3c89973af2f789488e51bff395d871be6a461490d62b3f5c8d860daad'
    assert all(x['candidate_sha256']==release['candidate_sha256'] for x in (stay,news,startup,history,departure))
    manifest=read(rom_path.with_suffix('.manifest.json'))
    assert manifest['profile']=='all-routes-unified-v803' and all(manifest['checks'].values())
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==470 and len(read('translations/release_stack.json')['accepted_layers'])==114
    config=read('translations/inn_editorial_release_v1.json');production=read(config['manuscript'])
    validate_natural_dialogue_batch(production)
    assert production['translation_policy']=='natural-dialogue-v2'
    assert [r['message_id'] for r in production['records']]==list(owned.IDS)
    assert {r['message_id'] for r in production['records'] if r['decision']=='retain'}=={1178,1183,1198,1199}
    parent=NdsImage.open('out/all_routes_combined_v799_candidate.nds')
    c,a,_=owned.apply_release(parent.read_file('/COMMON/MESFILE.DK4'),parent.read_file('/__arm9__.bin'),'translations/inn_editorial_release_v1.json')
    assert (c,a)==(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'))
    entries=owned.current_entries(c,a)
    assert all(owned.compiled(row)==entries[row['message_id']].text for row in production['records'])
    reconstruction=owned.ROOT/'clean_patch_reconstruction_RESEARCH_ONLY.nds';patch=Path(release['patch'])
    assert reconstruction.read_bytes()==rom_path.read_bytes() and sha(patch.read_bytes())==release['patch_sha256']
    assert release['clean_input_reconstruction_byte_exact'] and release['all3645_other_strings_and_earlier_formatting_fixes_preserved']
    native=read(owned.ROOT/'production_layout.json')
    assert native['native_layouts']==1169 and native['full_font_planes']==96 and not native['findings']
    assert native['COMMON_sha256']==sha(c) and native['ARM9_sha256']==sha(a)
    context=read('work/analysis/inn_context_v801/native_context.json')
    assert len(context['voice_cases'])==208 and len(context['stay_caller_fragments'])==10 and len(context['rumor_calls'])==6
    assert read('work/analysis/inn_runtime_v802/scope_proof.json')['cases']==35320
    assert read('work/analysis/inn_runtime_v802/status_contracts.json')['count']==140
    assert read('work/analysis/inn_runtime_v802/complete_month_phrases.json')['count']==144
    assert release['complete_warm_cold_copies']==5076 and len(startup['whole_screen_frame_pairs'])==7
    assert len(history['cases'])==6 and len(history['control_frames'])==12
    assert history['all_four_rumor_IDs_and_both_outcomes_per_type_verified']
    assert read(ROOT/'history_visual_review.json')['all_six_history_holds_visually_reviewed']
    assert departure['only_two_coins_and_two_days_charged'] and departure['A_yes_leaves_early']
    all_holds=stay['actual_holds']+news['actual_holds']+history['cases']+departure['actual_holds']
    actual_IDs=sorted({r['message_id'] for r in all_holds});assert len(all_holds)==20 and len(actual_IDs)==16
    assert set(range(1194,1200))<=set(actual_IDs)
    source_paths=[owned.ROOT/p for p in ('registered_verification.json','production_layout.json','prospective_common_repack.json',
        'stay_gameplay_verification.json','news_report_refusal_gameplay.json','newgame_regression.json','complete_current_message_map_v803.json')]
    source_paths += [ROOT/p for p in ('input_preflight.json','history_gameplay_verification.json','history_visual_review.json',
        'departure_gameplay_verification.json','early_departure_button_mapping.json')]
    evidence={str(p):sha(p.read_bytes()) for p in source_paths}
    audit=[
        dict(requirement='Every Inn source and actual caller/argument/voice context reviewed',evidence='inn_context_v801/native_context.json;production manuscript23;208 voice/10 stay/6 rumor cases',achieved=True),
        dict(requirement='Natural faithful English and justified retained wording with all5 per-record gates',evidence=config['manuscript'],achieved=True),
        dict(requirement='Exact source argument order and native presentation retained',evidence='registered apply_release replay plus35320 exact caller/ID/ABI cases',achieved=True),
        dict(requirement='All generated boundaries/letters/fonts/bounds and pagination checked',evidence='1169 production layouts/96 fonts;20 actual holds;all dialog dismissals and next panels sampled',achieved=True),
        dict(requirement='Full affected COMMON native copies and other strings/opaque data preserved',evidence='5076 complete warm/cold copies;3645 unselected texts exact',achieved=True),
        dict(requirement='Combined registered ROM with complete inherited stack and exact patch',evidence='V803 manifest470 batches/114 layers;exact clean reconstruction re-read',achieved=True),
        dict(requirement='Actual stay,market,report,refusal,history and interruption families verified',evidence='20 holds across16 IDs;all3 original history types/both outcomes;2 of30 nights charged;normal returns',achieved=True),
        dict(requirement='All voice variants and every individual branch actually played',evidence='Not required for this family scope;native208 voice matrix and representative actual voice1. Early-departure No/resume not separately activated.',achieved=False,not_claimed=True),
        dict(requirement='Full editorial goal including remaining shared/routes/help and separate graphics audit',evidence='Only Inn23 closes;other project coverage remains incomplete.',achieved=False,not_claimed=True)]
    family_proof=ROOT/'Inn_family_completion.json'
    save(family_proof,dict(candidate=str(rom_path),candidate_sha256=release['candidate_sha256'],profile=manifest['profile'],
        reviewed_native_IDs=list(owned.IDS),proposed_revisions_integrated=19,retained_wordings=4,
        requirements_audit=audit,source_evidence_sha256=evidence,actual_holds=20,actually_sampled_native_IDs=actual_IDs,
        all23_source_native_coverage_and_actual_consumer_families_complete=True,
        native_layouts=1169,full_font_planes=96,complete_native_copies=5076,selector_ABI_cases=35320,status_contracts=140,
        full_relative_month_native_cases=144,history_actual_holds=6,early_departure_actual_holds=2,
        full30_night_completion_or_every_voice_branch_not_claimed=True,ROM_changed=False,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    completed=deepcopy(production)
    for row in completed['records']:
        row['status']='editorially-complete-full-source-native-and-actual-consumer-family-samples'
        row['context']+=' V804 closes this family after20 actual holds across16 IDs and all source/native contracts. Every regional NPC and voice branch was not separately played;all208 native voice selections and complete paragraph fonts are covered. Early-departure Yes and ordinary continuation are tested;the interrupt No option is not separately activated.'
        row['completed_candidate_reference']={k:v for k,v in vars(entries[row['message_id']]).items() if k!='text'}
        row['native_and_gameplay_family_evidence']=str(family_proof)
    completed.update(status='editorially-complete-at-full-source-native-plus-actual-family-scope',
        inherited_production_manuscript=config['manuscript'],inherited_production_manuscript_sha256=sha(Path(config['manuscript']).read_bytes()),
        completed_candidate=str(rom_path),completed_candidate_sha256=release['candidate_sha256'],ROM_changed=False,full_goal_complete=False)
    assert [(r['english'],r['source_meaning']) for r in completed['records']]==[(r['english'],r['source_meaning']) for r in production['records']]
    save(MANUSCRIPT,completed)
    ledger=read(LEDGER)
    assert ledger['records_editorially_completed']==527 and ledger['records_with_source_and_prose_pass']==553
    assert ledger['active_source_prose_drafts']['native_message_IDs']==[750,751,752,*owned.IDS]
    assert not set(owned.IDS)&{n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    ledger['records_editorially_completed']+=23;ledger['records_revised_and_integrated']+=19;ledger['retained_wordings_editorially_completed']+=4
    assert ledger['records_editorially_completed']==550==ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']
    active=ledger['active_source_prose_drafts'];active['native_message_IDs']=[750,751,752]
    active['manuscripts']=[p for p in active['manuscripts'] if 'inn_editorial_manuscript' not in p]
    active['status']='750-752-context-unmapped';active['note']='Inn23 complete at source/native plus actual-family scope. Three older source/prose drafts750-752 remain context-unmapped. Wider shared text,all routes and other prose remain unfinished.'
    records=[]
    for row in completed['records']:
        records.append({k:row[k] for k in ('message_id','decision','english','source_meaning','speaker','context','source_hex','completed_candidate_reference','native_and_gameplay_family_evidence')}|dict(full_source_native_coverage_and_actual_consumer_family_samples=True,individual_branch_activation_not_claimed=True))
    ledger['completed_editorial_families'].append(dict(id='Inn-stays-market-news-reports-and-history1177-1199',native_message_IDs=list(owned.IDS),records=records))
    current=ledger['current_integrated_candidate'];assert current['sha256']==release['candidate_sha256']
    current.update(status='experimental-Inn-editorial-family-verified',details=str(DOC),supplemental_verification=str(family_proof),
        remaining_in_this_registered_batch='Inn23 complete at full source/native and representative actual-family scope. Wider shared1200+,older750-752 contexts,all routes and help/other prose remain incomplete.',full_goal_complete=False)
    ledger['next_Inn_source_packet'].update(status='complete-full-source-native-and-actual-family-samples',completion_credit=23,completed_manuscript=str(MANUSCRIPT),family_completion=str(family_proof))
    for f in ledger['findings']:
        if f['id']=='Inn-relative-month-prose-abbreviations':
            f.update(status='corrected-integrated-and-actual-all-three-history-types-both-outcomes-verified',proof=str(ROOT/'history_gameplay_verification.json'))
    summary=('V804 completes23 Inn COMMON entries in unchanged V803(19 revised/4 retained):550 complete(407 revised/143 retained),553 source-prose reviewed,three older contexts750-752 pending. '
        'All23 source/native contexts,208 voice selections,35320 selector/ABI cases,140 full8MiB status cases,144 month cases,1169 layouts,96 fonts and5076 complete copies pass. '
        '20 actual holds across16 IDs cover stays,market pairs,Strategist report/info window,zero-funds refusal,all3 history types/both outcomes,and early departure. '
        'A requested30-night stay is interrupted after2 nights;only2coins/96ticks are charged,with no later covered-object changes and normal return. '
        'Six seeded-history cases preserve the original dispatcher and consume their event;no actual battle victory or earned knowledge is claimed. '
        'Seven startup frames and exact clean-input patch pass. V803/470 batches/114 accepted layers and canonical base remain unchanged. Wider shared/routes/prose and separate graphics audit remain unfinished;full goal active.')
    ledger['latest_checkpoint']=summary
    ledger['coverage_units'][0]['next']='Inventory shared1200 onward against clean/current bytes and original callers;retain completed1245/1246 and prior overlaps. Then older750-752 contexts,all route scenes and other prose.'
    ledger['formatting_watchlist']['latest_reference_proof']=str(family_proof)
    ledger['formatting_watchlist']['reference_case']+=' V804 adds six complete actual history/month font holds and two complete1199 holds;30-night confirmation fits one line. Two-night cancellation charges2coins/96ticks only. Inn23 closes;global formatting audit remains open.'
    ledger['research_checkpoints'].append(dict(id='V804-Inn23-complete',documentation=str(DOC),new_source_prose_reviewed=0,new_editorially_completed=23,new_ROM=False,full_goal_complete=False))
    assert ledger['approved_names']==['Rafael','Joakim','Maria','Camille'] and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    save(LEDGER,ledger);save('out/editorial_review_latest.json',current)
    post=read(rom_path.with_suffix('.verification.json'))
    post.update(actual_revised_gameplay_pending=False,actual_remaining_IDs=[],scope='Inn23 only;full editorial and graphics goals unfinished',
        inn_family_completion=str(family_proof),inn_family_completion_sha256=sha(family_proof.read_bytes()),full_goal_complete=False)
    save(rom_path.with_suffix('.verification.json'),post)
    DOC.write_text('# V804: Inn editorial family complete in unchanged V803\n\n'+summary+'\n\n'
        '## Scope and current release\n\n'
        'This closes COMMON1177–1199 at full source/native plus representative actual-consumer scope. '
        'Twenty actual holds sample16 distinct IDs;the other seven voice variants have the complete208-actor native selector matrix and rendered font coverage. '
        'Not every cultural NPC,choice or every possible substitution combination was activated in the emulator. The early-departure No/resume option is not separately played.\n\n'
        f"The combined ROM is still `{rom_path.resolve()}`, SHA-256 `{release['candidate_sha256']}`. "
        f"Its exact clean-input patch remains `{release['patch_sha256']}`. Profile `all-routes-unified-v803`,470 inherited batches and114 accepted layers remain frozen. "
        'The canonical parent stays `out/raphael_natural_v2_accepted_base.nds`, SHA-256 '
        '`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. No new ROM or canonical promotion. '
        'The V803 integration changes only COMMON and ARM9 from V799;all other routes,HELP,graphics and source controls remain exact.\n\n'
        '## New actual evidence\n\n'
        'Six fresh isolated donor copies exercise the original history dispatcher for fleet battles,town raids and town defense,both outcomes each. '
        'Original region/validity methods accept the typed pending history. Original knowledge setters make eligible reports already known so they do not precede history. '
        'Only declared assignment/knowledge/event input bytes change;no ROM code,text,menu or dispatcher is replaced. '
        'The actual time arguments cover This month,Last month,and2/3/10/11 months ago. Every number,word and first/final letter matches the complete native/independent font mask. '
        'All six events are consumed normally,each stay costs1coin/48ticks,and twelve menu/town controls match across cases. These are seeded rumors,not combat or earned-progress verification.\n\n'
        'A separate ordinary fresh-save run selects30 nights and uses B at the night boundary.1199 remains fully visible across two holds;A chooses Yes. '
        'The game returns to the Inn menu and town with cash8371→8369 and96ticks elapsed. The remaining28 nights are not charged. '
        'Covered models,actors,towns,items,goods and couriers remain unchanged after Yes. No condition,location,inventory or other new fixture is used. '
        'A separate initial B-mask calibration left the Inn area and entered a Port event;its captures are preserved only as input research and receive no Inn scene credit. '
        'The frozen journal disclaims execution receipts and leaves completion_confirmed false;observed exit0 and terminal capture reports prove completion.\n\n'
        '## Manuscripts,coverage and next work\n\n'
        '`translations/inn_editorial_manuscript_v4.json` adds completion metadata/current references only;English and source glosses match the frozen production V3 exactly. '
        '`work/analysis/inn_history_v804/Inn_family_completion.json` records the requirement audit and exact evidence hashes. '
        'The old V803 pending-gameplay descriptions are historical build-time metadata;the post-test verification and current ledger supersede them. '
        'Do not edit frozen release dependencies merely to change their historical status.\n\n'
        'Next,inspect shared1200 onward,including religious services and their actual neighbors/consumers;1245/1246 already have prior coverage and must not be counted twice. '
        'Older750-752 contexts,all route review,other prose and the separate graphics/18-plaque audit remain open. '
        'Keep the complete editorial goal active;revisit older record checks after that full goal is achieved.\n',encoding='utf-8')
    for name in ('todo','translation_progress','editorial_review_goal','known_issues'):
        p=Path('docs')/(name+'.md');text=p.read_text(encoding='utf-8');heading='## V804: Inn23 editorial family complete'
        assert heading not in text;p.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [Inn completion](inn_editorial_v804_completion.md).\n',encoding='utf-8')
    files=[DOC,LEDGER,MANUSCRIPT,family_proof,Path('translations/inn_editorial_release_v1.json'),rom_path.with_suffix('.verification.json')]+source_paths
    files += [Path('scripts')/p for p in ('native_inn_history_fixture_v804.py','run_inn_history_capture_v804.py','prepare_inn_history_v804.py','verify_inn_history_v804.py','verify_inn_departure_v804.py',Path(__file__).name)]
    archive=[copy_exact(p,ARCHIVE/p.name) for p in dict.fromkeys(files)]
    guide=[]
    for item in history['cases']:
        p=Path(item['hold']['path']);receipt=copy_exact(p,GUIDE/(item['label']+'.png'))
        receipt.update(message_id=item['message_id'],fixture='Typed completed-history input plus original knowledge/assignment fields;not actual combat.')
        guide.append(receipt)
        p=Path(item['report']);archive.append(copy_exact(p,ARCHIVE/(p.parent.name+'_capture_report.json')))
    for f,label in ((6200,'Thirty_night_confirmation'),(6900,'Leave_early_confirmation'),(7300,'Inn_menu_after_two_nights'),(7700,'Town_after_two_nights')):
        p=Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/inn_v804_early_departure/frame_{f:06d}_navigation.png')
        guide.append(copy_exact(p,GUIDE/(label+'.png')))
    p=Path(departure['report']);archive.append(copy_exact(p,ARCHIVE/'early_departure_capture_report.json'))
    save(ARCHIVE/'archive_manifest.json',dict(candidate=current,artifacts=archive,screenshots=guide,Inn23_complete=True,full_goal_complete=False))
    save(GUIDE/'screenshots_manifest.json',dict(candidate=current,screenshots=guide,fixture_and_gameplay_limits_disclosed=True,full_goal_complete=False))
    print(f'Inn23 closed:550 COMMON complete(407 revised/143 retained),553 reviewed,only old750-752 drafts pending. V803 unchanged;{len(guide)} new guide screens/{len(archive)} archived artifacts. Full goal active.',flush=True)


if __name__=='__main__':main()
