"""Derive whole-only B50 independent fixture/trace/complete body-and-name readers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_actual_production_tools_v8521');assert not root.exists()
    path=Path('dk4tool/patch/hodram_B49_actual_evidence_v1.py');source=path.read_text(encoding='utf-8')
    a=source.index("            if scope=='whole':\n                start=8;");b=source.index('            logical=bytearray(',a)
    c=source.index("            if scope=='whole':\n                ids=");d=source.index("            require([s['id'] for s in speechrows]",c)
    result=derive(str(path),'dk4tool/patch/hodram_B50_actual_evidence_v1.py',{
        'B49':'B50','original[49]':'original[50]','target)[49]':'target)[50]',
        'len(source_commands)==36':'len(source_commands)==12','all36 original':'all12 original',
        "[('whole','fixtures'),('tail','tail_fixtures')]":"[('whole','fixtures')]",
        'len(selected_speeches)==14 and len(selected_commands)==36':'len(selected_speeches)==3 and len(selected_commands)==12',
        source[a:b]:"            start=8;shift=34;entry=b'';outer=None;chosen=selected_commands\n",
        "f['source_block']==49":"f['source_block']==50",
        'original_block=49':'original_block=50',
        "relative==f['source_relative_sites']==(8 if scope=='whole' else 5)":"relative==f['source_relative_sites']==0",
        "len(objects)==(36 if scope=='whole' else 23) and len(texts)==(14 if scope=='whole' else 8)":"len(objects)==12 and len(texts)==3",
        "[('whole','actual'),('tail','tail_actual')]":"[('whole','actual')]",
        "group['block']==49":"group['block']==50",
        'Hodram_B49_scene_runs_v8407':'Hodram_B50_scene_runs_v8505',
        "plan['inputs_sha256']==group['input_schedule_sha256']":"plan['inputs_sha256']",
        "if scope=='tail':speech['kind']='system-FE' if FE else 'progressive'":"speech['kind']='system-FE' if FE else 'progressive'",
        "dict(scope='whole-script-opening' if scope=='whole' else 'bounded-possession-dialogue-tail',version=version,choice=choice,source_selector=actor,selected_capture=holds[-1],complete_holds=len(holds),name=None if FE else name['text'])":"dict(version=version,source_selector=actor,name=None if FE else name['text'],selected_capture=holds[-1],complete_holds=len(holds))",
        source[c:d]:"            ids=['DK4_MES_B50_R0007','DK4_MES_B50_R0010','DK4_MES_B50_R0013'];require(len(pairs)==20 and not any(p['word']==0x2100 for p in pairs),'whole B50 exchange all12commands/3speeches/no menu')\n",
        "len(results)==6 and page_occurrences==34 and totalholds==200":"len(results)==2 and page_occurrences==6 and totalholds==50",
        'all six actual groups/34page occurrences/200complete body-name orabsent-header holds':'both actual groups/6page occurrences/50complete body-name orabsent-header holds',
        'whole_andbounded_frames=60006,complete_actual_page_occurrences=34,complete_actual_holds=200,unique_speech_IDs=14,both_original_menu_results_andnormal_value_carry_verified=True':'whole_actual_frames=20002,complete_actual_page_occurrences=6,complete_actual_holds=50,unique_speech_IDs=3,all12_original_commands_andnormal_value_carry_verified=True',
        'whole/bounded fixtures':'whole fixtures',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_original_fixture_ROM_inverses_trace_CPU_resident_payload_controller_schedule_complete_glyph_name_FE_header_andfollowing_command_guards_preserved=True,only_complete_B50_whole_scope_no_bounded_tail_or_menu_is_authorized=True,no_emulator_replay_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
