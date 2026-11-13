"""Correct selected-event membership;the current B49 packet contains event49,not its event48 prerequisite."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_reference_tools_v8405b');assert not root.exists()
    source=read('work/analysis/Hodram_B49_source_controls_v8384/source_controls.json')
    assert [(e['event_ID'],e['script_block'],e['must_be_completed']) for e in source['source_event_records']]==[(48,48,[]),(49,49,[48])]
    result=derive('scripts/verify_Hodram_B49_references_v8405.py','scripts/verify_Hodram_B49_references_v8405b.py',{
        'Hodram_B49_references_v8405':'Hodram_B49_references_v8405b',
        "for e in events]==[(48,48,[]),(49,49,[48])]":"for e in events]==[(49,49,[48])]",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,prior_verifier_preserved=True,selected_B49_packet_has_only_event49=True,source_dependency_packet_separately_verifies_event48_has_no_prerequisites=True,no_native_prose_command_entry_orROM_change=True))
