"""Source-locked one-label successor; all native instructions and address guards retained."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/shady_man_label_tools_v6257')
if __name__=='__main__':
    assert not ROOT.exists()
    proof=derive('dk4tool/patch/generic_speaker_label_data_v1.py','dk4tool/patch/shady_man_label_data_v1.py',{
      '39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1':'03a905a9e4a4df117b8a4b5280ec3c669a4db00547972397413bc8bebc4afbbd',
      "EXPECTED={164:('カップル男','Man in a Couple','Man'),165:('カップル女','Woman in a Couple','Woman'),172:('行き倒れ','Collapsed Person','Stranger')}":"EXPECTED={173:('怪しい人','Suspicious Person','Shady Man')}",
      'Generic speaker labels ':'Shady Man label ',
      "len(rows)==3 and [r['actor_ID'] for r in rows]==[164,165,172]":"len(rows)==1 and [r['actor_ID'] for r in rows]==[173]",
      'three exact source-owned actors required':'one exact source-owned actor required',
      'len(payload)==123040':'len(payload)==123264',
      "==['Man','Woman','Stranger']":"==['Shady Man']",
      'original123040_payload_extent_and_final48_byte_copy_wrapper_exact':'original123264_payload_extent_and_final48_byte_copy_wrapper_exact',
      'only_three_owned_ASCII_prefixes_changed_no_global_substitution':'only_one_owned_ASCII_prefix_changed_no_global_substitution',
    })
    ROOT.mkdir(parents=True);save(ROOT/'one_owned_label_transform_source_derivation.json',proof)
    print('One-actor source-locked data transform prepared; same621 fields,5 sections and native addresses.')
