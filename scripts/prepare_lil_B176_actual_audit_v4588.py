"""Prepare the actual-scene audit with all B176 commands and its impersonal notice."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

root=Path('work/analysis/lil_B176_actual_tools_v4588')
assert not root.exists()
source=Path('scripts/audit_lil_B175_actual_v4534.py')
text=source.read_text(encoding='utf-8')
start=text.index('        presentations=[')
end=text.index('        ui=[',start)
presentation_checks=text[start:end]
tool=derive(source,'scripts/audit_lil_B176_actual_v4588.py',{
    'B175':'B176','lil_B175':'lil_B176',
    'actual_v4534':'actual_v4588','display_fixture_v4531':'display_fixture_v4585',
    'native_approval_v4518/all32':'native_approval_v4572/all10',
    'display_run_v4533':'display_run_v4587','display_v4533':'display_v4587',
    "report['frames']==16001":"report['frames']==9001",
    'source_event175_not_selected':'source_event176_not_selected',
    'all_source39_commands_23_progressive9_FE_resource_three_presentations_C200_and_two_ends_retained':
        'all_source13_commands_9_progressive1_impersonal_FE_A000_C200_and_single_end_retained',
    "source['block']!=175":"source['block']!=176",
    'original_source_block=175':'original_source_block=176',
    'len(expected)==47':'len(expected)==22',
    "len({r['id'] for r in intervals})==32":"len({r['id'] for r in intervals})==10",
    "sum(r['prefix']==254 for r in intervals)==9":"sum(r['prefix']==254 for r in intervals)==1",
    "selected[-1]['original_source_offset']==1702":"selected[-1]['original_source_offset']==386",
    "        assert not any(r.get('original_source_offset')==1706 for r in selected)\n":'',
    "sum(r['word']==0xA000 for r in selected)==4":"sum(r['word']==0xA000 for r in selected)==5",
    presentation_checks:"        effects=[r for r in selected if r.get('original_source_block')==176 and r['word']==0xA000]\n        assert len(effects)==1 and effects[0]['original_source_offset']==8\n",
    "ui[0]['original_source_offset']==1700":"ui[0]['original_source_offset']==384",
    'source_three_presentations=presentations,source_resource=resources':'source_A000=effects',
    'first_source_end1702_actually_reached=True,second_source_end1706_stored_but_unvisited_offline_decoder_only=True':
        'single_source_end386_actually_reached=True',
    'len(actual)==32':'len(actual)==10',"sum(r['prefix']==254 for r in actual)==9":"sum(r['prefix']==254 for r in actual)==1",
    'actual_all32_progressive_FE_controls_C200_and_first_end':'actual_all10_progressive_FE_A000_C200_and_single_end',
    'fresh_actual_unique_speech_panels=32':'fresh_actual_unique_speech_panels=10','frames_per_boot=16001':'frames_per_boot=9001',
    'all39_source_commands_stored_and47_of48_fixture_commands_actually_selected':
        'all13_source_commands_stored_and_all22_fixture_commands_actually_selected',
    'all32_unconditional_speeches23_progressive9_FE_observed=True,second_declared_end1706_offline_native_only=True':
        'all10_speeches9_progressive1_impersonal_FE_observed=True,single_source_end386_actually_reached=True',
    'three_presentations_resource_C200_and_first_end_actually_executed_without_source_omission':
        'source_A000_C200_and_single_end_actually_executed_without_source_omission',
    'source_packed_presentation_semantics_and_anonymous_woman_identity_not_inferred':
        'source_A000_packed_semantics_earlier_scene_location_and_earned_fashion_state_not_inferred',
    'actual_source_event175_not_selected':'actual_source_event176_not_selected',
    'actual_panels=32,FE=9':'actual_panels=10,FE=1',
})
root.mkdir(parents=True)
save(root/'source_derivation.json',dict(tool=tool,source_speeches=10,source_commands=13,fixture_commands=22,
    source_A000=1,original_prelude_A000=4,impersonal_FE=1,single_end=386,frames=9001,
    no_new_editorial_credit=True,full_goal_complete=False))
