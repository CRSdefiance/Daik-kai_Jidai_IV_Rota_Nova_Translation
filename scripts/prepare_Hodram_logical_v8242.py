"""Source-lock the four-alignment logical expansion probe to captain1 and six mapped actors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_logical_tools_v8242')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/prove_Rafael_B50_logical_v8139.py','scripts/prove_Hodram_logical_v8242.py',{
      'Rafael_B50_logical_v8139':'Hodram_B137_B45_B46_logical_v8242',
      'translations/rafael_B50_editorial_manuscript_v1.json':'translations/hodram_B137_B45_B46_editorial_manuscript_v1.json',
      'Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json':'Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json',
      "'assert identity==prefix and captain==0'":"'assert identity==prefix and captain==1'",
      'own-captain0':'own-captain1','prefix in [0,2,9]':'prefix in [1,2,9,16,18,113]',
      "b'Rafael'":"b'Hodram'","b'Castor'":"b'Bergstrom'","b'Castor Co.'":"b'Bergstrom Fleet'",
      'original_captain=0':'original_captain=1','measured_default_FI6_FA6_FO10':'measured_default_FI6_FA9_FO15',
      'source_macro_totals=dict(FI=1,FA=2,FO=0)':'source_macro_totals=dict(FI=0,FA=0,FO=0)',
      'B50_has28_progressive_no_FE_no_fallback208_source_state_only':'Hodram_three_blocks28_progressive_no_FE_all_six_static_source_actors_only',
      'ordinary_captain0_context':'ordinary_captain1_context',
      'Original four-alignment macro/literal checks for28 B50 paragraphs;no FE consumers.':'Original four-alignment macro/literal checks for28 Hodram paragraphs;no FE consumers.',
      'allprogressive/noFE,sourceFA2/FI1':'allprogressive/noFE,sourcezeroFA/FI/FO',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
