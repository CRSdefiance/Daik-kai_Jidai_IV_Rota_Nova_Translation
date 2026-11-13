"""Close only the14 crew-abandonment/flagship-loss voice alternatives."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/aftermath_defeat_completion_v1277')
ACTUAL = Path('work/analysis/aftermath_defeat_verified_v1276/actual_abandonment_and_flagship_defeat.json')
FINAL = Path('translations/battle_aftermath_defeat_final_review_v1.json')
ROM = Path('out/all_routes_combined_v1266_candidate.nds')
IDS = (*range(2016,2022),*range(2138,2146))


def main():
    assert not ROOT.exists() and not FINAL.exists()
    actual = read(ACTUAL)
    digest = sha(ROM.read_bytes())
    assert actual['candidate_sha256'] == digest and len(actual['all31_fixture_replays']) == 31
    assert len(actual['complete_actual_holds']) == 6
    assert {h['message_ID'] for h in actual['complete_actual_holds']} == {1973,2016,2138}
    assert all(h['missing_or_unexpected_foreground_pixels'] == 0 for h in actual['complete_actual_holds'])
    assert actual['no_during_or_post_combat_health_ability_equipment_location_or_result_changes']
    manifest_path = ROM.with_suffix('.manifest.json')
    manifest = read(manifest_path)
    release_path = Path('work/analysis/battle_aftermath_release_v1265/registered_release_verification.json')
    release = read(release_path)
    assert release['candidate_sha256'] == manifest['candidate_sha256'] == digest and release['complete_reconstruction_byte_exact']
    manuscript = Path('translations/battle_aftermath_editorial_manuscript_v3.json')
    doc = read(manuscript)
    font_path = Path(doc['native_font_proof'])
    font = read(font_path)
    rom = NdsImage.open(ROM)
    common,arm = rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    entries = current_entries(common,arm)
    selected = [deepcopy(r) for r in doc['records'] if r['message_id'] in IDS]
    assert tuple(r['message_id'] for r in selected) == IDS and all(r['editorial_decision'] == 'revise' for r in selected)
    for row in selected:
        n = row['message_id']
        case = next(c for c in font['cases'] if c['message_id'] == n and c['name_case'] is None)
        assert entries[n].text == compiled(row) and all(row['review'].values())
        row.update(before_reference=deepcopy(row['current_reference']),before_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[n]).items() if k != 'text'},
            current_text_hex=entries[n].text.hex(),current_English=row['english'],
            decision='revised-and-integrated',status='complete-with-source-native-and-representative-original-defeat-gameplay',
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            complete_native_font_proof=str(font_path),complete_native_font_proof_sha256=sha(font_path.read_bytes()),
            complete_native_formatted_lines=case['lines'],
            actual_holds=[h for h in actual['complete_actual_holds'] if h['message_ID'] == n],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
    scope = ('All14 alternatives2016-2021 and2138-2145 have clean Japanese,original role/table/speaker/outcome context,faithful natural English and complete native speech/font review. Original natural duel defeat reaches2016 crew-abandonment and2138 flagship-loss announcements from source717F8;the following A dismissals reach Game Over and the ordinary title. Actual Charles18 source selection,stored templates,post-expansion wrapping and two complete228x64 font/RGB holds per new announcement pass. Two additional1973 escape holds verify its earlier translation under the same decoder. All31 pre-duel fixture receipts reproduce every4MiB byte,208 identities,RNG/event exclusions and accepted inputs;last fixture5770,before duel5772. Disclosed low positive HP31,live ship recovery,contact and original shield-to-inventory transfer only. No during/post-combat health,equipment,ability,location or result edits. Natural HP changes31/117 to0/45. Source/disposable saves remain exact. Only2016 and2138 have individual actual activations;the remaining12 have representative source-family coverage. The flooding-specific2006-2010 announcements are a separate unverified family. This is targeted headless testing,not a full route,earned progression or hardware verification.')
    ROOT.mkdir(parents=True)
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','native_message_IDs':list(IDS),
        'manuscript':str(manuscript),'manuscript_sha256':sha(manuscript.read_bytes()),'records':selected,
        'candidate':str(ROM),'candidate_sha256':digest,'actual_gameplay':str(ACTUAL),
        'actual_gameplay_sha256':sha(ACTUAL.read_bytes()),'registered_release':str(release_path),
        'registered_release_sha256':sha(release_path.read_bytes()),'actual_verification_scope':scope,
        'completed_entries':14,'revised':14,'retained':0,'other55_aftermath_records_incomplete':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1266 and ledger['records_with_source_and_prose_pass'] == 1373
    save(ROOT/'coverage_before_completion.json',ledger)
    before = deepcopy(ledger)
    assert all(not set(IDS).intersection(f.get('native_message_IDs',[])) for f in ledger['completed_editorial_families'])
    for family,numbers in (('crew-abandonment',list(range(2016,2022))),('flagship-loss',list(range(2138,2146)))):
        ledger['completed_editorial_families'].append({'id':'Shared-aftermath-'+family,
            'native_message_IDs':numbers,'records':[r for r in selected if r['message_id'] in numbers],
            'final_review':str(FINAL),'documentation':'docs/aftermath_defeat_v1277_completion.md',
            'actual_verification_scope':scope})
    ledger['records_editorially_completed'] += 14
    ledger['records_revised_and_integrated'] += 14
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] += 14
    done = set(IDS)
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [n for n in drafts['native_message_IDs'] if n not in done]
    for name,values in drafts['manuscript_record_subsets_pending'].items():
        if name.replace('\\','/') == manuscript.as_posix():
            drafts['manuscript_record_subsets_pending'][name] = [n for n in values if n not in done]
            assert len(drafts['manuscript_record_subsets_pending'][name]) == 55
    ledger['reviewed_but_incomplete_COMMON_IDs'] = [n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in done]
    assert len(drafts['native_message_IDs']) == len(ledger['reviewed_but_incomplete_COMMON_IDs']) == 93
    drafts['status'] = '55-aftermath-and38-older-reviewed-entries-open'
    drafts['note'] = '20 aftermath alternatives are complete through original fled-victory,crew-abandonment and flagship-loss samples. Other55 are integrated/native-approved but need their separate original source-family scenes/transitions. Older38 sighting,successful Lookout-shot and750-752 entries remain open;broader shared/routes/raw inventory unfinished.'
    ref = ledger['current_native_relocation_reference']
    assert ref['parser'] == 'dk4tool.patch.battle_aftermath_editorial.current_entries'
    ref.pop('75_source_native_approved_only6_fled_family_scene_complete_other69_pending')
    ref['75_source_native_approved20_family_records_complete55_pending'] = True
    ledger['latest_registered_aftermath_candidate']['status'] = 'experimental-20-aftermath-complete55-original-scenes-pending'
    ledger['latest_registered_aftermath_candidate']['latest_actual_proof'] = str(ACTUAL)
    summary = ('V1277 completes14 additional crew-abandonment/flagship-loss alternatives2016-2021,2138-2145:14 revisions. Counts1280 complete (953 revised327 retained),1373 source/prose. Registered V1266 now has20 of75 aftermath entries complete through representative original fled-victory and defeat paths;55 remain integrated/native-approved with original scenes pending. Total93 reviewed COMMON entries remain incomplete,including38 older entries,plus the broader unreviewed shared/routes/raw inventory. Six complete actual font/RGB holds cover preserved1973 and new2016/2138.31 full pre-duel fixture/208-identity/RNG/input audits pass;natural HP31/117 becomes0/45,then original abandonment,flagship loss,Game Over and title. Last fixture5770 before duel5772;no during/post-combat changes or forced outcomes. Source/disposable saves unchanged. Same registered ROM,exact patch,eight startup controls and earlier native/copy regressions;no additional build needed. Canonical,V997,all18 plaques,separate graphics audit and global editorial goal remain unchanged/open.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1277-aftermath-defeat14-completion','proof':str(FINAL),
        'actual':str(ACTUAL),'completed_entries_added':14,'source_prose_reviews_added':0,'full_goal_complete':False})
    assert ledger['records_editorially_completed'] == ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed'] == 1280
    assert sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1280
    for key in ('current_integrated_candidate','source_pins','unresolved_graphics_work',
                'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit'):
        assert ledger[key] == before[key],key
    save(ledger_path,ledger)
    docs = Path('docs/aftermath_defeat_v1277_completion.md')
    assert not docs.exists()
    docs.write_text('# V1277: original defeat aftermath verification\n\n'+summary+'\n\n## Actual scope\n\n'+scope+
        '\n\nFinal review: `'+str(FINAL)+'`. Actual proof: `'+str(ACTUAL)+'`. Registered ROM/patch details remain in [V1273](aftermath_fled_v1273_completion.md). Guide captures: `E:/Rota Nova translations/Guide screenshots/V1266 Defeat aftermath`.\n\n'+
        'Next original scene gates:town surrender/report/white flag,enemy flagship destroyed or captured,own flooding,ship surrender,city defense and withdrawal.55 aftermath records remain incomplete;no credit for flooding from the distinct crew-loss sample. Global source/prose coverage1373 is not the total project inventory.\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md'):
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1277 original defeat aftermath verification\n\n'+summary+'\n\nSee [evidence](aftermath_defeat_v1277_completion.md).\n')
    save(ROOT/'completion_receipt.json',{'final_review':str(FINAL),'final_review_sha256':sha(FINAL.read_bytes()),
        'candidate_sha256':digest,'completed':1280,'revised':953,'retained':327,'source_prose':1373,
        'newly_completed':14,'all_current_aftermath_completed':20,'other_aftermath_records_still_incomplete':55,
        'global_goal_active':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('14 additional alternatives complete:1280 complete1373 source/prose;55 aftermath and38 older reviewed entries remain open.',flush=True)


if __name__ == '__main__':
    main()
