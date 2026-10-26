"""Close war8 after source/native/registered/original response-transition verification."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.declaration_responses_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.declaration_responses_native_plan_v1535b import compiled, IDS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/declaration_responses_completion_v1549')
ROM = Path('out/all_routes_combined_v1542_candidate.nds')
DOC = Path('translations/declaration_responses_editorial_manuscript_v3.json')
FINAL = Path('translations/declaration_responses_final_review_v1.json')
ACTUAL = Path('work/analysis/declaration_responses_actual_fonts_v1547b/actual_NPC_response_font_and_transition_verification.json')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1542 NPC declaration responses')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not GUIDE.exists()
    release_path = Path('work/analysis/declaration_responses_release_v1541/registered_release_verification.json')
    release, actual, doc = read(release_path), read(ACTUAL), read(DOC)
    digest = sha(ROM.read_bytes())
    assert digest == release['candidate_sha256'] == actual['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and release['actual_changed_message_IDs'] == list(IDS)
    assert release['all471_batches114_accepted_layers_and_prior_profiles_preserved']
    assert len(actual['complete_actual2205_holds']) == 2
    assert {h['frame'] for h in actual['complete_actual2205_holds']} == {6120, 6150}
    assert all(h['whole228x64_native_independent_reference_and_actual_RGB_exact'] and h['whole_current_COMMON23_resident_exactly_once'] and
        h['whole256x384_changed_pixels'] == 907 and h['every_changed_pixel_exact_old_new_native_glyph_symmetric_difference'] for h in actual['complete_actual2205_holds'])
    assert len(actual['all_other_sampled_whole_frames_exact_to_V1520']) == 43
    assert actual['every_changed_frame_and_pixel_explained_no_mask_waiver_or_retiming']
    assert actual['normal_declaration_Yes_NPC_response_A_close_battle_duel_defeat_retreat_transfer_and_return_to_sailing']
    assert actual['one40byte_prebattle_location_fixture_no_combat_actor_RNG_outcome_changes_saves_unchanged']
    fonts_path = Path(doc['native_font_proof'])
    fonts = read(fonts_path)
    assert len(fonts['cases']) == 8 and not fonts['findings']
    assert len(fonts['all207_existing_actor_choices']) == 207 and len(fonts['invalid_compiler_inputs_rejected']) == 14
    assert read(doc['visual_review'])['all1_sheet_and8_native_panels_actually_visually_reviewed']
    startup_path, shop_path = [release_path.parent / name for name in ['ordinary_startup_verification.json', 'photographed_shop_formatting.json']]
    startup, shop = read(startup_path), read(shop_path)
    assert startup['candidate_sha256'] == digest and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert startup['no_battery_save_savestate_or_fixtures'] and sha(Path(startup['review_sheet']).read_bytes()) == startup['review_sheet_sha256']
    assert shop['candidate_sha256'] == digest and all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in shop['entries'])
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    entries = current_entries(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'))
    japanese = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    rows = []
    for record in doc['records']:
        row = deepcopy(record)
        n = row['message_id']
        assert n in IDS and row['source_hex'] == japanese[n].text.hex() and all(row['review'].values())
        assert row['editorial_decision'] == 'revise' and entries[n].text == compiled(row)
        case = next(c for c in fonts['cases'] if c['message_ID'] == n)
        assert case['compiled_hex'] == entries[n].text.hex() and not case['findings']
        row.update(manuscript=str(DOC), previous_current_text_hex=row['current_text_hex'],
            current_reference={k: v for k, v in asdict(entries[n]).items() if k != 'text'},
            current_text_hex=entries[n].text.hex(), current_English=row['english'], decision='revised-and-integrated',
            status='complete-source-native-and-representative-original-NPC-response-gameplay',
            completed_candidate_reference=str(ROM), completed_candidate_sha256=digest,
            complete_native_font_proof=str(fonts_path), complete_native_font_proof_sha256=sha(fonts_path.read_bytes()),
            complete_native_formatted_lines=case['lines'], actual_holds=actual['complete_actual2205_holds'] if n == 2205 else [],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
        rows.append(row)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'], len(ledger['reviewed_but_incomplete_COMMON_IDs'])) == (1330, 1482, 152)
    assert not any(set(IDS) & set(f.get('native_message_IDs', [])) for f in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True)
    save(ROOT / 'coverage_before_completion.json', before)
    visual = ROOT / 'actual_and_startup_visual_review.json'
    save(visual, {'startup_sheet': startup['review_sheet'], 'startup_sheet_sha256': startup['review_sheet_sha256'],
        'all8_startup_panels_actually_visually_reviewed': True,
        'actual6120_6150_NPC_response6300_battle_and9200_sailing_screens_actually_visually_reviewed': True,
        'actual_font_proof': str(ACTUAL), 'actual_font_proof_sha256': sha(ACTUAL.read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    scope = ('Eight alternative NPC company-leader war responses2201-2208 are source/context/prose/native reviewed and revised. '
        'Natural American English restores2202 interception preparation,2203 resolve not to lose,2205 full personal boast and2208 reckless-decision promise; '
        '2206 explicit threat and2207 frightened plea retain their intent with ordinary ASCII I. No names,relationships,ranks,outcomes,source arguments or macros are invented. '
        'Original company leader3CD2C/table021184E0 at6F024/direct53F0C call6F02C,parent53F40/SP274 is mapped. V1530 incorrectly called6F0A4/E2838 a UI constructor; '
        'V1531 proves it is unrelated DMA and preserves an explicit erratum.207 original actor choices,all8 original selection/loader/printf/macro/post-expansion-wrap/full228x64 '
        'native/independent glyph planes,ordered edge letters,uniform6px margins,bounds/blank paper and14 compiler negatives pass. The complete8-panel sheet is actually viewed. '
        'Two source-faithful clause refinements remove final-word orphans;the initial1537 event assertion counted a zero-ink duplicate first-cell continuation guard. '
        '1537b/c explicitly prove its blank font and narrow placement without dropping any visible glyph or changing game bytes. One exact actor-table membership encodes186 of188 '
        'owned selector bytes;172-byte gate,all previous helpers/sections/BSS/cache/arena/ITCM and123040 staged bytes remain exact.529442 native selector/ABI cases plus3668 '
        'fixed-synthetic modal routing controls,238 wrong-parent5 edge140 whole-memory status controls pass;this is not3668 distinct game-text coverage.7336 whole native copies180 '
        'cache sequences13 earlier escape pipelines pass.471 batches114 accepted layers,3660 other message/copy spans,40 blocks,opaque duel prefix,routes/graphics/fonts/components '
        'are preserved. Exact clean-input patch reconstructs every ROM byte;8 ordinary fixture-free startup/title/New Game controls match reference and are viewed. '
        'Photographed shop676/677 full native planes remain exact without a fresh shop visit. One original9200-frame cold-boot encounter uses only40 prebattle own-location bytes. '
        'The normal unknown-faction Yes declaration produces actual James Clifford28/company4/voice4/2205. Two complete6120/6150 holds match full native/independent/reference/RGB '
        'planes and whole current COMMON23 residence. Every one of907 changed pixels in each full screen equals the old/new native glyph symmetric difference;all other pixels '
        'are exact.43 other sampled whole frames match V1520,including original A dismissal,battle6300,automatic duel/defeat/evacuation,completed retreat7 and normal sailing9200 '
        'with4 survivors. No combat state,actor identities/abilities/health/crew/equipment/RNG/outcomes or later position are edited;source/disposable saves remain unchanged. '
        'Only2205 is individually activated;other7 voices have full native and representative-family coverage,not individual gameplay claims. Targeted headless evidence does not '
        'prove earned travel,full routes or hardware behavior. No older32 reaction24 loss/surrender16 sinking34 aftermath38 pending entries are completed here. '
        'The separate fear/sea table2209-2216 is not merged into these war responses. V1542 remains experimental,V1492 remains explicitly promoted;global editorial/graphics goals stay open.')
    save(FINAL, {'format': 'dk4-editorial-family-final-review-v1', 'native_message_IDs': list(IDS), 'records': rows,
        'manuscript': str(DOC), 'candidate': str(ROM), 'candidate_sha256': digest, 'actual_gameplay': str(ACTUAL),
        'actual_gameplay_sha256': sha(ACTUAL.read_bytes()), 'registered_release': str(release_path),
        'registered_release_sha256': sha(release_path.read_bytes()), 'actual_verification_scope': scope,
        'completed_entries': 8, 'revised': 8, 'retained': 0, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    family, document = 'Shared-NPC-declaration-responses8', 'docs/declaration_responses_v1549_completion.md'
    ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': list(IDS), 'records': rows,
        'final_review': str(FINAL), 'documentation': document, 'actual_verification_scope': scope})
    unit = next(u for u in ledger['coverage_units'] if u['id'] == 'Shared-NPC-declaration-responses8-source-prose')
    unit.update(status='superseded-by-complete-family', completed_family=family, final_review=str(FINAL))
    ledger['coverage_units'].append({'id': family, 'status': 'complete-source-native-and-representative-original-gameplay',
        'native_message_IDs': list(IDS), 'final_review': str(FINAL), 'actual_proof': str(ACTUAL), 'full_goal_complete': False})
    ledger['records_editorially_completed'] += 8
    ledger['records_revised_and_integrated'] += 8
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] += 8
    pending = ledger['reviewed_but_incomplete_COMMON_IDs'] = [n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [n for n in drafts['native_message_IDs'] if n not in IDS]
    for name in drafts['manuscript_record_subsets_pending']:
        if 'declaration_responses_editorial_manuscript' in name:
            drafts['manuscript_record_subsets_pending'][name] = []
    drafts.update(status='32-reactions24-loss-surrender16-sinking34-aftermath38-older-reviewed-entries-open',
        note='War8 complete in V1542. Earlier144 reviewed COMMON entries,broader shared/routes/raw prose and separate graphics audit remain unfinished.')
    ledger['current_native_relocation_reference'].update(candidate=str(ROM), candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'], ARM9_sha256=release['ARM9_sha256'],
        parser='dk4tool.patch.declaration_responses_editorial.current_entries', release_config='translations/declaration_responses_editorial_release_v1.json',
        NPC_declaration_response8_source_native_and_representative_gameplay_complete=True)
    ledger['latest_registered_declaration_responses_candidate'] = {**release,
        'status': 'experimental-war8-source-native-and-representative-gameplay-complete', 'final_review': str(FINAL),
        'actual_proof': str(ACTUAL), 'completed_entries_added': 8, 'full_goal_complete': False}
    ledger['formatting_watchlist']['NPC_declaration_responses8'].update(status='completed-in-V1542', final_review=str(FINAL),
        registered_release_and_revised_original_event_pending=False, actual_proof=str(ACTUAL), individually_activated_original_ID=2205)
    ledger['formatting_watchlist']['latest_reference_proof'] = str(shop_path)
    ledger['formatting_watchlist']['latest_photographed_shop_recheck'] = {'checkpoint': 'V1549', 'candidate': str(ROM),
        'candidate_sha256': digest, 'proof': str(shop_path), 'result': 'Exact repaired676/677 full native planes pass;no new shop activation.', 'global_formatting_audit_complete': False}
    summary = ('V1549 completes8 NPC declaration responses2201-2208,all revised,in registered V1542. '
        'Counts1338 complete(1000 revised338 retained),1482 source/prose;144 reviewed-incomplete COMMON(32 reactions24 loss/surrender16 sinking34 aftermath38 older), '
        'plus broader shared/routes/raw prose. Full source intent restored,ordinary ASCII I/all8 full glyph planes/207 actor choices/14 compiler negatives and viewed8-panel sheet pass. '
        '529442 dispatch/ABI cases,7336 copies180 cache13 escape regressions pass;186/188 selector,172-byte gate and123040 staged bytes unchanged. '
        'Exact clean patch,471 batches114 accepted layers,3660 other messages/copies,40 blocks and all prior routes/graphics/fonts/helpers preserved. '
        'All8 startup frames match and are viewed;shop676/677 retained. Original James Clifford28/voice4/2205 has2 complete6120/6150 native/reference/RGB holds, '
        'each differs at exactly907 predicted native letter pixels;43 other whole V1520 frames exact. Normal declaration,A close,battle,duel/defeat,retreat7/transfer/sailing9200 '
        'with4 survivors and one40byte prebattle location fixture audited;no combat/actor/RNG/outcome/later position edits,saves unchanged. '
        'V1530 DMA label and1537 zero-ink guard assumptions are corrected explicitly with frozen failures retained. Only2205 individually activated;other7 voices have full native/family proof. '
        'V1542 experimental,V1492 promoted,canonical/V997 unchanged;separate graphics/all18 plaques and later older-record re-audit remain open;goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id': 'V1549-NPC-war8-complete', 'proof': str(FINAL), 'actual': str(ACTUAL),
        'completed_entries_added': 8, 'source_prose_reviews_added': 0, 'full_goal_complete': False})
    complete = [n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs', [])]
    assert len(complete) == len(set(complete)) == 1337
    assert len(pending) == len(set(pending)) == len(drafts['native_message_IDs']) == 144
    assert not set(complete) & set(pending) and len(set(complete) | set(pending)) == 1481
    assert ledger['records_editorially_completed'] == ledger['records_revised_and_integrated'] + ledger['retained_wordings_editorially_completed'] == 1338
    assert sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1338
    for k in ['records_with_source_and_prose_pass', 'records_with_source_prose_drafts', 'source_prose_reviewed_counts_by_file',
        'current_integrated_candidate', 'source_pins', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal', 'raw_source_coverage_revisit']:
        assert ledger[k] == before[k], k
    save(ledger_path, ledger)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    pin = 'E:/Rota Nova translations/Generated/out/all_routes_combined_v1542_candidate.nds'
    assert not any(p['path'] == pin for p in pins)
    pins.append({'path': pin, 'reason': 'Completed NPC war8 source/native/original response and current native COMMON parent;preserve all earlier layers for remaining editorial work.'})
    save(pins_path, pins)
    GUIDE.mkdir(parents=True)
    screenshots = []
    for name, frame in [('NPC_declaration_response', 6150), ('ordinary_battle_after_response', 6300), ('ordinary_sailing_after_retreat', 9200)]:
        source = Path('E:/Rota Nova translations/Generated/work/emulation_v193/declaration_responses_v1546_1542') / f'frame_{frame:06d}_navigation.png'
        target = GUIDE / (name + '.png')
        copy2(source, target)
        assert sha(target.read_bytes()) == sha(source.read_bytes())
        screenshots.append({'path': str(target), 'source': str(source), 'frame': frame, 'sha256': sha(target.read_bytes())})
    save(GUIDE / 'provenance.json', {'candidate_sha256': digest, 'screenshots': screenshots,
        'actual_verification': str(ACTUAL), 'sole40byte_prebattle_location_fixture_disclosed': True,
        'not_earned_travel_full_route_or_individual_other_voice_activation': True, 'full_goal_complete': False})
    Path(document).write_text('# V1549 eight NPC declaration responses complete\n\n' + summary + '\n\n## Exact experimental release\n\n'
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1542_candidate.nds`;SHA-256 `' + digest + '`.\n'
        '- Canonical base: `out/raphael_natural_v2_accepted_base.nds`;SHA-256 `' + release['canonical_sha256'] + '`.\n'
        '- Profile: `all-routes-unified-v1542`;471 manifest batches114 accepted layers.\n'
        '- Only COMMON23/eight paragraphs,original ARM9 offset/directory metadata and the existing188-byte selector span change versus V1520;172-byte gate exact.\n'
        '- Patch: `' + release['patch'] + '`;SHA-256 `' + release['patch_sha256'] + '`;clean input `' + release['clean_input_sha256'] + '`.\n'
        '- Checks: runtime1536,fonts1537c,copies1538,escape1539,release1543,startup1544,original replay1547,actual fonts1547b,shop1548.\n'
        '- V1542 experimental;V1492 remains promoted. User cold-boot testing may cover title/New Game,declaration confirmation,the NPC response and entry into battle.\n\n'
        '## Evidence scope\n\n' + scope + '\n\nFinal review: `' + str(FINAL) + '`. Guide screenshots: `' + str(GUIDE) + '`.\n', encoding='utf-8')
    for name in ['translation_progress.md', 'known_issues.md', 'todo.md', 'editorial_review_goal.md']:
        with (Path('docs') / name).open('a', encoding='utf-8', newline='\n') as f:
            f.write('\n\n## V1549 NPC war8 complete\n\n' + summary + '\n\nSee [completion](declaration_responses_v1549_completion.md).\n')
    save(ROOT / 'completion_receipt.json', {'completed': 1338, 'revised': 1000, 'retained': 338, 'source_prose': 1482,
        'newly_completed': 8, 'unique_complete_COMMON': 1337, 'reviewed_incomplete_COMMON': 144,
        'final_review': str(FINAL), 'final_review_sha256': sha(FINAL.read_bytes()), 'candidate_sha256': digest,
        'actual_proof': str(ACTUAL), 'visual_review': str(visual), 'guide_screenshots': screenshots,
        'V1492_promoted_canonical_and_V997_unchanged_global_goal_active': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('War8 complete:1338 complete/1482 reviewed;144 reviewed COMMON entries and broader prose/graphics remain open.')
