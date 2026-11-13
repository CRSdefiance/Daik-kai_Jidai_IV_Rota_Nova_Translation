"""Research B74's79 speeches, typed tutorial choice and20 relative operands."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/research_lil_lessons_relocation_v1760.py')
SOURCE_SHA = '87d8a37275b8fe10823180ff44ce98eb74e1c2cb91add7bcb2942507e7b99254'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'lil_lessons_relocation_v1760':'lil_Hamburg_relocation_v1960',
        'out/all_routes_combined_v1711_candidate.nds':'out/all_routes_combined_v1945_candidate.nds',
        'translations/lil_lessons_editorial_manuscript_v5.json':'translations/lil_hamburg_recruitment_editorial_manuscript_v3.json',
        'work/analysis/lil_Deck_label_approval_v1758/all60_current_native_font_reconciliation.json':
            'work/analysis/lil_Hamburg_font_approval_v1959/all79_complete_native_font_and_macro_reconciliation.json',
        'translations/lil_lesson_choices_editorial_draft_v2.json':'translations/lil_hamburg_recruitment_choices_editorial_draft_v2.json',
        "    packet=read('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')":
            """    original=read('work/analysis/lil_Hamburg_source_v1949/all79_source_native_context_and_two_choices.json')
    commands=original['all_current_native_commands']
    choices=[dict(offset=c['offset'],current_hex=c['whole_command_hex'],
        source_hex=next(s['whole_command_hex'] for s in original['all_clean_native_commands'] if s['offset']==c['offset']))
        for c in commands if c['word']==0x2100]
    packet={'blocks':[dict(block=74,all_nested_native_commands=commands,choices=choices)]}""",
        'work/analysis/lil_lesson_branches_v1722/original_relative_skip_operand_proof.json':
            'work/analysis/lil_Hamburg_branches_v1957/original_relative_skip_operand_proof.json',
        'all60_texts_four_choice_labels_and36_relative_operands_preserved':'all79_texts_two_choice_labels_and20_relative_operands_preserved',
        'all180_relocated_native_skip_cases_match_original_target_mapping':'all100_relocated_native_skip_cases_match_original_target_mapping',
        '==180':'==100',
    }
    for old,new in changes.items():
        count = 2 if old.startswith('work/analysis/lil_lesson_branches_v1722/') else 1
        assert text.count(old) == count,(old,text.count(old))
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
