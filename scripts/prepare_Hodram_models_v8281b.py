"""Preserve failed8281; fix duplicate metadata key assembly only."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_model_tools_v8281b');assert not root.exists()
    result=derive('scripts/model_Hodram_actual_v8281.py','scripts/model_Hodram_actual_v8281b.py',{
        'Hodram_actual_models_v8281':'Hodram_actual_models_v8281b',
        "dict(id=row['id'],block=row['block'],source_selector=row['source_selector'],input_hex=prior['stored_hex'],**reused)":"{**reused,'id':row['id'],'block':row['block'],'source_selector':row['source_selector'],'input_hex':prior['stored_hex']}",
    })
    root.mkdir(parents=True);save(root/'metadata_only_successor.json',dict(derivation=result,
        earlier_failed_duplicate_metadata_assembly_andone_native_Japanese_plane_preserved=True,
        native_code_guards_font_oracles_andsource_inputs_unchanged=True))
