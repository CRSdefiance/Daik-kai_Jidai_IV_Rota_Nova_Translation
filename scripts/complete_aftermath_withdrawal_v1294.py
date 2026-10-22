"""Record exact completion of eight withdrawal alternatives; keep other work open."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/aftermath_withdrawal_completion_v1294')
ACTUAL = Path('work/analysis/aftermath_withdrawal_verified_v1293/actual_withdrawal_verification.json')
FINAL = Path('translations/battle_aftermath_withdrawal_final_review_v1.json')
ROM = Path('out/all_routes_combined_v1266_candidate.nds')
IDS = tuple(range(2114,2122))


def main():
    assert not ROOT.exists() and not FINAL.exists()
    actual, digest = read(ACTUAL), sha(ROM.read_bytes())
    assert actual['candidate_sha256'] == digest and actual['terminal_frame'] == 7510
    assert len(actual['complete_actual_holds']) == 2
    assert {h['message_ID'] for h in actual['complete_actual_holds']} == {2114}
    assert all(h['missing_or_unexpected_foreground_pixels'] == 0 for h in actual['complete_actual_holds'])
    assert actual['normal_A_dismissal_clears_battle_and_town_ID_and_returns_to_ordinary_sailing']
    release_path = Path('work/analysis/battle_aftermath_release_v1265/registered_release_verification.json')
    release = read(release_path)
    assert release['candidate_sha256'] == read(ROM.with_suffix('.manifest.json'))['candidate_sha256'] == digest
    assert release['complete_reconstruction_byte_exact']
    manuscript = Path('translations/battle_aftermath_editorial_manuscript_v3.json')
    doc = read(manuscript)
    font_path = Path(doc['native_font_proof'])
    font = read(font_path)
    rom = NdsImage.open(ROM)
    entries = current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'))
    selected = [deepcopy(row) for row in doc['records'] if row['message_id'] in IDS]
    assert tuple(row['message_id'] for row in selected) == IDS
    assert sum(row['editorial_decision'] == 'revise' for row in selected) == 4
    assert sum(row['editorial_decision'] == 'retain' for row in selected) == 4
    for row in selected:
        number = row['message_id']
        case = next(case for case in font['cases'] if case['message_id'] == number and case['name_case'] is None)
        assert entries[number].text == compiled(row) and all(row['review'].values())
        row.update(before_reference=deepcopy(row['current_reference']),before_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[number]).items() if k != 'text'},
            current_text_hex=entries[number].text.hex(),current_English=row['english'],
            decision='revised-and-integrated' if row['editorial_decision'] == 'revise' else 'retained-after-source-review',
            status='complete-with-source-native-and-representative-original-withdrawal-gameplay',
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            complete_native_font_proof=str(font_path),complete_native_font_proof_sha256=sha(font_path.read_bytes()),
            complete_native_formatted_lines=case['lines'],
            actual_holds=[hold for hold in actual['complete_actual_holds'] if hold['message_ID'] == number],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
    scope = ('All8 withdrawal alternatives2114-2121 have clean Japanese,original role/table/context,natural faithful American English and complete native layout/font review. Original city-target input attacks Sao Tome73 without an eligible docked defender. The unedited ship sails away from the fixed town center;original513D0 changes from0 to1 to2,then original7251C/717F8 mode2 selects2114 through First Mate Charles18/table02117D00. Two entire228x64 native/independent-font RGB holds match all296 ink pixels,blank paper,uniform margins,all first/final letters and wrapped bytes. Normal A dismissal clears battle mode to[0,0,0] and town ID to115,returning to ordinary sailing without an extra page. Town defenses remain100;natural ship Hull/Crew change60/39 to59/33. The sole pre-battle fixture at5000 changes12 bytes within18 owned bytes:own live/cached position and existing Charles from duty8 to an existing First Mate room15. All other4MiB bytes,actors/IDs,health,towns,defenses,shares,diplomacy,RNG and events remain exact;no subsequent fixture or forced outcome. Original inputs and source/disposable saves are exact. Only2114 has individual actual activation;other7 use representative family coverage. No surrender,flagship destruction/capture or flooding credit. Targeted headless testing is not earned travel/crew assignment,full-route or hardware verification.')
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass']) == (1288,1373)
    assert not any(set(IDS).intersection(f.get('native_message_IDs',[])) for f in ledger['completed_editorial_families'])
    assert set(IDS) <= set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_completion.json',before)
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','native_message_IDs':list(IDS),
        'manuscript':str(manuscript),'manuscript_sha256':sha(manuscript.read_bytes()),'records':selected,
        'candidate':str(ROM),'candidate_sha256':digest,'actual_gameplay':str(ACTUAL),'actual_gameplay_sha256':sha(ACTUAL.read_bytes()),
        'registered_release':str(release_path),'registered_release_sha256':sha(release_path.read_bytes()),
        'actual_verification_scope':scope,'completed_entries':8,'revised':4,'retained':4,
        'other39_aftermath_records_incomplete':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    family_id, documentation = 'Shared-aftermath-withdrawal','docs/aftermath_withdrawal_v1294_completion.md'
    ledger['completed_editorial_families'].append({'id':family_id,'native_message_IDs':list(IDS),'records':selected,
        'final_review':str(FINAL),'documentation':documentation,'actual_verification_scope':scope})
    assert family_id not in {u['id'] for u in ledger['coverage_units']}
    ledger['coverage_units'].append({'id':family_id,'status':'complete-with-source-native-and-representative-gameplay-evidence',
        'native_message_IDs':list(IDS),'final_review':str(FINAL),'actual_proof':str(ACTUAL),'full_goal_complete':False})
    ledger['records_editorially_completed'] += 8
    ledger['records_revised_and_integrated'] += 4
    ledger['retained_wordings_editorially_completed'] += 4
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] += 8
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [n for n in drafts['native_message_IDs'] if n not in IDS]
    for name,values in drafts['manuscript_record_subsets_pending'].items():
        if name.replace('\\','/') == manuscript.as_posix():
            drafts['manuscript_record_subsets_pending'][name] = [n for n in values if n not in IDS]
            assert len(drafts['manuscript_record_subsets_pending'][name]) == 39
    pending = ledger['reviewed_but_incomplete_COMMON_IDs'] = [n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    drafts['status'] = '39-aftermath-and38-older-reviewed-entries-open'
    drafts['note'] = '36 aftermath alternatives complete through original fled-victory,crew-abandonment,flagship-loss,city-defense and withdrawal samples. Other39 require their own original source-family scenes. Older38 and broader shared/routes/raw inventory remain open.'
    reference = ledger['current_native_relocation_reference']
    reference.pop('75_source_native_approved28_family_records_complete47_pending')
    reference['75_source_native_approved36_family_records_complete39_pending'] = True
    ledger['latest_registered_aftermath_candidate']['status'] = 'experimental-36-aftermath-complete39-original-scenes-pending'
    ledger['latest_registered_aftermath_candidate']['latest_actual_proof'] = str(ACTUAL)
    summary = ('V1294 completes8 withdrawal alternatives2114-2121:4 revisions4 retentions. Counts1296 complete(964 revised332 retained),1373 source/prose;39 aftermath+38 older reviewed COMMON remain incomplete,plus broader unreviewed shared/routes/raw prose. Original Sao Tome town battle73 produces2114 from Charles18 after ordinary movement crosses native distance class2. Two complete glyph/RGB holds match all296 ink pixels,blank paper,margins and letters. A dismissal clears battle/town state and returns to ordinary sailing. Only the pre-battle location/First Mate fixture is used;12 changed bytes across18 owned bytes,full4MiB replay,all actors/IDs,health,defenses/shares,diplomacy,RNG and events preserved. Town defenses100 remain unchanged;natural ship60/39 becomes59/33. No surrender or other outcome credit. Registered V1266/exact patch unchanged;36 of75 aftermath alternatives complete. No ROM build or allocation change. Shop676/677 formatting remains a regression reference. Canonical,V997,all18 plaques,separate graphics audit,older-record revisit and full editorial goal remain unchanged/open.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1294-withdrawal8-completion','proof':str(FINAL),'actual':str(ACTUAL),
        'completed_entries_added':8,'source_prose_reviews_added':0,'full_goal_complete':False})
    complete = [n for family in ledger['completed_editorial_families'] for n in family.get('native_message_IDs',[])]
    assert len(complete) == len(set(complete)) == 1295
    assert len(pending) == len(set(pending)) == len(drafts['native_message_IDs']) == 77
    assert not set(complete).intersection(pending) and len(set(complete)|set(pending)) == 1372
    assert ledger['records_editorially_completed'] == ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed'] == 1296
    assert sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1296
    for key in ['current_integrated_candidate','source_pins','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit']:
        assert ledger[key] == before[key]
    save(ledger_path,ledger)
    Path(documentation).write_text('# V1294: original town-battle withdrawal verified\n\n'+summary+'\n\n## Actual scope\n\n'+scope+
        '\n\nFinal review: `'+str(FINAL)+'`. Actual proof: `'+str(ACTUAL)+'`. Guide screenshots: `E:/Rota Nova translations/Guide screenshots/V1266 Town withdrawal`. Exact ROM/patch remains [V1273](aftermath_fled_v1273_completion.md).\n\n'+
        'Remaining original scene gates:town surrender/report/white flag,enemy flagship destroyed/captured,own flooding and ship surrender. All39 remain open. The original distance getter returns class1 at frame6910 and class2 by7110;class2,rather than an assumed hand-calculated boundary,is the source condition used here.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1294 withdrawal family completed\n\n'+summary+'\n\nSee [evidence](aftermath_withdrawal_v1294_completion.md).\n')
    save(ROOT/'completion_receipt.json',{'completed':1296,'revised':964,'retained':332,'source_prose':1373,
        'newly_completed':8,'unique_complete_COMMON':1295,'reviewed_incomplete_COMMON':77,'remaining_aftermath':39,
        'no_duplicate_source_or_completion_credit':True,'coverage_unit_registered':True,'final_review':str(FINAL),
        'final_review_sha256':sha(FINAL.read_bytes()),'candidate_sha256':digest,'global_goal_active':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('8 withdrawal alternatives complete:1296 total;39 aftermath+38 older reviewed COMMON remain open.',flush=True)


if __name__ == '__main__':
    main()
