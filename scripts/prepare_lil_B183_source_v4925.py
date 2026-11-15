"""Bind all25 B183 speeches and28 source commands to the exact current checkpoint."""
from scripts.prepare_lil_B156_layout_v3705 import derive
if __name__=='__main__':
    print(derive('scripts/map_lil_B181_source_v4832.py','scripts/map_lil_B183_source_v4925.py',{
        'B181':'B183','source_v4832':'source_v4925','verification_v4828':'verification_v4921',
        'clean_context_v4831/all10':'clean_context_v4923/all25','len(known)==5923':'len(known)==5941',
        'blocks[181]':'blocks[183]','len(old)==13 and len(spoken)==10':'len(old)==28 and len(spoken)==25',
        'in [166,167,168,254]':'in [85,110,132,148,153,254]','block=181':'block=183',
        'lil_B180_runs_v4823':'lil_B182_runs_v4916','physical_speeches=10':'physical_speeches=25',
        'source_selectors=[166,167,168,254]':'source_selectors=[85,110,132,148,153,254]',
        'FE_panels=1':'FE_panels=2','all10_clean_current_complete_context':'all25_clean_current_complete_context',
        'total_editorial_objects=10,speech_objects=10,ordinary_source_speeches=9,system_FE_panels=1':
        'total_editorial_objects=25,speech_objects=25,ordinary_source_speeches=23,system_FE_panels=2',
        'source_static_actor_selectors=[166,167,168],source_native_commands=13':'source_static_actor_selectors=[85,110,132,148,153],source_native_commands=28',
        'all10_clean_first_glosses':'all25_clean_first_glosses',
        'B181 bound:10 complete speeches,13 commands,A000/C200/end;three source actors and current V4821 opening snapshot. No credit.':
        'B183 bound:25 speeches,28 commands,A000/C200/end;five source actors,two FE and current V4914 opening snapshot. No credit.'
    }))
