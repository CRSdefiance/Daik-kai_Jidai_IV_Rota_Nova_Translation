"""Bind the clean B204 exchange to the verified current ROM and five native actors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B204_source_tools_v6062')
if __name__=='__main__':
    assert not ROOT.exists();prior=read('work/analysis/editorial_handoff_verification_v6061/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    registry=read('translations/release_stack.json');profile=registry['profiles'][prior['profile']]
    assert profile['status']=='experimental' and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    rows=[derive('scripts/map_lil_B203_source_v6010.py','scripts/map_lil_B204_source_v6062.py',{
        'B203':'B204','source_v6010':'source_v6062','verification_v6009':'verification_v6061','clean_context_v6007':'clean_context_v6059',
        'all22_clean_cordyceps_book_offer_and1000_to100_negotiation_glosses.json':'all20_clean_castle_figurehead_claim_missing_shachihoko_and_letter_glosses.json',
        'len(known)==6327':'len(known)==6349','.blocks[203]':'.blocks[204]','block=203':'block=204',
        'len(old)==31 and len(spoken)==22':'len(old)==26 and len(spoken)==20',
        'in [2,76,170,254]':'in [2,11,124,130,145,254]',
        '[0x4820,0x4735,0x6003,0x632E,0xA000,0xA000,0xA000,0xA000,0]':'[0x4301,0x4381,0x4835,0x4735,0xA000,0]',
        'dict(FI=1,FA=0,FO=0)':'dict(FI=0,FA=0,FO=0)',
        'lil_B202_runs_v6000':'lil_B203_runs_v6052',
        'physical_speeches=22,source_selectors=[2,76,170,254],source_macro_counts=macros,FE_panels=1':'physical_speeches=20,source_selectors=[2,11,124,130,145,254],source_macro_counts=macros,FE_panels=4',
        'all22_clean_current_complete_context.json':'all20_clean_current_complete_context.json',
        'total_editorial_objects=22,speech_objects=22,ordinary_source_speeches=21,system_FE_panels=1':'total_editorial_objects=20,speech_objects=20,ordinary_source_speeches=16,system_FE_panels=4',
        'source_selectors=[2,76,170,254],source_static_actor_selectors=[2,76,170],source_native_commands=31':'source_selectors=[2,11,124,130,145,254],source_static_actor_selectors=[2,11,124,130,145],source_native_commands=26',
        'source_A000=4':'source_A000=1','all22_clean_first_glosses':'all20_clean_first_glosses',
        'B203 bound:22 objects/31 commands/one FE FI notice;three source actors and actual V5998 opening snapshot.No old-English prose comparison or credit.':'B204 bound:20 objects/26 commands/four FE letters,no macros;five source actors and actual V6050 opening snapshot.No old-English prose comparison or credit.',
    })]
    rows.append(derive('scripts/reconcile_lil_B203_voices_v6011.py','scripts/reconcile_lil_B204_voices_v6063.py',{
        'B203':'B204','voices_v6011':'voices_v6063','source_v6010':'source_v6062','all22_clean_current_complete_context':'all20_clean_current_complete_context',
        '[2,76,170]':'[2,11,124,130,145]','fresh3_actor_names':'fresh5_actor_names','len(fresh)==3':'len(fresh)==5','three_source_selectors':'five_source_selectors',
        'three B203 actors from actual V5998 RAM':'five B204 actors from actual V6050 RAM',
        'no_kinship_rank_employment_item_identity_or_guaranteed_bargaining_outcome_inferred_from_dialogue':'no_invented_kinship_rank_employment_item_identity_or_ownership_provenance',
    }))
    rows.append(derive('scripts/prove_lil_B203_names_v6012b.py','scripts/prove_lil_B204_names_v6064.py',{
        'B203':'B204','names_v6012':'names_v6064','source_v6010':'source_v6062','voices_v6011':'voices_v6063',
        'all22_clean_current_complete_context':'all20_clean_current_complete_context',
        '[2,76,170]':'[2,11,124,130,145]','fresh3_actor_names':'fresh5_actor_names','and_three_source_selectors':'and_five_source_selectors',
        "len(native['rows'])==6":"len(native['rows'])==10",'native_six_consumer_cases':'native_ten_consumer_cases',
        'six_original_progressive':'ten_original_progressive','Six source-owned':'Ten source-owned',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_preparation.json',dict(tools=rows,prior_verified_handoff='work/analysis/editorial_handoff_verification_v6061/verified_handoff.json',previous_goal_turn_classification='progress',profile=prior['profile'],no_ROM_ledger_or_registry_change=True,full_goal_complete=False))
    print('B204 exact26-command context and five-speaker name tools prepared;previous turn progress verified.')
