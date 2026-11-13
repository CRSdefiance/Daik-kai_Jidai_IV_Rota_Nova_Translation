"""Bind the notes-only764 retention's current bytes and preserve stopped proofs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/earlier_common_wraps_tools_v4977c');assert not root.exists()
    tool=derive('scripts/review_earlier_common_wraps_v4977b.py','scripts/review_earlier_common_wraps_v4977c.py',{
        'earlier_common_wraps_review_v4977':'earlier_common_wraps_review_v4977c',
        "assert old.text.hex()==history['integrated_hex'] and jp.text.hex()==history['source_hex']==glosses[n]['source_hex']":
        "historical_binding_key='current_hex' if n==764 else 'integrated_hex'\n        assert old.text.hex()==history[historical_binding_key] and jp.text.hex()==history['source_hex']==glosses[n]['source_hex']",
        "historical_final_review=hp,historical_final_review_sha256=sha(Path(hp).read_bytes()),historical_record=deepcopy(history),":
        "historical_final_review=hp,historical_final_review_sha256=sha(Path(hp).read_bytes()),historical_record=deepcopy(history),historical_exact_payload_key=historical_binding_key,",
    })
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tool=tool,stopped_native_proof_and_both_producers_preserved=True,new_editorial_credit=0))
