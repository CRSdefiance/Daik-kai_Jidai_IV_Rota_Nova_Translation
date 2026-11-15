"""Complete five capture alternatives with new-ROM native and actual evidence."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from dk4tool.patch.flagship_capture_precision import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_aftermath_native_plan_v1255 import compiled as original_compiled
from scripts.flagship_precision_native_plan_v1356 import compiled as corrected_compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/flagship_capture_completion_v1371')
ROM = Path('out/all_routes_combined_v1364_candidate.nds')
ACTUAL = Path('work/analysis/flagship_capture_verified_v1370/actual_flagship_capture_verification.json')
FINAL = Path('translations/battle_aftermath_flagship_capture_final_review_v1.json')
IDS = list(range(2011,2016))


def main():
    assert not ROOT.exists() and not FINAL.exists()
    release_path = Path('work/analysis/flagship_precision_release_v1363/registered_release_verification.json')
    release,actual = read(release_path),read(ACTUAL)
    digest = sha(ROM.read_bytes())
    assert digest==release['candidate_sha256']==actual['candidate_sha256']
    assert release['actual_changed_message_IDs']==[2015] and release['complete_reconstruction_byte_exact']
    assert actual['terminal_frame']==13200 and len(actual['complete_actual2011_holds'])==2
    assert actual['all4MiB_fixture_input_schedule_primary_RAM_and_PNG_hash_audits_pass']
    assert actual['normal_A_dialogue_X_cargo_finish_touch_Yes_and_reward_dismissal_return_to_sailing']
    rom,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    arm,common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries = current_entries(common,arm)
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    old_manuscript = Path('translations/battle_aftermath_editorial_manuscript_v3.json')
    corrected_manuscript = Path('translations/flagship_capture_precision_manuscript_v2.json')
    rows = {r['message_id']:r for r in read(old_manuscript)['records'] if r['message_id'] in IDS}
    rows[2015] = read(corrected_manuscript)['records'][0]
    fonts_path = Path('work/analysis/flagship_precision_fonts_v1357/native_font_proof.json')
    fonts = read(fonts_path)
    assert len(fonts['cases'])==8 and not fonts['findings']
    assert len(fonts['all206_existing_actor_choices'])==206
    selected = []
    for number in IDS:
        row = deepcopy(rows[number])
        assert row['source_hex']==jp[number].text.hex() and all(row['review'].values())
        compiled = corrected_compiled(row) if number==2015 else original_compiled(row)
        assert compiled==entries[number].text
        case = next(c for c in fonts['cases'] if c['message_ID']==number and (number!=2011 or c['source_voice']==1))
        assert case['compiled_hex']==compiled.hex()
        row.update(manuscript=str(corrected_manuscript if number==2015 else old_manuscript),
            previous_current_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[number]).items() if k!='text'},
            current_text_hex=entries[number].text.hex(),current_English=row['english'],
            decision='revised-and-integrated',status='complete-source-native-and-representative-original-flagship-capture-gameplay',
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            complete_native_font_proof=str(fonts_path),complete_native_font_proof_sha256=sha(fonts_path.read_bytes()),
            complete_native_formatted_lines=case['lines'],
            actual_holds=actual['complete_actual2011_holds'] if number==2011 else [],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
        selected.append(row)
    release_root = release_path.parent
    startup_path = release_root/'ordinary_startup_verification.json'
    startup = read(startup_path)
    assert startup['candidate_sha256']==digest and len(startup['pairs'])==8 and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    shop_path = release_root/'photographed_shop_formatting.json'
    shop = read(shop_path)
    assert shop['candidate_sha256']==digest and all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in shop['entries'])
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1302,1395)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==93
    assert not any(set(IDS).intersection(f.get('native_message_IDs',[])) for f in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_completion.json',before)
    save(release_root/'ordinary_startup_visual_review.json',{'candidate_sha256':digest,'proof':str(startup_path),
        'proof_sha256':sha(startup_path.read_bytes()),'all8_frames_actually_visually_reviewed':True,
        'review_sheet':startup['review_sheet'],'review_sheet_sha256':startup['review_sheet_sha256'],
        'scope':'Fixture-free no-save title,New Game,Rafael selection/confirmation and opening Claudio scene.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    scope = ('All five capture alternatives2011-2015 have clean Japanese,original72368 mode0/53D44/table02117740 context,natural faithful American English and complete native layout/font review.2015 now explicitly confines the defeated crew to the captured flagship. The full V1364 stack retains471 batches114 accepted layers,all other3667 messages,routes/graphics/fonts/components and the complete runtime/selector/123040 staged bytes. Its clean-input patch reconstructs every byte.8 capture voice/font pipelines,206 unchanged actor selections,7336 copies180 cache sequences13 escape regressions pass. Two original current-ROM2011 holds at10800/10850 match the whole228x64 native/independent/reference/actual RGB plane,all letters,blank paper,margins and bounds. Source53D44 calls82478 logical role selection:Gerhard16 is selected with the physical First Mate slot empty;voice1 FFFFFFFF falls back to2011. Original Speyer encounter script,naval controls and the natural duel produce flagship capture,then2131 victory,food/water,4125 captured coins,75 national coins,cargo handling and power28 before ordinary sailing13200/mode000/cleared enemy parties. Normal X Finish and touch Yes discard untransferred spoil cargo;no cargo disposition is hidden. Only one prebattle fixture at4800 owns40 live position bytes for the existing five ships. It preserves health,crew,roles,actors/IDs,stored fleets,towns/companies,diplomacy,RNG and results. Earlier V1350 proves the offscreen cached and actual loaded target positions differ;V1352 uses a hashed actual position without moving the enemy. Every4MiB fixture delta and accepted input is audited;no later fixture,health/equipment/result/RNG edit or numeric message injection. Source/disposable donor saves unchanged. Only2011 is individually activated;other four use representative family evidence. Eight whole ordinary startup/title/New Game controls and photographed676/677 formatting pass. Targeted headless testing is not earned travel,full-route or hardware verification. No ship-sinking or other unreviewed notice completion is claimed.')
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','native_message_IDs':IDS,'records':selected,
        'manuscripts':[str(old_manuscript),str(corrected_manuscript)],'candidate':str(ROM),'candidate_sha256':digest,
        'actual_gameplay':str(ACTUAL),'actual_gameplay_sha256':sha(ACTUAL.read_bytes()),
        'registered_release':str(release_path),'registered_release_sha256':sha(release_path.read_bytes()),
        'actual_verification_scope':scope,'completed_entries':5,'revised':5,'retained':0,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    family = 'Shared-aftermath-flagship-capture5'
    documentation = 'docs/flagship_capture_v1371_completion.md'
    ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':IDS,'records':selected,
        'final_review':str(FINAL),'documentation':documentation,'actual_verification_scope':scope})
    assert family not in {r['id'] for r in ledger['coverage_units']}
    ledger['coverage_units'].append({'id':family,'status':'complete-source-native-and-representative-original-gameplay',
        'native_message_IDs':IDS,'final_review':str(FINAL),'actual_proof':str(ACTUAL),'full_goal_complete':False})
    ledger['records_editorially_completed'] += 5
    ledger['records_revised_and_integrated'] += 5
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] += 5
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [n for n in drafts['native_message_IDs'] if n not in IDS]
    for name,values in drafts['manuscript_record_subsets_pending'].items():
        if name.replace('\\','/')==old_manuscript.as_posix():
            drafts['manuscript_record_subsets_pending'][name] = [n for n in values if n not in IDS]
            assert len(drafts['manuscript_record_subsets_pending'][name])==34
    pending = ledger['reviewed_but_incomplete_COMMON_IDs'] = [n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    drafts['status'] = '16-sinking34-aftermath38-older-reviewed-entries-open'
    drafts['note'] = '41 of75 aftermath alternatives complete through original family scenes,including five flagship captures with2015 precision correction.34 aftermath,16 sinking and38 older reviewed COMMON entries remain incomplete;broader shared/routes/raw inventory remains open.'
    reference = ledger['current_native_relocation_reference']
    reference.pop('75_source_native_approved36_family_records_complete39_pending')
    reference.update(candidate=str(ROM),candidate_sha256=digest,COMMON_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],parser='dk4tool.patch.flagship_capture_precision.current_entries',
        release_config='translations/flagship_capture_precision_release_v1.json',
        flagship_capture5_source_native_and_representative_gameplay_complete=True)
    reference['75_source_native_approved41_family_records_complete34_pending'] = True
    ledger['latest_registered_aftermath_candidate'].update(status='experimental-41-aftermath-complete34-original-scenes-pending',latest_actual_proof=str(ACTUAL))
    ledger['latest_registered_flagship_precision_candidate'] = {**release,'status':'experimental-capture5-source-native-and-representative-gameplay-complete',
        'final_review':str(FINAL),'actual_proof':str(ACTUAL),'completed_entries_added':5,'full_goal_complete':False}
    ledger['formatting_watchlist']['latest_reference_proof'] = str(shop_path)
    ledger['formatting_watchlist']['latest_photographed_shop_recheck'] = {'checkpoint':'V1371','candidate':str(ROM),
        'candidate_sha256':digest,'proof':str(shop_path),'result':'Exact repaired676/677 native wrapping and full fonts pass;no fresh shop visit claimed.',
        'global_formatting_audit_complete':False}
    summary = ('V1371 completes five enemy-flagship capture alternatives2011-2015,all revised,in registered V1364. Counts1307 complete(975 revised332 retained),1395 source/prose;88 reviewed-incomplete COMMON(16 sinking34 aftermath38 older),plus broader shared/routes/raw prose. Original five-ship/Speyer encounter and natural duel yield2011 with two complete native/independent/actual RGB holds,proper Gerhard16 logical-role fallback and all first/final letters/margins/bounds. Normal rewards,cargo Finish/touch Yes and power notice return to sailing/mode000/cleared enemy parties. One40-owned-byte prebattle location fixture only;health,crew,roles,actors/IDs,enemy,diplomacy,RNG/results untouched at insertion,all4MiB/input/saves audited and no later fixture. V1354 stopped at a physical-role assumption;1354b/1370 bind original82478 logical selection without assigning a First Mate.2015 is clarified to the flagship crew specifically. All8 voice/five-text native font pipelines206 actor choices,7336 copies180 sequences13 escape regressions,eight ordinary startup frames and shop676/677 pass. All471 batches114 accepted layers,routes/graphics/fonts,3667 unselected messages,entire runtime/188-byte selector and123040 staged bytes are preserved;exact clean-input patch reconstructs. Only2011 has individual actual activation;no sinking credit.41 of75 aftermath alternatives complete. Canonical,V997,separate graphics/all18 plaques and later older-record re-audit stay unchanged/open;full goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1371-flagship-capture5-complete','proof':str(FINAL),'actual':str(ACTUAL),
        'completed_entries_added':5,'source_prose_reviews_added':0,'full_goal_complete':False})
    completed = [n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    assert len(completed)==len(set(completed))==1306
    assert len(pending)==len(set(pending))==len(drafts['native_message_IDs'])==88
    assert not set(completed).intersection(pending) and len(set(completed)|set(pending))==1394
    assert ledger['records_editorially_completed']==ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1307
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1307
    for key in ['records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file',
                'current_integrated_candidate','source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    path = 'E:/Rota Nova translations/Generated/out/all_routes_combined_v1364_candidate.nds'
    assert not any(r['path']==path for r in pins)
    pins.append({'path':path,'reason':'Verified captured-flagship5 editorial candidate and current native COMMON parent;retain for pending sinking and other original-scene tests.'})
    save(pins_path,pins)
    text = '# V1371: five flagship-capture messages completed\n\n'+summary+'\n\n## Exact experimental release\n\n'+\
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1364_candidate.nds`; SHA-256 `'+digest+'`.\n'+\
        '- Canonical base: `out/raphael_natural_v2_accepted_base.nds`; SHA-256 `'+release['canonical_sha256']+'`;profile `'+release['profile']+'`,all471 manifest batches114 accepted layers.\n'+\
        '- Relative to V1344,only COMMON block22/2015 and ARM9 original native offsets/directory change. Every executable/runtime/selector byte and all graphics/routes/fonts remain exact.\n'+\
        '- Patch: `out/all_routes_combined_v1364_candidate.xdelta`; SHA-256 `'+release['patch_sha256']+'`;clean input `'+release['clean_input_sha256']+'`;complete reconstruction byte-exact.\n'+\
        '- Verifiers: `probe_flagship_precision_fonts_v1357.py`,`verify_flagship_precision_copies_v1359.py`,`verify_flagship_precision_escape_v1360.py`,`verify_flagship_precision_release_v1365.py`,`run_flagship_precision_startup_v1366.py --verify`,`recheck_shop_formatting_v1367.py`,`verify_flagship_capture_replay_v1370.py`.\n\n## Evidence scope\n\n'+scope+'\n\nFinal review: `'+str(FINAL)+'`. Actual proof: `'+str(ACTUAL)+'`. Guide screenshots: `E:/Rota Nova translations/Guide screenshots/V1364 Flagship capture`. Earlier V1344 proof and source failures remain unchanged. The earlier physical First Mate assumption was a test binding error:the original logical role algorithm selects Gerhard16 automatically. No actor or room assignment was inserted. The sixteen sinking notices remain open;this was a capture. Broader route/shared/raw prose and the separate graphics audit remain unfinished.\n'
    Path(documentation).write_text(text,encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1371 flagship-capture5 complete\n\n'+summary+'\n\nSee [completion](flagship_capture_v1371_completion.md).\n')
    save(ROOT/'completion_receipt.json',{'completed':1307,'revised':975,'retained':332,'source_prose':1395,
        'newly_completed':5,'unique_complete_COMMON':1306,'reviewed_incomplete_COMMON':88,
        'aftermath75_complete':41,'aftermath75_pending':34,'source_review_credit_added':0,
        'final_review':str(FINAL),'final_review_sha256':sha(FINAL.read_bytes()),'candidate_sha256':digest,
        'canonical_and_V997_unchanged_global_goal_active':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Five flagship-capture alternatives completed:1307 complete/1395 reviewed;88 reviewed COMMON entries remain incomplete. Full goal active.',flush=True)


if __name__=='__main__':
    main()
