"""Freeze source-changing/prose/geometry/header/macro rejection checks forB36."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_confrontation_policy_validation_tools_v7815')
SEMANTIC=[
    ('readiness-to-completed-travel',36,5,'ready to sail','already back from our voyage'),
    ('recognition-wrong-person',36,9,'Lil Argot','Maria Li'),
    ('invented-rank',36,16,'Admiral','Queen'),
    ('introduction-invented-title',36,23,'My name is','My royal title is'),
    ('direct-arrival-as-invasion',36,27,'came here in person','invaded us with your fleet'),
    ('fear-as-fulfilled-event',36,31,'came to kill me?!','already killed me!'),
    ('tentative-inference-erased',36,34,'It seems','I know for certain'),
    ('metaphor-as-literal-poison',36,34,'really misled you','poisoned your food'),
    ('purpose-inverted',36,34,'tell you the truth','attack your fleet'),
    ('regional-confusion',36,37,'Southeast Asia','East Asia'),
    ('people-as-ships',36,37,'the people','the ships'),
    ('attempt-as-completed-rescue',36,37,"trying to save","finished saving"),
    ('counteraccusation-wider-rule',36,41,"China's underworld","all of China's government"),
    ('intended-plan-as-past-event',36,45,'He plans to','He already managed to'),
    ('proof-demand-as-proof-owned',36,49,'Do you have any proof','I have confirmed proof'),
    ('proof-challenge-invented-kinship',36,49,'the bad guy','my father'),
    ('life-danger-erased',36,52,'Your life is at stake','Your profits are guaranteed'),
    ('invented-deadline',36,52,"It's not too late",'The deadline is tomorrow'),
    ('refusal-as-acceptance',36,56,"You can't just spring that on me and expect me to believe it","I believe everything you said"),
    ('girl-as-daughter',36,60,'Stubborn girl','My stubborn daughter'),
]
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/validate_Maria_story_policy_v7770.py').read_text('utf8')
    node=next(n for n in ast.parse(source).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SEMANTIC' for t in n.targets))
    old=ast.get_source_segment(source,node);new='SEMANTIC='+repr(SEMANTIC)
    result=derive('scripts/validate_Maria_story_policy_v7770.py','scripts/validate_Maria_confrontation_policy_v7815.py',{
        old:new,
        'maria_story_profile_v1':'maria_B36_profile_v1','maria_story_layout_v1':'maria_B36_layout_v1',
        'freeze_Maria_story_policy_v7769':'freeze_Maria_confrontation_policy_v7814',
        'maria_story_policy_validation_v7770':'maria_confrontation_policy_validation_v7815',
        'row=records[34,5]':'row=records[36,23]',
        "english.replace('{SPEAKER:74}','{SPEAKER:01}')":"english.replace('{SPEAKER:03}','{SPEAKER:02}')",
        'for number in [34,108,35]:':'for number in [36]:',
        'len(positive)==67 and macro_cases==12 and len(negative)==134+len(geometry)+len(texts)+len(SEMANTIC)+macro_cases+12':
        'len(positive)==16 and macro_cases==3 and len(negative)==32+len(geometry)+len(texts)+len(SEMANTIC)+macro_cases+6',
        "for i in r['qa']['issues'])==22":"for i in r['qa']['issues'])==9",
        '67_positives200_actual_changing_guard_rejections.json':'16_positives81_actual_changing_guard_rejections.json',
        'positive_count=67':'positive_count=16',
        'twenty_two_row_infos_no_warnings_orwaivers':'nine_row_infos_no_warnings_orwaivers',
        'source_header_normalization_allthree_blocks_rejected':'source_B36_header_normalization_rejected',
        "'67policy positives /'":"'16policy positives /'",
        "'actual-changing guard rejections;12macro erasures;22row infos/no warnings;all shared inputs unchanged.'":
        "'actual-changing guard rejections;3macro erasures;9row infos/no warnings;all shared inputs unchanged.'",
        'Unreviewed Maria-story paragraph':'Unreviewed Maria-B36 paragraph',
    })
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivation=result,
        twenty_source_meaning_corruptions_selected_from_complete_clean_confrontation=True,
        all_original_native_numbers_positive_QA_geometry_header_andactual_change_guards_preserved=True,
        no_unchanged_input_schema_orstartup_failure_counted_asnegative=True,new_credit=0,full_goal_complete=False))
