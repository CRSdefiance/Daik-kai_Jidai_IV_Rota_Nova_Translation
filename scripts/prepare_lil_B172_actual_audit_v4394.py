"""Derive B172's complete content audit without repeating its terminal boots."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B172_actual_tools_v4394')
SOURCE = Path('scripts/audit_lil_B171_actual_v4342.py')
TARGET = Path('scripts/audit_lil_B172_actual_v4394.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text = SOURCE.read_text(encoding='utf-8')
    start = text.index('        selected = [row for row in pairs')
    stop = text.index('        for pending in trace', start)
    text = text[:start] + '''        selected = [row for row in pairs if row['block'] == 22]
        assert len(intervals) == len({row['id'] for row in intervals}) == 27
        assert not any(row['word'] in [0x8000,0x100,0x200,0x300,0x400,0x2000] for row in selected)
        native = {row['offset']: row for row in fixture['all47_stored_fixture_commands']}
        cursor, expected = 8, []
        while True:
            command = native[cursor]
            expected.append(cursor)
            if command['word'] == 0:
                break
            cursor += command['native_extent']
        assert len(expected) == 47 and [row['offset'] for row in selected] == expected
        assert selected[-1]['word'] == 0 and selected[-1]['original_source_offset'] == 1880
        assert sum(row['word'] == 0xA000 for row in selected) == 5
        effects = [row for row in selected if row['word'] == 0xA000 and row.get('original_source_block') == 172]
        assert len(effects) == 1 and effects[0]['original_source_offset'] == 1870
        effect_object = commands[effects[0]['offset']]
        assert effect_object['whole_command_hex'] == '00a0ffff010cc960'
        c200 = [row for row in selected if row['word'] == 0xC200]
        assert len(c200) == 1 and c200[0]['original_source_offset'] == 1868
        resources = [row for row in selected if row.get('original_source_block') == 172 and row['word'] & 0xFF00 == 0x6300]
        assert [row['word'] for row in resources] == [0x6329,0x6340,0x632A]
        presentations = [row for row in selected if row.get('original_source_block') == 172 and row['word'] in [0x6000,0x45FF,0x4651,0x4620,0x6240]]
        assert [row['word'] for row in presentations] == [0x6000,0x45FF,0x4651,0x4620,0x6240]
        assert [row['original_source_offset'] for row in presentations] == [8,10,18,1218,1878]
        assert sum(row['prefix'] == 254 for row in intervals) == 0
        final_speech = next(row for row in intervals if row['id'] == 'DK4_MES_B172_R0100')
        departing_speech = next(row for row in intervals if row['id'] == 'DK4_MES_B172_R0062')
        interrupted_speech = next(row for row in intervals if row['id'] == 'DK4_MES_B172_R0065')
        assert departing_speech['returned'] <= presentations[3]['start'] <= presentations[3]['returned'] <= resources[2]['start'] <= resources[2]['returned'] <= interrupted_speech['start']
        assert final_speech['returned'] <= c200[0]['start'] <= c200[0]['returned'] <= effects[0]['start'] <= effects[0]['returned'] <= presentations[4]['start'] <= presentations[4]['returned'] <= selected[-1]['start']
''' + text[stop:]
    start = text.index('        versions.append(dict(')
    stop = text.index('        photosets[case]', start)
    text = text[:start] + '''        versions.append(dict(case=case,source_block=172,ROM_sha256=report['ROM_sha256'],frames=20001,
            input_schedule=rp['original_inputs'],input_schedule_sha256=rp['inputs_sha256'],
            capture_report=str(paths[2]),observer_report=str(paths[3]),selected_B22_command_pairs=selected,
            selected_intervals=intervals,actual_C200=c200[0],actual_resources=resources,
            actual_presentation_commands=presentations,actual_source_A000=effects[0],
            source_A000_hex=effect_object['whole_command_hex'],
            departure_interval=[departing_speech,presentations[3],resources[2],interrupted_speech],
            final_C200_A000_return_interval=[final_speech,c200[0],effects[0],presentations[4],selected[-1]],
            fixture_exit_frame=selected[-1]['returned'],single_source_end_offset=1880,
            following_observed_blocks=sorted({row['block'] for row in pairs if row['block'] != 22}),
            all_retained_linear_control_flow_matches_original_commands=True,
            all27_speeches_five_presentations_three_resources_C200_then_A000_and_single_end_observed=True))
''' + text[stop:]
    start = text.index('    counts = Counter(')
    stop = text.index('    assert not failures', start)
    text = text[:start] + '''    counts = Counter(row['word'] for row in versions[1]['selected_B22_command_pairs'])
    save(ROOT/'actual_all27_presentations_resources_C200_A000_and_end.json',dict(versions=versions,
        actual_panels=actual,fresh_actual_unique_speech_panels=len(actual),complete_matching_observations=sum(bool(row['holds']) for row in actual),
        offline_only_display_IDs=offline,failures=failures,paired_region_differences=region_differences,
        review_sheets=sheets,visual_review_pending=True,actual_new_cold_boot_runs=2,
        selected_command_counts={format(word,'04X'):count for word,count in counts.items()},
        all38_source_commands_and_single_stored_end_preserved=True,
        all27_linear_progressive_speeches_observed=True,
        original_five_presentations_three_resources_C200_then_A0006240_and_end_executed=True,
        source_presentation_resource_and_A000_results_recorded_without_semantic_inference=True,
        actual_source_event172_not_selected=True,
        no_earned_recruitment_natural_eligibility_full_playthrough_or_hardware_claim=True,
        original_nine_B22_init_commands_and_all_B172_commands_preserved=True,
        single_source_end1880_actually_reached=True,
        evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
''' + text[stop:]
    changes = {'B171':'B172','source_event171':'source_event172',
        'v4342':'v4394','v4340':'v4389','v4341':'v4390','v4328':'v4378',
        'all37':'all27',
        'all_source_commands_presentations_resource_and_C200_retained':'all_source_commands_presentations_resources_C200_then_A000_retained'}
    for key in changes:
        assert key in text,key
    text = re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    text = re.sub(r'(?<!\d)171(?!\d)','172',text)
    text = text.replace('len(actual) + len(offline) == 37','len(actual) + len(offline) == 27')
    assert not re.search(r'B171|source_event171|== 37|all37|2112|2116|dream_speech|wake_speech',text)
    compile(text,str(TARGET),'exec')
    TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        target=str(TARGET),target_sha256=sha(TARGET.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),
        original_38_commands_and_nine_init_not_reduced=True,no_new_emulator_run=True))
    print('B172 actual audit prepared:27 panels,47 commands,C200 then A0006240 and single end1880.')
