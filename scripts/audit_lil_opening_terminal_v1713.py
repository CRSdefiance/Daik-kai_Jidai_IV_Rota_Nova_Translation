"""Reconcile the terminal cold boot to the byte-identical registered V1711."""
import json
from pathlib import Path
from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_opening_terminal_v1713')
RUN = Path('work/analysis/lil_opening_trace_v1706')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY')
RELEASE = Path('work/analysis/lil_opening_release_v1710')


if __name__ == '__main__':
    assert not ROOT.exists()
    release = read(RELEASE/'registered_release_verification.json')
    rom = Path(release['candidate']); digest = sha(rom.read_bytes())
    assert digest == release['candidate_sha256']
    assert release['registered_ROM_whole_file_byte_exact_to_actual_scene_research_ROM']
    report, terminal, observer, plan = [read(p) for p in
        [CAP/'capture_report.json', RUN/'terminal.json', CAP/'observer/commands.json', RUN/'run_plan.json']]
    assert report['ROM_sha256'] == terminal['research_ROM_sha256'] == plan['research_ROM_sha256'] == digest
    assert report['frames'] == 22930 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and 'battery_save_preloaded' not in report
    assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert terminal['terminal'] and terminal['observer_instances'] == 1
    assert terminal['observer_host_slots_restored'] and terminal['no_gameplay_fixture_save_or_ROM_runtime_edit']
    assert observer['all_host_slots_restored_and_core_file_exact']
    assert observer['errors'] == [] and observer['mismatches'] == 0
    assert sha(harness.CORE.read_bytes()) == report['core_DLL_sha256']
    assert sha(Path(harness.__file__).read_bytes()) == plan['harness_sha256']
    assert sha(Path(plan['original_readonly_observer']).read_bytes()) == plan['original_observer_sha256'] == observer['observer_sha256']
    assert sha((RUN/'source_contract.json').read_bytes()) == plan['source_contract_sha256'] == observer['source_contract_sha256']
    assert sha(Path(plan['original_inputs']).read_bytes()) == plan['inputs_sha256']
    prefix_path = Path('work/analysis/lil_opening_scene_v1708/immutable_completed_B22_trace_prefix.json')
    prefix = read(prefix_path)['rows']
    assert len(prefix) == 180 and observer['rows'][:180] == prefix
    assert len(observer['rows']) == observer['callbacks'] == 185
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] for r in observer['rows'])
    image = NdsImage.open(rom)
    blocks = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    for r in observer['rows']:
        s = r['source']
        assert s['classification'] == 'original_SC_cache' and s['route'] == 2
        assert s['whole_resident_payload_exact_ROM']
        assert sha(Path(s['actual_payload_file']).read_bytes()) == s['actual_sha256'] == sha(blocks[s['block']])
    tail = observer['rows'][180:]
    assert [r['kind'] for r in tail] == ['before_command','after_command','before_command','after_command','before_command']
    assert all(r['source']['block'] == 120 for r in tail)
    assert [r['source']['instruction_offset'] for r in tail] == [8,8,10,10,12]
    assert observer['unreturned_at_capture_end'] == [{'player':tail[-1]['player'],'entry_row':184}]
    assert tail[-1]['source']['first_word'] == 0x4000
    # The pending command is the next scene's first speech, deliberately held for review.
    assert tail[-1]['frame'] == 22628
    journal_path = CAP/'navigation_command_journal.json'
    journal = read(journal_path)
    source_commands = [json.loads(s) for s in (RUN/'navigation.jsonl').read_text().splitlines() if s.strip()]
    assert source_commands == [r['command'] for r in journal['commands_received']]
    assert journal['ROM_sha256'] == digest and journal['completion_confirmed']
    assert all(r['validation_passed'] for r in journal['commands_received'])
    assert source_commands[-1] == {'stop':True}
    schedule = list(read(plan['original_inputs']))
    # The original inputs file is the exact harness list, followed by ordinary live buttons.
    for r in journal['commands_received']:
        cmd = r['command']
        assert set(cmd) <= {'until','duration','buttons','stop'}
        if cmd.get('buttons'):
            schedule.append({'start':r['frame']+1,'duration':cmd['duration'],'buttons':cmd['buttons']})
    assert schedule == report['scripted_input_schedule']
    pictures = []
    for r in report['frames_captured']:
        path = Path(r['path']); assert sha(path.read_bytes()) == r['PNG_sha256']
        assert list(Image.open(path).size) == r['dimensions'] == [256,384]
        pictures.append({'path':str(path),'frame':r['frame'],'sha256':r['PNG_sha256']})
    snapshots = {}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        path = Path(r['path']); data = path.read_bytes()
        assert len(data) == r['bytes'] == 4194304 and sha(data) == r['sha256'] and r['read_only_export']
        snapshots[str(path)] = r['sha256']
    scene_path = Path('work/analysis/lil_opening_scene_v1708/complete_B22_actual_scene_proof.json')
    scene = read(scene_path)
    assert scene['research_ROM_sha256'] == digest and len(scene['dialogues']) == 49
    assert scene['all90_original_command_entry_return_pairs_and_entire3292_byte_resident_source_verified']
    for group in scene['dialogues']:
        assert len(group['two_full_actual_font_holds']) == 2
        assert group['whole_native_body_ink_and_caption_stable']
        assert group['all_letters_margins_bounds_and_no_extra_text_verified']
        for hold in group['two_full_actual_font_holds']:
            assert sha(Path(hold['capture']).read_bytes()) == hold['capture_sha256']
    visual_path = Path('work/analysis/lil_opening_references_v1709/actual_visual_review.json')
    visual = read(visual_path)
    assert visual['all5_actual_sheets49_panels_actually_viewed']
    for r in scene['actual_review_sheets']:
        assert sha(Path(r['path']).read_bytes()) == r['sha256']
    startup_path = RELEASE/'ordinary_startup_verification.json'
    startup = read(startup_path)
    assert startup['candidate_sha256'] == digest and startup['all8_complete_startup_title_NewGame_frames_exact']
    assert startup['no_battery_save_savestate_or_fixtures']
    assert sha(Path(startup['review_sheet']).read_bytes()) == startup['review_sheet_sha256']
    old = NdsImage.open('out/all_routes_combined_v1676_candidate.nds')
    assert all(image.read_file(p) == old.read_file(p) for p in ['/COMMON/MESFILE.DK4','/__arm9__.bin'])
    shop_path = Path('work/analysis/search_reports_release_v1675/photographed_shop_formatting.json')
    shop = read(shop_path)
    assert all(r['no_authored_indent_internal_gap_or_stray_Discover'] for r in shop['entries'])
    assert sha(Path(shop['reference']).read_bytes()) == shop['reference_sha256']
    saves = [{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
        for p in (CAP/'saves').rglob('*') if p.is_file()]
    ROOT.mkdir(parents=True)
    save(ROOT/'startup_visual_review.json', {'candidate_sha256':digest,
        'all8_startup_title_NewGame_panels_actually_viewed':True,
        'sheet':startup['review_sheet'],'sheet_sha256':startup['review_sheet_sha256']})
    save(RELEASE/'photographed_shop_preservation.json', {'candidate_sha256':digest,
        'COMMON_and_ARM9_byte_exact_to_V1676':True,'inherited_proof':str(shop_path),
        'inherited_proof_sha256':sha(shop_path.read_bytes()),'entries':shop['entries'],
        'new_shop_visit_claimed':False,'global_formatting_audit_still_open':True})
    save(ROOT/'terminal_scene_and_registered_ROM_reconciliation.json', {
        'candidate':str(rom),'candidate_sha256':digest,'terminal_frame':22930,
        'actual_ROM_whole_file_byte_exact_to_registered_candidate':True,
        'all49_dialogues98_complete_holds_and90_original_commands_verified':True,
        'all_original_three_joins_and_normal_Amsterdam_town_return_verified':True,
        'complete_B22_proof':str(scene_path),'complete_B22_proof_sha256':sha(scene_path.read_bytes()),
        'final_observer_prefix_exact_to_immutable180_rows':True,
        'all185_callbacks_preserved_CPU_RAM_and_configuration_at_boundaries':True,
        'observer_errors_or_mismatches':0,'host_observer_slots_restored_and_core_file_exact':True,
        'readonly_observer_does_not_exclude_temporary_write_then_restore':True,
        'cold_boot_no_preloaded_battery_save_no_savestate_no_gameplay_fixtures':True,
        'entire_input_journal_matches_terminal_schedule':True,
        'captured_PNGs':pictures,'all_unique4MiB_RAM_snapshots':snapshots,
        'runtime_generated_isolated_saves_retained':saves,
        'next_observed_source':{'file':'/data/SC2.DK4','block':120,'speech_command_offset':12,
            'entry_frame':22628,'complete_holds':[22900,22930],
            'original_source_payload_sha256':sha(blocks[120]),'unchanged_from_V1676':True,
            'pending_first_speech_intentional_at_terminal':True,
            'editorial_completion_claimed':False},
        'prior_checkpoint_B23_or_Bruges_following_scene_assumption_corrected_by_original_trace':True,
        'no_Bruges_arrival_full_route_or_hardware_verification_claim':True,
        'all8_fixture_free_startup_controls_and_viewed_sheet_verified':True,
        'COMMON676_677_repaired_layout_preserved_without_new_shop_visit':True,
        'proofs':{str(p):sha(p.read_bytes()) for p in [CAP/'capture_report.json',CAP/'observer/commands.json',
            RUN/'terminal.json',RUN/'run_plan.json',RUN/'navigation.jsonl',journal_path,prefix_path,visual_path,startup_path]},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Terminal22930: all49/98 holds,90 B22 commands,185 readonly callbacks and every capture/snapshot hash pass; registered V1711 exact.', flush=True)
    print('Observed next source is SC2 B120, held at its first speech; B120/B23/later Bruges remain unreviewed.', flush=True)
