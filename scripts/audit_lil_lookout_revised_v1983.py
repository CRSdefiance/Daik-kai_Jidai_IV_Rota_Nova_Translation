"""Focused Lookout/neighbor pixels, all original B23 results and normal return."""
import struct
import sys
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Lookout_actual_v1983')
RUN = Path('work/analysis/lil_Lookout_revised_run_v1982')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Lookout_revised_run_v1982_RESEARCH_ONLY')
MAP = Path('work/analysis/lil_Lookout_relocation_v1980/current_B23_typed_relocation_research.json')
OLD = Path('work/analysis/lil_crew_scene_v1763_final/complete_B23_scene_and_fixture_audit.json')
OLD_CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_crew_final_text_v1764_RESEARCH_ONLY')
BASE = 0x02000000

if __name__ == '__main__':
    assert not ROOT.exists()
    source = Path('scripts/verify_lil_crew_scene_v1763b.py')
    prefix = source.read_text(encoding='utf-8').split('    mapping=read(')[0]
    assert prefix.count("'lil_crew_final_text_v1764'") == 1
    prefix = prefix.replace("'lil_crew_final_text_v1764'","'lil_Lookout_revised_run_v1982'")
    old_root = "ROOT=Path('work/analysis/lil_crew_scene_v1763_'+args.version)"
    assert prefix.count(old_root) == 1
    prefix = prefix.replace(old_root,"ROOT=Path('work/analysis/lil_Lookout_actual_v1983')")
    argv = sys.argv
    sys.argv = [__file__,'--version','final']
    env = {'__name__':'__main__','__file__':__file__}
    try: exec(compile(prefix,str(source),'exec'),env)
    finally: sys.argv = argv
    # Prefix verifies exact inputs/schedules/PNGs/all4MiB snapshots, the one
    # coordinate-only fixture, all readonly callbacks and restored host slots.
    trace, arm, photos, snapshots, fixture, recomputed, digest = (
        env[k] for k in ('trace','arm','photos','snapshots','fixture','recomputed','digest'))
    plan, old = map(read,(MAP,OLD))
    assert digest == plan['research_ROM_sha256']
    for name, expected in old['proofs'].items(): assert sha(Path(name).read_bytes()) == expected,name
    old_trace = read(OLD_CAP/'observer/commands.json')
    rows = [r for r in trace['rows'] if r['source'].get('route') == 2 and r['source'].get('block') == 23]
    prior = [r for r in old_trace['rows'] if r['source'].get('route') == 2 and r['source'].get('block') == 23]
    assert len(rows) == len(prior) == 92
    mapped = {r['new_offset']:r for r in plan['mapped_native_commands']}
    edges = {r['new_offset']:r for r in plan['relative_skip_fixups']}
    results, previous = [], 0
    for index,(before,after,old_before,old_after) in enumerate(zip(rows[::2],rows[1::2],prior[::2],prior[1::2],strict=True)):
        src = before['source']
        command = mapped[src['instruction_offset']]
        assert before['kind'] == old_before['kind'] == 'before_command'
        assert after['kind'] == old_after['kind'] == 'after_command'
        assert before['source'] == after['source']
        assert trace['rows'][after['entry_row']] == before
        assert command['old_offset'] == old_before['source']['instruction_offset']
        assert src['first_word'] == old_before['source']['first_word'] == command['word']
        assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256'] == plan['research_block_sha256']
        assert old_before['source']['actual_sha256'] == plan['source_block_sha256']
        assert after['result_words'] == old_after['result_words']
        if command['word'] in (0x100,0x200,0x300):
            edge = edges[src['instruction_offset']]
            taken = command['word'] == 0x100 or (command['word'] == 0x200 and previous == 0) or (command['word'] == 0x300 and previous == 1)
            extent = (edge['new_matched_skip_target'] if taken else edge['new_unmatched_next'])-src['instruction_offset']
        else: extent = command['new_native_extent']
        assert after['decoded_length'] == extent
        if after['result_words'][0] == 2: previous = after['result_words'][1]
        if index+1 < len(rows)//2:
            assert rows[2*index+2]['source']['instruction_offset'] == src['instruction_offset']+extent
        results.append(dict(old_offset=command['old_offset'],new_offset=src['instruction_offset'],word=command['word'],
            native_result_words=after['result_words'],native_decoded_extent=extent,frames=[before['frame'],after['frame']],
            old_frames=[old_before['frame'],old_after['frame']]))
    assert rows[-1]['source']['first_word'] == 0 and rows[-1]['result_words'][0] == 0
    old_lesson = [r for r in old_trace['rows'] if r['source'].get('route') == 2 and r['source'].get('block') == 120]
    new_lesson = [r for r in trace['rows'] if r['source'].get('route') == 2 and r['source'].get('block') == 120]
    assert len(old_lesson) == len(new_lesson)
    for a,b in zip(old_lesson,new_lesson,strict=True):
        assert a['kind'] == b['kind'] and a['source']['instruction_offset'] == b['source']['instruction_offset']
        assert a['source']['actual_sha256'] == b['source']['actual_sha256']
        if a['kind'] == 'after_command':
            assert a['result_words'] == b['result_words'] and a['decoded_length'] == b['decoded_length']
    current_rows = {r['id']:r for r in read('translations/lil_lessons_editorial_manuscript_v6.json')['records']}
    old_fonts = {r['id']:r for r in read('work/analysis/lil_Deck_label_approval_v1758/all60_current_native_font_reconciliation.json')['cases']}
    new_case = read('work/analysis/lil_Lookout_affiliation_fonts_v1978/one_changed_native_macros_and_complete_font_plane.json')['cases'][0]
    changed = plan['text_records'][0]
    wrapped = struct.unpack_from('<I',arm,0x54450)[0]
    groups = []
    for ident, frames in (('DK4_MES_B23_R0138',(39110,39140)),('DK4_MES_B23_R0142',(39440,39470)),('DK4_MES_B23_R0146',(39770,39800))):
        row = current_rows[ident]
        old_at = row['current_reference']['offset']-5
        command = next(r for r in plan['mapped_native_commands'] if r['old_offset'] == old_at)
        active = next((a,b) for a,b in zip(rows[::2],rows[1::2],strict=True) if a['source']['instruction_offset'] == command['new_offset'])
        case = new_case if ident == 'DK4_MES_B23_R0142' else old_fonts[ident]
        preview = Image.open(case['preview']).convert('RGB')
        assert preview.size == (216,64)
        wanted = {(16+x,296+y) for y in range(64) for x in range(216) if preview.getpixel((x,y)) == (0,8,0)}
        body = (bytes.fromhex(changed['target_hex']) if ident == 'DK4_MES_B23_R0142' else bytes.fromhex(row['current_text_hex']))[1:]
        body = body.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        holds = []
        for at in frames:
            assert active[0]['frame'] < at < active[1]['frame']
            raw = Path(snapshots[at]['path']).read_bytes()
            im = Image.open(photos[at]['path']).convert('RGB')
            actual = {(x,y) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y)) == (0,8,0)}
            assert actual == wanted and cstring(raw,wrapped) == body
            src = active[0]['source']
            assert sha(raw[src['payload_address']-BASE:src['payload_address']-BASE+src['payload_bytes']]) == plan['research_block_sha256']
            holds.append(dict(frame=at,capture=photos[at]['path'],capture_sha256=photos[at]['PNG_sha256'],
                RAM_sha256=snapshots[at]['sha256'],complete_native_independent_actual_ink_equal=True))
        groups.append(dict(id=ident,source=active[0]['source'],holds=holds))
    terminal = Path(snapshots[41420]['path']).read_bytes()
    cpu,get = get_machine(arm,terminal)
    town = get(0x34674,get(0xCB1A8)+4+2*132)
    assert town == 3 and bytes(cpu.mem_read(BASE,0x400000)) == terminal
    current_return = Image.open(photos[41420]['path']).convert('RGB')
    old_return = Image.open(old['terminal_capture']['path']).convert('RGB')
    same_return = current_return.tobytes() == old_return.tobytes()
    ROOT.mkdir(parents=True)
    save(ROOT/'focused_Lookout_neighbors_original_B23_results_and_return.json',dict(candidate=env['plan']['research_ROM'],candidate_sha256=digest,
        terminal_frame=41420,focused_glyph_groups=groups,changed_Lookout_two_holds_complete_native_actual_ink=True,
        preceding_and_following_Camille_four_holds_complete_native_actual_ink=True,
        original_B23_native_command_results_preserved=results,all46_original_B23_command_results_and_mapped_targets_equal=True,
        all_unowned_B120_command_results_and_source_offsets_unchanged=True,unowned_B120_executed_pairs=len(new_lesson)//2,
        original_choice0_full_crew_lesson_and_normal_type0_return=True,normal_Bruges_town_ID=town,
        terminal_capture=photos[41420],whole_terminal_RGB_equal_original=same_return,
        one16_coordinate_byte_fixture_replay_exact=True,all_inputs_schedule_PNGs4MiB_snapshots_and_readonly_observers_host_restoration_pass=True,
        no_event_RNG_character_choice_outcome_or_funds_override=True,no_new_gameplay_claim_for_other_conditional_paths=True,
        actual_scope='One original crew-lesson path reexecuted. New full glyph comparisons cover the changed Lookout speech andtwo adjacent Camille speeches,six holds total. Other27 B23speeches execute inthis path withunchanged source-bound native planes;no fresh per-panel pixel claim. Three other B23speech objects areunvisited onthis path. Earlier both-choice/wind proofs remaininherited only.',
        source_reference_plan=str(MAP),source_reference_plan_sha256=sha(MAP.read_bytes()),
        fixture=fixture,fixture_recomputed=recomputed,visual_review_pending=True,
        registered_release_and_fresh_contextual_reconciliation_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in (MAP,OLD,source,RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',
            CAP/'capture_report.json',CAP/'observer/commands.json')},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(changed_Lookout_holds=2,neighbor_holds=4,B23_original_results=46,Bruges_return=True,
        whole_return_RGB_equal_original=same_return,one16_byte_fixture_exact=True,registered_integration_pending=True))
