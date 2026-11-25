"""B74 native typed choice getters, VM results and complete style planes."""
from pathlib import Path

SOURCE = Path('scripts/prove_lil_speyer_choice_v1927.py')

if __name__ == '__main__':
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'lil_Speyer_choice_v1927':'lil_Hamburg_choice_v1958',
        'work/analysis/lil_followups_after_London_v1914/source_followup_packets_and_random_query_classification.json':
            'work/analysis/lil_Hamburg_source_v1949/all79_source_native_context_and_two_choices.json',
        'translations/lil_speyer_choices_editorial_draft_v1.json':'translations/lil_hamburg_recruitment_choices_editorial_draft_v1.json',
        "spec = next(r for r in packet['packets'] if r['block']==128)":"spec = packet",
        '== 2314':'== 3504',
        'block=128,original_command_offset=2314':'block=74,original_command_offset=3504',
    }
    for old,new in changes.items():
        assert text.count(old) == 1,old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
