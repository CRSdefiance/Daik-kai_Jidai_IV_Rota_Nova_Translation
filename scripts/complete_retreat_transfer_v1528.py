"""Close retreat7 only after source/native/registered/original gameplay gates."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.retreat_transfer_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.retreat_transfer_native_plan_v1514 import compiled, IDS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/retreat_transfer_completion_v1528')
ROM = Path('out/all_routes_combined_v1520_candidate.nds')
MANUSCRIPT = Path('translations/retreat_transfer_editorial_manuscript_v3.json')
FINAL = Path('translations/retreat_transfer_final_review_v1.json')
ACTUAL = Path('work/analysis/retreat_transfer_actual_fonts_v1526c/actual_retreat_font_and_transition_verification.json')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1520 Flagship evacuation and transfer')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not GUIDE.exists()
    release_path = Path('work/analysis/retreat_transfer_release_v1519/registered_release_verification.json')
    release, actual, doc = read(release_path), read(ACTUAL), read(MANUSCRIPT)
    pixel_path = Path('work/analysis/retreat_transfer_actual_pixels_v1526d/all_changed_pixels_explained.json')
    pixels = read(pixel_path)
    digest = sha(ROM.read_bytes())
    assert digest == release['candidate_sha256'] == actual['candidate_sha256'] == pixels['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and release['actual_changed_message_IDs'] == list(IDS)
    assert release['all471_batches114_accepted_layers_and_prior_profiles_preserved']
    assert len(actual['complete_actual2684_holds']) == 3
    assert all(h['entire228x64_native_independent_reference_and_actual_RGB_exact'] and h['actual_current_COMMON28_resident_exactly_once'] for h in actual['complete_actual2684_holds'])
    assert len(actual['all_other_sampled_whole_frames_exact_to_V1492']) == 42
    assert actual['original_declaration_damage_auto_duel_defeat_evacuation_flagship_loss_transfer_A_dismissal_and_sailing_return']
    assert actual['one40byte_prebattle_location_fixture_no_later_mutations_and_saves_unchanged']
    assert len(pixels['all3_whole_screen_text_changes']) == 3 and pixels['no_mask_pixel_waiver_or_retiming']
    assert all(r['whole256x384_changed_RGB_pixels'] == 278 and r['every_changed_pixel_exactly_the_old_new_native_glyph_symmetric_difference'] for r in pixels['all3_whole_screen_text_changes'])
    fonts_path = Path(doc['native_font_proof'])
    fonts = read(fonts_path)
    assert len(fonts['cases']) == 208 and not fonts['findings']
    assert len(fonts['all206_source_existing_actor_choices']) == 206 and len(fonts['invalid_compiler_inputs_rejected']) == 15
    assert read(doc['visual_review'])['all8_sheets_and64_native_panels_actually_visually_reviewed']
    startup_path = release_path.parent / 'ordinary_startup_verification.json'
    startup = read(startup_path)
    assert startup['candidate_sha256'] == digest and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert startup['no_battery_save_savestate_or_fixtures'] and sha(Path(startup['review_sheet']).read_bytes()) == startup['review_sheet_sha256']
    shop_path = release_path.parent / 'photographed_shop_formatting.json'
    shop = read(shop_path)
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
        cases = [c for c in fonts['cases'] if c['message_ID'] == n]
        assert len(cases) == (52 if n == 2683 else 26)
        assert all(c['compiled_hex'] == entries[n].text.hex() and not c['findings'] for c in cases)
        row.update(manuscript=str(MANUSCRIPT), previous_current_text_hex=row['current_text_hex'],
            current_reference={k: v for k, v in asdict(entries[n]).items() if k != 'text'},
            current_text_hex=entries[n].text.hex(), current_English=row['english'], decision='revised-and-integrated',
            status='complete-source-native-and-representative-original-transfer-gameplay',
            completed_candidate_reference=str(ROM), completed_candidate_sha256=digest,
            complete_native_font_proof=str(fonts_path), complete_native_font_proof_sha256=sha(fonts_path.read_bytes()),
            complete_native_formatted_lines=next(c for c in cases if c['variant'] == 0)['lines'],
            actual_holds=actual['complete_actual2684_holds'] if n == 2684 else [],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
        rows.append(row)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'], len(ledger['reviewed_but_incomplete_COMMON_IDs'])) == (1323, 1474, 151)
    assert not any(set(IDS) & set(f.get('native_message_IDs', [])) for f in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True)
    save(ROOT / 'coverage_before_completion.json', before)
    visual = ROOT / 'actual_and_startup_visual_review.json'
    save(visual, {'startup_sheet': startup['review_sheet'], 'startup_sheet_sha256': startup['review_sheet_sha256'],
        'all8_startup_panels_actually_visually_reviewed': True,
        'actual8750_8800_8850_retreat_and9200_sailing_screens_actually_visually_reviewed': True,
        'actual_font_proof': str(ACTUAL), 'actual_font_proof_sha256': sha(ACTUAL.read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    scope = ('Seven mutually exclusive Japanese retreat reports2683-2689 preserve flagship incapacitation and a named replacement ship, '
        'not sinking/death/a port/whole-fleet destruction. All7 natural American English paragraphs are revised and authored without layout. '
        'Original role1/53D44/parent53DB8/SP27C/table02117080 receives one ship virtual-name argument;voice3 negative member falls back to2683. '
        'One exact membership protects literal runtime names before post-macro wrapping.186/188 selector bytes and the172-byte gate, '
        'all earlier helpers/sections/BSS/cache/arena/ITCM and123040 staged bytes remain exact.529429 native dispatch/ABI cases and inherited '
        '3668 fixed-synthetic modal routing,238 wrong-parent5 edge140 whole-memory status controls pass;this is not3668 distinct game-text coverage. '
        '208 full original role/printf/macro/wrap/native/independent font planes across8 voices26 names,206 existing actor choices,15 negative '
        'compiler cases,7336 complete copies180 cache sequences13 earlier escape paths pass. All8 sheets64 panels actually viewed;complete '
        'names/edge letters/uniform6px margins/bounds/blank paper pass.471 batches114 accepted layers,3661 other messages/copies,40 blocks, '
        'opaque duel prefix,routes/graphics/fonts/components preserved. Exact clean-input patch reconstructs every ROM byte. '
        'All8 fixture-free startup/title/New Game controls match reference and are viewed;shop676/677 full native planes pass without a fresh shop visit. '
        'One original9200-frame cold-boot encounter uses only40 prebattle own-position bytes. Normal unknown-faction war declaration,damage, '
        'automatic duel,defeat,evacuation,flagship loss,ship transfer,A dismissal and return to sailing with4 survivors are audited. '
        'Original logical first mate Gerhard16/voice1/table selects2684;actual replacement virtual name is Latina. Three complete8750/8800/8850 '
        'native/independent/reference/RGB planes pass with whole current COMMON28 residence. Each whole screen differs from V1492 at exactly278 '
        'old/new native glyph symmetric-difference pixels,all other pixels unchanged;42 other sampled whole screens including9000/9200 match V1492. '
        'No actor identities/abilities/HP/crew/equipment/RNG/outcomes or later battle state are edited;source/disposable saves unchanged. '
        'Only2684 is individually activated;other6 templates/voice3 fallback have complete native and representative-family evidence. '
        '1526 confused a physical slot with a logical role;1526b incorrectly classified8750 as an unchanged control. Both failed producers are '
        'retained;1526c uses the proper logical accessor and verifies all3 complete holds,1526d explains every changed pixel. '
        'These corrections do not require a new emulator run or game-byte change. Targeted headless checks do not prove earned travel,full routes '
        'or hardware behavior. No completion credit is given to older32 reactions24 loss/surrender16 sinking34 aftermath38 reviewed entries. '
        'V1520 remains experimental;V1492 remains the explicitly promoted checkpoint.')
    save(FINAL, {'format': 'dk4-editorial-family-final-review-v1', 'native_message_IDs': list(IDS), 'records': rows,
        'manuscript': str(MANUSCRIPT), 'candidate': str(ROM), 'candidate_sha256': digest,
        'actual_gameplay': str(ACTUAL), 'actual_gameplay_sha256': sha(ACTUAL.read_bytes()),
        'exact_actual_pixel_proof': str(pixel_path), 'exact_actual_pixel_proof_sha256': sha(pixel_path.read_bytes()),
        'registered_release': str(release_path), 'registered_release_sha256': sha(release_path.read_bytes()),
        'actual_verification_scope': scope, 'completed_entries': 7, 'revised': 7, 'retained': 0,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    family, document = 'Shared-replacement-ship-retreat7', 'docs/retreat_transfer_v1528_completion.md'
    ledger['completed_editorial_families'].append({'id': family, 'native_message_IDs': list(IDS), 'records': rows,
        'final_review': str(FINAL), 'documentation': document, 'actual_verification_scope': scope})
    unit = next(u for u in ledger['coverage_units'] if u['id'] == 'Shared-retreat-transfer7-source-prose')
    unit.update(status='superseded-by-complete-family', completed_family=family, final_review=str(FINAL))
    ledger['coverage_units'].append({'id': family, 'status': 'complete-source-native-and-representative-original-gameplay',
        'native_message_IDs': list(IDS), 'final_review': str(FINAL), 'actual_proof': str(ACTUAL), 'full_goal_complete': False})
    ledger['records_editorially_completed'] += 7
    ledger['records_revised_and_integrated'] += 7
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] += 7
    pending = ledger['reviewed_but_incomplete_COMMON_IDs'] = [n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [n for n in drafts['native_message_IDs'] if n not in IDS]
    for name in drafts['manuscript_record_subsets_pending']:
        if 'retreat_transfer_editorial_manuscript' in name:
            drafts['manuscript_record_subsets_pending'][name] = []
    drafts.update(status='32-reactions24-loss-surrender16-sinking34-aftermath38-older-reviewed-entries-open',
        note='Retreat7 complete in V1520. Earlier144 reviewed COMMON entries, broader shared/routes/raw prose and separate graphics audit remain unfinished.')
    ledger['current_native_relocation_reference'].update(candidate=str(ROM), candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'], ARM9_sha256=release['ARM9_sha256'],
        parser='dk4tool.patch.retreat_transfer_editorial.current_entries', release_config='translations/retreat_transfer_editorial_release_v1.json',
        replacement_ship_retreat7_source_native_and_representative_gameplay_complete=True)
    ledger['latest_registered_retreat_transfer_candidate'] = {**release,
        'status': 'experimental-retreat7-source-native-and-representative-gameplay-complete',
        'final_review': str(FINAL), 'actual_proof': str(ACTUAL), 'completed_entries_added': 7, 'full_goal_complete': False}
    ledger['formatting_watchlist']['retreat_transfer7'].update(status='completed-in-V1520', final_review=str(FINAL),
        registered_release_pending=False, original_transfer_replay_pending=False, actual_proof=str(ACTUAL),
        actual_pixel_proof=str(pixel_path), original_gameplay_individually_activated_ID=2684)
    ledger['formatting_watchlist']['latest_reference_proof'] = str(shop_path)
    ledger['formatting_watchlist']['latest_photographed_shop_recheck'] = {'checkpoint': 'V1528', 'candidate': str(ROM),
        'candidate_sha256': digest, 'proof': str(shop_path), 'result': 'Exact repaired676/677 full native planes pass;no new shop activation.', 'global_formatting_audit_complete': False}
    summary = ('V1528 completes seven replacement-ship retreat notices2683-2689,all revised,in registered V1520. '
        'Counts1330 complete(992 revised338 retained),1474 source/prose;144 reviewed-incomplete COMMON(32 reactions24 loss/surrender16 sinking34 aftermath38 older), '
        'plus broader shared/routes/raw prose. Literal names,all208 native full font planes/64 viewed panels,529429 dispatch cases,7336 copies180 cache13 escapes pass. '
        'Exact clean patch,471 batches114 accepted layers,3661 other messages,40 blocks,all prior routes/graphics/fonts/helpers and123040 staged bytes preserved. '
        'All8 ordinary startup frames match and are viewed;shop676/677 repairs retained. Original Gerhard16/voice1/2684/Latina transfer has3 complete native/reference/RGB holds; '
        'each differs at exactly278 predicted letter pixels,42 other whole frames exact to V1492. Normal declaration,battle,duel loss,evacuation,transfer,A dismissal,sailing9200 '
        'with4 survivors and one40byte prebattle location fixture are audited;no later combat/actor/RNG/result changes,saves unchanged. '
        'Failed1526 physical-slot and1526b early-hold assumptions are retained and corrected without rerunning gameplay or changing game bytes. '
        'Only2684 individually activated;other voices have complete native and representative-family proof. V1520 experimental,V1492 promoted,canonical/V997 unchanged; '
        'separate graphics/all18 plaques and later older-record re-audit remain open;goal active.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id': 'V1528-retreat7-complete', 'proof': str(FINAL), 'actual': str(ACTUAL),
        'completed_entries_added': 7, 'source_prose_reviews_added': 0, 'full_goal_complete': False})
    complete = [n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs', [])]
    assert len(complete) == len(set(complete)) == 1329
    assert len(pending) == len(set(pending)) == len(drafts['native_message_IDs']) == 144
    assert not set(complete) & set(pending) and len(set(complete) | set(pending)) == 1473
    assert ledger['records_editorially_completed'] == ledger['records_revised_and_integrated'] + ledger['retained_wordings_editorially_completed'] == 1330
    assert sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1330
    for key in ['records_with_source_and_prose_pass', 'records_with_source_prose_drafts', 'source_prose_reviewed_counts_by_file',
        'current_integrated_candidate', 'source_pins', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal', 'raw_source_coverage_revisit']:
        assert ledger[key] == before[key], key
    save(ledger_path, ledger)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    pin = 'E:/Rota Nova translations/Generated/out/all_routes_combined_v1520_candidate.nds'
    assert not any(p['path'] == pin for p in pins)
    pins.append({'path': pin, 'reason': 'Completed retreat7 source/native/original transfer and current native COMMON parent; preserve all V1492 layers for broader editorial work.'})
    save(pins_path, pins)
    GUIDE.mkdir(parents=True)
    screenshots = []
    for name, frame in [('flagship_retreat_to_replacement_ship', 8850), ('ordinary_sailing_with_surviving_ships', 9200)]:
        source = Path('E:/Rota Nova translations/Generated/work/emulation_v193/retreat_transfer_v1524_1520') / f'frame_{frame:06d}_navigation.png'
        target = GUIDE / (name + '.png')
        copy2(source, target)
        assert sha(target.read_bytes()) == sha(source.read_bytes())
        screenshots.append({'path': str(target), 'source': str(source), 'frame': frame, 'sha256': sha(target.read_bytes())})
    save(GUIDE / 'provenance.json', {'candidate_sha256': digest, 'screenshots': screenshots,
        'actual_verification': str(ACTUAL), 'sole40byte_prebattle_location_fixture_disclosed': True,
        'not_earned_travel_or_individual_other_voice_activation': True, 'full_goal_complete': False})
    Path(document).write_text('# V1528 seven retreat notices complete\n\n' + summary + '\n\n## Exact experimental release\n\n'
        '- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1520_candidate.nds`; SHA-256 `' + digest + '`.\n'
        '- Canonical base: `out/raphael_natural_v2_accepted_base.nds`; SHA-256 `' + release['canonical_sha256'] + '`.\n'
        '- Profile: `all-routes-unified-v1520`;471 manifest batches114 accepted layers.\n'
        '- Only COMMON28/seven paragraphs, original ARM9 offset/directory metadata and the existing188-byte selector span change versus V1492;172-byte gate exact.\n'
        '- Patch: `' + release['patch'] + '`; SHA-256 `' + release['patch_sha256'] + '`;clean input `' + release['clean_input_sha256'] + '`.\n'
        '- Checks: runtime1510,fonts1515,copies1516,escape1517,release1521,startup1522,original replay1525,fonts1526c,whole pixels1526d,shop1527.\n'
        '- V1520 experimental; V1492 remains promoted. User cold-boot testing may cover title/New Game,retreat after flagship loss and custom ship names.\n\n'
        '## Evidence scope\n\n' + scope + '\n\nFinal review: `' + str(FINAL) + '`. Guide screenshots: `' + str(GUIDE) + '`.\n', encoding='utf-8')
    for name in ['translation_progress.md', 'known_issues.md', 'todo.md', 'editorial_review_goal.md']:
        with (Path('docs') / name).open('a', encoding='utf-8', newline='\n') as f:
            f.write('\n\n## V1528 retreat7 complete\n\n' + summary + '\n\nSee [completion](retreat_transfer_v1528_completion.md).\n')
    save(ROOT / 'completion_receipt.json', {'completed': 1330, 'revised': 992, 'retained': 338, 'source_prose': 1474,
        'newly_completed': 7, 'unique_complete_COMMON': 1329, 'reviewed_incomplete_COMMON': 144,
        'final_review': str(FINAL), 'final_review_sha256': sha(FINAL.read_bytes()), 'candidate_sha256': digest,
        'actual_proof': str(ACTUAL), 'visual_review': str(visual), 'guide_screenshots': screenshots,
        'V1492_promoted_canonical_and_V997_unchanged_global_goal_active': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Retreat7 complete:1330 complete/1474 reviewed;144 reviewed COMMON entries and broader prose/graphics remain open.')
