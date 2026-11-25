"""Prepare exact2b6 source-span and sixteen-speech predecessor tools without weakening AA5 history."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B222_source_tools_v7037')
if __name__=='__main__':
    assert not ROOT.exists()
    helper={'aa5a7ed159f33fb8ca5dafdfc068ebc69cf9de0469ffe8eba388d3b954e20d05':'2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a',
        'out/all_routes_combined_v6541_candidate.nds':'out/all_routes_combined_v7029_candidate.nds'}
    changes={
        'lil_B220_source_v6921':'lil_B222_source_v7037','editorial_handoff_verification_v6916':'editorial_handoff_verification_v7035',
        'lil_B220_clean_context_v6919/all17_clean_empress_gown_flirtation_and_jewelry_glosses_before_old_English':'lil_B222_clean_context_v7036/all16_clean_sunset_Noritsune_armor_glosses_before_old_English',
        'current_V6910_native_v6920':'current_V7029_native_v7033','lil_B211_source_span_binding_v6550c':'lil_B222_source_span_binding_v7037',
        'seventeen_clean_current_empress_gown_exchange_source_references':'sixteen_clean_current_sunset_Noritsune_exchange_source_references',
        'B220':'B222','blocks[220]':'blocks[222]','block=220':'block=222','6586':'6619','1280':'1112',
        'all17_clean_glosses_precede_old_English':'all16_clean_speeches_glossed_together_before_old_English',
        'all17_complete_source_current_references_bound':'all16_complete_source_current_references_bound',
        'len(old)==20':'len(old)==18','len(spoken)==len(translated)==17':'len(spoken)==len(translated)==16',
        'len(regions)==17':'len(regions)==16','physical_speeches=17':'physical_speeches=16',
        'total_editorial_objects=17':'total_editorial_objects=16','ordinary_source_speeches=17':'ordinary_source_speeches=16',
        'objects=17,commands=20':'objects=16,commands=18','[26,199]':'[2,16]','all seventeen clean glosses':'all sixteen clean glosses',
        "relatives=[c for c in old if c['word'] in [0x100,0x200,0x300,0x400]];group=":"relatives=[c for c in old if c['word'] in [0x100,0x200,0x300,0x400]];assert not relatives and {c['word'] for c in old}=={0x4000,0xA000,0} and sum(c['word']==0xA000 for c in old)==sum(c['word']==0 for c in old)==1;group=",
        'source_A000=1,source_macro_counts=macros':'source_A000=1,source_C200=0,source_predicates=0,source_macro_counts=macros'}
    jobs=[('scripts/lil_B211_source_span_binding_v6550c.py','scripts/lil_B222_source_span_binding_v7037.py',helper),
        ('scripts/map_lil_B220_source_v6921.py','scripts/map_lil_B222_source_v7037.py',changes)]
    for source,target,mapping in jobs:
        assert not Path(target).exists();checked_text(Path(source).read_text('utf8'),mapping)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_helpers.json',dict(tools=[derive(*j) for j in jobs],
        old_AA5_helper_and_all_executed_producers_preserved=True,exact_final2b6_hash_and_current_whole_ARM9_required=True,
        all_native_instruction_constants_and_three_exact_BL_replacements_unchanged=True,new_review_credit=0,full_goal_complete=False))
