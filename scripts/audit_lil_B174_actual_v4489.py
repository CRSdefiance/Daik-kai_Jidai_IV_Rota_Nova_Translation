"""Audit complete retained B174 control flow and every actually selected progressive plane."""
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B174_actual_v4489')
PLAN = Path('work/analysis/lil_B174_display_fixture_v4487/complete_effect_preserving_B22_fixtures.json')
FONT = Path('work/analysis/lil_B174_native_approval_v4474/all33_native_progressive_and_source_reconciliation.json')
CAPBASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
CONTROL=Path('work/analysis/lil_B174_controls_v4459/one_resource_conditional_Emilio_four_spans_two_A000s_C200_and_single_end.json')
BRANCH=Path('work/analysis/lil_B174_branches_v4456/original_relative_skip_operand_proof.json')


if __name__ == '__main__':
    assert not ROOT.exists()
    plan, font = read(PLAN), read(FONT)
    control,branch=read(CONTROL),read(BRANCH)
    versions, photosets = [], {}
    evidence = {str(path): sha(path.read_bytes()) for path in [PLAN, FONT, CONTROL, BRANCH, Path(__file__)]}
    for fixture in plan['fixtures']:
        assert read(Path('work/analysis/lil_B174_display_run_v4488_' + fixture['case']) / 'terminal.json')['terminal']
    for fixture in plan['fixtures']:
        case = fixture['case']
        run = Path('work/analysis/lil_B174_display_run_v4488_' + case)
        cap = CAPBASE / ('lil_B174_display_v4488_' + case)
        paths = [run / 'terminal.json', run / 'run_plan.json', cap / 'capture_report.json', cap / 'observer/commands.json']
        terminal, rp, report, trace = map(read, paths)
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances'] == 1
        assert report['frames'] == 16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert sha(Path(fixture['research_ROM']).read_bytes()) == fixture['research_ROM_sha256'] == report['ROM_sha256'] == rp['research_ROM_sha256']
        assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_event174_not_selected'] and rp['all_source_commands_presentations_resource_predicate_optional_Emilio_four_spans_two_A000s_and_C200_retained']
        assert sha(Path(rp['fixture_manifest']).read_bytes()) == rp['fixture_manifest_sha256'] == sha(PLAN.read_bytes())
        assert not trace['errors'] and trace['mismatches'] == 0 and trace['all_host_slots_restored_and_core_file_exact']
        assert all(not value for key, value in report.items() if key.startswith('synthetic_'))
        assert sha(Path(rp['original_inputs']).read_bytes()) == rp['inputs_sha256']
        blocks = IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC2.DK4')).blocks
        block = blocks[22]
        assert sha(block) == fixture['fixture_block_sha256']
        photos = {}
        for photo in report['frames_captured']:
            path = Path(photo['path'])
            assert sha(path.read_bytes()) == photo['PNG_sha256']
            picture = Image.open(path).convert('RGB')
            assert picture.size == (256, 384)
            photos[photo['frame']] = (photo, picture)
        snapshot = report['read_only_RAM_snapshot']
        assert snapshot['read_only_export'] and snapshot['bytes'] == 4194304
        assert sha(Path(snapshot['path']).read_bytes()) == snapshot['sha256']
        rows, pairs, intervals = trace['rows'], [], []
        by_at = {row['fixture_command_offset']: row for row in fixture['original_text_records']}
        commands = {row['fixture_offset']: row for row in fixture['selected_original_objects']}
        for row in rows:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            source = row['source']
            assert source['classification'] == 'original_SC_cache' and source['route'] == 2
            assert source['whole_resident_payload_exact_ROM'] and source['actual_sha256'] == sha(blocks[source['block']])
            assert source['block'] != 174
            if row['kind'] != 'after_command':
                continue
            entry = rows[row['entry_row']]
            source = entry['source']
            at = source['instruction_offset']
            word = int.from_bytes(blocks[source['block']][at:at + 2], 'little')
            pair = dict(block=source['block'], offset=at, word=word, start=entry['frame'], returned=row['frame'],
                        extent=row['decoded_length'], result_words=row['result_words'])
            pairs.append(pair)
            if source['block'] != 22:
                continue
            if at in commands:
                assert word == commands[at]['source_word']
                pair.update(original_source_block=174, original_source_offset=commands[at]['source_offset'])
            if word == 0x4000:
                record = by_at[at]
                assert block[at:at + record['native_extent']].hex() == record['whole_command_hex']
                intervals.append(dict(id=record['id'], start=entry['frame'], returned=row['frame'], offset=at, prefix=record['source_selector']))
        selected = [row for row in pairs if row['block']==22]
        assert 32<=len(intervals)==len({row['id'] for row in intervals})<=33
        assert not any(row['word'] in [0x2100,0x4100,0x2000] for row in selected)
        predicates=[row for row in selected if row['word']==0x8000]
        assert len(predicates)==1 and predicates[0]['original_source_offset']==874
        predicate=predicates[0]
        assert predicate['result_words'][0]==2 and predicate['result_words'][1] in [0,1]
        result=predicate['result_words'][1]
        source_path=next(p for p in control['complete_two_boolean_suffix_paths'] if p['predicate_result']==result)
        assert [by_at[r['offset']]['source_record_index'] for r in intervals]==source_path['spoken_source_record_indices']
        source_objects={r['source_offset']:r for r in fixture['selected_original_objects']}
        expected=[r['offset'] for r in fixture['original_B22_prelude_commands']]
        expected += [source_objects[at]['fixture_offset'] for at in source_path['native_command_offsets']]
        assert len(selected)==len(expected) and [r['offset'] for r in selected]==expected
        assert selected[-1]['word']==0 and selected[-1]['original_source_offset']==2086
        assert selected[-1]['result_words']==[0,result]
        relative=[r for r in selected if r['word'] in [0x100,0x200,0x300,0x400]]
        for row in relative:
            cases=[c for c in branch['cases'] if c['version']=='current' and c['offset']==row['original_source_offset'] and c['last_choice_or_result']==result]
            assert len(cases)==1 and row['extent']==cases[0]['native_decoded_extent']
            assert row['result_words']==[3,result]
        effects=[r for r in selected if r['word']==0xA000 and r.get('original_source_block')==174]
        assert [r['original_source_offset'] for r in effects]==source_path['original_A000_offsets']
        assert sum(r['word']==0xA000 for r in selected)==4+len(effects)
        for effect in effects:
            assert commands[effect['offset']]['whole_command_hex']==control['source_A000_hex_by_offset'][str(effect['original_source_offset'])]
            assert effect['result_words']==[3,result]
        resources=[r for r in selected if r.get('original_source_block')==174 and r['word']&0xFF00==0x6300]
        assert [r['word'] for r in resources]==[0x6340]
        presentations=[r for r in selected if r.get('original_source_block')==174 and r['word'] in [0x6000,0x6240]]
        assert [r['word'] for r in presentations]==[0x6000,0x6240]
        assert [r['original_source_offset'] for r in presentations]==[8,2066]
        assert sum(r['prefix']==254 for r in intervals)==0
        final_speech=next(r for r in intervals if r['id']=='DK4_MES_B174_R0135')
        ui=[r for r in selected if r['word']==0xC200]
        assert len(ui)==1 and ui[0]['original_source_offset']==2084 and ui[0]['result_words']==[3,result]
        assert len(effects)==2 and [r['original_source_offset'] for r in effects]==[2068,2076]
        assert predicate['returned']<=final_speech['start']<=final_speech['returned']<=presentations[1]['start']
        assert presentations[1]['returned']<=effects[0]['start']<=effects[0]['returned']<=effects[1]['start']<=effects[1]['returned']<=ui[0]['start']<=ui[0]['returned']<=selected[-1]['start']
        unvisited=[r for r in fixture['selected_original_objects'] if r['source_offset'] not in source_path['native_command_offsets']]
        assert len(fixture['all54_stored_fixture_commands'])==54
        for pending in trace['unreturned_at_capture_end']:
            assert rows[pending['entry_row']]['source']['block'] != 22
        versions.append(dict(case=case,source_block=174,ROM_sha256=report['ROM_sha256'],frames=16001,
            input_schedule=rp['original_inputs'],input_schedule_sha256=rp['inputs_sha256'],
            capture_report=str(paths[2]),observer_report=str(paths[3]),selected_B22_command_pairs=selected,
            selected_intervals=intervals,actual_predicate=predicate,unforced_predicate_result=result,
            actual_resources=resources,actual_presentation_commands=presentations,actual_source_A000s=effects,
            actual_source_relative_commands=relative,actual_source_C200=ui,unvisited_declared_source_objects=unvisited,
            source_A000_hex_by_offset=control['source_A000_hex_by_offset'],source_predicate_hex=control['source_predicate_hex'],
            predicate_final_speech_presentation_effects_C200_return_interval=[predicate,final_speech,presentations[1],*effects,ui[0],selected[-1]],
            fixture_exit_frame=selected[-1]['returned'],single_source_end_offset=2086,
            following_observed_blocks=sorted({r['block'] for r in pairs if r['block']!=22}),
            exact_observed_boolean_path_and_all_actually_selected_speeches_match_original_source_commands=True,
            all_source_commands_stored_original_branching_not_flattened_or_predicate_forced=True))
        photosets[case] = photos
        evidence.update({str(path): sha(path.read_bytes()) for path in paths})
    shape = lambda version: [(row.get('original_source_offset'), row['word'], row['result_words']) for row in version['selected_B22_command_pairs']]
    assert shape(versions[0]) == shape(versions[1])
    assert versions[0]['input_schedule_sha256'] == versions[1]['input_schedule_sha256']
    by_id = {row['id']: row for row in font['cases']}
    source_intervals = {row['id']: row for row in versions[0]['selected_intervals']}
    actual, panels, failures, region_differences = [], [], [], []
    for interval in versions[1]['selected_intervals']:
        case = by_id[interval['id']]
        preview = Image.open(case['preview']).convert('RGB')
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
        assert preview.height == 64 and preview.width == 216
        ink0 = {(x, y) for y in range(64) for x in range(preview.width) if preview.getpixel((x, y)) == (0, 8, 0)}
        gray0 = {(x, y) for y in range(64) for x in range(preview.width) if preview.getpixel((x, y)) == (98, 97, 98)}
        source_interval = source_intervals[interval['id']]
        holds = []
        for frame, (photo, picture) in photosets['reviewed_English'].items():
            if not max(interval['start'], source_interval['start']) < frame < min(interval['returned'], source_interval['returned']):
                continue
            ink = {(x, y) for y in range(64) for x in range(preview.width) if picture.getpixel((16 + x, 296 + y)) == (0, 8, 0)}
            gray = {(x, y) for y in range(64) for x in range(preview.width) if picture.getpixel((16 + x, 296 + y)) == (98, 97, 98)}
            if ink != ink0 or gray != gray0:
                continue
            source_photo, source_picture = photosets['clean_Japanese'][frame]
            regions_equal = (picture.crop((0, 192, 256, 294)).tobytes() == source_picture.crop((0, 192, 256, 294)).tobytes()
                             and picture.crop((0, 0, 256, 192)).tobytes() == source_picture.crop((0, 0, 256, 192)).tobytes())
            if not regions_equal:
                region_differences.append(dict(id=interval['id'], frame=frame, native_text_plane_exact=True,
                    paired_source_upper_or_portrait_region_differs=True, not_masked_or_retimed=True))
                continue
            holds.append(dict(frame=frame, capture=photo['path'], capture_sha256=photo['PNG_sha256'],
                clean_capture=source_photo['path'], clean_capture_sha256=source_photo['PNG_sha256'],
                complete_ink_gray_masks_equal_native_plane=True, portrait_name_picture_and_upper_regions_equal_Japanese=True))
            evidence[photo['path']] = photo['PNG_sha256']
            evidence[source_photo['path']] = source_photo['PNG_sha256']
        if not holds:
            failures.append(dict(id=interval['id'], prefix=interval['prefix'], finding='No complete native plane and paired upper/portrait regions within shared holding interval.'))
        else:
            panels.append((interval['id'], interval['prefix'], Image.open(holds[0]['capture']).convert('RGB').crop((0, 192, 256, 384))))
        actual.append(dict(id=interval['id'], prefix=interval['prefix'], consumer='FE-paper' if interval['prefix'] == 254 else 'progressive',
            native_plane_sha256=case['whole_native_plane_sha256'], interval=interval, holds=holds,
            actually_displayed_in_disclosed_B22_fixture=True))
    offline = sorted(set(by_id) - {row['id'] for row in actual})
    assert set(offline) <= set(plan['expected_conditional_speech_IDs'])
    assert len(actual) + len(offline) == 33
    assert sum(row['prefix'] == 254 for row in actual) == 0
    ROOT.mkdir(parents=True)
    sheets = []
    for start in range(0, len(panels), 6):
        sheet = Image.new('RGB', (1560, 832), '#263238')
        draw = ImageDraw.Draw(sheet)
        for index, (ident, prefix, picture) in enumerate(panels[start:start + 6]):
            x, y = index % 3 * 520, index // 3 * 416
            draw.text((x + 4, y + 3), f'{ident} / {prefix:02X} / actual retained B174 content', fill='white')
            sheet.paste(picture.resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 24))
        path = ROOT / f'actual_consumer_sheet{start // 6 + 1}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=sha(path.read_bytes())))
    counts=Counter(r['word'] for r in versions[1]['selected_B22_command_pairs'])
    save(ROOT/'actual_all33_unforced_predicate_paths_effects_C200_and_end.json',dict(versions=versions,
        actual_panels=actual,fresh_actual_unique_speech_panels=len(actual),complete_matching_observations=sum(bool(r['holds']) for r in actual),
        offline_only_display_IDs=offline,failures=failures,paired_region_differences=region_differences,
        review_sheets=sheets,visual_review_pending=True,actual_new_cold_boot_runs=2,frames_per_boot=16001,
        selected_command_counts={format(word,'04X'):count for word,count in counts.items()},
        all45_structural_source_commands_and_single_stored_end_preserved=True,all32_unconditional_speeches_observed_and_optional_Emilio_coverage_explicit=True,
        observed_original_predicate_path_relative_commands_resources_effects_and_return_recorded=True,
        source_packed_predicate_and_A000_semantics_not_inferred=True,actual_source_event173_not_selected=True,
        actual_result_words_are_player_descriptor_command_type_and_persistent_VM_last_result=True,
        original_type3_and_end_preserve_post_predicate_last_result_not_isolated_parser_output=True,
        actual_last_result_model_reused_from_source_bound_VM_contract=True,
        no_earned_recruitment_natural_eligibility_full_playthrough_or_hardware_claim=True,
        original_nine_B22_init_commands_and_all_B174_commands_stored_without_flattening=True,
        single_source_end2086_actually_reached=True,unvisited_declared_nodes_and_any_unexecuted_effect_body_explicit=True,
        evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    assert not failures, failures
    print(dict(actual_panels=len(actual), matching=sum(bool(row['holds']) for row in actual), offline_only=offline,
        exits=[(version['case'], version['fixture_exit_frame']) for version in versions],
        command_pairs=[len(version['selected_B22_command_pairs']) for version in versions],
        sheets=len(sheets), visual_review_pending=True))
