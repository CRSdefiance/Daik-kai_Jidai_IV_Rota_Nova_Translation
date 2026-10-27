"""Record integrated50-entry work and first actual family without completion credit."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.register_shared_release_v782 import CONFIG, CURRENT, MANUSCRIPT, ROOT
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v782_candidate.nds')
LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/shared_dialogue_v782_integration_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V782 Shared dialogue integration')
SHOTS = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V782 Shared dialogue')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    config = read(CONFIG)
    for p, h in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    assert sha(MANUSCRIPT.read_bytes()) == config['manuscript_sha256']
    release = read(ROOT/'registered_verification.json')
    patch = read(ROOT/'patch_proof.json')
    boot = read(ROOT/'newgame_regression.json')
    game = read(ROOT/'recruit_capacity_gameplay_verification.json')
    manifest = read(ROM.with_suffix('.manifest.json'))
    watch = read('work/analysis/dialogue_formatting_user_recheck_v782/COMMON676_677.json')
    digest = sha(ROM.read_bytes())
    assert digest == release['candidate_sha256'] == patch['candidate_sha256'] == boot['candidate_sha256'] == game['candidate_sha256'] == watch['sha256'] == manifest['candidate_sha256']
    assert patch['byte_exact_reconstruction'] and sha(ROM.with_suffix('.xdelta').read_bytes()) == patch['patch_sha256']
    assert all(release['negative_gates'].values()) and release['all7336_complete_native_copies']
    assert release['all470_batches114_accepted_layers_and_graphics_retained'] and all(manifest['checks'].values())
    assert boot['all_pixels_exact'] and len(boot['whole_screen_frame_pairs']) == 7
    assert len(game['holds']) == 2 and {h['message_id'] for h in game['holds']} == {1042}
    assert all(h['complete_independent_font_and_blank_paper_exact'] and h['all_other_pixels_exact'] for h in game['holds'])
    assert len(game['whole_screen_controls']) == len(game['paired_state_model_object_task_frames']) == 11
    assert len(game['original_whole_screen_blink_phase_controls']) == 1 and game['normal_town_return_frame'] == 8800
    assert not game['batch_completion_credit']
    protected = dict(read('work/analysis/shared_editorial_v781/checkpoint.json')['protected_files_unchanged'])
    for p, h in protected.items():
        assert sha(Path(p).read_bytes()) == h, p
    doc = read(MANUSCRIPT)
    assert len(doc['records']) == 50 and sum(r['decision'] == 'revise' for r in doc['records']) == 34
    assert all(all(r['review'].values()) for r in doc['records'])
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 367 and ledger['records_with_source_and_prose_pass'] == 420
    assert ledger['records_revised_and_integrated'] == 259 and ledger['retained_wordings_editorially_completed'] == 108
    assert ledger['current_integrated_candidate']['path'] == str(CURRENT)
    if not (ROOT/'editorial_ledger_before_v782.json').exists():
        save(ROOT/'editorial_ledger_before_v782.json', ledger)
    pending = {'path': str(ROM), 'sha256': digest, 'profile': manifest['profile'],
               'MESFILE_sha256': release['COMMON_sha256'], 'ARM9_sha256': release['ARM9_sha256'],
               'patch_sha256': patch['patch_sha256'], 'manifest': str(ROM.with_suffix('.manifest.json')),
               'status': 'experimental-pending-other-shared-family-gameplay', 'details': str(DOC),
               'completed_in_this_batch': 0, 'new_editorially_completed': 0,
               'verified_actual_family': '1042-capacity-recruiting-confirmation',
               'remaining_actual_families': game['other_shared_families_pending'], 'full_goal_complete': False}
    ledger['pending_integrated_candidate'] = pending
    ledger['active_source_prose_drafts'].update({
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'status': '750-752-context-unmapped;1020-1069-native-reviewed-and-integrated-with-first-actual-family;other-actual-families-pending',
        'note': '50 source/context/naturalness/native-formatting-approved entries are integrated in registered V782,with no completed-entry credit until representative remaining actual families pass. 53 active drafts remain.'})
    remaining = ['Actual missing-information and warning dialogs', 'Both village-coordinate modes',
                 'Anchored and destination fleet rumors', 'Required-crew shortfall confirmation',
                 'Private barmaid topics and normal transitions']
    checkpoint = {'id': 'V782-shared-integration-and-first-actual-family', 'documentation': str(DOC),
                  'candidate': pending, 'new_source_prose_records': 0, 'native_approved_integrated_records': 50,
                  'new_editorially_completed': 0, 'native_routing_cases': 34343, 'production_layouts': 857,
                  'complete_native_copies': 7336, 'complete_font_planes': 83,
                  'actual_complete_holds': 2, 'actual_IDs': [1042], 'newgame_whole_frame_pairs': 7,
                  'remaining_gates': remaining, 'full_goal_complete': False}
    if not any(r['id'] == checkpoint['id'] for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    ledger['coverage_units'][0]['next'] = 'Finish V782 representative actual information,warning,village,fleet,shortfall and private-barmaid samples;then credit the50-entry batch. Continue COMMON1070 onward,resolve750-752,and review all routes and other prose. Keep separate graphics and older-record follow-up open.'
    summary = 'V782 integrates50 source/context/native-formatting-approved shared entries(34 revisions/16 retained) through exact128-byte table and144-byte gate without memory growth.34343 routing cases,857 production layouts,83 complete fonts,7336 copies,12 negative gates and exact clean patch pass. Seven cold-boot/New Game frames match V780. First1042 capacity prompt has2 complete actual holds,11 strict whole-screen controls,one complete original blink-phase match,11 state/model/task pairs and town return. Other actual families remain required:367 completed,420 source/prose,53 drafts. V780 remains the current batch-verified ROM;V782 is registered experimental pending further gameplay. Full editorial and graphics goals remain unfinished.'
    ledger['latest_checkpoint'] = summary
    save(LEDGER, ledger)
    latest = read('out/editorial_review_latest.json')
    assert latest['sha256'] == sha(CURRENT.read_bytes())
    latest['latest_research_checkpoint'] = str(DOC)
    latest['pending_integrated_candidate'] = pending
    save('out/editorial_review_latest.json', latest)
    DOC.write_text(f'''# V782: shared dialogue integrated; actual families still open

COMMON1020–1069 now have50 native-approved integrated paragraphs:34 revisions and
16 retained wordings. These are natural-dialogue-v2,source-faithful American English
with exact Japanese,current-build,argument and context references. All50 pass
offline native formatting. They receive **no completed-entry credit yet** because
the other representative actual families remain required. Totals stay367 completed
(259 revised/108 retained),420 source/prose passes and53 drafts. V780 remains the
current batch-verified ROM. V782 is registered experimental,with further gameplay
required. The whole editorial goal and separate graphics audit remain unfinished.

## Native consumers and original conditions

114 immutable town/culture/role13 mappings,four unmodified real role/voice-provider
bindings,705 direct bindings and21 private-barmaid bindings reach the original
portrait consumer. A null-actor negative reaches the original system consumer,
which is unchanged. Only message I/O is stubbed to exact current entries in this
ABI probe;supplied argument sentinels are not actual earned counts or coordinates.

616 original warning-threshold branches,eight cancel/schedule results,204 crew
shortfall/capacity/funds branches,four relationship stages,30 original chance
selections,160 fleet candidate filters and three missing-information branches pass.
150 complete original village-selector cases cover both modes,all24 individually
eligible villages,the empty list,and the original threshold boundary. World bytes
supplied to the CPU probes are restored. These are offline native tests,not actual
earned events. Original captain208 produces faction21;the English does not invent
a pirate identity. Anchorage and destination remain distinct. Source RNG branches
and original source providers remain unchanged in the ROM.

## Exact integration and formatting

The exact contract table uses its existing128 bytes;the gate fits its existing144
bytes. Coordinate1028/1029 use the existing scoped helper,while842 and905/906 retain
their previous routes. Near,unaligned,wrong-parent and wrong-high-half keys remain
rejected.34343 native routing/register cases pass. A first148-byte prototype was
rejected before integration. Deriving the pointer high half from the fixed table
bank removes a redundant literal and fits the existing allocation. Sections,BSS,
cache plan,arena bounds and123040-byte staged payload do not grow.

The smallest fitting contiguous existing block window is13–40,proved by287
candidate windows in increasing block count. All2661 selections1007–3667 are mapped;
all3618 unedited visible strings,13 unselected blocks,and complete opaque1854/1865
payloads are exact.857 supplied-value cases pass through the actual original
call target,trampoline and dispatcher. Every output matches its reviewed preview;
83 complete independent font planes match the nine previously reviewed sheets.
Original numeric/coordinate arguments retain all bytes.7336 complete original
warm/cold copies cover all3668 messages,including post-NUL spans.

The registered builder preserves470 batches,114 accepted layers and all inherited
graphics. Ten explicit parser-dependency replays retain their exact former stage
outputs. Only COMMON/MESFILE.DK4 and ARM9 differ from V780. Twelve hard negative
gates reject bad provenance,unreviewed prose,missing approval,legacy policy,padding,
manual breaks,missing/extra arguments,wrong coordinate sources and macros. The
clean-input patch reconstructs the combined candidate byte for byte.

## Actual scope and the highlight observation

Seven ordinary cold-boot/New Game whole-frame pairs match V780,without a battery
save,savestate or test fixtures. The first new actual family is capacity prompt1042,
spoken by Charles Rochefort with original full-width51. Two complete holds6800/7200
have exact leading/trailing letters,all glyphs,blank paper and outside-text pixels.
Eleven strict whole-screen controls and eleven state/model/object/task pairs pass.
Cancel returns through the original Assign Sailors/unassigned confirmation and
Tavern menu to the ordinary Istanbul town screen at8800. The donor is copied before
cold boot and its original hash remains unchanged. No runtime cheat is used here.

At8000 the cyan selection highlight differs in its blink phase. This was not
ignored with a rectangular mask. An additional V780 cold boot using the identical
input schedule captures7900–8000. The **entire** V7828000 screen matches22 original
frames,including7989–7999;the original source control also matches every other
sampled stable frame. The independent state/model/task checks match at8000 too.
Thus this observed difference is an original animation phase,not missing text or
an altered selection. Evidence is in the first-family gameplay verifier/report.

Other actual samples still required: missing-information1020,warnings1021–1027,
village-coordinate1028/1029,fleet1030–1034,required-shortfall1035–1041 and private
barmaid1049–1069. Normal outcomes and transitions must also pass. The50-entry batch
is not complete. COMMON1070 onward,drafts750–752,all route scenes and other prose
remain in scope. Older route leads and older-record follow-up are preserved.

COMMON676/677—the user's shopkeeper-formatting examples—retain their repaired
bytes and native wrapping in V782. The prior actual V747 capture remains the actual
shop reference;no fresh V782 activation of that particular shop scene is claimed.
Every new family retains margin,wrap,pagination and complete-letter checks.

## Candidate and preservation

- ROM:`{ROM}`
- ROM SHA-256:`{digest}`
- Profile:`{manifest['profile']}` (experimental)
- COMMON SHA-256:`{release['COMMON_sha256']}`
- ARM9 SHA-256:`{release['ARM9_sha256']}`
- Patch SHA-256:`{patch['patch_sha256']}`
- Clean input:`{patch['clean_source_sha256']}`
- Canonical base:`out/raphael_natural_v2_accepted_base.nds`
- Canonical SHA-256:`{patch['canonical_base_sha256']}` (unchanged)

Initial frozen research flags describe the stage when each proof was produced.
The registration,patch and actual-family reports supersede their pending flags;
they are not rewritten retroactively. The50-entry completion gate remains open.
ROMs and research stay on E:/Rota Nova translations. Screenshots are archived as
test evidence,not promoted as finished guide screenshots. The separate graphics
audit—including the18 plaques,Online-body exclusion and preserved brown marks—is
unchanged. No GitHub commit or push was performed.
''', encoding='utf-8')
    for path in ('docs/todo.md', 'docs/known_issues.md', 'docs/translation_progress.md'):
        p = Path(path)
        text = p.read_text(encoding='utf-8')
        heading = '## V782: shared dialogue integrated and first actual capacity prompt'
        if heading not in text:
            p.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V782 integration checkpoint](shared_dialogue_v782_integration_checkpoint.md).\n', encoding='utf-8')
    checkpoint.update({'protected_files_unchanged': protected,
                       'registered_dependencies_unchanged': True, 'production_config_sha256': sha(CONFIG.read_bytes()),
                       'remaining_actual_families': remaining,
                       'previous_goal_turn_classification': 'No new editorial coverage;the already-fixed user example was rechecked. This turn revalidated current state and advanced50-entry integration.',
                       'producer_sha256': sha(Path(__file__).read_bytes())})
    save(ROOT/'checkpoint.json', checkpoint)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE/'evidence'/source.relative_to(ROOT))
    for source in (MANUSCRIPT, CONFIG, DOC, LEDGER, ROM.with_suffix('.manifest.json')):
        copy(source, ARCHIVE/source.name)
    for report in game['capture_reports']:
        source = Path(report)
        copy(source, ARCHIVE/source.parent.name/source.name)
    phase_report = Path(game['original_whole_screen_blink_phase_controls'][0]['capture_report'])
    copy(phase_report, ARCHIVE/phase_report.parent.name/phase_report.name)
    for hold in game['holds']:
        source = Path(hold['capture']['path'])
        copy(source, SHOTS/f'ID1042_{hold["frame"]}_V782_VERIFIED_TEST.png')
    capture_report = read(game['capture_reports'][1])
    return_frame = next(r for r in capture_report['frames_captured'] if r['frame'] == 8800)
    copy(Path(return_frame['path']), SHOTS/'Istanbul_return_8800_V782_VERIFIED_TEST.png')
    save(ROOT/'archive_receipt.json', {'archive': str(ARCHIVE), 'verified_test_screenshots': str(SHOTS),
                                       'every_copy_SHA256_verified': True, 'no_completion_credit': True})
    print('V782 integration/first-family checkpoint archived.367 completed,420 source-prose,53 drafts;other actual families remain open.', flush=True)


if __name__ == '__main__':
    main()
