"""Credit only the six fled-victory alternatives with original family evidence."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from dk4tool.patch.battle_aftermath_editorial import current_entries,CONFIG
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.battle_aftermath_layout_v1250 import IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/aftermath_fled_completion_v1273')
ROM = Path('out/all_routes_combined_v1266_candidate.nds')
FINAL = Path('translations/battle_aftermath_fled_final_review_v1.json')
ACTUAL = Path('work/analysis/aftermath_victory_verified_v1271/actual_fled_victory_verification.json')


def main():
    assert not ROOT.exists() and not FINAL.exists()
    actual = read(ACTUAL)
    digest = sha(ROM.read_bytes())
    assert actual['candidate_sha256'] == digest and len(actual['complete_actual_holds']) == 2
    assert all(h['message_ID'] == 2046 and h['missing_or_unexpected_foreground_pixels'] == 0 for h in actual['complete_actual_holds'])
    assert len(actual['all31_fixture_replays']) == 31 and actual['no_during_or_post_duel_fixtures']
    release_path = Path('work/analysis/battle_aftermath_release_v1265/registered_release_verification.json')
    release = read(release_path)
    startup_path = Path('work/analysis/battle_aftermath_release_v1265/ordinary_startup_verification.json')
    startup = read(startup_path)
    assert release['candidate_sha256'] == startup['candidate_sha256'] == digest
    assert release['complete_reconstruction_byte_exact'] and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert sha(Path(startup['review_sheet']).read_bytes()) == startup['review_sheet_sha256']
    font_path = Path('work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json')
    font = read(font_path)
    assert len(font['cases']) == 783
    manuscript = Path('translations/battle_aftermath_editorial_manuscript_v3.json')
    doc = read(manuscript)
    selected = [deepcopy(r) for r in doc['records'] if 2046 <= r['message_id'] <= 2051]
    assert len(selected) == 6 and sum(r['editorial_decision'] == 'revise' for r in selected) == 5
    rom = NdsImage.open(ROM)
    common,arm = rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    entries = current_entries(common,arm)
    for row in selected:
        n = row['message_id']
        case = next(c for c in font['cases'] if c['message_id'] == n and c['name_case'] is None)
        assert entries[n].text == compiled(row) and case['compiled_hex'] == compiled(row).hex()
        row.update(before_reference=deepcopy(row['current_reference']),before_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[n]).items() if k != 'text'},
            current_text_hex=entries[n].text.hex(),current_English=row['english'],
            decision='revised-and-integrated' if row['editorial_decision'] == 'revise' else 'retained-and-editorially-reviewed',
            status='complete-with-source-native-and-representative-original-fled-victory-gameplay',
            completed_candidate_reference=str(ROM),completed_candidate_sha256=digest,
            complete_native_font_proof=str(font_path),complete_native_font_proof_sha256=sha(font_path.read_bytes()),
            complete_native_formatted_lines=case['lines'],
            actual_holds=actual['complete_actual_holds'] if n == 2046 else [],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True)
    scope = ('All six fled-victory voice alternatives2046-2051 have clean Japanese,original role/table/speaker context,natural faithful English and complete original speech-pipeline/native-font review. Registered V1266 preserves471 batches114 accepted layers and all earlier routes,graphics and fonts;its clean-input patch reconstructs exactly. Eight ordinary startup/title/New Game captures match V1105 and were visually reviewed. Original Charles18 fallback selects2046 from table02117900 following a natural duel victory. Two full228x64 foreground/blank-paper RGB holds match every letter and native wrapping,with uniform margins and no clipping. All31 pre-duel fixture receipts reproduce every4MiB byte,208 identities,RNG/event exclusions and accepted inputs;last fixture5770,before duel5772. Disclosed health,ability,equipment and location prerequisites only;no numeric message,actor ID,RNG,eligibility or result injection. No during/post-duel fixture. Original A dismissal clears battle context to0 and returns to ordinary sailing with no extra page. Only2046 has an individual actual activation;the other five have representative source-family evidence. Other69 aftermath paragraphs,38 older reviewed entries and the broader editorial goal remain unfinished. Targeted headless testing does not claim a full route,earned progression or hardware verification.')
    ROOT.mkdir(parents=True)
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','native_message_IDs':list(range(2046,2052)),
        'manuscript':str(manuscript),'manuscript_sha256':sha(manuscript.read_bytes()),
        'records':selected,'candidate':str(ROM),'candidate_sha256':digest,
        'registered_release':str(release_path),'registered_release_sha256':sha(release_path.read_bytes()),
        'ordinary_startup':str(startup_path),'ordinary_startup_sha256':sha(startup_path.read_bytes()),
        'actual_gameplay':str(ACTUAL),'actual_gameplay_sha256':sha(ACTUAL.read_bytes()),
        'actual_verification_scope':scope,'completed_entries':6,'revised':5,'retained':1,
        'all_other69_aftermath_records_incomplete':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1260 and ledger['records_with_source_and_prose_pass'] == 1373
    save(ROOT/'coverage_before_completion.json',ledger)
    before = deepcopy(ledger)
    assert all(not set(range(2046,2052)).intersection(f.get('native_message_IDs',[])) for f in ledger['completed_editorial_families'])
    ledger['completed_editorial_families'].append({'id':'Shared-aftermath-fled-victory2046-2051',
        'native_message_IDs':list(range(2046,2052)),'records':selected,'final_review':str(FINAL),
        'documentation':'docs/aftermath_fled_v1273_completion.md','actual_verification_scope':scope})
    ledger['records_editorially_completed'] += 6
    ledger['records_revised_and_integrated'] += 5
    ledger['retained_wordings_editorially_completed'] += 1
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4'] += 6
    done = set(range(2046,2052))
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = [n for n in drafts['native_message_IDs'] if n not in done]
    for name,values in drafts['manuscript_record_subsets_pending'].items():
        if name.replace('\\','/') == manuscript.as_posix():
            drafts['manuscript_record_subsets_pending'][name] = [n for n in values if n not in done]
    assert len(drafts['native_message_IDs']) == 107
    drafts['status'] = '69-aftermath-and38-older-reviewed-entries-open'
    drafts['note'] = 'The fled-victory6 alternatives are complete through representative original2046. Other69 aftermath paragraphs are integrated/native-approved but need their original source-family scenes/transitions. Older38 sighting,successful Lookout-shot and750-752 entries remain open. Broader shared/routes/raw inventory remains unfinished.'
    ledger['reviewed_but_incomplete_COMMON_IDs'] = [n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in done]
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs']) == 107
    ledger['current_native_relocation_reference'] = {'candidate':str(ROM),'COMMON_sha256':sha(common),
        'ARM9_sha256':sha(arm),'parser':'dk4tool.patch.battle_aftermath_editorial.current_entries',
        'release_config':CONFIG,'requires_guarded_single8192_cache_policy':True,
        'opaque1484byte_prefix_and_carrier1931_are_owned_and_hash_locked':True,
        '75_source_native_approved_only6_fled_family_scene_complete_other69_pending':True,
        'candidate_experimental_broader_goal_pending':True}
    ledger['latest_registered_aftermath_candidate'] = {**release,'status':'experimental-6-fled-complete69-other-aftermath-original-scenes-pending'}
    ledger['formatting_watchlist']['latest_photographed_shop_recheck'] = {
        'checkpoint':'V1272','candidate':str(ROM),'candidate_sha256':digest,
        'proof':'work/analysis/battle_aftermath_release_v1265/photographed_shop_formatting.json',
        'result':'676/677 exact repaired bytes,native wrapping and complete228x64 fonts pass under the new byte decoder. No fresh shop activation claimed.',
        'global_formatting_audit_complete':False}
    summary = ('V1273 completes only the six fled-victory alternatives2046-2051:5 revisions1 retention. Counts1266 complete (939 revised327 retained),1373 source/prose;107 reviewed COMMON entries remain incomplete,including69 other aftermath paragraphs and38 older entries,plus broader unreviewed shared/routes/raw inventory. Registered V1266 integrates all75 source/native-reviewed aftermath paragraphs with471 batches114 accepted layers and an exact clean-input patch. Eight ordinary startup/title/New Game screens match V1105 and are visually reviewed.529273 dispatch/ABI,783 native-font,7336 copy180 cache-sequence and13 escape regressions pass. Original2046 has two complete native-font/RGB holds,31 full pre-duel fixture/identity/RNG audits,and natural victory-to-A-dismissal-to-mode0-sailing return. Source/disposable saves remain unchanged;no during/post-combat fixtures or forced outcomes. Earlier676/677 formatting passes. No allocation or123040 staged growth. Canonical and prior whole-batch scene-verified V997 remain unchanged;V1266 is experimental until the other source families are verified. All18 plaques,separate graphics audit and global editorial goal remain open.')
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1273-aftermath-fled6-original-gameplay-completion',
        'proof':str(FINAL),'actual':str(ACTUAL),'completed_entries_added':6,'source_prose_reviews_added':0,
        'previous_goal_turn_classification':'progress:75 native-approved paragraphs,529273 dispatch783 font7336 copy proofs and archive',
        'this_goal_turn_classification':'progress:registered combined ROM,exact patch,eight startup controls,31 fixture audits and six fled-family completion credits',
        'full_goal_complete':False})
    assert ledger['records_editorially_completed'] == ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed'] == 1266
    assert sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1266
    for key in ('current_integrated_candidate','source_pins','unresolved_graphics_work',
                'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit'):
        assert ledger[key] == before[key],key
    save(ledger_path,ledger)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    physical = 'E:/Rota Nova translations/Generated/out/all_routes_combined_v1266_candidate.nds'
    assert not any(p['path'].replace('\\','/').lower() == physical.lower() for p in pins)
    pins.append({'path':physical,'reason':'Registered75-paragraph aftermath source;6 fled-victory alternatives scene-complete,69 other source families pending. Required for current gameplay and exact clean-input patch verification.'})
    save(pins_path,pins)
    docs = Path('docs/aftermath_fled_v1273_completion.md')
    assert not docs.exists()
    docs.write_text('# V1273: fled-victory family verification\n\n'+summary+'\n\n## Exact release\n\n'+
        '- Candidate: `'+str(ROM)+'`; SHA-256 `'+digest+'`.\n'+
        '- Canonical base: `out/raphael_natural_v2_accepted_base.nds`; SHA-256 `'+release['canonical_sha256']+'`.\n'+
        '- Profile: `'+release['profile']+'`;all471 batches114 accepted layers retained.\n'+
        '- Changed files relative to V1224: `/COMMON/MESFILE.DK4` blocks22/23 and ARM9 selection metadata/existing188/172-byte selector allocations. Routes,graphics,fonts,other files and components exact.\n'+
        '- Clean-input patch: `'+release['patch']+'`; SHA-256 `'+release['patch_sha256']+'`;reconstruction byte exact.\n\n'+
        '## Actual scope\n\n'+scope+'\n\n'+
        'Actual proof: `'+str(ACTUAL)+'`. Final family review: `'+str(FINAL)+'`. Startup sheet: `'+startup['review_sheet']+'`. Full registered release verification: `'+str(release_path)+'`. Guide captures: `E:/Rota Nova translations/Guide screenshots/V1266 Battle aftermath`.\n\n'+
        'Remaining original scene gates include town surrender/report/white flag,enemy flagship destroyed or captured,own crew abandonment/flooding/flagship defeat,ship surrender,city defense and withdrawal. No completion is granted to these families from the fled-victory sample. Canonical promotion is not authorized.\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md'):
        with (Path('docs')/name).open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1273 fled-victory family verification\n\n'+summary+'\n\nSee [evidence](aftermath_fled_v1273_completion.md).\n')
    save(ROOT/'completion_receipt.json',{'final_review':str(FINAL),'final_review_sha256':sha(FINAL.read_bytes()),
        'candidate_sha256':digest,'complete':1266,'revised':939,'retained':327,'source_prose':1373,
        'newly_complete':6,'other_aftermath_records_still_incomplete':69,
        'ordinary_startup8_visually_reviewed':True,'global_goal_active':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Only fled-victory6 completed:1266 complete1373 source/prose;69 other aftermath and38 older reviewed entries remain open.',flush=True)


if __name__ == '__main__':
    main()
