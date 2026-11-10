"""Bind the next clean exchange to the verified current ROM and native actors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B203_source_tools_v6010')
if __name__=='__main__':
    assert not ROOT.exists();prior=read('work/analysis/editorial_handoff_verification_v6009/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    rows=[derive('scripts/map_lil_B202_source_v5959.py','scripts/map_lil_B203_source_v6010.py',{
        'B202':'B203','source_v5959':'source_v6010','verification_v5958':'verification_v6009','clean_context_v5956':'clean_context_v6007',
        'all19_clean_unsolicited_book_handoff_pursuit_and_self_interested_request_glosses.json':'all22_clean_cordyceps_book_offer_and1000_to100_negotiation_glosses.json',
        'len(known)==6308':'len(known)==6327','.blocks[202]':'.blocks[203]','block=202':'block=203',
        'len(old)==26 and len(spoken)==19':'len(old)==31 and len(spoken)==22',
        'in [2,18,147,157]':'in [2,76,170,254]',
        '[0x632A,0x632A,0x4835,0xA000,0x4721,0xA000,0]':'[0x4820,0x4735,0x6003,0x632E,0xA000,0xA000,0xA000,0xA000,0]',
        'dict(FI=0,FA=0,FO=0)':'dict(FI=1,FA=0,FO=0)',
        'lil_B201_runs_v5949':'lil_B202_runs_v6000',
        'physical_speeches=19,source_selectors=[2,18,147,157],source_macro_counts=macros,FE_panels=0':'physical_speeches=22,source_selectors=[2,76,170,254],source_macro_counts=macros,FE_panels=1',
        'all19_clean_current_complete_context.json':'all22_clean_current_complete_context.json',
        'total_editorial_objects=19,speech_objects=19,ordinary_source_speeches=19,system_FE_panels=0':'total_editorial_objects=22,speech_objects=22,ordinary_source_speeches=21,system_FE_panels=1',
        'source_selectors=[2,18,147,157],source_static_actor_selectors=[2,18,147,157],source_native_commands=26':'source_selectors=[2,76,170,254],source_static_actor_selectors=[2,76,170],source_native_commands=31',
        'source_A000=2':'source_A000=4',
        'all19_clean_first_glosses':'all22_clean_first_glosses',
        'B202 bound:19 progressive speeches/26 commands/no FE or FI;four source actors and actual V5947 opening snapshot.No old-English speech comparison or credit.':'B203 bound:22 objects/31 commands/one FE FI notice;three source actors and actual V5998 opening snapshot.No old-English prose comparison or credit.',
    })]
    rows.append(derive('scripts/reconcile_lil_B202_voices_v5960.py','scripts/reconcile_lil_B203_voices_v6011.py',{
        'B202':'B203','voices_v5960':'voices_v6011','source_v5959':'source_v6010','all19_clean_current_complete_context':'all22_clean_current_complete_context',
        '[2,18,147,157]':'[2,76,170]','fresh4_actor_names':'fresh3_actor_names','len(fresh)==4':'len(fresh)==3','four_source_selectors':'three_source_selectors',
        'four B202 actors from actual V5947 RAM':'three B203 actors from actual V5998 RAM',
    }))
    rows.append(derive('scripts/prove_lil_B202_names_v5961.py','scripts/prove_lil_B203_names_v6012.py',{
        'B202':'B203','names_v5961':'names_v6012','source_v5959':'source_v6010','voices_v5960':'voices_v6011',
        'all19_clean_current_complete_context':'all22_clean_current_complete_context',
        '[2,18,147,157]':'[2,76,170]','fresh4_actor_names':'fresh3_actor_names',
        "len(native['rows'])==8":"len(native['rows'])==6",'native_eight_consumer_cases':'native_six_consumer_cases',
        'eight_original_progressive':'six_original_progressive','Eight source-owned':'Six source-owned',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_preparation.json',dict(tools=rows,prior_verified_handoff='work/analysis/editorial_handoff_verification_v6009/verified_handoff.json',previous_goal_turn_classification='progress',profile=prior['profile'],no_ROM_ledger_or_registry_change=True,full_goal_complete=False))
    print('B203 exact31-command context and three-speaker current-name tools prepared;previous turn progress verified.')
