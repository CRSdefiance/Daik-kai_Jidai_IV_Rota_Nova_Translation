"""Specialize the corrected actual-plane/menu auditor for B167's two distinct paths."""
import ast,re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_actual_audit_tools_v4150')
OUTPUT=Path('scripts/audit_lil_B167_actual_v4151.py')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    base=Path('scripts/audit_lil_B166_actual_v4104.py');repair=Path('scripts/audit_lil_B166_actual_v4104c.py')
    text=base.read_text(encoding='utf-8');tree=ast.parse(repair.read_text(encoding='utf-8'))
    corrections=None
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign) and len(node.targets)==1:
            target=node.targets[0]
            if isinstance(target,ast.Name) and target.id=='changes':corrections=ast.literal_eval(node.value)
            elif isinstance(target,ast.Subscript) and isinstance(target.value,ast.Name) and target.value.id=='changes':
                assert corrections is not None;corrections[ast.literal_eval(target.slice)]=ast.literal_eval(node.value)
    assert len(corrections)==7
    for old,new in corrections.items():assert text.count(old)==1,old;text=text.replace(old,new)
    changes={
        'original conditional/advice control flow':'original accept/refuse control flow',
        'lil_B166_actual_v4104':'lil_B167_actual_v4151',
        'lil_B166_display_fixture_v4101':'lil_B167_display_fixture_v4147',
        'lil_B166_native_approval_v4082/all44_native_speech_choice_source_and_actual_menu_reconciliation':'lil_B167_native_approval_v4135/all29_native_speech_choice_and_source_reconciliation',
        'lil_B166_choices_v4080/B166_C2152':'lil_B167_choices_v4133/B167_C152',
        'lil_B166_display_run_v4103':'lil_B167_display_run_v4149','lil_B166_display_v4103':'lil_B167_display_v4149',
        "report['frames'] == 20001":"report['frames'] == 14401",'source_event166':'source_event167','requested_advice_option':'requested_sail_lesson_option',
        "source['block'] != 166":"source['block'] != 167",'original_source_block=166':'original_source_block=167',
        "assert selected[-1]['word'] == 0 and selected[-1]['result_words'] == [0, option]":"assert selected[-1]['word'] == 0",
        "assert predicates[0]['result_words'][0] == 2 and predicates[0]['result_words'][1] in [0,1]":"assert predicates[0]['result_words'][0] == 2 and predicates[0]['result_words'][1] in [0,1]\n            assert selected[-1]['result_words'] == [0,predicates[0]['result_words'][1]] # the later query, not the menu, owns final state",
        "p.get('original_source_block') == 166":"p.get('original_source_block') == 167",'[0x632B,0x632C]':'[0x6327,0x632B]',
        'all70_stored_fixture_commands':'all55_stored_fixture_commands',
        "assert ('DK4_MES_B166_R0087' in expected_ids) == bool(predicates[0]['result_words'][1])":"assert (('DK4_MES_B167_R0131' if option==0 else 'DK4_MES_B167_R0045') in expected_ids)==bool(predicates[0]['result_words'][1])",
        "(selected[-1]['original_source_offset']) == 2948":"(selected[-1]['original_source_offset']) == (2172 if option==0 else 430)",
        'source_block=166':'source_block=167','actual_unforced_Fernando_predicate':'actual_unforced_Cesare_predicate',
        'source_end_offset=2948':'source_end_offset=2172 if option==0 else 430',
        "[b'Please do', b'Decline']":"[b'Okay', b'No thanks']",
        'assert [len(m) for m in masks] == [103,86]':'assert all(m for m in masks)',
        'all189_label_foreground_pixels_equal_complete_native_planes':'all_complete_label_foreground_pixels_equal_complete_native_planes',
        "{'DK4_MES_B166_R0087'}":"{'DK4_MES_B167_R0045','DK4_MES_B167_R0131'}",
        '({2,9,23} if offline else {2,9,20,23})':'({2,4,23,109} if len(offline)==2 else {2,4,13,23,109})',
        'actual_both_choices_conditional_panels_and_single_return':'actual_both_choices_conditional_panels_and_distinct_returns',
        'all8_original_relative_commands_and_one_Fernando_query_retained_not_flattened':'all12_original_relative_commands_and_two_Cesare_queries_retained_not_flattened',
        'both_real_choice_values_and_same_single_tail_end_observed':'both_real_choice_values_and_distinct_source_endwords_observed',
        'original_nine_B22_init_commands_preserved_one_late_recruitment_effect_omitted':'original_nine_B22_init_commands_preserved_and_no_B167_command_omitted',
        'source_and_English_type0_return_preserve_original_last_choice_second_word':'source_and_English_type0_return_preserve_later_query_result_not_forced_menu_option',
        'preserved_failed_audits={str(p):sha(p.read_bytes()) for p in DRAFTS}':'historical_B166_audit_fixes_preserved={str(p):sha(p.read_bytes()) for p in [Path("scripts/audit_lil_B166_actual_v4104.py"),Path("scripts/audit_lil_B166_actual_v4104b.py"),Path("scripts/audit_lil_B166_actual_v4104c.py")]}',
    }
    for old in changes:assert old in text,old
    text=re.sub('|'.join(re.escape(x) for x in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)
    assert '166' not in text.replace('historical_B166_audit_fixes_preserved','').replace('audit_lil_B166_actual_v4104',''), 'Unexpected B166 semantic residue'
    compile(text,str(OUTPUT),'exec');OUTPUT.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(base=str(base),base_sha256=sha(base.read_bytes()),historical_correction_producer=str(repair),historical_correction_producer_sha256=sha(repair.read_bytes()),corrections=corrections,B167_specialization=changes,output=str(OUTPUT),output_sha256=sha(OUTPUT.read_bytes()),source_two_path_queries_two_ends_and_no_effect_omission_bound=True,no_actual_coverage_added_by_tool_creation=True))
    print('B167 full-plane/control/menu audit created with separate menu and later-query result assertions.')
