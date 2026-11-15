"""Complete eight victory alternatives after native/current-ROM scene evidence."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from PIL import Image
from dk4tool.patch.battle_victory_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.battle_victory_native_plan_v1396 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/battle_victory_completion_v1411')
ROM = Path('out/all_routes_combined_v1404_candidate.nds')
MANUSCRIPT = Path('translations/battle_victory_editorial_manuscript_v2.json')
FINAL = Path('translations/battle_victory_final_review_v1.json')
ACTUAL = Path('work/analysis/battle_victory_verified_v1410/actual_victory_and_return_verification.json')
IDS = list(range(2130,2138))


if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    release_path = Path('work/analysis/battle_victory_release_v1403/registered_release_verification.json')
    release,actual,doc = read(release_path),read(ACTUAL),read(MANUSCRIPT)
    digest = sha(ROM.read_bytes())
    assert digest==release['candidate_sha256']==actual['candidate_sha256']
    assert release['actual_changed_message_IDs']==[2136,2137] and release['complete_reconstruction_byte_exact']
    assert actual['terminal_frame']==13200 and len(actual['complete_actual2131_holds'])==2
    assert actual['entire4MiB_fixture_input_primary_RAM_and_PNG_hash_audits_pass']
    assert actual['normal_victory_A_dismissal_rewards_X_cargo_finish_touch_Yes_and_return_to_sailing']
    assert all(h['whole_current_COMMON23_resident_exactly_once'] for h in actual['complete_actual2131_holds'])
    fonts_path = Path(doc['native_font_proof'])
    fonts = read(fonts_path)
    assert len(fonts['cases'])==8 and len(fonts['all206_existing_actor_choices'])==206 and not fonts['findings']
    assert len(fonts['invalid_compiler_inputs_rejected'])==14
    rom,clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    arm,common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries = current_entries(common,arm)
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    rows = []
    for record in doc['records']:
        row = deepcopy(record)
        n = row['message_id']
        assert n in IDS and row['source_hex']==jp[n].text.hex() and all(row['review'].values())
        assert entries[n].text==compiled(row)
        case = next(c for c in fonts['cases'] if c['message_ID']==n)
        assert case['compiled_hex']==entries[n].text.hex() and len(case['lines'])==1
        row.update(manuscript=str(MANUSCRIPT),previous_current_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[n]).items() if k!='text'},
            current_text_hex=entries[n].text.hex(),current_English=row['english'],
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-verified',
            status='complete-source-native-and-representative-original-victory-gameplay',
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            complete_native_font_proof=str(fonts_path),complete_native_font_proof_sha256=sha(fonts_path.read_bytes()),
            complete_native_formatted_lines=case['lines'],
            actual_holds=actual['complete_actual2131_holds'] if n==2131 else [],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
        rows.append(row)
    assert [r['message_id'] for r in rows]==IDS
    assert sum(r['editorial_decision']=='revise' for r in rows)==2
    startup_path = release_path.parent/'ordinary_startup_verification.json'
    startup = read(startup_path)
    assert startup['candidate_sha256']==digest and len(startup['pairs'])==8
    assert startup['all8_complete_startup_title_NewGame_frames_exact']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    shop_path = release_path.parent/'photographed_shop_formatting.json'
    shop = read(shop_path)
    assert shop['candidate_sha256']==digest and all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in shop['entries'])
    old_cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193/flagship_capture_v1369_1364')
    new_cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_victory_v1409_1404')
    pairs = []
    for frame in [10800,10850,10950,11000,11100,11200,11300,11400,11500,11600,12400,12500,12600,12900,13000,13200]:
        name = f'frame_{frame:06d}_navigation.png'
        old,new = old_cap/name,new_cap/name
        assert Image.open(old).convert('RGB').tobytes()==Image.open(new).convert('RGB').tobytes()
        pairs.append({'frame':frame,'old':str(old),'old_sha256':sha(old.read_bytes()),
            'current':str(new),'current_sha256':sha(new.read_bytes()),'whole256x384_RGB_exact':True})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1307,1403)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==96
    assert not any(set(IDS)&set(f.get('native_message_IDs',[])) for f in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_completion.json',before)
    save(ROOT/'sixteen_original_reward_return_screens.json',{'pairs':pairs,'all16_whole_screens_exact':True,
        'new_candidate_sha256':digest,'producer_sha256':sha(Path(__file__).read_bytes())})
    save(release_path.parent/'ordinary_startup_visual_review.json',{'candidate_sha256':digest,
        'proof':str(startup_path),'proof_sha256':sha(startup_path.read_bytes()),
        'review_sheet':startup['review_sheet'],'review_sheet_sha256':startup['review_sheet_sha256'],
        'all8_frames_actually_visually_reviewed':True,'no_save_savestate_or_fixtures':True,
        'scope':'Ordinary title,New Game,Rafael selection/confirmation and opening Claudio scene.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    scope = ('Eight alternatives2130-2137 have clean Japanese,original72168/72170 role1/53D44/table02117EE0 '
        'context and faithful natural English. Two revisions,six retentions;2132 genuine IC plural means we. '
        'Eight whole228x64 native/independent font planes and every ordered glyph event pass,including the '
        'original leading cell and exact odd-pair trailing blank. All206 existing NPC choices,14 invalid '
        'compiler controls,7336 full copies,180 cache sequences and13 escape paths pass. Only2136/2137 prose '
        'and COMMON23/native data offsets change;all3666 other text/copy spans,routes,graphics,fonts,entire '
        'runtime/188-byte selector/172-byte gate and123040 staged bytes remain exact. Full471 batches114 '
        'accepted layers and exact clean-input patch reconstruction pass. Eight whole ordinary startup '
        'frames match controls and were visually reviewed. Two original2131 holds from Gerhard16 match '
        'the complete native/independent/reference/actual RGB plane,all letters,margin,bounds and blank '
        'paper. Actual complete current COMMON23 is resident exactly once. The physical First Mate slot '
        'is empty;original82478 selects existing Gerhard16. A-dismissal leads through original rewards,'
        'cargo X Finish/touch Yes and power notice to ordinary sailing13200/mode000/cleared enemy parties. '
        'Untransferred spoil cargo is discarded through that original confirmation. Sixteen complete '
        'capture/victory/reward/cargo/return screens match the older V1364 encounter exactly. Only the '
        'prebattle40-owned-byte location fixture is applied at4800;all4MiB/input/primary RAM/PNG/donor '
        'audits pass. No equipment,health,crew,actor/ID,RNG,result or later battle/duel mutation occurs. '
        'Only2131 is individually activated;other seven use the representative-family scene and complete '
        'native voice proofs. This is targeted headless testing,not earned travel,a full route,or hardware '
        'verification. No sinking or other unreviewed family completion is claimed.')
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','native_message_IDs':IDS,'records':rows,
        'manuscript':str(MANUSCRIPT),'candidate':str(ROM),'candidate_sha256':digest,
        'actual_gameplay':str(ACTUAL),'actual_gameplay_sha256':sha(ACTUAL.read_bytes()),
        'registered_release':str(release_path),'registered_release_sha256':sha(release_path.read_bytes()),
        'actual_verification_scope':scope,'completed_entries':8,'revised':2,'retained':6,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    family = 'Shared-battle-victory8'
    document = 'docs/battle_victory_v1411_completion.md'
    ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':IDS,'records':rows,
        'final_review':str(FINAL),'documentation':document,'actual_verification_scope':scope})
    source_unit = next(r for r in ledger['coverage_units'] if r['id']=='Shared-battle-victory8-source-prose')
    source_unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(FINAL))
    ledger['coverage_units'].append({'id':family,'status':'complete-source-native-and-representative-original-gameplay',
        'native_message_IDs':IDS,'final_review':str(FINAL),'actual_proof':str(ACTUAL),'full_goal_complete':False})
    ledger['records_editorially_completed'] += 8
    ledger['records_revised_and_integrated'] += 2
    ledger['retained_wordings_editorially_completed'] += 6
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] += 8
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [n for n in drafts['native_message_IDs'] if n not in IDS]
    for name in drafts['manuscript_record_subsets_pending']:
        if name.replace('\\','/')=='translations/battle_victory_editorial_manuscript_v1.json':
            drafts['manuscript_record_subsets_pending'][name] = []
    pending = ledger['reviewed_but_incomplete_COMMON_IDs'] = [n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    drafts['status'] = '16-sinking34-aftermath38-older-reviewed-entries-open'
    drafts['note'] = ('Eight victory alternatives complete through original representative victory/reward/return '
        'and all native voices. Sixteen sinking,34 aftermath and38 older reviewed COMMON entries remain '
        'incomplete;broader shared/routes/raw prose and the separate graphics audit stay open.')
    reference = ledger['current_native_relocation_reference']
    reference.update(candidate=str(ROM),candidate_sha256=digest,COMMON_sha256=release['COMMON_sha256'],
        ARM9_sha256=release['ARM9_sha256'],parser='dk4tool.patch.battle_victory_editorial.current_entries',
        release_config='translations/battle_victory_editorial_release_v1.json',
        battle_victory8_source_native_and_representative_gameplay_complete=True)
    ledger['latest_registered_victory_candidate'] = {**release,
        'status':'experimental-victory8-source-native-and-representative-gameplay-complete',
        'final_review':str(FINAL),'actual_proof':str(ACTUAL),'completed_entries_added':8,'full_goal_complete':False}
    ledger['formatting_watchlist']['latest_reference_proof'] = str(shop_path)
    ledger['formatting_watchlist']['latest_photographed_shop_recheck'] = {'checkpoint':'V1411',
        'candidate':str(ROM),'candidate_sha256':digest,'proof':str(shop_path),
        'result':'Exact repaired676/677 native wrapping and full font planes pass;no fresh shop visit claimed.',
        'global_formatting_audit_complete':False}
    summary = ('V1411 completes eight battle victory alternatives2130-2137 in registered V1404:two revisions '
        'and six retentions. Counts1315 complete(977 revised338 retained),1403 source/prose;88 reviewed-incomplete '
        'COMMON(16 sinking34 aftermath38 older),plus broader shared/routes/raw prose. Eight whole native font '
        'planes/ordered glyph events,206 existing actor selections,14 invalid controls,7336 copies180 cache '
        'sequences13 escape paths and eight ordinary startup controls pass. Exact original one-cell margin '
        'and odd-pair trailing blank are verified without changing code. Two actual2131 Gerhard holds match '
        'the full native/reference/independent/RGB plane and complete current COMMON23. Original victory '
        'dismissal,rewards,cargo confirmation and sailing13200/mode000/cleared enemy parties pass;16 whole '
        'screens equal V1364. One40-byte prebattle location fixture only;all health,crew,equipment,actor/ID,'
        'RNG and result state untouched at insertion and no later fixture. Source/disposable saves unchanged. '
        'Only2131 individually activated;other voices use complete native proofs and representative family '
        'evidence. Only2136/2137 prose changes;3666 other texts/copies,all471 batches114 accepted layers,'
        'routes/graphics/fonts,entire runtime/188-byte selector/172-byte gate and123040 staged bytes exact. '
        'Clean-input patch reconstructs every byte. Shop676/677 formatting remains exact. No sinking credit. '
        'Canonical,V997,graphics/all18 plaques and later older-record re-audit remain unchanged/open;goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1411-victory8-complete','proof':str(FINAL),'actual':str(ACTUAL),
        'completed_entries_added':8,'source_prose_reviews_added':0,'full_goal_complete':False})
    complete = [n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    assert len(complete)==len(set(complete))==1314
    assert len(pending)==len(set(pending))==len(drafts['native_message_IDs'])==88
    assert not set(complete)&set(pending) and len(set(complete)|set(pending))==1402
    assert ledger['records_editorially_completed']==ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed']==1315
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1315
    for key in ['records_with_source_and_prose_pass','records_with_source_prose_drafts','source_prose_reviewed_counts_by_file',
        'current_integrated_candidate','source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key]==before[key],key
    save(ledger_path,ledger)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    pin = 'E:/Rota Nova translations/Generated/out/all_routes_combined_v1404_candidate.nds'
    assert not any(r['path']==pin for r in pins)
    pins.append({'path':pin,'reason':'Verified victory8 editorial candidate and current native COMMON parent;required for ongoing full editorial inventory and pending sinking/aftermath scenes.'})
    save(pins_path,pins)
    Path(document).write_text('# V1411 eight victory reports complete\n\n'+summary+
        '\n\n## Exact experimental release\n\n'
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1404_candidate.nds`;SHA-256 `'+digest+'`.\n'
        '- Canonical base: `out/raphael_natural_v2_accepted_base.nds`;SHA-256 `'+release['canonical_sha256']+'`.\n'
        '- Profile: `all-routes-unified-v1404`;all471 manifest batches and114 accepted layers preserved.\n'
        '- Changes relative to V1364: COMMON block23/two prose entries2136/2137 and original ARM9 native offset/directory data only.\n'
        '- Patch: `out/all_routes_combined_v1404_candidate.xdelta`;SHA-256 `'+release['patch_sha256']+'`;clean input `'+release['clean_input_sha256']+'`;byte-exact reconstruction.\n'
        '- Checks: native-font1397b,copies1399,escape1400,registered-release1405,startup1406,shop1407 and original-replay1410.\n'
        '- Experimental,not promoted. Any user testing should cold-boot the candidate and check the title,New Game,and battle victory/reward return.\n\n'
        '## Evidence scope\n\n'+scope+'\n\nFinal review: `'+str(FINAL)+'`. Guide screenshots: '
        '`E:/Rota Nova translations/Guide screenshots/V1404 Victory reports`. The sixteen sinking notices and '
        'remaining shared/routes/raw prose still need work. Existing graphics/all18 plaques remain a separate '
        'unfinished audit.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1411 victory8 complete\n\n'+summary+
                '\n\nSee [completion](battle_victory_v1411_completion.md).\n')
    save(ROOT/'completion_receipt.json',{'completed':1315,'revised':977,'retained':338,'source_prose':1403,
        'newly_completed':8,'unique_complete_COMMON':1314,'reviewed_incomplete_COMMON':88,
        'aftermath75_complete':41,'aftermath75_pending':34,'source_review_credit_added':0,
        'final_review':str(FINAL),'final_review_sha256':sha(FINAL.read_bytes()),'candidate_sha256':digest,
        'all16_sinking_entries_still_pending':True,'canonical_and_V997_unchanged_global_goal_active':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Eight victory alternatives complete:1315 complete/1403 reviewed;88 reviewed COMMON entries unfinished. Full goal active.',flush=True)
