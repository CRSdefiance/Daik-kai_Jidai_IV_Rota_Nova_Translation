"""Bind exact effective current surname paragraphs before authoring the consistency correction."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_effective_tools_v8201')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/prove_Rafael_B50_effective_v8137.py').read_text('utf8')
    macro=source[source.index('    derived=checked_text('):source.index("    exec(compile(derived")]
    receipt=derive('scripts/prove_Rafael_B50_effective_v8137.py','scripts/prove_Gerhard_effective_v8201.py',{
        'scripts.papal_trade_route_native_context_v7626':'scripts.Lil_current_route_context_v8198',
        'Rafael_B50_effective_v8137':'Gerhard_surname_effective_v8201',
        'Rafael_B50_current_v8136/all28_complete_source_current_refs_before_new_English_manuscript.json':'Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json',
        'Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json':'Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json',
        "source['all28_clean_whole_context_glosses_precede_current_English_exposure']":"source['all295_clean_records_reviewed_for_name_identity_context_not_full_new_prose_credit']",
        'dict(FI=6,FA=6,FO=10)':'dict(FI=3,FA=5,FO=9)',
        "sha(NAMES.read_bytes())==source['names_andmacros_packet_sha256']":"names['candidate_sha256']==source['current_ROM_sha256'] and names['candidate']==source['current_ROM']",
        "'route':0,'route_mask':1":"'route':2,'route_mask':4",macro:'    derived=inspect.getsource(inherited.expanded_current_body)\n',
        'measured-Rafael-macros':'measured-Lil-macros',"b'Rafael'":"b'Lil'","b'Castor'":"b'Argot'","b'Castor Co.'":"b'Argot Co.'",
        'len(cases)==56 and len(rows)==28':'len(cases)==10 and len(rows)==5',
        'all28_effective_English_templates56_original_dispatches_no_FE.json':'all5_effective_English_templates10_original_dispatches_no_FE.json',
        'all28_progressive_speakers':'all5_progressive_speakers','all28_actual_body_name_bounds':'all5_actual_body_name_bounds',
        'all_three_static_source_speakers_not_invented_from_incidental_r1':'all_three_static_source_speakers_bound_before_proposed_correction',
        'ordinary_captain0_opening_context_no_unlock_orstate_fixture':'ordinary_captain2_opening_context_no_unlock_orstate_fixture',
        '56 original dispatches/28 effective templates':'10 original dispatches/5 effective templates',
        'Bind28clean/current B50speeches through original captain0dispatch;noFEobjects.':'Bind five prior-reviewed surname records through original captain2 dispatch;noFEobjects.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
    print('Prepared5source/current effective surname dispatches;noROM orcredit changes.')
