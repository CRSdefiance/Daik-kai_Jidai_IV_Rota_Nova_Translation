"""Bind all fifteen clean/current spans only after the whole clean gloss."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_source_tools_v7130')
if __name__=='__main__':
    assert not ROOT.exists()
    helper={'v7067':'v7118'}
    changes={
      'B222':'B224','source_v7037':'source_v7130','source_span_binding_v7037':'source_span_binding_v7130',
      'verification_v7035':'verification_v7126',
      'clean_context_v7036/all16_clean_sunset_Noritsune_armor_glosses_before_old_English':'clean_context_v7128/all15_clean_Medusa_shield_flirtation_glosses_before_old_English',
      'current_V7029_native_v7033':'current_V7118_native_v7123',
      'len(known)==6619':'len(known)==6652',
      'all16_clean_speeches_glossed_together_before_old_English':'all15_clean_glosses_precede_old_English',
      'blocks[222]':'blocks[224]','block=222':'block=224',
      'len(spoken)==len(translated)==16':'len(spoken)==len(translated)==15','len(regions)==16':'len(regions)==15',
      "ends==[1112,1112] and len(source)==len(target)==1112 and source[1112:]==target[1112:]==b''":"ends==[958,958] and len(source)==len(target)==960 and source[958:]==target[958:]==bytes(2)",
      '{0x4000,0xA000,0}':'{0x4000,0xA000,0xC200,0}',
      'source_bytes=1112,current_bytes=1112,source_logical_end=1112,current_logical_end=1112,source_tail_bytes=0,current_tail_bytes=0':'source_bytes=960,current_bytes=960,source_logical_end=958,current_logical_end=958,source_tail_bytes=2,current_tail_bytes=2',
      'complete1112_byte_inverse':'complete960_byte_inverse',
      'physical_speeches=16':'physical_speeches=15','total_editorial_objects=16':'total_editorial_objects=15','ordinary_source_speeches=16':'ordinary_source_speeches=15',
      'source_static_actor_selectors=[2,16]':'source_static_actor_selectors=[26,197]','source_C200=0':'source_C200=1',
      'all16_complete_source_current_references_bound':'all15_complete_source_current_references_bound',
      'sixteen_clean_current_sunset_Noritsune_exchange_source_references':'fifteen_clean_current_Medusa_flirtation_exchange_source_references',
      'all sixteen clean glosses':'all fifteen clean glosses',
      'objects=16,commands=18,relative_sites=len(relatives),stored=1112,logical=1112,tail=0':'objects=15,commands=18,relative_sites=len(relatives),stored=960,logical=958,tail=2',
    }
    jobs=[('scripts/lil_B223_source_span_binding_v7078.py','scripts/lil_B224_source_span_binding_v7130.py',helper),('scripts/map_lil_B222_source_v7037.py','scripts/map_lil_B224_source_v7130.py',changes)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_source_tools.json',dict(tools=rows,exact2b6_and_three_existing_BL_replacements_preserved=True,clean_gloss_required_before_current_English=True,no_native_instruction_address_change=True,new_credit=0,full_goal_complete=False))
