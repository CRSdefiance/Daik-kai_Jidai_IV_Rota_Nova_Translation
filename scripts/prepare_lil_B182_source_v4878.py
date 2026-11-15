"""Derive the complete conditional B182 clean/current source binding."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__ == '__main__':
    print(derive('scripts/map_lil_B181_source_v4832.py','scripts/map_lil_B182_source_v4878.py',{
        'B181':'B182','source_v4832':'source_v4878','verification_v4828':'verification_v4874',
        'clean_context_v4831/all10':'clean_context_v4877/all8','len(known)==5923':'len(known)==5933',
        'blocks[181]':'blocks[182]','len(old)==13 and len(spoken)==10':'len(old)==25 and len(spoken)==8',
        'in [166,167,168,254]':'in [166,167,254]','block=181':'block=182',
        "assert [c['word'] for c in old if c['word']!=0x4000]==[0xA000,0xC200,0]":
        "assert [c['word'] for c in old if c['word'] not in [0x4000,0x100,0x200,0x300,0x400]]==[0x8000,0xA000,0x8000,0xA000,0xA000,0xC200,0]",
        'lil_B180_runs_v4823':'lil_B181_runs_v4869','physical_speeches=10':'physical_speeches=8',
        'source_selectors=[166,167,168,254]':'source_selectors=[166,167,254]',
        'FE_panels=1,relative_sites=0':'FE_panels=1,relative_sites=10',
        'all10_clean_current_complete_context':'all8_clean_current_complete_context',
        'all10_clean_first_glosses':'all8_clean_first_glosses',
        'total_editorial_objects=10,speech_objects=10,ordinary_source_speeches=9':'total_editorial_objects=8,speech_objects=8,ordinary_source_speeches=7',
        'source_static_actor_selectors=[166,167,168],source_native_commands=13':'source_static_actor_selectors=[166,167],source_native_commands=25',
        'source_A000=1,source_C200=1,source_relative_sites=0,source_predicates=0':'source_A000=3,source_C200=1,source_relative_sites=10,source_predicates=2',
        'B181 bound:10 complete speeches,13 commands,A000/C200/end;three source actors and current V4821 opening snapshot. No credit.':
        'B182 bound:8 complete speeches,25 commands,2 predicates,10 relative sites,3 A000/C200/end;two source actors and current V4867 opening snapshot. No credit.'
    }))
