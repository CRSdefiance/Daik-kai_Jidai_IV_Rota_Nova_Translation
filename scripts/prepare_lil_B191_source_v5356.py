"""Bind the three-predicate dye exchange to current V5346 without older English."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B191_source_tools_v5356')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/map_lil_B190_source_v5314.py','scripts/map_lil_B191_source_v5356.py',{
        'B190':'B191','source_v5314':'source_v5356','editorial_handoff_verification_v5310':'editorial_handoff_verification_v5352',
        'clean_context_v5313/all17':'clean_context_v5355/all13','len(known)==6071':'len(known)==6088','blocks[190]':'blocks[191]',
        'len(old)==29 and len(spoken)==17':'len(old)==38 and len(spoken)==13','[119,159,254]':'[86,154,254]','block=190':'block=191',
        '[0x8000,0xA000,0xA000,0xA000,0xC200,0]':'[0x8000,0x8000,0xA000,0xA000,0x8000,0xA000,0xA000,0xC200,0]',
        'lil_B189_runs_v5306':'lil_B190_runs_v5348','physical_speeches=17':'physical_speeches=13','relative_sites=6':'relative_sites=16',
        'all17_clean_current_complete_context':'all13_clean_current_complete_context',
        'total_editorial_objects=17,speech_objects=17,ordinary_source_speeches=16':'total_editorial_objects=13,speech_objects=13,ordinary_source_speeches=12',
        'source_static_actor_selectors=[119,159],source_native_commands=29':'source_static_actor_selectors=[86,154],source_native_commands=38',
        'source_A000=3':'source_A000=4','source_predicates=1':'source_predicates=3','all17_clean_first_glosses':'all13_clean_first_glosses',
        'B190 bound:17 complete speeches,29 commands,one500 predicate,six relative sites,three A000/C200/end;two source actors and current V5304 opening snapshot.':
        'B191 bound:13 speeches/38 commands,three500-700-500 predicates/16relative sites/four A000s/C200/end;two source actors/current V5346 opening snapshot. No credit.',
    })]
    rows.append(derive('scripts/reconcile_lil_B190_voices_v5315.py','scripts/reconcile_lil_B191_voices_v5357.py',{
        'B190':'B191','voices_v5315':'voices_v5357','source_v5314/all17':'source_v5356/all13','[119,159]':'[86,154]','V5304':'V5346',
        'no_rank_kinship_medical_role_or_relationship_inferred_from_remedy_rumor_or_danna':'no_rank_kinship_employment_or_relationship_inferred_from_dye_pitch_or_oyajisan',
    }))
    rows.append(derive('scripts/prove_lil_B190_dispatches_v5316.py','scripts/prove_lil_B191_dispatches_v5358.py',{
        'B190':'B191','dispatches_v5316':'dispatches_v5358','source_v5314/all17':'source_v5356/all13','voices_v5315':'voices_v5357',
        'Bind34 source/current speech calls and6':'Bind26 source/current speech calls and9','len(cases)==34 and len(leaves)==6':'len(cases)==26 and len(leaves)==9',
        'all17_source_current_dispatches_no_macros_and6_control_leaves':'all13_source_current_dispatches_no_macros_and9_control_leaves',
        'all6_nonrelative':'all9_nonrelative','34 source/current dispatches':'26 source/current dispatches','All6 nonrelative':'All9 nonrelative',
    }))
    rows.append(derive('scripts/prove_lil_B190_entry_v5317.py','scripts/prove_lil_B191_entry_v5359.py',{
        'B190':'B191','source_v5314/all17':'source_v5356/all13','voices_v5315':'voices_v5357','entry_v5317':'entry_v5359','in [190]':'in [191]',
    }))
    rows.append(derive('scripts/prove_lil_B190_branches_v5318.py','scripts/prove_lil_B191_branches_v5360.py',{
        'B190':'B191','source_v5314/all17':'source_v5356/all13','branches_v5318':'branches_v5360',
    }))
    rows.append(derive('scripts/prove_lil_B190_names_v5319.py','scripts/prove_lil_B191_names_v5361.py',{
        'B190':'B191','source_v5314/all17':'source_v5356/all13','voices_v5315':'voices_v5357','names_v5319':'names_v5361','[119,159]':'[86,154]',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_current_source_native_contracts.json',dict(tools=rows,
        previous_goal_turn_classification='progress',previous_goal_turn_evidence='work/analysis/editorial_handoff_verification_v5352/verified_handoff.json',
        source_commands=38,speeches=13,source_stored=736,source_logical=734,tailzeros=2,
        selectors_hex=['56','9A'],selectors_decimal=[86,154],predicates=[[8,500],[28,700],[76,500]],relative_sites=16,A000s=4,
        no_predecessor_English_ROM_registry_or_credit_change=True,full_goal_complete=False))
