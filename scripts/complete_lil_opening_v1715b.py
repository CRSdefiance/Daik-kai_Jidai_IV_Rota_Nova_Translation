"""Close all49 source/native/actual opening reviews without closing the full goal."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
import json
import os

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_opening_completion_v1715b')
RELEASE = Path('work/analysis/lil_opening_release_v1710/registered_release_verification.json')
ACTUAL = Path('work/analysis/lil_opening_terminal_v1713b/terminal_scene_and_registered_ROM_reconciliation.json')
MANUSCRIPT = Path('translations/lil_opening_editorial_manuscript_v2.json')
FINAL = Path('translations/lil_opening_final_review_v1.json')
GUIDE = Path('E:/Rota Nova translations/Guide screenshots/V1711 Lil Amsterdam opening verified')


if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not GUIDE.exists()
    release, actual, doc = map(read, (RELEASE, ACTUAL, MANUSCRIPT))
    rom = Path(release['candidate']); digest = sha(rom.read_bytes())
    assert digest == release['candidate_sha256'] == actual['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and release['all474_batches114_accepted_layers_and_prior_profiles_preserved']
    assert sha(Path(release['patch']).read_bytes()) == release['patch_sha256']
    assert actual['all49_dialogues98_complete_holds_and90_original_commands_verified']
    assert actual['all8_fixture_free_startup_controls_and_viewed_sheet_verified']
    assert actual['COMMON676_677_repaired_layout_preserved_without_new_shop_visit']
    assert actual['observer_errors_or_mismatches'] == 0
    assert doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
    assert not doc['formatting_review_pending'] and len(doc['records']) == 49
    assert sum(r['editorial_decision']=='revise' for r in doc['records']) == 43
    assert sum(r['editorial_decision']=='retain-wording' for r in doc['records']) == 6
    mapping_path = Path('translations/lil_opening_editorial_relocation_map_v1.json')
    mapping = read(mapping_path); refs = {r['id']:r for r in mapping['records']}
    scene = read(actual['complete_B22_proof']); holds = {r['id']:r for r in scene['dialogues']}
    clean = NdsImage.open('work/clean.nds'); image = NdsImage.open(rom)
    source = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[22]
    target = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[22]
    assert sha(target) == mapping['target_block_sha256']
    ledger_path = Path('translations/editorial_review_current_v1.json')
    raw = ledger_path.read_bytes(); ledger = read(ledger_path); before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],
        ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass']) == (1375,1033,342,1568)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs']) == 144
    family = 'Lil-Amsterdam-opening49'
    assert not any(f['id']==family for f in ledger['completed_editorial_families'])
    rows = []
    for original in doc['records']:
        row = deepcopy(original); ident = row['id']; ref = refs[ident]
        assert all(row['review'].values()) and ident in holds
        s = row['source_reference']; source_bytes = bytes.fromhex(row['source_hex'])
        assert source[s['offset']:s['offset']+s['bytes']] == source_bytes
        value = bytes.fromhex(ref['target_hex']); offset = ref['new_offset']
        assert target[offset:offset+len(value)] == value
        assert target[offset-5:offset] == source[s['offset']-5:s['offset']] == b'\0\x40\xff\xff\0'
        assert value[:1] == source_bytes[:1]
        row.update(previous_current_reference=row['current_reference'],previous_current_text_hex=row['current_text_hex'],
            current_reference={'file_path':'/data/SC2.DK4','block':22,'offset':offset,'bytes':len(value),
                'header_offset':offset-5,'record_index':row['record_index']},
            current_text_hex=value.hex(),current_English=row['english'],
            completed_candidate_reference=str(rom),completed_candidate_sha256=digest,
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-after-source-native-review',
            status='complete-source-native-and-individual-original-gameplay',
            reference_map=str(mapping_path),actual_proof=str(ACTUAL),
            actual_holds=holds[ident]['two_full_actual_font_holds'],individually_activated_in_gameplay=True)
        rows.append(row)
    scope = ('All49 original Lil Amsterdam-opening speeches in SC2 B22 individually activated with98 complete pixel-exact holds, '
        'all90 original commands completed,three original crew joins dismissed,and normal Amsterdam town return observed. '
        'Cold boot without preloaded battery save,savestate,cheats,location or gameplay fixtures. The tested research ROM is byte-identical '
        'to registered V1711. Only SC2 B22 differs from V1676;335 other blocks,every other file,ARM9,COMMON,fonts,graphics and123040 staged bytes remain exact. '
        'The actual following source is SC2 B120 at offset12,not assumed B23;its first speech remains pending at terminal22930. '
        'No B120/B23/Bruges editorial completion,full route orhardware claim. All8 startup controls and inherited photographed676/677 corrections pass. '
        'V1711 remains experimental;V1492 remains promoted;canonical construction baseline unchanged. Full editorial goal and separate graphics/all18 plaques remain open.')
    ROOT.mkdir(parents=True)
    save(ROOT/'coverage_before_completion.json',before)
    proof_paths = [RELEASE,ACTUAL,MANUSCRIPT,mapping_path,Path(actual['complete_B22_proof']),
        Path('work/analysis/lil_opening_release_v1710/ordinary_startup_verification.json'),
        Path('work/analysis/lil_opening_release_v1710/photographed_shop_preservation.json'),
        Path(doc['native_macro_proof']),Path(doc['native_font_proof']),Path(doc['visual_review'])]
    proofs = {str(p):sha(p.read_bytes()) for p in proof_paths}
    save(FINAL,{'format':'dk4-editorial-family-final-review-v1','file_path':'/data/SC2.DK4','block':22,
        'records':rows,'record_IDs':[r['id'] for r in rows],'manuscript':str(MANUSCRIPT),
        'candidate':str(rom),'candidate_sha256':digest,'proofs':proofs,'actual_verification_scope':scope,
        'completed_entries':49,'revised':43,'retained':6,'full_goal_complete':False})
    ledger['completed_editorial_families'].append({'id':family,'file_path':'/data/SC2.DK4','block':22,
        'record_IDs':[r['id'] for r in rows],'records':rows,'final_review':str(FINAL),
        'documentation':'docs/lil_opening_v1715_completion.md','actual_verification_scope':scope})
    unit = next(u for u in ledger['coverage_units'] if u['id']==family+'-source-prose')
    assert set(unit['record_IDs']) == set(refs)
    unit.update(status='superseded-by-complete-family',completed_family=family,final_review=str(FINAL))
    ledger['coverage_units'].append({'id':family,'file_path':'/data/SC2.DK4','block':22,
        'record_IDs':[r['id'] for r in rows],'status':'complete-source-native-and-individual-original-gameplay',
        'final_review':str(FINAL),'actual_proofs':[str(ACTUAL)],'completed_entries_added':49,'full_goal_complete':False})
    ledger['records_editorially_completed'] += 49
    ledger['records_revised_and_integrated'] += 43
    ledger['retained_wordings_editorially_completed'] += 6
    ledger['completed_editorial_record_counts_by_file']['/data/SC2.DK4'] += 49
    drafts = ledger['active_source_prose_drafts']
    for key, ids in drafts['route_record_subsets_pending'].items():
        drafts['route_record_subsets_pending'][key] = [i for i in ids if i not in refs]
    assert not any(drafts['route_record_subsets_pending'].values())
    drafts.update(status='144-reviewed-COMMON-and-broader-prose-open',
        note='All49 Lil Amsterdam-opening entries completed in V1711. Earlier144 reviewed COMMON and broader shared/routes/player-facing prose remain.')
    ledger.setdefault('integrated_candidate_reference_history',[]).append(deepcopy(ledger['current_integrated_candidate']))
    ledger['current_integrated_candidate'] = {'path':str(rom),'sha256':digest,'profile':release['profile'],
        'MESFILE_sha256':release['COMMON_sha256'],'ARM9_sha256':release['ARM9_sha256'],
        'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'manifest':str(rom.with_suffix('.manifest.json')),'status':'experimental-verified-editorial-checkpoint-not-promoted',
        'details':scope,'full_goal_complete':False}
    ledger.setdefault('native_completed_reference_history',[]).append(deepcopy(ledger['current_native_relocation_reference']))
    ledger['current_native_relocation_reference'].update(candidate=str(rom),candidate_sha256=digest,
        COMMON_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'])
    ledger['latest_registered_editorial_candidate'] = {**release,'status':'experimental-individually-verified-Lil-opening',
        'final_review':str(FINAL),'actual_proof':str(ACTUAL),'full_goal_complete':False}
    ledger['lil_opening_editorial_v1715'] = {'status':'complete49','manuscript':str(MANUSCRIPT),
        'final_review':str(FINAL),'actual_proof':str(ACTUAL),'registered_release':str(RELEASE),'full_goal_complete':False}
    ledger['formatting_watchlist']['Lil_Amsterdam_opening49'] = {'status':'completed-in-V1711',
        'literal_prefix_policy':'opt-in-native-guard-v255;historical-profiles-unchanged',
        'source_bound_runtime_and_relocation_map':True,'actual98_holds_and90_commands':True,
        'final_review':str(FINAL),'broader_route_formatting_audit_still_open':True}
    ledger['next_route_scene_editorial_packet'] = {'file_path':'/data/SC2.DK4','block':120,
        'source':'final original native observer at22628 and two complete holds22900/22930',
        'actual_proof':str(ACTUAL),'first_speech_offset':12,'editorial_review_complete':False,
        'following_B23_lesson_and_later_Bruges_also_open':True}
    summary = 'V1715 closes49 Lil Amsterdam-opening entries(43 revised6 retained):1424 complete(1076 revised348 retained),1568 source/prose reviewed;144 reviewed-incomplete COMMON plus broader routes/player-facing prose remain. '+scope
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1715-Lil-opening49-complete','proof':str(ROOT/'completion_receipt.json'),
        'completed_entries_added':49,'source_prose_reviews_added':0,'full_goal_complete':False})
    assert ledger['unresolved_graphics_work'] == before['unresolved_graphics_work']
    assert ledger['reviewed_but_incomplete_COMMON_IDs'] == before['reviewed_but_incomplete_COMMON_IDs']
    assert ledger['source_prose_reviewed_counts_by_file'] == before['source_prose_reviewed_counts_by_file']
    assert ledger['records_with_source_and_prose_pass'] == 1568
    assert ledger['goal_status'] == 'active' and ledger['full_goal_complete'] is False
    assert ledger['records_editorially_completed'] == sum(ledger['completed_editorial_record_counts_by_file'].values()) == 1424
    assert ledger['records_revised_and_integrated']+ledger['retained_wordings_editorially_completed'] == 1424
    pending = ledger_path.with_name('editorial_review_current_v1715_pending.json')
    assert not pending.exists() and ledger_path.read_bytes()==raw
    save(pending,ledger); assert read(pending)==ledger and ledger_path.read_bytes()==raw
    os.replace(pending,ledger_path)
    GUIDE.mkdir(parents=True); pictures=[]
    for index in (0,2,12,20,28,42,48):
        row = rows[index]; hold = row['actual_holds'][0]
        source_picture = Path(hold['capture']); target_picture = GUIDE/f'{index+1:02d}_{row["speaker"].replace(" ","_")}_{row["record_index"]:04d}.png'
        copy2(source_picture,target_picture)
        assert sha(target_picture.read_bytes())==hold['capture_sha256']
        pictures.append({'guide':str(target_picture),'source':str(source_picture),'sha256':hold['capture_sha256'],
            'record_ID':row['id'],'frame':hold['frame']})
    town = Path(scene['town_exit_capture']); town_copy = GUIDE/'50_Normal_Amsterdam_town_return.png'
    copy2(town,town_copy); assert sha(town_copy.read_bytes())==scene['town_exit_capture_sha256']
    pictures.append({'guide':str(town_copy),'source':str(town),'sha256':scene['town_exit_capture_sha256'],'frame':19760})
    save(GUIDE/'capture_provenance.json',{'candidate':str(rom),'candidate_sha256':digest,'captures':pictures,
        'captured_research_ROM_whole_file_identical_to_registered_candidate':True,
        'original256x384_lossless_framebuffer_captures':True,'no_save_savestate_or_gameplay_fixtures':True,
        'targeted_headless_DeSmuME_not_full_route_or_hardware':True,'verification':str(ACTUAL)})
    pins_path = Path('translations/rom_retention_pins.json'); pins = read(pins_path)
    for p,reason in [('E:/Rota Nova translations/Generated/out/all_routes_combined_v1711_candidate.nds','Current verified Lil opening49 cumulative editorial checkpoint;experimental,not promoted.'),
        (str(Path(release['reconstruction']).absolute()),'Exact V1711 clean-input patch reconstruction evidence.'),
        (str(Path(release['actual_scene_research_ROM']).absolute()),'Byte-identical actual49-dialogue98-hold and90-command cold-boot source.')]:
        if not any(x['path'].replace('\\','/').lower()==p.replace('\\','/').lower() for x in pins):pins.append({'path':p,'reason':reason})
    save(pins_path,pins)
    handoff = f'''# Current editorial handoff - V1715

## Active goal and verified accounting

Full scene-by-scene editorial review remains ACTIVE: natural faithful American English against clean Japanese, all routes and remaining player-facing prose. Approved Rafael, Joakim, Maria, Camille. Do not narrow or mark the goal complete, blocked or paused because this batch finished. No subagents authorized.

1424 entries complete =1076 revised +348 retained. 1568 source/prose reviewed. Exact earlier144 reviewed-incomplete COMMON IDs remain in translations/editorial_review_current_v1.json; broader untouched routes/shared/player prose remain. Completed counts:1374 COMMON +50 SC2 (opening49 and earlier B294 one). Unique record references and all49 retention/revision reasons: translations/lil_opening_final_review_v1.json. Source/prose count did not increase at this completion.

Separate graphics/all18 plaque audit remains unfinished. Accepted wood texture/borders do not close that audit. Four low-resolution Online bodies remain excluded;two brown marks preserved. Older-record re-audit remains queued after the full editorial goal. Sources/ read-only. Keep ALL generated ROMs;no pruning/policy bypass.

## Latest verified combined candidate

- ROM: out/all_routes_combined_v1711_candidate.nds.
- Physical: E:/Rota Nova translations/Generated/out/all_routes_combined_v1711_candidate.nds.
- ROM SHA256: {digest}.
- Patch: {release['patch']}; SHA256 {release['patch_sha256']}.
- Profile: all-routes-unified-v1711, experimental;474 manifest batches,114 accepted layers. Complete V1676 stack plus final runtime-bound lil_opening_editorial stage.
- Only SC2 B22 changes relative to V1676 (3000 to3292 bytes). All335 other SC2 blocks, every other file/component, ARM9, COMMON, fonts and graphics remain byte-exact. Staged payload remains123040 bytes.
- Canonical construction base remains out/raphael_natural_v2_accepted_base.nds, SHA256 3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
- Clean patch input work/clean.nds SHA256 f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d;reconstruction matches every candidate byte.
- V1492 remains promoted (tag promoted-v1492). Last pushed commit53c0b58c4be456731024a1e594c3121360395296,branch codex/combined-routes-v89. No new push/promotion authorized during this continuation. Canonical and historical V997 preserved.

## Completed opening evidence - do not repeat without a concrete risk

- Manuscript: translations/lil_opening_editorial_manuscript_v2.json (43 revisions6 retentions), natural-dialogue-v2/en-US;49 approved source/context/naturalness/native formatting reviews.
- Final review: translations/lil_opening_final_review_v1.json.
- Exact registration and clean patch: work/analysis/lil_opening_release_v1710/registered_release_verification.json.
- Final terminal audit: {ACTUAL}.
- Full B22 actual proof: work/analysis/lil_opening_scene_v1708/complete_B22_actual_scene_proof.json, reconciled by final audit. All49 individual speeches98 complete full-font/RGB holds,90 original command entry/return pairs,three crew joins and normal Amsterdam return.
- Actual cold boot: E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY. Terminal22930;no preloaded battery save,savestate or gameplay fixtures. Byte-identical whole ROM to registered V1711. Runtime-generated isolated save retained;not an input save.
- Observer commands185,errors0,mismatches0,host slots restored/core file exact. Prefix180 rows exactly matches closed B22 trace. Observer boundary snapshots do not rule out temporary write-restore.
- All8 fixture-free startup/title/Rafael New Game comparisons match V1105 and were visually viewed. Photographed shop676/677 corrections inherited via exact COMMON/ARM9;no new shop visit claimed.
- Native proofs: macro196 cases work/analysis/lil_opening_macro_v1698d,fonts49 planes work/analysis/lil_opening_fonts_v1699b,seven native sheets andfive actual sheets actually viewed. 73 formatter tests passed in work/analysis/lil_opening_checks_v1702/formatter_regression.xml.
- Reference map: translations/lil_opening_editorial_relocation_map_v1.json. Original EV2 block-index loader/cache/initial offset8 and full90 straight-through commands;not a global map for arbitrary blocks.
- New native profile opts into existing V255 literal guards;historical profiles retain forbid default. Direct generic playable batching is rejected;source/runtime-bound post-layer required. Do not weaken macro/control guards or shorten prose to fit old slots.

## Next work and corrected scene identity

Authoritative terminal native source is SC2 B120,first speech command offset12,entry22628,complete captures22900/22930. Earlier summary guessed B23/following Bruges:that was incorrect. B120 is the sailing lesson ('At sea at last...' source record;runtime displayed revised natural English/Camille via existing catalog). It remains editorially unreviewed. B23 is a later lesson continuation;Bruges arrival was NOT reached. No full-route/hardware claim.

Next: create clean Japanese/current/runtime context packet for B120 and linked lesson branches,then review prose and source controls before authoring. Alternatively complete exact earlier144 pending COMMON entries where original contexts are available. Do not repeat completed hot-spring RNG campaign or completed B22.

Context-unmapped shop750-752 remain open. V1688b production SC matches750/752 are CS body-length fields;alternate testdata SC3 B164 CS0101 word750 remains unclassified. No unused-text claim. Sighting close-range pilot V1693 stopped at Syracuse Dock prompt,not a sighting. An unloaded enemy null mobile pointer is not inactivity proof;original eligibility vtable+10 returned1. Use an original open-water context;do not force seen flags/events. 'Vicinity'/Armed Latina actual UI remains pending.

## Process and preservation

All jobs in this batch are terminal: build47985,actual93757/22930,navigators,patch43185,startup7410/title and verification. Never restart a process merely because an observation times out;poll its same handle or inspect authoritative live state.

Read AGENTS.md,docs/build_continuity_protocol.md,release_stack,relevant known_issues before build;natural_dialogue_workflow/dialogue_delegation_protocol before prose. Executed research producers/proofs are frozen;use explicit successors. V1713 failed before writing proof because it mistook journal completion_confirmed (always false by harness design) for terminal evidence. V1713b audits final terminal report/captures/inputs instead and passes;both producers retained. Do not rewrite either. Locked manuscript/map/profile/runtime dependencies must remain exact.

Python C:/Python314/python.exe;PYTHONUTF8=1;PYTHONPATH=.;.deps. Sandbox launcher fails on P-drive credentials;use scoped require_escalated. out and work/analysis are E junctions;archive lexical absolute paths without resolve(). Eight guide captures/provenance: {GUIDE}.
'''
    Path('docs/editorial_handoff_current.md').write_text(handoff,encoding='utf-8')
    Path('docs/lil_opening_v1715_completion.md').write_text('# V1715 Lil Amsterdam opening complete\n\n'+summary+'\n\nSee editorial_handoff_current.md for release,proofs,test scope and next scene.\n',encoding='utf-8')
    for name in ['translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:
            f.write('\n\n## V1715 Lil Amsterdam opening49 complete\n\n'+summary+'\n\nSee [completion](lil_opening_v1715_completion.md).\n')
    save(ROOT/'completion_receipt.json',{'candidate':str(rom),'candidate_sha256':digest,
        'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'newly_completed':49,'newly_revised':43,'newly_retained':6,
        'completed':1424,'revised':1076,'retained':348,'source_prose':1568,'reviewed_incomplete_COMMON':144,
        'complete_COMMON':1374,'complete_SC2':50,'final_review':str(FINAL),'proofs':proofs,
        'guide':str(GUIDE),'screenshots':pictures,'all_current_jobs_terminal':True,
        'canonical_V1492_promotion_prior_profiles_graphics_and_all_ROMs_preserved':True,
        'next_native_source_SC2_B120_not_B23_or_Bruges':True,
        'ledger_sha256':sha(ledger_path.read_bytes()),'handoff_sha256':sha(Path('docs/editorial_handoff_current.md').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Closed49 entries:1424 complete(1076 revised348 retained),1568 source/prose,144 earlierCOMMON pending. V1711/exact patch and all scene/startup gates pass;8 guide captures saved;full goal ACTIVE.',flush=True)
