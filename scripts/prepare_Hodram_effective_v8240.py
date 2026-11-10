"""Derive the existing guarded dispatch probe for the verified captain1 input."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_effective_tools_v8240')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/prove_Rafael_B50_effective_v8137.py','scripts/prove_Hodram_effective_v8240.py',{
        'Rafael_B50_effective_v8137':'Hodram_B137_B45_B46_effective_v8240',
        'Rafael_B50_current_v8136/all28_complete_source_current_refs_before_new_English_manuscript.json':'Hodram_B137_B45_B46_current_v8239/28_exact_clean_current_refs_after_whole_source_glosses.json',
        'Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json':'Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json',
        "source['all28_clean_whole_context_glosses_precede_current_English_exposure']":"source['clean_whole_exchanges_and27_prior_B44_source_callbacks_read_before_current_English']",
        'dict(FI=6,FA=6,FO=10)':'dict(FI=6,FA=9,FO=15)',
        "sha(NAMES.read_bytes())==source['names_andmacros_packet_sha256']":"names['candidate_sha256']==source['current_ROM_sha256'] and names['candidate']==source['current_ROM']",
        "'route':0,'route_mask':1":"'route':1,'route_mask':2",
        "b'Rafael'":"b'Hodram'","b'Castor'":"b'Bergstrom'","b'Castor Co.'":"b'Bergstrom Fleet'",
        'measured-Rafael-macros':'measured-Hodram-macros',
        'all_three_static_source_speakers_not_invented_from_incidental_r1':'all_six_static_source_speakers_not_invented_from_incidental_r1',
        'ordinary_captain0_opening_context_no_unlock_orstate_fixture':'ordinary_captain1_opening_context_no_unlock_orstate_fixture',
        'Bind28clean/current B50speeches through original captain0dispatch;noFEobjects.':'Bind28clean/current Hodram B137/B45/B46 speeches through original captain1dispatch;noFEobjects.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
    print('Prepared56original Hodram dispatches withnative addresses andguards unchanged.')
