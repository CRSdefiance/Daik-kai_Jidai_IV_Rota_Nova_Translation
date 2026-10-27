"""Audit complete B173 panels and the naturally observed conditional suffix."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_actual_tools_v4438')
SOURCE=Path('scripts/audit_lil_B172_actual_v4394.py')
TARGET=Path('scripts/audit_lil_B173_actual_v4438.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    a=text.index('        selected = [row for row in pairs');b=text.index('        for pending in trace',a)
    text=text[:a]+'''        selected = [row for row in pairs if row['block']==22]
        assert len(intervals)==len({row['id'] for row in intervals})==11
        assert not any(row['word'] in [0x2100,0x4100,0x2000,0xC200] for row in selected)
        predicates=[row for row in selected if row['word']==0x8000]
        assert len(predicates)==1 and predicates[0]['original_source_offset']==728
        predicate=predicates[0]
        assert predicate['result_words'][0]==2 and predicate['result_words'][1] in [0,1]
        result=predicate['result_words'][1]
        source_path=next(p for p in control['complete_two_boolean_suffix_paths'] if p['predicate_result']==result)
        source_objects={r['source_offset']:r for r in fixture['selected_original_objects']}
        expected=[r['offset'] for r in fixture['original_B22_prelude_commands']]
        expected += [source_objects[at]['fixture_offset'] for at in source_path['native_command_offsets']]
        assert len(selected)==len(expected) and [r['offset'] for r in selected]==expected
        assert selected[-1]['word']==0 and selected[-1]['original_source_offset']==762
        assert selected[-1]['result_words']==[0,0]
        relative=[r for r in selected if r['word'] in [0x100,0x200,0x300,0x400]]
        for row in relative:
            cases=[c for c in branch['cases'] if c['version']=='current' and c['offset']==row['original_source_offset'] and c['last_choice_or_result']==result]
            assert len(cases)==1 and row['extent']==cases[0]['native_decoded_extent']
            assert row['result_words']==[3,0]
        effects=[r for r in selected if r['word']==0xA000 and r.get('original_source_block')==173]
        assert [r['original_source_offset'] for r in effects]==source_path['original_A000_offsets']
        assert sum(r['word']==0xA000 for r in selected)==4+len(effects)
        for effect in effects:
            assert commands[effect['offset']]['whole_command_hex']==control['source_A000_hex_by_offset'][str(effect['original_source_offset'])]
            assert effect['result_words']==[3,0]
        resources=[r for r in selected if r.get('original_source_block')==173 and r['word']&0xFF00==0x6300]
        assert [r['word'] for r in resources]==[0x6329,0x6340]
        presentations=[r for r in selected if r.get('original_source_block')==173 and r['word'] in [0x6000,0x6240]]
        assert [r['word'] for r in presentations]==[0x6000,0x6240]
        assert [r['original_source_offset'] for r in presentations]==[8,760]
        assert sum(r['prefix']==254 for r in intervals)==0
        final_speech=next(r for r in intervals if r['id']=='DK4_MES_B173_R0044')
        assert final_speech['returned']<=effects[0]['start']<=effects[0]['returned']<=predicate['start']<=predicate['returned']
        assert predicate['returned']<=presentations[1]['start']<=presentations[1]['returned']<=selected[-1]['start']
        unvisited=[r for r in fixture['selected_original_objects'] if r['source_offset'] not in source_path['native_command_offsets']]
        assert len(fixture['all32_stored_fixture_commands'])==32
''' + text[b:]
    a=text.index('        versions.append(dict(');b=text.index('        photosets[case]',a)
    text=text[:a]+'''        versions.append(dict(case=case,source_block=173,ROM_sha256=report['ROM_sha256'],frames=9001,
            input_schedule=rp['original_inputs'],input_schedule_sha256=rp['inputs_sha256'],
            capture_report=str(paths[2]),observer_report=str(paths[3]),selected_B22_command_pairs=selected,
            selected_intervals=intervals,actual_predicate=predicate,unforced_predicate_result=result,
            actual_resources=resources,actual_presentation_commands=presentations,actual_source_A000s=effects,
            actual_source_relative_commands=relative,unvisited_declared_source_objects=unvisited,
            source_A000_hex_by_offset=control['source_A000_hex_by_offset'],source_predicate_hex=control['source_predicate_hex'],
            final_effect_predicate_and_return_interval=[final_speech,effects[0],predicate,presentations[1],selected[-1]],
            fixture_exit_frame=selected[-1]['returned'],single_source_end_offset=762,
            following_observed_blocks=sorted({r['block'] for r in pairs if r['block']!=22}),
            exact_observed_boolean_path_and_all11_speeches_match_original_source_commands=True,
            all_source_commands_stored_original_branching_not_flattened_or_predicate_forced=True))
''' + text[b:]
    a=text.index('    counts = Counter(');b=text.index('    assert not failures',a)
    text=text[:a]+'''    counts=Counter(r['word'] for r in versions[1]['selected_B22_command_pairs'])
    save(ROOT/'actual_all11_unforced_predicate_paths_effects_and_end.json',dict(versions=versions,
        actual_panels=actual,fresh_actual_unique_speech_panels=len(actual),complete_matching_observations=sum(bool(r['holds']) for r in actual),
        offline_only_display_IDs=offline,failures=failures,paired_region_differences=region_differences,
        review_sheets=sheets,visual_review_pending=True,actual_new_cold_boot_runs=2,frames_per_boot=9001,
        selected_command_counts={format(word,'04X'):count for word,count in counts.items()},
        all23_structural_source_commands_and_single_stored_end_preserved=True,all11_progressive_speeches_observed=True,
        observed_original_predicate_path_relative_commands_resources_effects_and_return_recorded=True,
        source_packed_predicate_and_A000_semantics_not_inferred=True,actual_source_event173_not_selected=True,
        no_earned_recruitment_natural_eligibility_full_playthrough_or_hardware_claim=True,
        original_nine_B22_init_commands_and_all_B173_commands_stored_without_flattening=True,
        single_source_end762_actually_reached=True,unvisited_declared_nodes_and_any_unexecuted_effect_body_explicit=True,
        evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
''' + text[b:]
    changes={'B172':'B173','source_event172':'source_event173','v4394':'v4438','v4389':'v4436','v4390':'v4437','v4378':'v4425',
        'all27':'all11','report[\'frames\'] == 20001':"report['frames'] == 9001",
        'all_source_commands_presentations_resources_C200_then_A000_retained':'all_source_commands_presentations_resources_predicate_four_spans_and_two_A000s_retained',
        'len(actual) + len(offline) == 27':'len(actual) + len(offline) == 11',
        "assert source['block'] != 172":"assert source['block'] != 173",
        'original_source_block=172':'original_source_block=173',
        "    plan, font = read(PLAN), read(FONT)":"    plan, font = read(PLAN), read(FONT)\n    control,branch=read(CONTROL),read(BRANCH)",
        "[PLAN, FONT, Path(__file__)]":"[PLAN, FONT, CONTROL, BRANCH, Path(__file__)]",
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    anchor="CAPBASE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')"
    assert text.count(anchor)==1
    text=text.replace(anchor,anchor+"\nCONTROL=Path('work/analysis/lil_B173_controls_v4417/two_resources_one_predicate_four_spans_two_A000s_and_single_end.json')\nBRANCH=Path('work/analysis/lil_B173_branches_v4414/original_relative_skip_operand_proof.json')")
    assert not re.search(r'B172|source_event172|original_source_block=172|all27|20001|1880|1930',text)
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),target=str(TARGET),
        target_sha256=sha(TARGET.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),
        actual_unforced_boolean_path_required=True,all11_complete_panels_required=True,no_new_emulator_run=True,full_goal_complete=False))
    print('Prepared B173 actual audit:11 complete panels,original unforced suffix path,effects and single end762.')
