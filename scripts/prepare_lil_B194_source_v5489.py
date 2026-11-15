"""Bind the conditional sake exchange,one FI and exact original native control shape."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B194_source_tools_v5489')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/map_lil_B191_source_v5356.py','scripts/map_lil_B194_source_v5489.py',{
        'B191':'B194','source_v5356':'source_v5489','verification_v5352':'verification_v5484','clean_context_v5355/all13':'clean_context_v5488/all11',
        'len(known)==6088':'len(known)==6124','blocks[191]':'blocks[194]','len(old)==38 and len(spoken)==13':'len(old)==21 and len(spoken)==11',
        '[86,154,254]':'[6,117,156,254]','[86,154]':'[6,117,156]','block=191':'block=194','lil_B190_runs_v5348':'lil_B193_runs_v5480',
        '[0x8000,0x8000,0xA000,0xA000,0x8000,0xA000,0xA000,0xC200,0]':'[0xA000,0x8000,0x632A,0xC200,0xC200,0]',
        'dict(FI=0,FA=0,FO=0)':'dict(FI=1,FA=0,FO=0)','physical_speeches=13':'physical_speeches=11','relative_sites=16':'relative_sites=4','all13':'all11',
        'total_editorial_objects=13,speech_objects=13,ordinary_source_speeches=12':'total_editorial_objects=11,speech_objects=11,ordinary_source_speeches=10',
        'source_native_commands=38':'source_native_commands=21','source_A000=4,source_C200=1,source_relative_sites=16,source_predicates=3':'source_A000=1,source_C200=2,source_relative_sites=4,source_predicates=1',
        'B191 bound:13 speeches/38 commands,three500-700-500 predicates/16relative sites/four A000s/C200/end;two source actors/current V5346 opening snapshot. No credit. No credit.':
        'B194 bound:11 speeches/21 commands,one source predicate/four relative sites/one A000/resource632A/two C200/end/one FI;three source actors/current V5478 opening snapshot. No credit.'})]
    rows.append(derive('scripts/reconcile_lil_B193_voices_v5448.py','scripts/reconcile_lil_B194_voices_v5490.py',{
        'B193':'B194','voices_v5448':'voices_v5490','source_v5447/all15':'source_v5489/all11','[166,167,168]':'[6,117,156]','V5437':'V5478',
        'no_rank_class_marriage_or_kinship_inferred_from_genteel_cooking_register':'no_rank_kinship_or_employment_inferred_from_drinking_or_excited_conditional_register'}))
    rows.append(derive('scripts/prove_lil_B193_dispatches_v5449.py','scripts/prove_lil_B194_dispatches_v5491.py',{
        'B193':'B194','source_v5447/all15':'source_v5489/all11','voices_v5448':'voices_v5490','dispatches_v5449':'dispatches_v5491',
        'Bind30':'Bind22','len(cases)==30':'len(cases)==22','len(leaves)==3':'len(leaves)==6','all15_source_current':'all11_source_current','no_macros_and3':'one_FI_and6',
        'all3_nonrelative_nonspeech':'all6_nonrelative_nonspeech','30 source/current dispatches':'22 source/current dispatches','no macros. All3 nonrelative leaves':'one FI. All6 nonrelative leaves'}))
    rows.append(derive('scripts/prove_lil_B193_entry_v5450.py','scripts/prove_lil_B194_entry_v5492.py',{
        'B193':'B194','source_v5447/all15':'source_v5489/all11','voices_v5448':'voices_v5490','entry_v5450':'entry_v5492','in [193]':'in [194]'}))
    rows.append(derive('scripts/prove_lil_B191_branches_v5360.py','scripts/prove_lil_B194_branches_v5493.py',{
        'B191':'B194','branches_v5360':'branches_v5493','source_v5356/all13':'source_v5489/all11'}))
    rows.append(derive('scripts/prove_lil_B193_names_v5452.py','scripts/prove_lil_B194_names_v5494.py',{
        'B193':'B194','source_v5447/all15':'source_v5489/all11','voices_v5448':'voices_v5490','names_v5452':'names_v5494','[166,167,168]':'[6,117,156]'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_source_native_contracts.json',dict(tools=rows,previous_goal_turn_classification='progress',
        previous_goal_turn_evidence='work/analysis/editorial_handoff_verification_v5484/verified_handoff.json',current_candidate='out/all_routes_combined_v5478_candidate.nds',
        source_commands=21,speeches=11,source_stored_logical=540,source_tailzeros=0,source_FI=1,source_predicates=1,source_relative_sites=4,source_C200=2,source_resource_word=0x632A,
        no_predecessor_English_ROM_registry_or_credit_change=True,full_goal_complete=False))
