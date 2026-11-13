"""Reconcile79 fresh source-first retentions with current and historical evidence."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/guild_courier_completion_v2247')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/guild_courier_contextual_editorial_manuscript_v1.json')
NOTES=Path('translations/guild_courier_contextual_editorial_manuscript_v2.json')
FINAL=Path('translations/guild_courier_contextual_final_review_v1.json')
MATRIX=Path('work/analysis/guild_courier_layouts_v2241/all79_current_native_layouts.json')
FONTS=Path('work/analysis/guild_courier_fonts_v2242/all79_native_font_pagination_and_physical_samples.json')
ACTUAL=Path('work/analysis/guild_transactions_verification_v2244/current_Guild_full_foreground_state_transitions.json')
HISTORY=Path('work/analysis/guild_courier_history_v2246b/historical_family_binding.json')
PRICE=Path('work/analysis/guild_price_domain_v2245/original_item_prices_skill_clamp_and_English_unit_contract.json')
RELEASE=Path('work/analysis/town_trade_port_release_v2172/registered_release_verification.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2171 Guild courier letters79 contextual retentions verified')
FAMILY='Guild-items-Purser-bargaining-diplomatic-letters-courier79'
IDS=[346,347,348,*range(1070,1146)]
SUMMARY=('V2247 reconciles79 historical COMMON entries346-348 and1070-1145 as fresh individually justified retentions. '
 'Clean Japanese and complete consumer exchanges establish Guild buying/selling, Purser bargaining, First Mate diplomatic drafting, recipient/enemy selection, confirmations, delivery promises and separate courier arrival/relationship notices. All79 retain existing English with individual source glosses and reasons. '
 'Receipt is distinct from acceptance of letter contents; refusal is refusal to receive the letter, not a rejected pact. The merchant promises delivery without guaranteeing the later result. IC remains the source first-person command. '
 'Six runtime letter labels receive auxiliary individual source/context/format reviews without adding COMMON record credit. Native current context passes2080 actor-voice selections,90 Guild NPC mappings,1260 direct bindings and10 role bindings. Three courier notices use the separate original modal consumer and native faction/number arguments. '
 'Eleven current eligibility cases and six original target lists bind actual six-mode labels, Speech/proof thresholds and player-company exclusion. Qualification inputs are CPU-only, not earned states or new emulator fixtures. '
 'All2823 current native layouts pass:2774 progressive plus49 separate modal, complete printf, words, argument copies, canaries, bounds and ABI. Twelve wrong-parent modal controls and12 direct/object label getters pass; existing document width24 is unchanged. Ordinary class13 document GPU menu coverage is not claimed. '
 'All186 selected full native font samples on16 viewed sheets complete one page at logical228x48 with6x12 metrics. Physical16pixel pitch is a separate oracle. The common postformat font fixture is not misrepresented as an actual courier callback. '
 'A new fixture-free V2171 Seoul cold boot runs15601frames. Eleven complete foreground holds cover1071/1073/1074/1085/1086/1096; eight menus/returns and six complete actual native font continuations pass. Ten paired state/company/fleet/ship/persistent/task controls match the historical run with identical inputs. '
 'Declined purchase/sale preserve cash. Original purchase7700 and sale6160 change cash38816 to31116 to37276. Paid company cash is compared against the matching source run. The battery history is inherited, not re-earned. Other observer rows remain context-only, including a stale62 attribution on a direct item description. '
 'Historical qualified V789/V790/V792 evidence contributes35 complete holds across21 IDs, separately labeled and viewed on5 sheets. Historical role/XP/proof/relation and PRNG controls remain disclosed; random daily world objects are not globally approved. Entry346 has native family evidence but no individual actual activation. All sampled complete paragraphs and all2823 formatted layouts are identical to current. No exhaustive conditional, full-route or hardware claim. '
 'Original218 item bases and skill clamp0..500 yield102204 checked native arithmetic cases:minimum purchase90 and sale80. Plural coins is valid for the source offer domain; synthetic one-coin layout vectors are unreachable size stress. '
 'No English, ROM, profile, registry, manifest or patch changes are needed. Both existing registered editorial stages bind all79 IDs. Cumulative V2171 remains492batches/114accepted layers with exact clean-input patch. Fresh coverage1236 reread/1236 integrated-reconciled/0pending. '
 'Historical2143=1498revised+645retained,source/prose2259 and116 incompleteCOMMON remain unchanged. Another907 historical completions require fresh review:906COMMON andSC2B294R73. All never-reviewed storylines/shared town/shop/random/player prose remain in scope. '
 'All ROMs and earlier translations preserved. V1492 remains promoted;canonical and clean inputs unchanged. Full objective active. Separate graphics/all18 plaques,SC3B109 classification and later older-record technical re-audit remain open. All jobs terminal.')

def key(row):
    path=row.get('file_path','/COMMON/MESFILE.DK4');n=row.get('message_id')
    return path,f'COMMON_MESSAGE_{n}'if n is not None and path=='/COMMON/MESFILE.DK4'else row['id']

if __name__=='__main__':
    assert not any(p.exists()for p in(ROOT,NOTES,FINAL,GUIDE))
    l,d,matrix,fonts,actual,historical,price,release=[read(p)for p in(LEDGER,DOC,MATRIX,FONTS,ACTUAL,HISTORY,PRICE,RELEASE)]
    f=l['contextual_story_natural_dialogue_pass_v1871']
    assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(1157,1157,0)
    assert len(d['records'])==79 and d['revised_IDs']==[]and d['retained_count']==79
    assert matrix['case_count']==2823 and not matrix['findings']and matrix['all79_original_consumer_parent_table_or_ID_bindings_used']
    assert fonts['font_count']==186 and len(fonts['physical_sheets'])==16 and fonts['all186_single_native_pages_complete']
    assert {r['message_ID']for r in fonts['full_font_samples']}==set(IDS)
    assert len(actual['actual_holds'])==11 and len(actual['transition_frames'])==8 and len(actual['paired_native_state_model_task_controls'])==10
    assert actual['no_fixture_or_savestate_or_original_save_mutation']and actual['all6_selected_native_font_returns_complete']and actual['all11_full_foregrounds_equal_native_and_independent']
    assert len(historical['historical_holds'])==35 and len(historical['historical_IDs'])==21 and historical['all_sampled_complete_paragraphs_identical_current']and historical['all2823_current_formatted_bytes_identical_historical']
    assert price['one_coin_is_not_an_eligible_Guild_item_offer']and price['native_arithmetic_cases']==102204
    for p,h in d['native_context_proofs'].items():assert sha(Path(p).read_bytes())==h
    rompath=Path(l['current_integrated_candidate']['path']);digest=sha(rompath.read_bytes());mp=rompath.with_suffix('.manifest.json');manifest=read(mp)
    registry_path=Path('translations/release_stack.json');registry=read(registry_path)
    assert digest==l['current_integrated_candidate']['sha256']==d['current_ROM_sha256']==actual['candidate_sha256']==historical['candidate_sha256']==release['candidate_sha256']==manifest['candidate_sha256']
    assert sha(mp.read_bytes())==release['manifest_sha256']and manifest['release_stack_sha256']==sha(registry_path.read_bytes())and all(manifest['checks'].values())
    assert len(manifest['batches'])==492 and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    patch=Path(release['patch']);assert release['whole_ROM_reconstruction_byte_exact']and sha(patch.read_bytes())==release['patch_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==release['clean_input_sha256']and sha(Path(manifest['base_rom']).read_bytes())==manifest['base_sha256']
    bindings=[]
    for stage,ids in [('item_diplomacy_editorial',list(range(1070,1146))),('arrival_notices_editorial',[346,347,348])]:
        row=manifest['relocations']['/COMMON/MESFILE.DK4'][stage];config=Path(registry['profiles'][manifest['profile']][stage]);c=read(config);man=Path(c['manuscript'])
        assert Path(row['release_config'])==config and row['release_config_sha256']==sha(config.read_bytes())and c['manuscript_sha256']==sha(man.read_bytes())
        assert set(row['proof']['changed_records'])=={f'COMMON_MESSAGE_{n}'for n in ids}
        bindings.append(dict(stage=stage,config=str(config),config_sha256=sha(config.read_bytes()),manuscript=str(man),manuscript_sha256=sha(man.read_bytes()),IDs=ids))
    rom,clean=NdsImage.open(rompath),NdsImage.open('work/clean.nds');arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm);jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    assert sha(arm)==d['current_ARM9_sha256']==fonts['ARM9_sha256']==release['ARM9_sha256']and sha(common)==d['current_COMMON_sha256']==fonts['COMMON_sha256']==release['COMMON_sha256']
    history={key(r):g['id']for g in l['completed_editorial_families']for r in g['records']};keys={(r['file_path'],r['id'])for r in f['record_keys']};selected={('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in IDS}
    assert len(history)==2143 and not keys&selected and selected<=set(history)
    docs=[Path('docs')/p for p in('editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md')]
    ROOT.mkdir(parents=True)
    for p in[LEDGER,*docs]:(ROOT/(p.name+'.before')).write_bytes(p.read_bytes())
    notes=deepcopy(d);notes.update(status='complete-fresh-contextual-retention-reconciled-registered-V2171',formatting_review_pending=False,English_identical_to_v1_and_current_ROM=True,no_new_ROM_profile_manifest_or_patch=True,final_review=str(FINAL),current_native_layouts=str(MATRIX),current_native_fonts=str(FONTS),current_actual_evidence=str(ACTUAL),historical_family_evidence=str(HISTORY),original_price_domain=str(PRICE),registered_native_stage_bindings=bindings)
    for r in notes['records']:
        n=r['message_id'];assert r['source_hex']==jp[n].text.hex()and entries[n].text==b' '+r['english'].removesuffix('{PAD}').encode('ascii')and r['current_hex']==entries[n].text.hex()
        r['review']['formatting']=True
        r.update(status='complete-fresh-whole-exchange-retention-native-display-representative-family-evidence-registered-reconciliation',original_historical_family=history[(r['file_path'],r['id'])],integrated_hex=entries[n].text.hex(),integrated_reference=dict(block=entries[n].block,offset=entries[n].block_offset,copy_end=entries[n].copy_end,bytes=len(entries[n].text)),integrated_stored_English=entries[n].text.decode('cp932'),formatting_gate_scope='2823 complete native layouts including49 separate modal;186 full native font pages/16 viewed sheets;logical228x48 at6x12;physical16pitch separate.',actual_gameplay_coverage=[h for h in actual['actual_holds']if h['message_ID']==n],actual_gameplay_visited=n in(1071,1073,1074,1085,1086,1096),historical_actual_gameplay_coverage=[h for h in historical['historical_holds']if h['message_ID']==n],native_display_evidence=dict(layouts=str(MATRIX),fonts=str(FONTS),current_actual=str(ACTUAL),historical_only=str(HISTORY),separate_modal_path=n<1000,only6_IDs_new_current_visits=True))
        if n in(1072,1073,1083,1086,1095):r['fresh_retained_wording_justification']+=' Plural coins is valid: original218 item base prices and clamped0..500 ability produce minimum purchase90 and sale80; one-coin matrix inputs are unreachable size stress. Exact proof: '+str(PRICE)
    for label in notes['runtime_letter_labels']:
        label['review']['formatting']=True;label['native_formatting_evidence']=dict(direct_and_object_getters=12,all_six_in_current1098_full_font_samples=True,fonts=str(FONTS),current_question_consumer=str(MATRIX),historical_all_six_actual_questions=str(HISTORY))
    assert sum(r['actual_gameplay_visited']for r in notes['records'])==6
    validate_natural_dialogue_batch(notes);save(NOTES,notes)
    visual=ROOT/'visual_review.json';save(visual,dict(all186_native_font_samples_on16_sheets_viewed=True,all79_IDs_complete_leading_trailing_glyphs_names_numbers_punctuation_and_final_lines_visible=True,all2823_layouts_zero_findings_or_waivers=True,current11holds_and8_menu_returns_viewed=True,historical35holds_on5sheets_for21_IDs_viewed_explicitly_labeled=True,current6_native_returns_complete=True,six_auxiliary_labels_complete=True,physical16pitch_separate_from_logical12pitch_capacity=True,shared_font_fixture_not_actual_modal_callback=True,original_price_domain_grammar_resolved=True,no_new_ROM_or_geometry=True,full_goal_complete=False))
    paths=[DOC,NOTES,MATRIX,FONTS,ACTUAL,HISTORY,PRICE,RELEASE,mp,registry_path,visual,Path(__file__),Path(d['source_context_packet']),Path('work/analysis/guild_courier_prose_v2240/source_first_whole_exchange_review.json')]
    paths.extend(Path(p)for p in d['native_context_proofs'])
    paths.extend(Path(actual[k])for k in('source_plan','source_report','source_observer','native_continuation'))
    paths.extend(Path(r['path'])for r in historical['historical_proofs'])
    evidence={str(p):sha(p.read_bytes())for p in paths}
    save(FINAL,dict(format='dk4-editorial-family-final-review-v1',family=FAMILY,file_path='/COMMON/MESFILE.DK4',native_message_IDs=IDS,revised_count=0,retained_count=79,historical_reconciliation_only=True,new_completed_records=0,records=notes['records'],runtime_letter_labels=notes['runtime_letter_labels'],auxiliary_labels_not_extra_COMMON_credit=True,summary=SUMMARY,evidence=evidence,registered_native_stage_bindings=bindings,candidate=str(rompath),candidate_sha256=digest,profile=manifest['profile'],patch=str(patch),patch_sha256=release['patch_sha256'],whole_clean_input_reconstruction_exact=True,no_ROM_profile_registry_manifest_patch_changes=True,current_actual_scope=actual,historical_actual_scope=historical,offline_layout_count=2823,offline_font_count=186,all23_review_sheets_viewed=True,failed2246_parser_attempt_preserved_and_corrected_by_build_specific_parsers=True,failed2238_overbroad_clean_span_corrected_by_registered_V792_modal_bridge_binding=True,stale2235_stdout_not_used_over_current_English_label_JSON=True,full_goal_complete=False))
    f['record_keys'].extend(dict(file_path=r['file_path'],id=r['id'])for r in notes['records']);f['record_IDs'].extend(r['id']for r in notes['records'])
    f.update(fresh_pass_records_explicitly_reread=1236,fresh_pass_records_integrated=1236,fresh_pass_records_pending_native_actual_release=0,historical_completed_records_outside_reconciled_fresh_pass=907,latest_contextual_manuscript=str(NOTES),latest_completed_family=FAMILY,latest_reconciled_historical_family=FAMILY,latest_contextual_retention_review=str(FINAL),latest_final_review=str(FINAL),latest_pending_contextual_family=None,coverage_note='1236 file-qualified fresh rereads integrated/reconciled;907 other historical completions,116 incomplete COMMON and all never-reviewed route/shared town/shop/random/player prose remain in scope.')
    f['reconciled_families'].append(dict(id=FAMILY,records=79,final_review=str(FINAL),new_revisions=0,justified_retentions=79,historical_reconciliation_only=True,new_completed_records=0,all_source_native_representative_family_registered_reconciliation_complete=True,current_recorded_ID_visits=6,historical_sample_IDs=21,new_emulator_runs=1))
    l['active_source_prose_drafts']['note']=f['coverage_note'];l['guild_courier_contextual_v2247']=dict(summary=SUMMARY,final_review=str(FINAL),evidence=evidence,goal_turn_classification='progress',full_goal_complete=False);l['latest_checkpoint']=SUMMARY
    l['current_integrated_candidate']['details']+=' V2247 freshly reconciles79 unchanged Guild/courier/letter entries; binary and exact patch remain V2171.'
    l['formatting_watchlist']['guild_courier_contextual_v2247']=dict(status='79complete-current-V2171-retentions-original228x48-four12rows',final_review=str(FINAL),all2823_current_native_layouts_pass=True,all186_full_fonts_and16sheets_viewed=True,current6_IDs11holds_complete=True,historical21_IDs35holds_explicit=True,no_runtime_font_or_geometry_changes=True)
    keys={(r['file_path'],r['id'])for r in f['record_keys']}
    assert len(keys)==len(f['record_keys'])==len(f['record_IDs'])==1236 and Counter(p for p,i in keys)=={'/COMMON/MESFILE.DK4':580,'/data/SC2.DK4':428,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert l['records_editorially_completed']==2143 and l['records_revised_and_integrated']==1498 and l['retained_wordings_editorially_completed']==645 and sum(l['source_prose_reviewed_counts_by_file'].values())==2259 and len(l['reviewed_but_incomplete_COMMON_IDs'])==116 and l['goal_status']=='active'and not l['full_goal_complete']
    remaining=[dict(file_path=p,id=i,historical_family=g)for(p,i),g in history.items()if(p,i)not in keys]
    assert len(remaining)==907 and Counter(r['file_path']for r in remaining)=={'/COMMON/MESFILE.DK4':906,'/data/SC2.DK4':1}
    inv=ROOT/'remaining_historical_fresh_review_inventory.json';save(inv,dict(remaining=907,records=remaining,counts_by_file=dict(Counter(r['file_path']for r in remaining)),counts_by_family=dict(Counter(r['historical_family']for r in remaining)),full_goal_complete=False))
    l['next_remaining_historical_inventory_v2247']=dict(path=str(inv),sha256=sha(inv.read_bytes()),records=907);save(LEDGER,l)
    section='## V2247: Guild courier letters79 contextual retentions reconciled\n\n'+SUMMARY+'\n\nIndividual source/current references and reasons: '+FINAL.as_posix()+'. Current native layouts: '+MATRIX.as_posix()+'. Fonts: '+FONTS.as_posix()+'. Current gameplay: '+ACTUAL.as_posix()+'. Historical-only family binding: '+HISTORY.as_posix()+'. Source price-domain grammar: '+PRICE.as_posix()+'.\n\nRemaining inventory: '+inv.as_posix()+'. Continue palace1146-1176 and inn1177-1199, then remaining shared/route/random/player prose. Full goal remains active. Guide: '+GUIDE.as_posix()+'.\n\n'
    text=docs[0].read_text();assert text.startswith('# Current editorial handoff - V2234');first,rest=text.split('\n',1)
    docs[0].write_text('# Current editorial handoff - V2247\n\n'+section+rest,newline='\n')
    for p in docs[1:]:
        first,rest=p.read_text().split('\n',1);p.write_text(first+'\n\n'+section+rest,newline='\n')
    GUIDE.mkdir(parents=True);images=[]
    for scope,rows in [('current-actual-fixture-free',actual['review_sheets']),('historical-only-qualified',historical['review_sheets']),('offline-native-font-not-gameplay',fonts['physical_sheets'])]:
        for r in rows:
            source=Path(r['path']);assert sha(source.read_bytes())==r['sha256'];target=GUIDE/(scope+'_'+source.name);copy2(source,target);assert sha(target.read_bytes())==r['sha256'];images.append(dict(path=str(target),sha256=r['sha256'],kind=scope))
    assert len(images)==23
    save(GUIDE/'scope.json',dict(candidate=str(rompath),candidate_sha256=digest,final_review=str(FINAL),images=images,current_historical_and_offline_labels_distinct=True,current79_recorded_IDs=[1071,1073,1074,1085,1086,1096],new_emulator_runs=1,no_ROM_or_geometry_change=True,full_goal_complete=False))
    save(ROOT/'completion_receipt.json',dict(checkpoint='V2247',summary=SUMMARY,fresh_reconciliations=79,new_revisions=0,justified_retentions=79,fresh_integrated=1236,historical_complete=2143,source_prose_reviewed=2259,COMMON_incomplete=116,other_historical_fresh_reviews=907,candidate_sha256=digest,patch_sha256=release['patch_sha256'],guide=str(GUIDE),guide_images=23,evidence=evidence,updated_files={str(p):sha(p.read_bytes())for p in[LEDGER,*docs,NOTES,FINAL]},goal_turn_classification='progress',full_goal_complete=False))
    print(dict(checkpoint='V2247',fresh_integrated=1236,reconciled79=True,revised=0,retained=79,ROM='unchanged-V2171',other_historical_fresh_reviews=907,full_goal_complete=False))
