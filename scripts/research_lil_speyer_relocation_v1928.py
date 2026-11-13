"""Research-only57 speeches/two choices/48 relative spans; no release approval."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/research_lil_lessons_relocation_v1760.py')
SOURCE_SHA = '87d8a37275b8fe10823180ff44ce98eb74e1c2cb91add7bcb2942507e7b99254'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    old_packet = "    packet=read('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')"
    new_packet = """    original=read('work/analysis/lil_followups_after_London_v1914/source_followup_packets_and_random_query_classification.json')
    packet={'blocks':[]}
    for row in original['packets']:
        if row['block'] not in (25,128):continue
        commands=row['all_current_native_commands']
        choices=[]
        for command in commands:
            if command['word']!=0x2100:continue
            source=next(c for c in row['all_clean_native_commands']if c['offset']==command['offset'])
            choices.append(dict(offset=command['offset'],current_hex=command['whole_command_hex'],source_hex=source['whole_command_hex']))
        packet['blocks'].append(dict(block=row['block'],all_nested_native_commands=commands,choices=choices))
    assert [r['block']for r in packet['blocks']]==[25,128]
"""
    changes = {
        'lil_lessons_relocation_v1760':'lil_Speyer_relocation_v1928',
        'out/all_routes_combined_v1711_candidate.nds':'out/all_routes_combined_v1909_candidate.nds',
        'translations/lil_lessons_editorial_manuscript_v5.json':'translations/lil_speyer_encounter_editorial_manuscript_v1.json',
        'work/analysis/lil_Deck_label_approval_v1758/all60_current_native_font_reconciliation.json':
            'work/analysis/lil_Speyer_fonts_v1922/all57_native_macros_and_complete_font_planes.json',
        'translations/lil_lesson_choices_editorial_draft_v2.json':'translations/lil_speyer_choices_editorial_draft_v1.json',
        old_packet:new_packet,
        'work/analysis/lil_lesson_branches_v1722/original_relative_skip_operand_proof.json':
            'work/analysis/lil_Speyer_branches_v1926/original_relative_skip_operand_proof.json',
        'all60_texts_four_choice_labels_and36_relative_operands_preserved':'all57_texts_two_choice_labels_and48_relative_operands_preserved',
        'all180_relocated_native_skip_cases_match_original_target_mapping':'all240_relocated_native_skip_cases_match_original_target_mapping',
        '==180':'==240',
        'FE_actual_context_choice_drawing_external_references_and_complete_revised_gameplay_pending':
            'new_scene_controls_external_references_and_revised_gameplay_pending',
    }
    for old,new in changes.items():
        expected = 2 if old.startswith('work/analysis/lil_lesson_branches_v1722/') else 1
        assert text.count(old) == expected,(old,text.count(old))
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
