"""Bind all thirteen original/current objects after the completed clean-only gloss."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_source_tools_v7178')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={
      'B224':'B225','source_v7130':'source_v7178','source_span_binding_v7130':'source_span_binding_v7178',
      'verification_v7126':'verification_v7175',
      'clean_context_v7128/all15_clean_Medusa_shield_flirtation_glosses_before_old_English':'clean_context_v7177/all13_clean_children_hero_play_and_remembrance_glosses_before_old_English',
      'current_V7118_native_v7123':'current_V7168_native_v7173',
      'len(known)==6652':'len(known)==6667','all15_clean_glosses_precede_old_English':'all13_clean_glosses_precede_old_English',
      'blocks[224]':'blocks[225]','block=224':'block=225','len(old)==18':'len(old)==16',
      'len(spoken)==len(translated)==15':'len(spoken)==len(translated)==13','len(regions)==15':'len(regions)==13',
      'ends==[958,958] and len(source)==len(target)==960 and source[958:]==target[958:]==bytes(2)':'ends==[974,974] and len(source)==len(target)==976 and source[974:]==target[974:]==bytes(2)',
      '{0x4000,0xA000,0xC200,0}':'{0x4000,0x630B,0xA000,0}',
      'source_bytes=960,current_bytes=960,source_logical_end=958,current_logical_end=958':'source_bytes=976,current_bytes=976,source_logical_end=974,current_logical_end=974',
      'complete960_byte_inverse':'complete976_byte_inverse',
      'physical_speeches=15':'physical_speeches=13','total_editorial_objects=15':'total_editorial_objects=13','ordinary_source_speeches=15':'ordinary_source_speeches=13',
      'source_static_actor_selectors=[26,197]':'source_static_actor_selectors=[2,16,151,162]',
      'source_C200=1':'source_C200=0,source_630B=1',
      'all15_complete_source_current_references_bound':'all13_complete_source_current_references_bound',
      'fifteen_clean_current_Medusa_flirtation_exchange_source_references':'thirteen_clean_current_children_heroes_exchange_source_references',
      'all fifteen clean glosses':'all thirteen clean glosses',
      'objects=15,commands=18,relative_sites=len(relatives),stored=960,logical=958,tail=2':'objects=13,commands=16,relative_sites=len(relatives),stored=976,logical=974,tail=2',
    }
    jobs=[('scripts/lil_B224_source_span_binding_v7130.py','scripts/lil_B225_source_span_binding_v7178.py',{'v7118':'v7168'}),('scripts/map_lil_B224_source_v7130.py','scripts/map_lil_B225_source_v7178.py',changes)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_source_tools.json',dict(tools=rows,strict2b6_and_three_existing_BL_replacements_preserved=True,clean_gloss_required_before_predecessor_English=True,source_630B_and_selector97_not_assumed=True,no_native_high_integer_constant_change=True,new_credit=0,full_goal_complete=False))
