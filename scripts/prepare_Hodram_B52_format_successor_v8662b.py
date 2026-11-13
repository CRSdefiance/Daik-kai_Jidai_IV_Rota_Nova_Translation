"""Keep stopped approval; bind exploratory manuscript to the supported relocatable encoder."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B52_format_tools_v8662b')
    assert not root.exists()
    receipt = derive('scripts/approve_Hodram_B52_format_v8662.py', 'scripts/approve_Hodram_B52_format_v8662b.py', {
        'work/analysis/Hodram_B52_format_v8662': 'work/analysis/Hodram_B52_format_v8662b',
        'translations/hodram_B52_editorial_manuscript_v5.json': 'translations/hodram_B52_editorial_manuscript_v6.json',
        'translations/hodram_B52_speaker_name_review_v3.json': 'translations/hodram_B52_speaker_name_review_v4.json',
        "doc.update(predecessor_manuscript=str(OLD),": "doc.update(encoder='dialogue-relocatable-v1', predecessor_encoder_preserved=old['encoder'], supported_encoder_binding_note='Exploratory natural-dialogue metadata is now explicitly bound to the supported relocatable encoder; no prose or native compiled byte changes.', predecessor_manuscript=str(OLD),",
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=receipt,
         stopped_approval='scripts/approve_Hodram_B52_format_v8662.py',
         failure='Standard v2 rejected exploratory encoder natural-dialogue. Bind dialogue-relocatable-v1 without changing validation, prose, compiled bytes or completed native/actual evidence.',
         partial_names_v3_andoriginal_producer_preserved=True,
         no_completed_native_probe_orcapture_replay=True))
