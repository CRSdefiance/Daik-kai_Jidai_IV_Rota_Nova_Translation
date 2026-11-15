"""Record one completed editorial entry with its exact native/gameplay evidence."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_specialty_question_v752 import MANUSCRIPT, ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v752_candidate.nds')
DOC = Path('docs/specialty_question_v752_checkpoint.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V752 Specialty question')


def main():
    native, registered, gameplay, patch = (read(ROOT/name) for name in (
        'native_review.json','registered_verification.json','gameplay_verification.json','patch_proof.json'))
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert sha(ROM.read_bytes()) == manifest['candidate_sha256'] == gameplay['candidate_sha256'] == patch['candidate_sha256']
    assert len(native['all25_original_prerequisite_pairs']) == 25
    assert len(gameplay['actual_complete_question_holds']) == len(gameplay['actual_complete_response_holds']) == 8
    assert sum(map(len,gameplay['unchanged_full_frame_controls'].values())) == 32
    assert len(registered['native_warm_cold_copies']) == 122 and all(registered['rejections'].values())
    assert patch['whole_ROM_byte_exact']
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 92 and ledger['records_revised_and_integrated'] == 61
    save(ROOT/'editorial_ledger_at_V751.json',ledger)
    row = read(MANUSCRIPT)['records'][0]
    family = 'Market-specialty-item-request'
    ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':[742],
        'records':[{'message_id':742,'decision':'revised-and-integrated','manuscript':str(MANUSCRIPT),
            'complete_clean_source_context_and_all25_native_pairs_verified':True,
            'complete_fixture_gameplay_display_and_both_response_paths_verified':True}],
        'proof':str(ROOT/'proof.json'),'ordinary_item_acquisition_not_claimed':True})
    ledger.update({'records_editorially_completed':93,'records_revised_and_integrated':62,
        'latest_checkpoint':'V752 specialty question742 completed with all25 original prerequisite pairs and both actual response/state paths;730 and wider shared/routes remain open'})
    assert ledger['retained_wordings_editorially_completed'] == 31
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next'] = 'Finish readable full category arguments730; continue further shared shop/town prose, then Lil and every other route.730 is the remaining draft in this packet, not the whole remaining-game inventory.'
    ledger['active_source_prose_drafts']['native_message_IDs'] = [730]
    for finding in ledger['findings']:
        if finding['id'] == 'COMMON-742-specialty-question-runtime-formatting':
            finding.update({'status':'source-all25-native-font-and-both-actual-gameplay-paths-verified-integrated-V752',
                'detail':'Number-neutral request plus tentative local-specialty prediction. Only original Yes/No742 wraps after substitutions. All25 product/item prerequisites fit3 lines. One inventory availability bit triggers unmodified native eligibility; actual acceptance consumes the item and clears the original town specialty bit, refusal retains both. Eight complete question holds and eight response holds pass.'})
    for previous in ledger['completed_editorial_families']:
        if previous['id'] == 'Square-related-trend-and-specialty-shop-responses':
            previous.pop('730_category_sentence_and742_question_remain_open',None)
            previous['730_remains_open_742_completed_later_in_V752'] = True
            for record in previous['records']:
                if record['message_id'] in (743,744):
                    record['additional_actual_gameplay_display_evidence'] = str(ROOT/'gameplay_verification.json')
    ledger['current_integrated_candidate'] = {'path':str(ROM),'sha256':manifest['candidate_sha256'],
        'profile':manifest['profile'],'MESFILE_sha256':read('translations/specialty_question_editorial_release_v1.json')['target_common_sha256'],
        'ARM9_sha256':read('translations/specialty_question_editorial_release_v1.json')['target_arm9_sha256'],
        'patch_sha256':patch['patch_sha256'],'status':'experimental','manifest':str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten':True}
    save(LEDGER,ledger)
    master_path = Path('translations/town_events_editorial_manuscript_v1.json')
    master = read(master_path)
    for record in master['records']:
        if record['message_id'] == 742:
            for key in ('english','speaker','context','source_meaning','localization_note','decision','review'):
                record[key] = row[key]
            record.update({'status':'reviewed-and-integrated-V752-see-release-manuscript-and-proof',
                'integrated_evidence':str(ROOT/'proof.json')})
    save(master_path,master)
    DOC.write_text(f'''# V752: specialty item request

COMMON742 completes review. Cumulative coverage is93 completed entries:62 revised and31 retained wordings. Category730, the wider shared prose, every route and remaining player-facing prose still require review. The full editorial goal remains active; the graphics audit remains separately unfinished.

## Faithful natural English

> {row['english'].removesuffix('{PAD}')}

The clean Japanese calls for attention, asks for the player's specific item, predicts that it can enable the named local specialty, and repeats the request. English combines the repeated appeal into one clear question. Your works with singular and plural item names, including seeds and silkworms. I think we could preserves the speculative tone; here preserves the town context. The item/product substitution order and all original event calls remain intact.

The original eligibility routineBAB64 checks218 inventory objects against five town slots and requires product byte13 to match the item index. All124 current product metadata rows bind that field to source byte7;25 product rows reference items0-19, all others are outside the original218-item range. Native name getters and every complete name are bound to the current ROM. All25 actual prerequisite pairs receive complete native printf/wrap/font-plane checks and visual preview review; each fits three lines with complete first/last letters, blank cells and bounds.

## Scoped formatting and preservation

All18340 five-parent/message dispatch cases add only original Yes/No parent53FCC and ID742. Forty-nine complete fallback copy/return controls are exact. The existing36-byte dispatch is replaced in place. A16-byte helper occupies a source-owned20-byte padded Fleet label allocation; its sole pointer owner now references an already existing byte-identical complete Fleet string. An every-byte pointer scan across all five loaded sections rejects interior aliases. No mutable caption bitmap or resource-pointer zero area is reused. No section, staged pool, startup payload, arena or cache grows. The packed743 response remains byte-exact; reclaimed padding precedes742's native entry instead of adding a blank continuation to743.

All122 warm/cold native copies across block9 and its boundaries, seven rejection controls,3668 ID/NUL-owner invariants and original allocations pass. The integrated ROM preserves the previous61 revisions,675 graphics and other internal files. All470 batches and114 accepted layers remain registered. The clean-input patch reconstructs the entire ROM exactly.

## Actual emulator evidence

Four terminal6501-frame cold boots pair V751/V752 for both answers. A declared one-byte availability-bit fixture supplies Baby Shark in a disposable copy of the Istanbul save. All other main RAM bytes are unchanged at insertion. Original full eligibility returns without a request before the fixture and reaches742 with Baby Shark/Caviar afterward; no getter or eligibility result is supplied. Ordinary Market input then displays the actual question. Eight complete question holds match every glyph and blank cell; Yes/No controls and every pixel outside the text plane match baseline. Eight acceptance/refusal holds match full native743/744 text. Thirty-two complete baseline/control/return frames match. At5200 original getters show acceptance consumes the available item and clears the town slot's specialty bit; refusal retains both. Earned item acquisition, full-route and hardware verification are not claimed.

An ordinary4000-frame New Game cold boot uses no save or fixture. Five shared baseline frames match exactly; intro1600 and captain selection2000 were also visually inspected. Protected original and disposable donor saves retain SHA256 {gameplay['protected_and_disposable_source_saves_unchanged']['sha256']}.

## Reproduction and remaining work

- Candidate: `{ROM}`
- SHA256: `{manifest['candidate_sha256']}`
- Profile: `all-routes-unified-v752` (experimental)
- Patch: `{ROM.with_suffix('.xdelta')}`
- Patch SHA256: `{patch['patch_sha256']}`
- Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Clean input SHA256: `{patch['clean_source_sha256']}`.

The registry, source/current manuscript,25-pair native report, final captures, exact patch proof and scripts record reproduction details. Initial navigation probes selected Palace/Inn/Tavern and earn no request credit. A corrected top-left Market touch28,34 is used in every final paired test. One initial command omitted touchscreen permission and terminated before capture. Import formatting was finalized after all probes stopped and before all final runs. No live producer or capture dependency was edited. Historical probe receipts are not substituted for final-run evidence.

ROM/patch and evidence remain on E. Selected screenshots are explicitly labeled test fixtures. The graphics audit,18 plaques, Online exclusions, preserved brown marks and later older-record follow-up are unchanged. Next: finish730's full category arguments, then continue shared prose and every route. The candidate is not promoted to the canonical baseline.
''',encoding='utf-8')
    reports = ('native_review.json','registered_verification.json','gameplay_verification.json','patch_proof.json','repack_proof.json')
    save(ROOT/'proof.json',{'candidate':str(ROM),'candidate_sha256':manifest['candidate_sha256'],'profile':manifest['profile'],
        'reviewed_IDs':[742],'revised_IDs':[742],'retained_wordings':[],
        'verification_reports':{str(ROOT/f):sha((ROOT/f).read_bytes()) for f in reports},
        'all25_native_previews_and_question_response_intro_captain_selection_visually_inspected':True,
        'all_prior61_revisions470_batches114_layers675_graphics_preserved':True,
        'canonical_source_saves_harness_preserved_no_promotion':True,
        '730_wider_shared_all_routes_and_graphics_audit_remain_open':True,
        'editorial_ledger_sha256':sha(LEDGER.read_bytes()),'full_goal_complete':False})
    summary = '\n\n## V752: specialty item request\n\nOne revision742 completes review. All25 original prerequisite pairs fit three complete native lines;18340 dispatch cases change only original Yes/No742. Forty-nine complete fallback controls,122 native copies and seven rejection controls pass. Four paired cold boots with a disclosed one-byte inventory fixture verify eight complete question holds, eight743/744 response holds,32 unchanged controls and both original post-answer states. Ordinary New Game has five exact baseline frames plus visually inspected intro/captain selection. Registered470/114 combined V752 and exact clean-input patch preserve earlier prose and675 graphics without growth. Total93 reviewed,62 revised,31 retained;730, wider shared/routes and graphics audit remain open. Canonical and source saves unchanged. See [V752 checkpoint](specialty_question_v752_checkpoint.md).\n'
    for name in ('todo.md','translation_progress.md','known_issues.md','release_build.md'):
        path=Path('docs')/name
        text=path.read_text(encoding='utf-8')
        assert '## V752: specialty item request' not in text
        path.write_text(text.rstrip()+summary,encoding='utf-8')
    save('out/editorial_review_latest.json',{**ledger['current_integrated_candidate'],'details':str(DOC),'full_goal_complete':False})
    shots=Path('E:/Rota Nova translations/Screenshots/Test fixtures/V752 Specialty request')
    for number,rows in ((742,gameplay['actual_complete_question_holds']),(743,gameplay['actual_complete_response_holds']),(744,gameplay['actual_complete_response_holds'])):
        item=next(r for r in rows if r['message_id']==number)
        copy(Path(item['capture']['path']),shots/f'COMMON_{number}_controlled.png')
    save(shots/'provenance.json',{'candidate_sha256':manifest['candidate_sha256'],'one_byte_inventory_availability_fixture':True,
        'ordinary_acquisition_not_claimed':True,'gameplay_proof':str(ROOT/'gameplay_verification.json'),
        'files':{p.name:sha(p.read_bytes()) for p in shots.glob('*.png')}})
    files=[DOC,LEDGER,MANUSCRIPT,Path('translations/specialty_question_editorial_release_v1.json'),
        Path('dk4tool/patch/specialty_question_editorial.py'),ROOT/'proof.json',ROOT/'editorial_ledger_at_V751.json',
        *(ROOT/f for f in (*reports,'runtime_names.json','all25_preview_sheet.png','inputs_specialty_tradehouse.json','inputs_specialty_accept.json','inputs_newgame.json')),
        *(Path('scripts')/f for f in ('prepare_specialty_question_v752.py','register_specialty_question_v752.py','verify_specialty_release_v752.py',
            'verify_specialty_gameplay_v752.py','native_specialty_fixture_v752.py','run_specialty_capture_v752.py')),Path(__file__)]
    for path in files:
        copy(path,ARCHIVE/path.name)
    save(ARCHIVE/'provenance.json',{'candidate_sha256':manifest['candidate_sha256'],
        'files':{p.name:sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name!='provenance.json'},'full_goal_complete':False})
    assert all(sha((ARCHIVE/name).read_bytes())==digest for name,digest in read(ARCHIVE/'provenance.json')['files'].items())
    print('V752 recorded:93 completed,62 revised,31 retained;730 and broad editorial/graphics goals remain open.',flush=True)


if __name__ == '__main__':
    main()
