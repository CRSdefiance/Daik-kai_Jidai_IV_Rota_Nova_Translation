"""Close six fully verified fire alerts and update exact coverage/native reference."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from dk4tool.patch.powder_fire_editorial import current_entries,CONFIG
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.powder_fire_native_plan_v1309 import compiled
from scripts.powder_fire_layout_v1304 import IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_completion_v1323')
RELEASE = Path('work/analysis/powder_fire_release_v1315')
ACTUAL = Path('work/analysis/powder_fire_verified_v1322b/actual_powder_fire_verification.json')
FINAL = Path('translations/powder_fire_editorial_final_review_v1.json')
ROM = Path('out/all_routes_combined_v1316_candidate.nds')


def main():
    assert not ROOT.exists() and not FINAL.exists()
    actual,release = read(ACTUAL),read(RELEASE/'registered_release_verification.json')
    digest = sha(ROM.read_bytes())
    assert actual['candidate_sha256'] == release['candidate_sha256'] == digest
    assert release['complete_reconstruction_byte_exact'] and release['actual_changed_message_IDs'] == list(IDS)
    assert len(actual['complete_actual_holds']) == 4
    assert sum(hold['new_fire_message'] for hold in actual['complete_actual_holds']) == 2
    assert all(hold['missing_or_unexpected_foreground_pixels'] == 0 for hold in actual['complete_actual_holds'])
    assert actual['normal_A_dismissals_preserve_extinguished_response_clear_fire_and_return_to_original_sea_battle']
    assert actual['cleanup_is_deferred_until_original_extinguished_notice_is_dismissed_in_both_versions']
    startup_path = RELEASE/'ordinary_startup_verification.json'
    startup = read(startup_path)
    assert startup['candidate_sha256'] == digest and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert sha(Path(startup['review_sheet']).read_bytes()) == startup['review_sheet_sha256']
    shop = read(RELEASE/'photographed_shop_formatting.json')
    assert shop['candidate_sha256'] == digest and len(shop['entries']) == 2
    assert all(row['complete228x64_native_and_independent_font_equal'] for row in shop['entries'])
    visual_path = RELEASE/'ordinary_startup_visual_review.json'
    assert not visual_path.exists()
    save(visual_path,{'startup_proof':str(startup_path),'startup_proof_sha256':sha(startup_path.read_bytes()),
        'sheet_actually_visually_reviewed':startup['review_sheet'],'sheet_sha256':startup['review_sheet_sha256'],
        'all8_title_NewGame_full_frame_pairs_visually_reviewed':True,'no_save_savestate_or_fixtures':True,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    manuscript = Path(read(CONFIG)['manuscript'])
    doc = read(manuscript)
    font_path = Path(doc['native_font_proof'])
    fonts = read(font_path)
    rom = NdsImage.open(ROM)
    entries = current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'))
    selected = deepcopy(doc['records'])
    assert tuple(row['message_id'] for row in selected) == IDS
    assert all(row['editorial_decision'] == 'revise' and all(row['review'].values()) for row in selected)
    for row in selected:
        number = row['message_id']
        assert entries[number].text == compiled(row)
        cases = [case for case in fonts['cases'] if case['message_id'] == number]
        assert cases and all(case['compiled_hex'] == entries[number].text.hex() for case in cases)
        row.update(before_reference=deepcopy(row['current_reference']),before_text_hex=row['current_text_hex'],
            current_reference={key:value for key,value in asdict(entries[number]).items() if key != 'text'},
            current_text_hex=entries[number].text.hex(),current_English=row['english'],decision='revised-and-integrated',
            status='complete-with-source-native-and-representative-original-powder-fire-gameplay',
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            complete_native_font_proof=str(font_path),complete_native_font_proof_sha256=sha(font_path.read_bytes()),
            complete_native_formatted_lines=cases[0]['lines'],
            actual_holds=[hold for hold in actual['complete_actual_holds'] if hold['new_fire_message'] and hold['native_message_IDs_matching_cached_template'] == [number]],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
    scope = ('All6 powder-fire alternatives2052-2057 have clean Japanese,original gun-position actor/direct-table context,natural faithful American English and complete native layout/font review. Source table02117980 retains both FFFFFFFF fallbacks to2052.206 existing noncaptain selections,all8 voice pipelines,12 malformed compiler controls,529286 selector/ABI,7336 native copies180 cache transitions and13 escape regressions pass. Registered V1316 preserves471 batches114 accepted layers,all other3662 messages/routes/graphics/fonts and123040 staged bytes;its clean-input patch reconstructs every ROM byte. Eight ordinary no-save startup/title/New Game frames match V1105 and were visually reviewed. The original unforced powder-fire event selects Gerhard16/voice1/2053 in the revised candidate. Two complete228x64 new-alert RGB/font holds and two preserved extinguished-response holds match every letter,blank paper,margin and wrap. Normal A dismissals retain the original follow-up,then clear fire bit0 and return to the continuing original town battle. Source also defers cleanup until its follow-up is dismissed;final source/target ship state56 Hull112 Crew and flag0E4 agree. The sole prebattle fixture at5000 reproduces all4MiB:16 changed bytes within24 owned bytes for position,existing Charles/Gerhard duties and native-capacity124 sailors. Actors/IDs/attributes,towns/defenses/shares,diplomacy,RNG and events are unchanged at insertion;no later fixture or forced outcome. Source/disposable saves remain exact. Only2053 has individual actual activation;other5 have representative family evidence. No town surrender or additional aftermath credit. Targeted headless testing is not earned prerequisites,full-route or hardware verification.')
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass']) == (1296,1379)
    assert set(IDS) <= set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert not any(set(IDS).intersection(family.get('native_message_IDs',[])) for family in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_completion.json',before)
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','native_message_IDs':list(IDS),
        'manuscript':str(manuscript),'manuscript_sha256':sha(manuscript.read_bytes()),'records':selected,
        'candidate':str(ROM),'candidate_sha256':digest,'actual_gameplay':str(ACTUAL),'actual_gameplay_sha256':sha(ACTUAL.read_bytes()),
        'registered_release':str(RELEASE/'registered_release_verification.json'),
        'registered_release_sha256':sha((RELEASE/'registered_release_verification.json').read_bytes()),
        'actual_verification_scope':scope,'completed_entries':6,'revised':6,'retained':0,
        'other39_aftermath_and38_older_reviewed_records_incomplete':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    family_id = 'Shared-powder-fire6'
    ledger['completed_editorial_families'].append({'id':family_id,'native_message_IDs':list(IDS),'records':selected,
        'final_review':str(FINAL),'documentation':'docs/powder_fire_v1323_completion.md','actual_verification_scope':scope})
    unit = next(unit for unit in ledger['coverage_units'] if unit['id'] == 'Shared-powder-fire6-source-prose')
    unit.update(status='complete-with-source-native-and-representative-gameplay-evidence',completed_family_id=family_id,
        final_review=str(FINAL),actual_proof=str(ACTUAL),completed_entries_added=6)
    ledger['records_editorially_completed'] += 6
    ledger['records_revised_and_integrated'] += 6
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] += 6
    pending = ledger['reviewed_but_incomplete_COMMON_IDs'] = [number for number in ledger['reviewed_but_incomplete_COMMON_IDs'] if number not in IDS]
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [number for number in drafts['native_message_IDs'] if number not in IDS]
    old = 'translations/powder_fire_editorial_manuscript_v1.json'
    drafts['manuscripts'] = [name for name in drafts['manuscripts'] if name.replace('\\','/') != old]
    for name in list(drafts['manuscript_record_subsets_pending']):
        if name.replace('\\','/') == old:
            assert drafts['manuscript_record_subsets_pending'].pop(name) == list(IDS)
    drafts['status'] = '39-aftermath-and38-older-reviewed-entries-open'
    drafts['note'] = 'Six powder-fire alerts are complete through original revised2053 and complete8-voice native review.39 other aftermath and38 older reviewed COMMON entries remain incomplete;broader shared/routes/raw inventory remains open,including56 neighboring ship-result/ram entries inventoried only.'
    ref = ledger['current_native_relocation_reference']
    ref.update(candidate=str(ROM),candidate_sha256=digest,COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        parser='dk4tool.patch.powder_fire_editorial.current_entries',release_config=CONFIG,
        powder_fire6_source_native_and_representative_gameplay_complete=True)
    ledger['latest_registered_powder_fire_candidate'] = {**release,'status':'experimental-six-source-native-and-representative-gameplay-verified',
        'actual_proof':str(ACTUAL),'startup_visual_review':str(visual_path),'full_goal_complete':False}
    summary = ('V1323 completes all6 powder-fire alerts2052-2057:6 revisions. Counts1302 complete(970 revised332 retained),1379 source/prose;77 reviewed-incomplete COMMON remain(39 aftermath+38 older),plus broader unreviewed shared/routes/raw prose and56 inventoried-only neighbors. Registered V1316 retains471 batches114 accepted layers and exact clean-input patch. Only COMMON22,six texts/native offsets and the existing188-byte selector table change;renderer code,all routes/graphics/fonts,other3662 texts and123040 staged bytes stay exact.529286 selector/ABI,8 complete voice/font pipelines206 source selections,7336 copies180 cache transitions13 escape regressions and eight whole startup/title/New Game controls pass. Actual new2053 has two full font/RGB holds;two old extinguished-response holds and normal dismissal/fire cleanup return to the original ongoing town battle. One24-owned-byte prebattle fixture changes16 bytes;full4MiB/actors/towns/companies/RNG/input audits pass and no later fixture occurs. Original source also defers cleanup until the follow-up closes;1322b corrects an early cleanup assumption and matches final56/112 health and flag4. Source/disposable saves unchanged;only2053 individually activated. Shop676/677 exact native formatting and glyphs pass;no new shop visit claimed. Guide images saved on E. Canonical,V997,all18 plaques,separate graphics audit,older-record revisit and full goal remain unchanged/open.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1323-powder-fire6-completion','proof':str(FINAL),'actual':str(ACTUAL),
        'completed_entries_added':6,'source_prose_reviews_added':0,'full_goal_complete':False})
    complete = [number for family in ledger['completed_editorial_families'] for number in family.get('native_message_IDs',[])]
    assert len(complete) == len(set(complete)) == 1301
    assert len(pending) == len(set(pending)) == len(drafts['native_message_IDs']) == 77
    assert not set(complete).intersection(pending) and len(set(complete)|set(pending)) == 1378
    assert ledger['records_editorially_completed'] == ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed'] == 1302
    assert sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1302
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values()) == ledger['records_with_source_prose_drafts'] == 1379
    for key in ['current_integrated_candidate','source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key] == before[key]
    save(ledger_path,ledger)
    Path('docs/powder_fire_v1323_completion.md').write_text('# V1323: powder-fire alerts completed\n\n'+summary+'\n\n## Exact release\n\n'+
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1316_candidate.nds`; SHA-256 `'+digest+'`.\n'+
        '- Canonical base: `out/raphael_natural_v2_accepted_base.nds`; SHA-256 `'+release['canonical_sha256']+'`.\n'+
        '- Profile: `all-routes-unified-v1316`;471 batches114 accepted layers retained.\n'+
        '- Patch: `out/all_routes_combined_v1316_candidate.xdelta`; SHA-256 `'+release['patch_sha256']+'`;clean input `'+release['clean_input_sha256']+'`;every reconstructed byte matches.\n'+
        '- Relative to V1266:COMMON block22 and ARM9 native offsets/existing188-byte selector data only. All code and full123040 staged bytes are unchanged.\n\n## Actual scope\n\n'+scope+
        '\n\nFinal review: `'+str(FINAL)+'`. Actual proof: `'+str(ACTUAL)+'`. Guide images: `E:/Rota Nova translations/Guide screenshots/V1316 Powder fire`. Source-only failures and preserved context remain documented in [V1305](powder_fire_v1305_source_checkpoint.md). V1322 expected fire bit0 to clear before the original extinguished notice closed;V1322b binds the correct deferred phase and original source comparison. No game rule or verification requirement was waived.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1323 powder-fire family completed\n\n'+summary+'\n\nSee [evidence](powder_fire_v1323_completion.md).\n')
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    target = 'E:/Rota Nova translations/Generated/out/all_routes_combined_v1316_candidate.nds'
    assert not any(pin['path'].replace('\\','/') == target for pin in pins)
    pins.append({'path':target,'reason':'Latest registered complete powder-fire6 layer and native relocation reference;required for broader editorial work and remaining39 aftermath scenes.'})
    save(pins_path,pins)
    save(ROOT/'completion_receipt.json',{'completed':1302,'revised':970,'retained':332,'source_prose':1379,
        'newly_completed':6,'unique_complete_COMMON':1301,'reviewed_incomplete_COMMON':77,
        'no_duplicate_source_or_completion_credit':True,'existing_source_coverage_unit_promoted_without_duplicate':True,
        'final_review':str(FINAL),'final_review_sha256':sha(FINAL.read_bytes()),'candidate_sha256':digest,
        'current_native_reference_updated_canonical_and_whole_batch_V997_unchanged':True,
        'global_goal_active':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Six powder-fire alerts complete:1302 total,1379 source/prose;77 reviewed COMMON plus broader inventory remain open.',flush=True)


if __name__ == '__main__':
    main()
