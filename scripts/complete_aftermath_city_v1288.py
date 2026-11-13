"""Close only eight source/native-reviewed city-defense voice alternatives."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/aftermath_city_completion_v1288')
ACTUAL = Path('work/analysis/aftermath_city_verified_v1287/actual_city_defense_verification.json')
FINAL = Path('translations/battle_aftermath_city_defense_final_review_v1.json')
ROM = Path('out/all_routes_combined_v1266_candidate.nds')
IDS = tuple(range(2038, 2046))


def main():
    assert not ROOT.exists() and not FINAL.exists()
    actual, digest = read(ACTUAL), sha(ROM.read_bytes())
    assert actual['candidate_sha256'] == digest and actual['terminal_frame'] == 6940
    assert len(actual['complete_actual_holds']) == 2
    assert {h['message_ID'] for h in actual['complete_actual_holds']} == {2043}
    assert all(h['missing_or_unexpected_foreground_pixels'] == 0 for h in actual['complete_actual_holds'])
    assert actual['no_diplomacy_health_actor_ID_eligibility_result_RNG_or_message_injection']
    assert actual['normal_A_dismissal_enters_original_defender_fleet_battle_without_extra_page']
    release_path = Path('work/analysis/battle_aftermath_release_v1265/registered_release_verification.json')
    release, manifest = read(release_path), read(ROM.with_suffix('.manifest.json'))
    assert release['candidate_sha256'] == manifest['candidate_sha256'] == digest and release['complete_reconstruction_byte_exact']
    manuscript = Path('translations/battle_aftermath_editorial_manuscript_v3.json')
    doc = read(manuscript)
    font_path = Path(doc['native_font_proof'])
    font = read(font_path)
    rom = NdsImage.open(ROM)
    entries = current_entries(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'))
    selected = [deepcopy(row) for row in doc['records'] if row['message_id'] in IDS]
    assert tuple(row['message_id'] for row in selected) == IDS
    revised = sum(row['editorial_decision'] == 'revise' for row in selected)
    retained = sum(row['editorial_decision'] == 'retain' for row in selected)
    assert (revised, retained) == (7, 1)
    for row in selected:
        number = row['message_id']
        case = next(case for case in font['cases'] if case['message_id'] == number and case['name_case'] is None)
        assert entries[number].text == compiled(row) and all(row['review'].values())
        row.update(before_reference=deepcopy(row['current_reference']), before_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[number]).items() if k != 'text'},
            current_text_hex=entries[number].text.hex(), current_English=row['english'],
            decision='revised-and-integrated' if row['editorial_decision'] == 'revise' else 'retained-after-source-review',
            status='complete-with-source-native-and-representative-original-city-defense-gameplay',
            completed_candidate_reference=str(ROM), completed_candidate_sha256=digest,
            complete_native_font_proof=str(font_path), complete_native_font_proof_sha256=sha(font_path.read_bytes()),
            complete_native_formatted_lines=case['lines'],
            actual_holds=[hold for hold in actual['complete_actual_holds'] if hold['message_ID'] == number],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
    scope = ('All8 city-defense alternatives2038-2045 have clean Japanese,original defending-captain/table context,faithful natural English and complete native speech/font review. Original target controls select Madeira,show the native attack confirmation,and the unchanged6ED34 presence/company/share checks and unforced519D4(3) choice select existing fleet22,Paulo Morais46. Original direct parent53F40/table178C0 selects2043. Two complete228x64 font/RGB holds match all696 foreground pixels,blank paper,wrapped bytes and every first/final letter. Normal A dismissal enters original defender-fleet battle mode[0,1,22] without another page. The sole frame5000 fixture changes only16 owned bytes of the own ships cached/live location;the whole4MiB replay preserves diplomacy,actors and IDs,defender,towns,defenses,shares,health,RNG and events. Subsequent discovery,docking,resupply,departure,target selection and conflict are original gameplay/input. Source/disposable saves remain exact. Only2043 has individual actual activation;the other7 have representative source-family coverage. No town surrender or battle outcome is claimed. Targeted headless testing is not earned travel,full-route or hardware verification.')
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass']) == (1280, 1373)
    assert not any(set(IDS).intersection(f.get('native_message_IDs', [])) for f in ledger['completed_editorial_families'])
    assert set(IDS) <= set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_completion.json', before)
    save(FINAL, {'format':'dk4-editorial-family-final-review-v1', 'native_message_IDs':list(IDS),
        'manuscript':str(manuscript), 'manuscript_sha256':sha(manuscript.read_bytes()), 'records':selected,
        'candidate':str(ROM), 'candidate_sha256':digest, 'actual_gameplay':str(ACTUAL),
        'actual_gameplay_sha256':sha(ACTUAL.read_bytes()), 'registered_release':str(release_path),
        'registered_release_sha256':sha(release_path.read_bytes()), 'actual_verification_scope':scope,
        'completed_entries':8, 'revised':7, 'retained':1, 'other47_aftermath_records_incomplete':True,
        'producer_sha256':sha(Path(__file__).read_bytes()), 'full_goal_complete':False})
    family_id = 'Shared-aftermath-city-defense'
    documentation = 'docs/aftermath_city_v1288_completion.md'
    ledger['completed_editorial_families'].append({'id':family_id, 'native_message_IDs':list(IDS),
        'records':selected, 'final_review':str(FINAL), 'documentation':documentation, 'actual_verification_scope':scope})
    assert family_id not in {unit['id'] for unit in ledger['coverage_units']}
    ledger['coverage_units'].append({'id':family_id, 'status':'complete-with-source-native-and-representative-gameplay-evidence',
        'native_message_IDs':list(IDS), 'final_review':str(FINAL), 'actual_proof':str(ACTUAL), 'full_goal_complete':False})
    ledger['records_editorially_completed'] += 8
    ledger['records_revised_and_integrated'] += revised
    ledger['retained_wordings_editorially_completed'] += retained
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] += 8
    done = set(IDS)
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [n for n in drafts['native_message_IDs'] if n not in done]
    for name, values in drafts['manuscript_record_subsets_pending'].items():
        if name.replace('\\', '/') == manuscript.as_posix():
            drafts['manuscript_record_subsets_pending'][name] = [n for n in values if n not in done]
            assert len(drafts['manuscript_record_subsets_pending'][name]) == 47
    ledger['reviewed_but_incomplete_COMMON_IDs'] = [n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in done]
    drafts['status'] = '47-aftermath-and38-older-reviewed-entries-open'
    drafts['note'] = '28 aftermath alternatives complete through original fled-victory,crew-abandonment,flagship-loss and city-defense samples. Other47 require their own original source-family scenes/transitions. Older38 and broader unreviewed shared/routes/raw inventory remain open.'
    reference = ledger['current_native_relocation_reference']
    reference.pop('75_source_native_approved20_family_records_complete55_pending')
    reference['75_source_native_approved28_family_records_complete47_pending'] = True
    ledger['latest_registered_aftermath_candidate']['status'] = 'experimental-28-aftermath-complete47-original-scenes-pending'
    ledger['latest_registered_aftermath_candidate']['latest_actual_proof'] = str(ACTUAL)
    summary = ('V1288 completes8 city-defense alternatives2038-2045:7 revised1 retained. Counts1288 complete(960 revised328 retained),1373 source/prose. Registered V1266 now has28 of75 aftermath entries complete through representative original family scenes;47 aftermath plus38 older reviewed COMMON entries remain incomplete,alongside broader unreviewed shared/routes/raw prose. Actual2043 from existing defender Paulo Morais46 has two exact full native font/RGB holds(696 ink pixels each),uniform margins,complete letters and original A-dismissal to battle mode[0,1,22]. The sole16-byte location fixture is replayed across the entire4MiB;diplomacy,actors,defender,health,defenses,shares,RNG and events remain unchanged. Discovery,docking,resupply,departure and city attack use original controls;no outcome or town surrender is claimed. Source/disposable saves unchanged. Same registered V1266 ROM/exact patch;no ROM build or allocation change. Earlier shop676/677 formatting remains a regression reference. Canonical,V997,separate graphics/all18 plaques,older-record revisit and the full editorial goal remain unchanged/open.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1288-city-defense8-completion', 'proof':str(FINAL),
        'actual':str(ACTUAL), 'completed_entries_added':8, 'source_prose_reviews_added':0, 'full_goal_complete':False})
    complete = [n for family in ledger['completed_editorial_families'] for n in family.get('native_message_IDs', [])]
    pending = ledger['reviewed_but_incomplete_COMMON_IDs']
    assert len(complete) == len(set(complete)) == 1287
    assert len(pending) == len(set(pending)) == len(drafts['native_message_IDs']) == 85
    assert not set(complete).intersection(pending) and len(set(complete)|set(pending)) == 1372
    assert ledger['records_editorially_completed'] == ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed'] == 1288
    assert sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1288
    for key in ['current_integrated_candidate', 'source_pins', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal', 'raw_source_coverage_revisit']:
        assert ledger[key] == before[key], key
    save(ledger_path, ledger)
    Path(documentation).write_text('# V1288: original city-defense verification\n\n'+summary+'\n\n## Actual scope\n\n'+scope+
        '\n\nFinal review: `'+str(FINAL)+'`. Actual proof: `'+str(ACTUAL)+'`. Exact release details: [V1273](aftermath_fled_v1273_completion.md). Guide screenshots: `E:/Rota Nova translations/Guide screenshots/V1266 City defense`.\n\n## Uncredited research and corrections\n\n'+
        'V1281 navigation and V1283b early-war pilots ended normally with preserved donors;they receive no additional translation completion credit. V1283b entered an automatic sea battle,whose Info Mode lacks the Search/Declare controls. V1286 retains neutral diplomacy and demonstrates the original Info/Search/Declare War cycle before attacking Madeira. V1284 used the wrong position-query ABI in a disposable CPU copy;its geometry fields are invalid. V1284b failed a source guard before querying. V1284c uses the proven output-buffer ABI and separates localized menu words from clean code. None of these research queries changed the emulator.\n\n'+
        'The V1280 zero-B3FD4 leads are supplemental town indices90-113 with no market shares;they are not proven eligible city targets. Original town surrender/report/white flag,enemy flagship destroyed/captured,own flooding,ship surrender and withdrawal still need their distinct scene evidence. No completion credit is inferred from the city-defense sample.\n', encoding='utf-8')
    for name in ['translation_progress.md', 'known_issues.md', 'todo.md', 'editorial_review_goal.md']:
        with (Path('docs')/name).open('a', encoding='utf-8', newline='\n') as handle:
            handle.write('\n\n## V1288 city-defense family completed\n\n'+summary+'\n\nSee [evidence](aftermath_city_v1288_completion.md).\n')
    save(ROOT/'completion_receipt.json', {'final_review':str(FINAL), 'final_review_sha256':sha(FINAL.read_bytes()),
        'completed':1288, 'revised':960, 'retained':328, 'source_prose':1373, 'newly_completed':8,
        'unique_complete_COMMON':1287, 'reviewed_incomplete_COMMON':85, 'remaining_aftermath':47,
        'no_duplicate_source_or_completion_credit':True, 'coverage_unit_registered':True,
        'candidate_sha256':digest, 'global_goal_active':True, 'producer_sha256':sha(Path(__file__).read_bytes()), 'full_goal_complete':False})
    print('8 city-defense alternatives complete:1288 total;47 aftermath+38 older reviewed COMMON remain open.', flush=True)


if __name__ == '__main__':
    main()
