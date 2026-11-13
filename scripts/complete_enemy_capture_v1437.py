"""Close the eight capture reports after source/native/integration/gameplay gates."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from dk4tool.patch.enemy_capture_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.enemy_capture_native_plan_v1423 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/enemy_capture_completion_v1437')
ROM = Path('out/all_routes_combined_v1430_candidate.nds')
MANUSCRIPT = Path('translations/enemy_capture_editorial_manuscript_v3.json')
FINAL = Path('translations/enemy_capture_final_review_v1.json')
ACTUAL = Path('work/analysis/enemy_capture_verified_v1435b/actual_capture_and_return_verification.json')
IDS = list(range(2082,2090))

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    release_path = Path('work/analysis/enemy_capture_release_v1429/registered_release_verification.json')
    release,actual,doc = read(release_path),read(ACTUAL),read(MANUSCRIPT)
    digest = sha(ROM.read_bytes())
    assert digest==release['candidate_sha256']==actual['candidate_sha256']
    assert release['actual_changed_message_IDs']==IDS and release['complete_reconstruction_byte_exact']
    assert actual['terminal_frame']==13200 and len(actual['complete_actual2082_holds'])==2
    assert actual['entire4MiB_fixture_input_primary_RAM_and_PNG_hash_audits_pass']
    assert actual['normal_capture_A_dismissal_flagship_victory_rewards_X_cargo_finish_touch_Yes_and_return_to_sailing']
    assert all(h['whole_current_COMMON22_resident_exactly_once'] and
        h['whole228x64_native_independent_reference_and_actual_RGB_exact'] for h in actual['complete_actual2082_holds'])
    comparisons = actual['later9_whole_reward_cargo_and_sailing_screens_exact_plus10850_A_prompt_phase_only']
    assert len(comparisons)==10 and sum(r['whole_RGB_equal_to_V1404'] for r in comparisons)==9
    icon = next(r for r in comparisons if r['frame']==10850)['A_prompt_phase_only']
    assert icon['rectangle']==[224,360,240,376] and icon['all_text_portraits_scenes_and_every_other_pixel_exact']
    fonts_path = Path(doc['native_font_proof']);fonts = read(fonts_path)
    assert len(fonts['cases'])==208 and len(fonts['all206_source_existing_actor_choices'])==206 and not fonts['findings']
    assert len(fonts['invalid_compiler_inputs_rejected'])==15
    rom,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    arm,common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries = current_entries(common,arm)
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    rows = []
    for record in doc['records']:
        row = deepcopy(record);n = row['message_id']
        assert n in IDS and row['source_hex']==jp[n].text.hex() and all(row['review'].values())
        assert row['editorial_decision']=='revise' and entries[n].text==compiled(row)
        cases = [c for c in fonts['cases'] if c['message_ID']==n]
        assert len(cases)==26 and all(c['compiled_hex']==entries[n].text.hex() and not c['findings'] for c in cases)
        row.update(manuscript=str(MANUSCRIPT),previous_current_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[n]).items() if k!='text'},
            current_text_hex=entries[n].text.hex(),current_English=row['english'],decision='revised-and-integrated',
            status='complete-source-native-and-representative-original-capture-gameplay',
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            complete_native_font_proof=str(fonts_path),complete_native_font_proof_sha256=sha(fonts_path.read_bytes()),
            complete_native_formatted_lines=next(c for c in cases if c['variant']==0)['lines'],
            actual_holds=actual['complete_actual2082_holds'] if n==2082 else [],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
        rows.append(row)
    assert [r['message_id'] for r in rows]==IDS
    startup_path = release_path.parent/'ordinary_startup_verification.json';startup = read(startup_path)
    assert startup['candidate_sha256']==digest and len(startup['pairs'])==8 and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    shop_path = release_path.parent/'photographed_shop_formatting.json';shop = read(shop_path)
    assert shop['candidate_sha256']==digest and all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in shop['entries'])
    ledger_path = Path('translations/editorial_review_current_v1.json');ledger = read(ledger_path);before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1315,1411)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==96
    assert not any(set(IDS)&set(f.get('native_message_IDs',[])) for f in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True);save(ROOT/'coverage_before_completion.json',before)
    save(release_path.parent/'ordinary_startup_visual_review.json',{'candidate_sha256':digest,
        'proof':str(startup_path),'proof_sha256':sha(startup_path.read_bytes()),
        'review_sheet':startup['review_sheet'],'review_sheet_sha256':startup['review_sheet_sha256'],
        'all8_frames_actually_visually_reviewed':True,'no_save_savestate_or_fixtures':True,
        'scope':'Ordinary title,New Game,Rafael selection/confirmation and opening Claudio scene.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    scope = ('Eight mutually exclusive reports2082-2089 have clean Japanese,original74050/74058/direct53F0C/'
        'table02117B00 context and natural faithful English. All8 paragraphs are revised:seven spoken '
        'clauses and one intentionally clipped report. The named enemy vessel and exactly one source%s '
        'argument are preserved,without invented casualties,sinking or whole-fleet victory. Original '
        '55DC4(attacker,8) selects the existing announcing officer. The previously unscoped path corrupts '
        'FA/IC/FI/FO/FU-like names and fails long-name bounds;one exact parent/table membership activates '
        'the existing literal-name and word-wrap formatter. Numeric bias512,pointer bias896 and adjusted '
        'historical numeric dispatch thresholds fit188 selector bytes and172 gate bytes.529325 native '
        'selector/ABI/guard cases pass;historical3668 modal-ID routing controls use a fixed synthetic '
        'paragraph,not3668 distinct game texts.238 wrong-parent5 edge and140 whole-memory status cases '
        'pass. All208 original selection/printf/macro/wrap/full228x64 independent font cases pass with '
        'literal complete names,uniform6px visible margins,all leading/trailing letters,bounds and15 '
        'compiler rejections. All8 sheets/64 preview panels are visually reviewed. Complete long runtime '
        'proper names may occupy their own final row as the intact grammatical object;no isolated '
        'non-name predicate is waived. V1422 revisits five earlier caption retentions as natural spoken '
        'clauses;these are longer source-faithful English,not fit-only abbreviations. No shared BALANCE,'
        'literal wrapper,live status tail or earlier formatter is changed.7336 complete copies180 cache '
        'sequences13 direct escape regressions pass. All471 batches114 accepted layers,3660 other '
        'texts/copy spans,40 other COMMON blocks,routes/graphics/fonts/components and opaque duel code '
        'remain exact. No section/BSS/cache/arena/ITCM or123040 staged growth. The clean-input patch '
        'reconstructs every ROM byte;all8 ordinary startup/title/New Game controls match and are viewed. '
        'Two original2082 Charles18 holds10750/10780 match the complete native/reference/independent/'
        'actual RGB plane and entire current COMMON22 residence. Original enemy virtual name is Hanse '
        'Cog,Hull30/Crew0. Original A dismisses capture and continues through flagship capture,victory,'
        'food/water29,captured coins4125,national award75,cargo X Finish/touch Yes,power28 and ordinary '
        'sailing13200/mode000/cleared enemy parties with five own ships. Untransferred spoil cargo is '
        'discarded through that original confirmation. Nine later whole screens match V1404;10850 '
        'differs only inside the original16x16 blinking A icon after80 extra capture reading frames,with '
        'all text,portraits and other pixels exact. V1435 stopped at a whole-screen assumption;V1435b '
        'requires that precise icon-only difference. One40-owned-byte prebattle location fixture is '
        'applied at4800;all4MiB/input/RAM/PNG/donor audits pass with no later fixture,health,crew,'
        'equipment,actor/ID,RNG or result injection. Only2082 is individually activated;other seven '
        'have complete native proofs and representative-family gameplay. Targeted headless evidence '
        'does not prove earned travel,full-route or hardware play. No sinking completion credit.')
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','native_message_IDs':IDS,'records':rows,
        'manuscript':str(MANUSCRIPT),'candidate':str(ROM),'candidate_sha256':digest,
        'actual_gameplay':str(ACTUAL),'actual_gameplay_sha256':sha(ACTUAL.read_bytes()),
        'registered_release':str(release_path),'registered_release_sha256':sha(release_path.read_bytes()),
        'actual_verification_scope':scope,'completed_entries':8,'revised':8,'retained':0,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    family = 'Shared-individual-enemy-ship-capture8';document = 'docs/enemy_capture_v1437_completion.md'
    ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':IDS,'records':rows,
        'final_review':str(FINAL),'documentation':document,'actual_verification_scope':scope})
    unit = next(r for r in ledger['coverage_units'] if r['id']=='Shared-individual-enemy-ship-capture8-source-prose')
    unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(FINAL))
    ledger['coverage_units'].append({'id':family,'status':'complete-source-native-and-representative-original-gameplay',
        'native_message_IDs':IDS,'final_review':str(FINAL),'actual_proof':str(ACTUAL),'full_goal_complete':False})
    ledger['records_editorially_completed'] += 8;ledger['records_revised_and_integrated'] += 8
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] += 8
    pending = ledger['reviewed_but_incomplete_COMMON_IDs'] = [n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [n for n in drafts['native_message_IDs'] if n not in IDS]
    for name in drafts['manuscript_record_subsets_pending']:
        if 'enemy_capture_editorial_manuscript' in name:
            drafts['manuscript_record_subsets_pending'][name] = []
    drafts['status'] = '16-sinking34-aftermath38-older-reviewed-entries-open'
    drafts['note'] = 'Capture8 is complete with native/name protection and representative original gameplay.16 sinking,34 aftermath and38 older reviewed COMMON entries remain incomplete,plus broader shared/routes/raw prose and the separate graphics audit.'
    ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        parser='dk4tool.patch.enemy_capture_editorial.current_entries',release_config='translations/enemy_capture_editorial_release_v1.json',
        individual_enemy_capture8_source_native_and_representative_gameplay_complete=True)
    ledger['latest_registered_enemy_capture_candidate'] = {**release,
        'status':'experimental-capture8-source-native-and-representative-gameplay-complete',
        'final_review':str(FINAL),'actual_proof':str(ACTUAL),'completed_entries_added':8,'full_goal_complete':False}
    ledger['formatting_watchlist']['individual_enemy_capture_research'].update(status='completed-in-V1430',
        final_review=str(FINAL),native_font_evidence=doc['native_font_proof'],
        unresolved_non_name_layout_findings=0,prior53_findings_superseded_by_source_refinement_and_explicit_complete_name_review=True,
        registered_ROM_repair_and_actual_capture_transition_pending=False)
    ledger['formatting_watchlist']['latest_reference_proof'] = str(shop_path)
    ledger['formatting_watchlist']['latest_photographed_shop_recheck'] = {'checkpoint':'V1437','candidate':str(ROM),
        'candidate_sha256':digest,'proof':str(shop_path),'result':'Exact repaired676/677 native wrapping and full font planes pass;no fresh shop visit claimed.',
        'global_formatting_audit_complete':False}
    summary = ('V1437 completes individual enemy ship-capture8(2082-2089),all revised,in registered V1430. '
        'Counts1323 complete(985 revised338 retained),1411 source/prose;88 reviewed-incomplete COMMON'
        '(16 sinking34 aftermath38 older),plus broader shared/routes/raw prose. Exact direct caller protects '
        'literal ship names and wraps after original printf;all208 full native font/name/margin/bounds '
        'cases and15 negative compiler cases pass. Complete long-name objects are explicitly reviewed;'
        'no orphan non-name predicates remain.188 selector/172 gate/123040 staged bytes fit without '
        'growth;all earlier formatter/status code remains unchanged.529325 dispatch/ABI,7336 copies180 '
        'cache sequences13 escape paths,8 startup controls and shop676/677 pass. Exact clean-input patch '
        'reconstructs all bytes;471 batches114 accepted layers,3660 other messages,routes/graphics/fonts '
        'and opaque duel prefix preserved. Two actual2082 Charles18/Hanse Cog holds match full native/'
        'independent/reference/RGB and current COMMON22. Normal dismissal,flagship/victory/rewards/cargo '
        'and sailing13200/mode000/cleared enemies verified. Nine later whole screens match;10850 has '
        'only the16x16 blinking A phase difference after80 extra reading frames. One40-byte prebattle '
        'location fixture,full4MiB/input/RAM/PNG/save audit;no health/crew/equipment/actor/ID/RNG/result '
        'or later battle mutation. Only2082 individually activated;other voices use native and family '
        'proof. Untransferred spoil cargo is discarded via original confirmation. No sinking credit. '
        'Canonical,V997,separate graphics/all18 plaques and later older-record re-audit stay unchanged/open;goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1437-enemy-capture8-complete','proof':str(FINAL),'actual':str(ACTUAL),
        'completed_entries_added':8,'source_prose_reviews_added':0,'full_goal_complete':False})
    complete = [n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    assert len(complete)==len(set(complete))==1322
    assert len(pending)==len(set(pending))==len(drafts['native_message_IDs'])==88
    assert not set(complete)&set(pending) and len(set(complete)|set(pending))==1410
    assert ledger['records_editorially_completed']==ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1323
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1323
    for key in ['records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file',
        'current_integrated_candidate','source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    pins_path = Path('translations/rom_retention_pins.json');pins = read(pins_path)
    pin = 'E:/Rota Nova translations/Generated/out/all_routes_combined_v1430_candidate.nds'
    assert not any(r['path']==pin for r in pins)
    pins.append({'path':pin,'reason':'Verified capture8 editorial candidate and current native COMMON parent;required for ongoing source inventory and pending sinking/aftermath scene work.'});save(pins_path,pins)
    Path(document).write_text('# V1437 eight enemy ship-capture reports complete\n\n'+summary+
        '\n\n## Exact experimental release\n\n'
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1430_candidate.nds`;SHA-256 `'+digest+'`.\n'
        '- Canonical base: `out/raphael_natural_v2_accepted_base.nds`;SHA-256 `'+release['canonical_sha256']+'`.\n'
        '- Profile: `all-routes-unified-v1430`;all471 manifest batches114 accepted layers preserved.\n'
        '- Changes versus V1404: COMMON22/capture8 prose,original ARM9 native offset/directory data and exactly the existing188-byte selector/172-byte gate.\n'
        '- Exact patch: `out/all_routes_combined_v1430_candidate.xdelta`;SHA-256 `'+release['patch_sha256']+'`;clean input `'+release['clean_input_sha256']+'`.\n'
        '- Checks: runtime1418,fonts1424,copies1425,escape1426,release1431,startup1432,original capture1435b,shop1436.\n'
        '- Experimental,not promoted. User testing can cold-boot title/New Game and a capture report/reward return,including custom ship names.\n\n'
        '## Evidence scope\n\n'+scope+'\n\nFinal review: `'+str(FINAL)+'`. Guide screenshots: '
        '`E:/Rota Nova translations/Guide screenshots/V1430 Enemy ship capture`. Global editorial and separate graphics audits remain unfinished.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1437 enemy capture8 complete\n\n'+summary+'\n\nSee [completion](enemy_capture_v1437_completion.md).\n')
    save(ROOT/'completion_receipt.json',{'completed':1323,'revised':985,'retained':338,'source_prose':1411,
        'newly_completed':8,'unique_complete_COMMON':1322,'reviewed_incomplete_COMMON':88,
        'aftermath75_complete':41,'aftermath75_pending':34,'source_review_credit_added':0,
        'final_review':str(FINAL),'final_review_sha256':sha(FINAL.read_bytes()),'candidate_sha256':digest,
        'all16_sinking_entries_still_pending':True,'canonical_and_V997_unchanged_global_goal_active':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Capture8 complete:1323 complete/1411 reviewed;88 reviewed COMMON entries unfinished. Full goal active.',flush=True)
