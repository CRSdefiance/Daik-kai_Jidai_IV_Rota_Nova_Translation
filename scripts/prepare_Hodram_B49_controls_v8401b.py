"""Preserve the stopped verifier and correct only picture-proof field binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_controls_tools_v8401b');assert not root.exists()
    result=derive('scripts/prove_Hodram_B49_controls_v8401.py','scripts/prove_Hodram_B49_controls_v8401b.py',{
        'Hodram_B49_controls_v8401':'Hodram_B49_controls_v8401b',
        "source['source_picture_andhide_cases'] if r['offset']==before['offset']":"source['source_picture_andhide_cases'] if r['source_offset']==before['offset']",
        "pictures.append(dict(word=word,source_offset=before['offset'],final_offset=after['offset'],**result))":"pictures.append(dict(word=word,original_source_offset=before['offset'],final_offset=after['offset'],**result))",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,stopped_v8401_preserved=True,only_picture_reference_key_andoutput_key_corrected=True,no_prose_native_address_guard_orROM_change=True))
