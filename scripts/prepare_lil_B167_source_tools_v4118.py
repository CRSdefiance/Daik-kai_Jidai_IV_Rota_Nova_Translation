"""Derive clean-first B167 source/current binding without inheriting B166 counts or roles."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT = Path('work/analysis/lil_B167_source_tools_v4118')
if __name__ == '__main__':
    assert not ROOT.exists()
    tool = derive('scripts/map_lil_B166_source_v4054.py','scripts/map_lil_B167_source_v4118.py',{
        'lil_B166_source_v4054':'lil_B167_source_v4118',
        'editorial_handoff_verification_v4051':'editorial_handoff_verification_v4115',
        'lil_B165_source_v4008/all24_clean_current_complete_context':
            'lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice',
        'lil_B166_clean_v4052/complete_clean42_speeches_two_choice_labels_before_English':
            'lil_B167_clean_v4116/complete_clean27_speeches_two_choice_labels_before_English',
        'lil_B166_clean_context_v4053/all44_complete_B166_exchange_and_fresh_glosses':
            'lil_B167_clean_context_v4117/all29_complete_B167_exchange_and_fresh_glosses',
        'len(known)==5529':'len(known)==5573','blocks[166]':'blocks[167]',
        'len(old)==62 and len(spoken)==42':'len(old)==46 and len(spoken)==27',
        '[2,9,20,23]':'[2,4,13,23,109]','{2,9,20,23}':'{2,4,13,23,109}',
        'B166':'B167',"menus[0]['command_offset']==2152":"menus[0]['command_offset']==152",
        "['お願いする','遠慮する']":"['いいわよ','やめとくわ']",
        "{'FI':3,'FA':0,'FO':0}":"{'FI':0,'FA':0,'FO':0}",
        'block=166':'block=167','physical_speeches=42':'physical_speeches=27','relative_sites=8':'relative_sites=12',
        'all44_clean_current_complete_context_with_typed_choice':'all29_clean_current_complete_context_with_typed_choice',
        'total_editorial_objects=44':'total_editorial_objects=29','speech_objects=42':'speech_objects=27',
        'ordinary_source_speeches=42':'ordinary_source_speeches=27','source_native_commands=62':'source_native_commands=46',
        'source_relative_sites=8':'source_relative_sites=12','all44_clean_first_glosses':'all29_clean_first_glosses',
        'objects=44,progressive=42,choices=2,commands=62':'objects=29,progressive=27,choices=2,commands=46',
        'FI=3':'FI=0','Player choice about hearing flagship room advice;not recruitment acceptance':
            'Player choice about hearing an optional sail lecture;not recruitment or payment',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,source_scope=dict(block=167,speeches=27,choice_labels=2,
        native_commands=46,relative_sites=12,static_actors=[2,4,13,23,109],FI=0),no_ROM_registry_ledger_credit_change=True))
    print('B167 clean-first source/current mapper created.')
